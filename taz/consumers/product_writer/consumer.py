import time
from datetime import datetime, timedelta
from functools import cached_property
from typing import Dict, List, Optional

import dateutil.parser
import pymongo
import requests
from maaslogger import base_logger
from simple_settings import settings
from slugify import slugify

from taz.constants import (
    BADGE_CACHE_KEY,
    MAGAZINE_LUIZA_SELLER_ID,
    MEDIA_TYPES,
    PRODUCT_WRITER_ERROR_CODE,
    PRODUCT_WRITER_NO_CORRELATION_FOUND_CODE,
    PRODUCT_WRITER_NO_CORRELATION_FOUND_MESSAGE,
    PRODUCT_WRITER_PRICE_NOT_FOUND_CODE,
    PRODUCT_WRITER_PRICE_NOT_FOUND_MESSAGE,
    PRODUCT_WRITER_PRODUCT_DISABLE_CODE,
    PRODUCT_WRITER_PRODUCT_DISABLE_MESSAGE,
    PRODUCT_WRITER_SUCCESS_CODE,
    PRODUCT_WRITER_SUCCESS_MESSAGE,
    SINGLE_SELLER_STRATEGY,
    UPDATE_ACTION
)
from taz.consumers.core.aws.kinesis import KinesisManager
from taz.consumers.core.brokers.stream import (
    PubSubBroker,
    PubSubRecordProcessor
)
from taz.consumers.core.cache.redis import CacheMixin
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.google.stream import StreamPublisherManager
from taz.consumers.core.stock import StockHelper
from taz.core.cache.layered_cache import LayeredCache
from taz.core.cache.layers import MemoryTTLCache, RedisCache
from taz.core.common.media import build_media
from taz.core.notification.notification_sender import NotificationSender
from taz.helpers.category import build_category_data
from taz.helpers.format import generate_sku_seller_id_key
from taz.helpers.json import json_dumps
from taz.helpers.url import get_variation_url
from taz.utils import sort_nicely

logger = base_logger.get_logger(__name__)

ACTION_DELETE = 'delete'
ACTION_UPDATE = 'update'
SCOPE = 'product_writer'


