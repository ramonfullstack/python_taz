from functools import cached_property
from typing import Dict, Optional

from maaslogger import base_logger
from simple_settings import settings

from taz.constants import (
    AVAILABILITY_IN_STOCK,
    AVAILABILITY_OUT_OF_STOCK,
    MAGAZINE_LUIZA_SELLER_ID
)
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.reviews import Reviews
from taz.consumers.core.stock import StockHelper
from taz.consumers.product_exporter.helpers import (
    _create_enriched_payload,
    _generate_factsheet_url,
    _get_product_url,
    contains_fulfillment
)
from taz.consumers.product_exporter.scopes.helpers import ScopeHelper
from taz.core.common.cached_badge import CachedBadge
from taz.utils import convert_id_to_nine_digits

logger = base_logger.get_logger(__name__)


class Scope(MongodbMixin):
    name = 'simple_product'

    def __init__(self, seller_id: str, sku: str) -> None:
        self.seller_id = seller_id
        self.sku = sku
        self.reviews = Reviews()
        self.scope_helper = ScopeHelper()
        self.stock_helper = StockHelper()
        self.cached_badge = CachedBadge()

    @cached_property
    def raw_products(self):
        return self.get_collection('raw_products')

    @cached_property
    def prices(self):
        return self.get_collection('prices')

    @cached_property
    def unpublished_products(self):
        return self.get_collection('unpublished_products')

    def get_data(self):
        product = self._get_product(self.seller_id, self.sku)

        if not product:
            return

        main_category = product.get('main_category', {}).get('id') or ''
        navigation_id = product['navigation_id']

        if main_category == 'TM':
            logger.warning(
                'Discarding the product because not categorized for '
                f'sku:{self.sku} seller_id:{self.seller_id} '
                f'navigation_id:{navigation_id}'
            )
            return

        path = _get_product_url(product)

        if not path:
            logger.info(
                f'Discarding the product {navigation_id} because it was '
                'not possible to generate the url'
            )
            return

        price = self._get_prices(self.seller_id, self.sku)
        raw_media = self.scope_helper.get_medias(self.seller_id, self.sku)
        media = (
            self.scope_helper.get_media_urls(
                sku=self.sku,
                seller_id=self.seller_id,
                title=product.get('title', ''),
                reference=product.get('reference', ''),
                media=raw_media
            ) if raw_media else {}
        )
        logger.debug(f'media: {media}')

        factsheet_url = _generate_factsheet_url(self.sku, self.seller_id)
        navigation_id = convert_id_to_nine_digits(product['navigation_id'])
        seller_name = product.get('seller_description')
        if not seller_name:
            seller_name = self.scope_helper.get_seller_name(self.seller_id)

        stock_count = price.get('stock_count') or 0

        minimum_order_quantity = price.get('minimum_order_quantity')
        if self.seller_id == MAGAZINE_LUIZA_SELLER_ID:
            stock = self._get_stocks(
                sku=self.sku,
                seller_id=self.seller_id,
                navigation_id=navigation_id
            )

            stock_count = stock.get('stock_count', 0)

        payload = {
            'scope': self.name,
            'sku': self.sku,
            'seller_id': self.seller_id,
            'seller_name': seller_name,
            'type': product['type'],
            'dimensions': product.get('dimensions') or {},
            'ean': product.get('ean') or product.get('isbn') or '',
            'brand': product['brand'],
            'title': product['title'],
            'description': product['description'] or '',
            'categories': self.scope_helper.get_categories_detail(
                product['categories']
            ),
            'reference': product['reference'],
            'active': not product['disable_on_matching'],
            'attributes': product.get('attributes') or [],
            'medias': media.get('images') or [],
            'factsheet_url': factsheet_url,
            'created_at': product['created_at'],
            'parent_sku': product['parent_sku'],
            'navigation_id': navigation_id,
            'price': price['price'],
            'list_price': price['list_price'],
            'currency': price.get('currency', settings.DEFAULT_CURRENCY),
            'path': f'{settings.BASE_DESKTOP_URL}/{path}',
            'selections': product.get('selections') or {},
            'review_count': self.reviews.get_customer_behavior(
                navigation_id=product['navigation_id'],
                behavior_type='product_total_review_count'
            ),
            'review_rating': self.reviews.get_customer_behavior(
                navigation_id=product['navigation_id'],
                behavior_type='product_average_rating'
            ),
            'sells_to_company': product.get('sells_to_company'),
            'matching_uuid': product.get('matching_uuid'),
            'audios': media.get('audios') or [],
            'podcasts': media.get('podcasts') or [],
            'videos': media.get('videos') or [],
        }

        stock_availability = self._get_availability_stock(
            minimum_order_quantity=minimum_order_quantity,
            stock_count=stock_count,
            seller_id=self.seller_id
        )

        payload.update(stock_availability)

        if minimum_order_quantity:
            payload.update({'minimum_order_quantity': minimum_order_quantity})

        if settings.ENABLE_PARENT_MATCHING:
            payload.update({
                'parent_matching_uuid': product.get('parent_matching_uuid')
            })

        badges = self._get_badges()
        if badges:
            payload.update({'badges': badges})

        ids_info = self.scope_helper.get_offer_id_and_id_correlations(
            self.sku,
            self.seller_id
        )
        if ids_info:
            payload.update(ids_info)

        enriched_products = self.scope_helper.get_enriched_products(
            self.seller_id,
            self.sku
        )

        metadata = _create_enriched_payload(enriched_products)
        payload.update(metadata)

        if product['type'] == 'bundle':
            if not product.get('bundles'):
                logger.warning(
                    'It is a bundle product, but does not have children for '
                    f'sku:{self.sku} seller_id:{self.seller_id} '
                    f'navigation_id:{navigation_id}'
                )
                return

            payload.update(self._get_bundles(product['bundles']))

        payload.update(
            self.scope_helper.create_unavailable_product_payload(navigation_id)
        )

        if settings.ENABLE_FULFILLMENT and contains_fulfillment(product):
            payload.update({'fulfillment': product['fulfillment']})

        if settings.ENABLE_EXTRA_DATA:
            payload.update({'extra_data': product.get('extra_data')})

        return payload

    def _get_product(self, seller_id: str, sku: str):
        product = self.raw_products.find_one({
            'sku': sku,
            'seller_id': seller_id
        })

        if not product:
            logger.warning(
                f'Product not found for sku:{sku} seller_id:{seller_id}'
            )

        return product

    def _get_prices(self, seller_id: str, sku: str):
        price = self.prices.find_one(
            {
                'sku': sku,
                'seller_id': seller_id
            },
            {
                '_id': 0,
                'price': 1,
                'list_price': 1,
                'stock_count': 1,
                'minimum_order_quantity': 1,
                'currency': 1,
            }
        )

        if not price:
            logger.warning(
                f'Price not found for sku:{sku} seller_id:{seller_id}'
            )
            return {
                'price': '0.00',
                'list_price': '0.00',
                'stock_count': 0
            }

        payload = {
            'price': '{0:.2f}'.format(price.get('price') or 0.00),
            'list_price': '{0:.2f}'.format(price.get('list_price') or 0.00),
            'currency': price.get('currency', settings.DEFAULT_CURRENCY),
            'stock_count': price.get('stock_count') or 0
        }

        minimum_order_quantity = price.get('minimum_order_quantity')
        if minimum_order_quantity:
            payload.update({
                'minimum_order_quantity': minimum_order_quantity
            })

        return payload

    def _get_stocks(self, seller_id: str, sku: str, navigation_id: str):
        return self.stock_helper.mount(
            sku=sku,
            seller_id=seller_id,
            navigation_id=navigation_id
        )

    def _get_bundles(self, bundles):
        bundle_ids = [
            {
                'sku': key,
                'seller_id': MAGAZINE_LUIZA_SELLER_ID
            }
            for key in bundles.keys()
        ]

        fields = {'_id': 0, 'title': 1, 'reference': 1, 'brand': 1, 'sku': 1}

        products = list(self.raw_products.find(
            {'$or': bundle_ids},
            fields
        ))

        if not products:
            return []

        for product in products:
            sku = product['sku']

            bundle = bundles[sku]
            product.update(bundle)

        return {'bundles': products}

    def _get_badges(self):
        delete_fields = ('products', 'start_at', 'end_at', '_id')
        fields = {
            field: 0
            for field in delete_fields
        }
        return self.cached_badge.get_badges_by_seller_id_sku(
            seller_id=self.seller_id,
            sku=self.sku,
            fields=fields,
            sort_by='priority'
        )

    @staticmethod
    def _get_availability_stock(
        minimum_order_quantity: Optional[int],
        stock_count: int,
        seller_id: str
    ) -> Dict:
        stock_availability = (
            (
                seller_id == MAGAZINE_LUIZA_SELLER_ID and
                (
                    (
                        bool(minimum_order_quantity) and
                        stock_count >= minimum_order_quantity
                    ) or
                    (not bool(minimum_order_quantity) and stock_count > 0)
                )
            ) or (
                seller_id != MAGAZINE_LUIZA_SELLER_ID and
                stock_count > 0
            )
        )

        return (
            {
                'availability': AVAILABILITY_IN_STOCK,
                'stock_count': stock_count
            } if stock_availability else {
                'availability': AVAILABILITY_OUT_OF_STOCK,
                'stock_count': 0
            }
        )