class ProductWriterProcessor(MongodbMixin, CacheMixin, PubSubRecordProcessor):
    stream_name = settings.INDEXING_PROCESS_STREAM_NAME

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pubsub = StreamPublisherManager()
        self.kinesis_manager = KinesisManager(self.stream_name)
        self.notification_sender = NotificationSender()
        self.cache_categories = LayeredCache()
        self.cache_categories.set_layers([
            MemoryTTLCache(
                ttl=int(settings.EXPIRES_CACHE_CATEGORIES),
                interval=float(settings.CACHE_CLEANING_INTERVAL)
            ),
            RedisCache(
                key_pattern=settings.PRODUCT_WRITER_REDIS_KEY_PATTERN,
                ttl=int(settings.EXPIRES_REDIS_CACHE_CATEGORIES),
                host=settings.REDIS_SETTINGS['host'],
                port=settings.REDIS_SETTINGS['port'],
                password=settings.REDIS_SETTINGS.get('password')
            )
        ])

    @cached_property
    def categories(self):
        return self.get_collection('categories')

    @cached_property
    def id_correlations(self):
        return self.get_collection('id_correlations')

    @cached_property
    def medias(self):
        return self.get_collection('medias')

    @cached_property
    def badges(self):
        return self.get_collection('badges')

    @cached_property
    def prices(self):
        return self.get_collection('prices')

    @cached_property
    def raw_products(self):
        return self.get_collection('raw_products')

    @cached_property
    def unpublished_products(self):
        return self.get_collection('unpublished_products')

    @cached_property
    def custom_attributes(self):
        return self.get_collection('custom_attributes')

    @cached_property
    def unified_objects(self):
        return self.get_collection('unified_objects')

    @cached_property
    def sellers(self):
        return self.get_collection('sellers')

    @cached_property
    def stock_helper(self):
        return StockHelper()

    @classmethod
    def cache(self):
        return self.get_cache(self)

    def process_message(self, message):
        """
        This method process a product write request and
        assembles a payload to perform the desired action
        on Acme. In the meanwhile, seller priority/affinity is
        sorted on this flow in order to compose the buybox.
        The buybox composition currently follows this sequence:
        - ML items
        - cheapest items
        - out of stock items
        """
        origin = message.get('origin', 'UNKNOWN')
        sku, seller = message['sku'], message['seller_id']

        raw_product = self.raw_products.find_one(
            {
                'sku': sku,
                'seller_id': seller
            },
            {
                '_id': 0,
                'navigation_id': 1,
                'sku': 1,
                'seller_id': 1,
                'matching_strategy': 1,
                'disable_on_matching': 1,
                'matching_uuid': 1
            }
        )

        action = 'unknown'

        if not raw_product:
            reason = (
                f'Variation sku:{sku} seller_id:{seller} '
                'not found on raw_products.'
                f'Removing from the queue (requester:{origin})'
            )
            logger.warning(reason)
            self.notification_sender.notify_patolino_about_error(
                message,
                UPDATE_ACTION,
                reason,
                PRODUCT_WRITER_ERROR_CODE
            )
            return True

        if (
            raw_product.get('disable_on_matching', False) and
            message.get('type', 'matching') != 'matching'
        ):
            reason = (
                f'Variation sku:{sku} seller_id:{seller} is disabled. '
                f'Removing from the queue (requester:{origin})'
            )
            logger.warning(reason)
            return True

        price = self._get_price(sku, seller)
        if not price or 'list_price' not in price:
            payload = {'id': raw_product.get('navigation_id')}

            self._send_stream(payload, ACTION_DELETE, sku, seller)
            action = ACTION_DELETE

            self.notification_sender.send(
                sku=raw_product['sku'],
                seller_id=raw_product['seller_id'],
                code=PRODUCT_WRITER_PRICE_NOT_FOUND_CODE,
                message=PRODUCT_WRITER_PRICE_NOT_FOUND_MESSAGE,
                payload={
                    'navigation_id': raw_product.get('navigation_id')
                }
            )

            logger.info(
                f'Delete product because price not found for sku:{sku} '
                f'seller_id:{seller}'
            )
            return True

        correlations_info = self.id_correlations.find({
            'sku': sku, 'seller_id': seller
        })

        publish_status = False

        if correlations_info.count() == 0:
            logger.warning(
                f'Pending matching for variation sku:{sku} '
                f'seller:{seller}. Postponing publishing '
                f'(requester:{origin})'
            )
            return True

        for correlation_info in correlations_info:
            product_id = self._find_product_id(correlation_info)

            if raw_product.get('matching_strategy') != SINGLE_SELLER_STRATEGY:
                for old_id in correlation_info.get('old_product_ids') or []:
                    if (
                        not old_id or
                        correlation_info['variation_id'].startswith(old_id)
                    ):
                        continue

                    payload = {'id': old_id}
                    self._send_stream(payload, ACTION_DELETE, sku, seller)
                    action = ACTION_DELETE

                    self.notification_sender.send(
                        sku=raw_product['sku'],
                        seller_id=raw_product['seller_id'],
                        code=(
                            PRODUCT_WRITER_NO_CORRELATION_FOUND_CODE
                        ),
                        message=(
                            PRODUCT_WRITER_NO_CORRELATION_FOUND_MESSAGE
                        ),
                        payload={
                            'navigation_id': raw_product.get('navigation_id')
                        }
                    )

                    logger.info(
                        f'Product product_id:{old_id} sku:{sku} '
                        f'seller:{seller} unpublished through '
                        f'old_product_ids (requester:{origin})'
                    )

            unified_product = self.unified_objects.find_one({
                'id': product_id
            })

            if not unified_product:
                logger.warning(
                    f'Unified product not found for variation sku:{sku} '
                    f'seller:{seller} product_id:{product_id}. Postponing '
                    f'publishing (requester:{origin})'
                )

                if product_id:
                    payload = {'id': product_id}
                    publish_status = self._send_stream(
                        payload,
                        ACTION_DELETE,
                        sku,
                        seller
                    )

                    action = ACTION_DELETE

                    self.notification_sender.send(
                        sku=raw_product['sku'],
                        seller_id=raw_product['seller_id'],
                        code=PRODUCT_WRITER_PRODUCT_DISABLE_CODE,
                        message=PRODUCT_WRITER_PRODUCT_DISABLE_MESSAGE,
                        payload={
                            'navigation_id': raw_product.get('navigation_id')
                        }
                    )
                continue

            self._unset_disabled(unified_product, sku, seller, origin)

            if (
                raw_product['disable_on_matching'] and
                len(unified_product['variations']) == 0
            ):
                payload = {
                    'id': unified_product['id'],
                    'variations': [
                        {
                            'id': correlation_info['variation_id'],
                            'sellers': [
                                {
                                    'sku': correlation_info['sku'],
                                    'id': correlation_info['seller_id']
                                }
                            ]
                        }
                    ]
                }

                publish_status = self._send_stream(
                    payload,
                    ACTION_DELETE,
                    sku,
                    seller
                )

                action = ACTION_DELETE

                self.notification_sender.send(
                    sku=raw_product['sku'],
                    seller_id=raw_product['seller_id'],
                    code=PRODUCT_WRITER_PRODUCT_DISABLE_CODE,
                    message=PRODUCT_WRITER_PRODUCT_DISABLE_MESSAGE,
                    payload={
                        'navigation_id': raw_product.get('navigation_id')
                    }
                )

                logger.info(
                    'Product product_id:{product_id} sku:{sku} '
                    'seller_id:{seller_id} is removed because '
                    'it is disabled {disabled} or no variations '
                    '{variations} (requester:{origin})'.format(
                        product_id=unified_product['id'],
                        origin=origin,
                        disabled=raw_product['disable_on_matching'],
                        variations=len(unified_product['variations']),
                        sku=sku,
                        seller_id=seller
                    )
                )
                continue

            product = self._build_payload(unified_product)

            if not product:
                logger.warning(
                    'It was not possible to mount the payload of the product '
                    f'sku:{sku} seller:{seller} product_id:{product_id} '
                    f'(requester:{origin})'
                )
                return True

            product['timestamp'] = message.get('timestamp') or 0

            start = time.time()
            publish_status = self._send_stream(
                product,
                ACTION_UPDATE,
                sku,
                seller
            )

            action = ACTION_DELETE if (
                raw_product['disable_on_matching']
            ) else ACTION_UPDATE

            notification_payload = {
                'sku': sku,
                'seller_id': seller,
                'navigation_id': raw_product['navigation_id'],
                'action': action,
                'url': get_variation_url(
                    product,
                    raw_product['navigation_id']
                )
            }

            self.notification_sender.send(
                sku=sku,
                seller_id=seller,
                code=PRODUCT_WRITER_SUCCESS_CODE,
                message=PRODUCT_WRITER_SUCCESS_MESSAGE,
                payload=notification_payload,
                tracking_id=message.get('tracking_id')
            )

            end = time.time()
            logger.info(
                'Successfully sent product:{product_id} sku:{sku} '
                'seller_id:{seller_id} matching_strategy:{matching_strategy} '
                'and matching_uuid:{matching_uuid} to Stream in {duration} '
                'seconds action:{action} and status:{status} '
                '(requester:{origin})'.format(
                    product_id=product['id'],
                    sku=sku,
                    seller_id=seller,
                    matching_uuid=raw_product.get('matching_uuid'),
                    matching_strategy=raw_product.get('matching_strategy'),
                    duration=end - start,
                    origin=origin,
                    status=publish_status,
                    action=action
                )
            )

        return publish_status

    def _find_product_id(self, correlation):
        if correlation['product_id']:
            return correlation['product_id']

        if not correlation['old_product_ids']:
            return

        for old_product_id in correlation['old_product_ids']:
            product = self.unified_objects.find_one({
                'id': old_product_id
            }, {
                '_id': 0,
                'id': 1,
                'variations.id': 1,
                'variations.sellers.sku': 1,
                'variations.sellers.id': 1
            })

            if not product:
                continue

            if not product['variations']:
                return product['id']

            for variation in product['variations']:
                for seller in variation['sellers']:
                    if (
                        seller['sku'] == correlation['sku'] and
                        seller['id'] == correlation['seller_id']
                    ):
                        return product['id']

        logger.warning(
            'Could not find any ID to get the unified_objects record '
            'for sku:{sku} seller_id:{seller_id}'.format(
                sku=correlation['sku'],
                seller_id=correlation['seller_id']
            )
        )

    def _unpublish_product(self, product_id, origin):
        start = time.time()
        unpublish_status = self._unpublish(product_id)
        end = time.time()

        logger.info(
            f'Successfully removed product:{product_id} on Acme in '
            f'{end - start} seconds (requester:{origin})'
        )

        return unpublish_status

    def _unpublish(self, product_id):
        res = requests.delete(
            f'{settings.ACME_URL}/product/{product_id}/',
            headers=settings.ACME_REQUEST_HEADER
        )

        if res.status_code == 204:
            return True

        if res.status_code == 404:
            logger.info(
                f'Could not find product:{product_id} to be deleted on Acme, '
                'although operation should not be retried.'
            )
            return True

        logger.error(
            f'Failed to delete product:{product_id} on Acme. '
            f'Reason: HTTP {res.status_code} with {res.content}'
        )
        return False

    def _publish(self, payload: Dict, sku: str, seller: str):
        json_payload = json_dumps(payload)

        logger.debug(
            f'Sending product sku:{sku} seller_id:{seller} '
            f'to acme:{json_payload}'
        )

        res = requests.post(
            f'{settings.ACME_URL}/product/',
            data=json_payload,
            headers=settings.ACME_REQUEST_HEADER
        )

        if res.status_code == 409:
            res = requests.put(
                '{}/product/{}/'.format(settings.ACME_URL, payload['id']),
                data=json_payload,
                headers=settings.ACME_REQUEST_HEADER
            )

        if res.status_code in (200, 201, 204):
            return True

        logger.error(
            f'Failed to save product:{json_dumps(payload)} on Acme. '
            f'Reason: HTTP {res.status_code} with {res.content}'
        )
        return False

    def _unset_disabled(
        self,
        product: Dict,
        sku: str,
        seller_id: str,
        origin: str
    ):
        available_variations = []

        variations = product['variations']
        for variation in variations:

            available_sellers = []

            sellers = variation['sellers']
            for seller in sellers:
                seller_variation = self.raw_products.find_one({
                    'sku': seller['sku'],
                    'seller_id': seller['id'],
                    'disable_on_matching': False
                }, {
                    'seller_id': 1,
                    'sku': 1,
                    '_id': 0
                })

                if seller_variation:
                    available_sellers.append(seller)
                else:
                    logger.info(
                        'Variation disabled for '
                        'sku:{} seller:{}. Unsetting.'.format(
                            seller['sku'], seller['id']
                        )
                    )

            if available_sellers:
                variation['sellers'] = available_sellers
                available_variations.append(variation)

        if not available_variations:
            logger.warning(
                'No variations available for product:{product_id} '
                'sku:{sku} seller_id:{seller_id} origin:{origin} '.format(
                    product_id=product['id'],
                    sku=sku,
                    seller_id=seller_id,
                    origin=origin
                )
            )

        product.update({'variations': available_variations})

    def _verify_all_skus_have_prices(self, skus: List, prices: List):
        if not prices:
            logger.info('No SKUs were sent for price verification')
            return False

        skus_only = [sku for sku, _ in skus]
        prices_skus = [price['sku'] for price in prices]

        skus_without_prices = set(skus_only).difference(prices_skus)
        if len(skus_without_prices) > 0:
            missing_prices = [
                (sku, seller)
                for sku, seller in skus
                if sku in skus_without_prices
            ]
            logger.warning(
                f'Prices are missing for the following skus:{missing_prices}.'
            )

        return True

    def _build_payload(self, product: Dict) -> Optional[Dict]:
        product['message_timestamp'] = time.time()

        if '_id' in product:
            del product['_id']
        skus_info = self._extract_skus(product)

        if not skus_info:
            logger.warning(
                f'Could not extra any skus from product:{product}'
            )
            return False

        criteria = [
            {'sku': sku, 'seller_id': seller_id}
            for sku, seller_id in skus_info
        ]

        variations_prices = self.prices.find({
            '$or': criteria
        }).sort('stock_count', pymongo.ASCENDING)

        variations_prices = self._list_price_merger(
            variations_prices
        )

        if not self._verify_all_skus_have_prices(
            skus_info, variations_prices
        ):
            return False

        criteria = [
            {'sku': sku, 'seller_id': slugify(seller_id)}
            for sku, seller_id in skus_info
        ]

        variations_medias = list(self.medias.find({'$or': criteria}))

        sold_count = 0

        is_product_delivery_available = False

        unavailable_image_url = build_media(
            **settings.UNAVAILABLE_IMAGE_OPTIONS
        )

        """
        First iteration of variations is needed to inject all
        subsets of data
        """
        for variation in product['variations']:
            is_variation_delivery_available = False

            variation_sellers = variation['sellers']

            variation_sellers_ids = [
                variation_seller['id']
                for variation_seller in variation_sellers
            ]

            prices = []
            for variation_price in variations_prices:
                if variation_price['seller_id'] not in variation_sellers_ids:
                    continue
                prices.append(variation_price)

            sellers = []
            priced_sellers = []

            for price in prices:
                seller = None

                for variation_seller in variation_sellers:
                    if (
                        price['seller_id'] == variation_seller['id'] and
                        price['sku'] == variation_seller['sku']
                    ):
                        seller = variation_seller
                        break

                if not seller:
                    continue

                seller_sold_count = seller.get('sold_count', 0)
                sells_to_company = seller.get('sells_to_company') or False
                stock_count = price.get('stock_count') or 0

                priced_seller = {
                    'description': seller['description'],
                    'id': seller['id'],
                    'sku': seller['sku'],
                    'delivery_availability': (
                        price.get('delivery_availability') or 'unavailable'
                    ),
                    'list_price': price['list_price'],
                    'price': price['price'],
                    'currency': price.get('currency', settings.DEFAULT_CURRENCY), # noqa
                    'stock_count': stock_count,
                    'stock_type': price.get('stock_type') or 'on_seller',
                    'sold_count': seller_sold_count,
                    'sells_to_company': sells_to_company,
                    'score': self._get_seller_score(seller['id']),
                    'store_pickup_available': seller.get('store_pickup_available') or False,  # noqa
                    'delivery_plus_1': seller.get('delivery_plus_1') or False,
                    'delivery_plus_2': seller.get('delivery_plus_2') or False
                }

                minimum_order_quantity = price.get('minimum_order_quantity')

                if (
                    seller['id'] == MAGAZINE_LUIZA_SELLER_ID and
                    minimum_order_quantity is not None and
                    stock_count > 0
                ):
                    stock_1p = self.stock_helper.mount(
                        sku=seller['sku'],
                        seller_id=MAGAZINE_LUIZA_SELLER_ID,
                        navigation_id=seller['sku']
                    )
                    if minimum_order_quantity > stock_1p.get('stock_count', 0):
                        priced_seller.update({'stock_count': 0})

                if minimum_order_quantity:
                    priced_seller['minimum_order_quantity'] = (
                        minimum_order_quantity
                    )

                fulfillment = seller.get('fulfillment')
                if settings.ENABLE_FULFILLMENT and fulfillment is not None:
                    priced_seller['fulfillment'] = fulfillment

                priced_seller['matching_uuid'] = seller.get('matching_uuid')
                priced_seller['extra_data'] = seller.get('extra_data')

                if settings.ENABLE_PARENT_MATCHING:
                    priced_seller['parent_matching_uuid'] = seller.get(
                        'parent_matching_uuid'
                    )

                badges = self._get_badges(seller['sku'], seller['id'])
                if badges:
                    logger.info(
                        'Badges applied to sku:{sku} '
                        'seller:{seller_id}'.format(
                            sku=seller['sku'],
                            seller_id=seller['id']
                        )
                    )

                    priced_seller['badges'] = badges

                if (price.get('stock_count') or 0) <= 0:
                    logger.debug('Item sku:{} seller:{} out of stock'.format(
                        seller['sku'], seller['id']
                    ))

                custom_attributes = self._get_custom_attributes(
                    seller['sku'], seller['id']
                )

                if custom_attributes and custom_attributes is not None:
                    variation['short_title'] = (
                        custom_attributes['short_title']
                    )

                    variation['short_description'] = (
                        custom_attributes['short_description']
                    )

                if (
                    (price.get('stock_count') or 0) > 0 and
                    not is_product_delivery_available
                ):
                    is_product_delivery_available = True

                if (
                    (price.get('stock_count') or 0) > 0 and
                    not is_variation_delivery_available
                ):
                    is_variation_delivery_available = True

                if (seller['id'], seller['sku'],) not in priced_sellers:
                    sold_count += seller_sold_count
                    sellers.append(priced_seller)
                    priced_sellers.append((seller['id'], seller['sku'],))

            variation['sellers'] = sellers
            variation['is_delivery_available'] = is_variation_delivery_available  # noqa

            main_seller = variation_sellers[0]

            variation_medias = [
                variation_media
                for variation_media in variations_medias
                if variation_media['sku'] == main_seller['sku']
            ]

            if variation_medias:
                medias = {}

                for media in variation_medias:
                    for media_type in MEDIA_TYPES:
                        if media_type in media:
                            medias[media_type] = build_media(
                                main_seller['sku'],
                                variation.get('title'),
                                variation.get('reference'),
                                slugify(main_seller['id']),
                                media_type,
                                media[media_type]
                            )

                if not medias.get('images'):
                    logger.warning(
                        'Images not found for sku:{} seller:{}. '
                        'Setting unavailable image.'.format(
                            main_seller['sku'],
                            main_seller['id'],
                        )
                    )
                    medias['images'] = unavailable_image_url

                variation['media'] = medias
            else:
                logger.warning(
                    'No medias found for sku:{} seller:{}. '
                    'Setting unavailable image.'.format(
                        main_seller['sku'],
                        main_seller['id']
                    )
                )

                variation['media'] = {'images': unavailable_image_url}

        main_variation = product['variations'][0]

        if main_variation.get('sellers'):
            product['price'] = main_variation['sellers'][0]['price']

        product.update({
            'created_at': main_variation['created_at'],
            'updated_at': main_variation['updated_at'],
            'sold_count': sold_count,
            'is_delivery_available': is_product_delivery_available,
        })

        """
        Second iteration is needed for proper sorting
        """
        for variation in product['variations']:
            sellers = variation['sellers']
            for seller in sellers:
                seller.update({'status': 'published'})

            price_sorted = sorted(
                [
                    s for s in sellers
                    if s['delivery_availability'] != 'unavailable'
                ],
                key=lambda s: s['price']
            )

            unavailable_items = [
                s for s in sellers
                if s['delivery_availability'] == 'unavailable'
            ]

            sorted_sellers = (
                price_sorted +
                unavailable_items
            )

            variation['sellers'] = []
            for idx, value in enumerate(sorted_sellers):
                value['order'] = idx
                variation['sellers'].append(value)

            if 'categories' in variation:
                variation['categories'] = self._build_categories(variation)

            del variation['created_at']
            del variation['updated_at']

        product['attributes'] = self._sorted_attributes(product)

        product['variations'] = sorted(
            product['variations'],
            key=lambda v: int(v['is_delivery_available']), reverse=True
        )

        categories = self._build_categories(product)

        if not categories:
            return False

        product['categories'] = categories

        return product

    def _list_price_merger(self, variations_prices):
        merged_variations = {}
        for price in variations_prices:
            sku_key = generate_sku_seller_id_key(
                sku=price['sku'],
                seller_id=price['seller_id']
            )
            if sku_key in merged_variations:
                merged_variations[sku_key].update(price)
            else:
                merged_variations[sku_key] = price

        return [
            price
            for _, price in merged_variations.items()
            if 'list_price' in price
        ]

    def _sorted_attributes(self, product):
        attributes = []
        for attribute in product.get('attributes', {}).values():
            if not attribute.get('values'):
                break

            attribute['values'] = sort_nicely(attribute.get('values'))
            attributes.append(attribute)

        return sorted(attributes, key=lambda k: k['type'])

    def _build_categories(self, product):
        """
        We gather all category descriptive attributes from DB and complement
        the product with this information.
        """
        categories = []
        for category in product['categories']:
            categories_ids = [category['id']]

            if 'subcategories' in category:
                categories_ids += [
                    sub['id'] for sub in category['subcategories']
                ]

            stored_categories = []
            for category_id in categories_ids:
                c = self._get_category(category_id)
                if c:
                    stored_categories.append(c)

            stored_categories = {
                category.get('id'): category
                for category in stored_categories
            }

            stored_category = stored_categories.get(category['id'])

            if not stored_category:
                logger.warning(
                    'Category:{category_id} not found. '
                    'Trying to set default RC/RCNM category'.format(
                        category_id=category['id']
                    )
                )

                return self._build_default_missing_category_subcategory(
                    product.get('id')
                )

            assembled_category = self._mount_category_payload(stored_category)

            assembled_subcategories = []
            if 'subcategories' in category:
                assembled_subcategories = self._assemble_subcategories(
                    product.get('id'),
                    category,
                    stored_category,
                    stored_categories
                )

            if not assembled_subcategories:
                return self._build_default_missing_category_subcategory(
                    product.get('id')
                )

            assembled_category['subcategories'] = assembled_subcategories
            categories.append(assembled_category)

        return categories

    def _build_default_missing_category_subcategory(
        self,
        product_id
    ):
        categories = []

        default_category = self._get_category(
            settings.FALLBACK_MISSING_CATEGORY
        )

        if not default_category:
            logger.warning(
                'Fallback for missing category {category_id} '
                'not found for product:{product_id}. '
                'Postponing publishing'.format(
                    category_id=settings.FALLBACK_MISSING_CATEGORY,
                    product_id=product_id
                )
            )
            return False

        default_subcategory = self._get_category(
            settings.FALLBACK_MISSING_SUBCATEGORY,
        )

        if not default_subcategory:
            logger.warning(
                'Fallback for missing subcategory {subcategory_id} '
                'not found for product:{product_id}. '
                'Postponing publishing'.format(
                    subcategory_id=settings.FALLBACK_MISSING_SUBCATEGORY,
                    product_id=product_id
                )
            )
            return False

        assembled_missing_category = self._mount_category_payload(
            default_category
        )

        assembled_missing_subcategory = self._mount_category_payload(
            default_subcategory
        )

        assembled_missing_subcategories = list()
        assembled_missing_subcategories.append(assembled_missing_subcategory)

        assembled_missing_category['subcategories'] = (
            assembled_missing_subcategories
        )

        categories.append(assembled_missing_category)
        return categories

    def _assemble_subcategories(
        self,
        product_id,
        category,
        stored_category,
        stored_categories
    ):
        assembled_subcategories = []

        for subcategory in category['subcategories']:
            stored_subcategory = stored_categories.get(subcategory['id'])

            if not stored_subcategory:
                logger.debug(
                    'Subcategory:{} not found for product:{}. '.format(
                        subcategory['id'],
                        product_id,
                    )
                )
            else:
                assembled_subcategories.append({
                    'id': stored_subcategory['id'],
                    'name': stored_subcategory['description'],
                    'composite_name': '{}|{}'.format(
                        stored_subcategory['id'],
                        stored_subcategory['description']
                    ),
                    'url': build_category_data(
                        stored_category,
                        stored_subcategory
                    ),
                })

            if not assembled_subcategories:
                logger.warning(
                    'Subcategory:{} not found for product:{}. '.format(
                        subcategory['id'],
                        product_id
                    )
                )

        return assembled_subcategories

    def _send_stream(self, payload, action, sku, seller):
        if not settings.PUBLISH_STREAM:
            if action == ACTION_DELETE:
                return self._unpublish_product(payload['id'], 'UNKNOWN')

            return self._publish(payload, sku, seller)

        try:
            self.pubsub.publish(
                content={'data': payload, 'action': action},
                topic_name=settings.INDEXING_PROCESS_STREAM_TOPIC_NAME,
                project_id=settings.INDEXING_PROCESS_STREAM_PROJECT_ID
            )

            if seller == MAGAZINE_LUIZA_SELLER_ID:
                self.kinesis_manager.put(action, payload)
        except Exception as e:
            logger.error(
                'Failed to sent product:{product_id} sku:{sku} '
                'seller_id:{seller_id} on pubsub stream:{stream_name} and '
                'error:{error} payload:{payload}'.format(
                    product_id=payload['id'],
                    sku=sku,
                    seller_id=seller,
                    stream_name=self.stream_name,
                    error=e,
                    payload=payload
                )
            )
            return False

        logger.info(
            'Product id:{product_id} sku:{sku} seller_id:{seller_id} '
            'sent to successfully for stream:{stream_name} with '
            'action:{action}'.format(
                sku=sku,
                seller_id=seller,
                stream_name=self.stream_name,
                product_id=payload['id'],
                action=action
            )
        )

        logger.debug(
            'Send to stream:{stream_name} with payload:{payload}'.format(
                stream_name=self.stream_name,
                payload=payload
            )
        )

        return True

    def _extract_skus(self, product):
        skus_info = []
        for variation in product['variations']:
            skus_info += [
                (seller['sku'], seller['id'])
                for seller in variation['sellers']
            ]
        return skus_info

    def _get_badges(self, sku, seller):
        cache_key = BADGE_CACHE_KEY.format(
            sku=sku,
            seller_id=seller
        )

        cache_value = self.cache().get(cache_key)
        if not cache_value:
            return []

        cache_value = cache_value.decode()

        badges = self.badges.find({
            'products.sku': sku,
            'products.seller_id': seller,
            'slug': cache_value
        })

        result = []
        for badge in list(badges):
            result.append(
                self._remove_badge_fields(badge)
            )

        return sorted(result, key=lambda k: k.get('priority'))

    def _get_custom_attributes(self, sku, seller):
        custom_attributes = None
        if (seller in settings.CUSTOM_ATTRIBUTES_SELLERS or
                '*' in settings.CUSTOM_ATTRIBUTES_SELLERS):
            criteria = {'sku': sku, 'seller_id': seller}
            custom_attributes = self.custom_attributes.find_one(criteria)
        return custom_attributes

    def _get_seller_score(self, seller_id):
        return 1 if seller_id == MAGAZINE_LUIZA_SELLER_ID else 0

    @staticmethod
    def _remove_badge_fields(content):
        delete_fields = ('products', 'start_at', 'end_at', '_id',)

        keys = content.copy().keys()
        for key in keys:
            if key not in delete_fields:
                continue

            del content[key]

        return content

    def _get_price(self, sku, seller):
        prices = list(self.prices.find({'sku': sku, 'seller_id': seller}))
        prices = sorted(
            prices,
            key=lambda item: item.get('last_updated_at', datetime.min)
        )

        price = {}
        for record in prices:
            price.update(record)

        if not price:
            logger.warning(
                'Cannot find price for item sku:{sku} '
                'from seller:{seller}'.format(
                    sku=sku,
                    seller=seller
                )
            )

            return {}

        return price

    def _verify_out_of_stock(self, price):
        if not price or not price.get('last_updated_at'):
            return True

        if (price.get('stock_count') or 0) <= 0:
            return self._is_out_of_stock_by_period(
                price['last_updated_at']
            )

    def _is_out_of_stock_by_period(self, stock_last_updated_at):
        stock_days_ago_timestamp = (datetime.now() - timedelta(
            days=settings.MAX_DAYS_OUT_OF_STOCK
        )).timestamp()

        stock_last_update_timestamp = dateutil.parser.parse(
            stock_last_updated_at
        ).timestamp()

        return stock_days_ago_timestamp >= stock_last_update_timestamp

    def _get_category(
        self,
        category_id
    ):
        cache_value = self.cache_categories.get(category_id)

        if not cache_value:
            category = self.categories.find_one(
                {'id': category_id},
                {'_id': 0}
            )

            if not category:
                logger.warning('Category id:{} not found'.format(category_id))
                return None

            self.cache_categories.set(
                key=category_id,
                value=category
            )
            return category

        return cache_value

    @staticmethod
    def _mount_category_payload(
        category,
        subcategories=None
    ):
        return {
            'id': category['id'],
            'name': category['description'],
            'composite_name': '{}|{}'.format(
                category['id'],
                category['description']
            ),
            'url': build_category_data(
                category,
                subcategories
            )
        }


class ProductWriterConsumer(PubSubBroker):
    scope = SCOPE
    record_processor_class = ProductWriterProcessor
    project_name = settings.GOOGLE_PROJECT_ID
    subscription_name = settings.PUBSUB_PRODUCT_WRITER_SUB_NAME
