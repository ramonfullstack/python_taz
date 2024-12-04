import logging
from collections import OrderedDict
from datetime import datetime
from decimal import Decimal
from functools import cached_property
from typing import Dict, List, Optional, Tuple

from simple_settings import settings

from taz import constants
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.exceptions import NavigationIdNotFound
from taz.consumers.core.reviews import Reviews
from taz.core.notification.notification_sender import NotificationSender
from taz.helpers.format import generate_sku_seller_id_key
from taz.helpers.json import json_dumps
from taz.helpers.solr import convert_id_to_solr_format
from taz.helpers.url import generate_product_url
from taz.utils import convert_id_to_nine_digits

logger = logging.getLogger(__name__)


class BaseAssembler(MongodbMixin):

    def __init__(self, strategy_name: str, persist_changes: bool = True):
        self.persist_changes = persist_changes
        self.strategy_name = strategy_name
        self.notification_sender = NotificationSender()
        self.reviews = Reviews()

    @cached_property
    def id_correlations(self):
        return self.get_collection('id_correlations')

    @cached_property
    def raw_products(self):
        return self.get_collection('raw_products')

    @cached_property
    def unified_objects(self):
        return self.get_collection('unified_objects')

    @cached_property
    def customer_behaviors(self):
        return self.get_collection('customer_behaviors')

    @cached_property
    def unpublished_products(self):
        return self.get_collection('unpublished_products')

    @cached_property
    def scores(self):
        return self.get_collection('scores')

    def assemble(self, grouped_variations: OrderedDict):
        """
        This method receives a list of grouped variations and
        assembles them into a single product.
        """

        source_ids = [
            {
                'sku': variation['sku'],
                'seller_id': variation['seller_id']
            }
            for variations in grouped_variations.values()
            for variation in variations
        ]

        if not source_ids:
            return False, False

        elected_id = self.get_product_id(grouped_variations)
        product = self._build_product(elected_id, grouped_variations)

        fields_projection = {
            '_id': 0,
            'sku': 1,
            'seller_id': 1,
            'product_id': 1,
            'variation_id': 1
        }
        discarded = []
        correlations = []
        correlations_to_update = {}
        if len(source_ids) > 1:
            for source_id in source_ids:
                finded_correlations = self.id_correlations.find(
                    source_id,
                    fields_projection
                )
                if not finded_correlations:
                    continue

                correlations += [
                    {
                        'sku': correlation['sku'],
                        'seller_id': correlation['seller_id'],
                        'product_id': correlation['product_id'],
                        'variation_id': correlation['variation_id'],
                    }
                    for correlation in finded_correlations
                    if correlation['product_id'] != elected_id
                ]

        for correlation in correlations:
            discarded.append(correlation['product_id'])

            variation_key = generate_sku_seller_id_key(
                sku=correlation['sku'],
                seller_id=correlation['seller_id']
            )
            correlations_to_update[variation_key] = correlation

        if product:
            self._store_unified(dict(product))

            for variation in product.get('variations') or []:
                for seller in variation['sellers']:
                    variation_key = generate_sku_seller_id_key(
                        sku=seller['sku'],
                        seller_id=seller['id']
                    )
                    correlations_to_update[variation_key] = {
                        'variation_id': variation['id'],
                        'sku': seller['sku'],
                        'seller_id': seller['id']
                    }

            [
                self._update_correlation(
                    product_id=elected_id,
                    variation_id=correlation['variation_id'],
                    sku=correlation['sku'],
                    seller_id=correlation['seller_id']
                )
                for correlation in correlations_to_update.values()
            ]
        else:
            discarded.append(elected_id)

        if discarded:
            self._clean_discarded(discarded)

        return (product, []) if product else (False, False)

    def disassemble(self, variation: Dict) -> Optional[Dict]:
        product_id, _ = self.find_product_id([
            (variation['sku'], variation['seller_id'], '')
        ])

        unified_product = self.unified_objects.find_one(
            {'id': product_id},
            {'_id': 0}
        )

        if not unified_product:
            logger.warning(
                'Unified product:{} not found for sku:{} seller:{}'.format(
                    product_id, variation['sku'], variation['seller_id']
                )
            )
            return

        new_variations = []
        for old_variation in unified_product['variations']:
            for seller in old_variation['sellers']:
                if (
                    seller['id'] == variation['seller_id'] and
                    seller['sku'] == variation['sku']
                ):
                    old_variation['sellers'].remove(seller)

            if len(old_variation['sellers']) > 0:
                new_variations.append(old_variation)

        unified_product['variations'] = new_variations
        self._store_unified(dict(unified_product))

        return unified_product

    def _clean_discarded(self, discarded: List) -> None:
        if not self.persist_changes:
            return

        self.unified_objects.remove(
            {'id': {'$in': list(set(discarded))}}
        )

    def _get_highest_score(self, skus: List) -> Optional[Dict]:
        if len(skus) == 1:
            return

        fields_projection = {
            '_id': 0,
            'final_score': 1,
            'sku': 1,
            'seller_id': 1
        }
        scores = []
        for sku in skus:
            finded_scores = self.scores.find(
                {**sku, 'active': True},
                fields_projection
            )

            if not finded_scores:
                continue

            scores += [
                {
                    'sku': score['sku'],
                    'seller_id': score['seller_id'],
                    'final_score': score['final_score'],
                }
                for score in finded_scores
            ]

        if not scores:
            return

        score = max(scores, key=lambda s: s['final_score'])
        return {'sku': score['sku'], 'seller_id': score['seller_id']}

    def _build_product(self, product_id: str, grouped_variations: OrderedDict):
        """
        This method builds a list of products.
        The returned list contains almost the same object structure,
        although, what differs is their ids.
        """
        review_average_rating = constants.META_TYPE_PRODUCT_AVERAGE_RATING
        review_total_rating = constants.META_TYPE_PRODUCT_TOTAL_REVIEW_COUNT
        assembled_variations = []
        attributes_summary = {}
        all_subs = OrderedDict()
        main_product_variation = None

        review_count = 0
        review_score_total = 0
        review_quantity = 0

        main_variation = None

        for grouped_variation in grouped_variations.values():
            variation_reviews = None

            # TODO: passar navigation_id, junto com SKU e Seller ID
            variation_id = self.find_variation_id(
                sku=grouped_variation[0]['sku'],
                seller_id=grouped_variation[0]['seller_id']
            )

            variation_sellers = []
            variation_canonical_ids = []
            computed_sellers = []

            grouped_variation = self._filter_by_available_variation(
                grouped_variation
            )

            for variation in grouped_variation:
                variation_review_count = self.reviews.get_customer_behavior(
                    variation['navigation_id'],
                    review_total_rating
                )

                variation_average_rating = self.reviews.get_customer_behavior(
                    variation['navigation_id'],
                    review_average_rating
                )

                variation_reviews = {
                    review_total_rating: variation_review_count,
                    review_average_rating: variation_average_rating
                }
                review_count += variation_review_count
                review_score_total += variation_average_rating
                review_quantity += 1

                variation_seller = {
                    'id': variation['seller_id'],
                    'description': variation['seller_description'],
                    'sku': variation['sku'],
                    'sold_count': variation.get('sold_count', 0),
                    'sells_to_company': variation.get(
                        'sells_to_company'
                    ) or False
                }

                if variation.get('delivery_plus_1'):
                    variation_seller.update({'delivery_plus_1': True})

                if variation.get('delivery_plus_2'):
                    variation_seller.update({'delivery_plus_2': True})

                if variation.get('store_pickup_available'):
                    variation_seller.update({'store_pickup_available': True})

                if variation['seller_id'] in [
                    v['id']
                    for v in variation_sellers
                ]:
                    logger.debug(
                        'Multiple SKUs from same seller are being '
                        'grouped. sku:{} seller:{} will be skipped. '
                        'Fix the product on its source and submit it for '
                        'matching again.'.format(
                            variation['sku'],
                            variation['seller_id']
                        )
                    )

                    continue

                if (
                    variation_seller not in variation_sellers and
                    variation_seller['id'] not in computed_sellers
                ):
                    logger.debug(
                        'Adding item sku:{} seller:{}, to '
                        'product:{}, variation:{} persist_changes:{}'.format(
                            variation_seller['sku'],
                            variation_seller['id'],
                            product_id,
                            variation_id,
                            self.persist_changes
                        )
                    )
                    computed_sellers.append(variation_seller['id'])
                    variation_sellers.append(variation_seller)

                    variation_canonical_ids.append(variation['navigation_id'])

                for category in variation['categories']:
                    category_id = category['id']
                    subcategories = category['subcategories']
                    all_subs.setdefault(
                        category_id,
                        {'id': category_id, 'subcategories': []}
                    )
                    all_subs[category_id]['subcategories'] += subcategories

            if not variation_sellers:
                continue

            main_seller_variation = grouped_variation[0]
            subs = self._get_variation_category_and_subcategory(
                main_seller_variation
            )

            if not main_variation:
                main_variation = main_seller_variation

            main_variation_attributes = main_seller_variation.get(
                'attributes', []
            )

            if main_variation_attributes:
                self._set_attribute_labels(main_variation_attributes)

            winning_variation = self._select_winning_variation(
                grouped_variation
            )

            assembled_variation = OrderedDict(
                id=variation_id,
                ean=main_seller_variation.get('ean') or '',
                title=main_seller_variation['title'],
                description=main_seller_variation.get('description'),
                reference=main_seller_variation.get('reference'),
                brand=main_seller_variation['brand'],
                dimensions=main_seller_variation.get('dimensions') or '',
                sellers=variation_sellers,
                factsheet=winning_variation,
                main_media=winning_variation,
                attributes=main_variation_attributes,
                created_at=main_seller_variation['created_at'],
                updated_at=main_seller_variation.get('updated_at'),
                url=generate_product_url(
                    variation_id,
                    main_seller_variation,
                    [c for c in subs.values() or []],
                    self.persist_changes
                ),
                canonical_ids=variation_canonical_ids
            )

            if variation_reviews:
                assembled_variation.update(variation_reviews)
                variation_reviews = None

            bundles = main_seller_variation.get('bundles')
            if bundles:
                assembled_variation['bundles'] = bundles

            gift_product = main_seller_variation.get('gift_product')
            if gift_product:
                assembled_variation['gift_product'] = gift_product

            selections = main_seller_variation.get('selections')
            if selections:
                assembled_variation['selections'] = selections

            categories = main_seller_variation.get('categories')
            if categories:
                assembled_variation['categories'] = categories

            assembled_variations.append(
                assembled_variation
            )

            for attribute in main_seller_variation.get('attributes') or []:
                if 'type' not in attribute:
                    logger.warning(
                        'Attribute without a type found '
                        'for sku:{} seller:{} persist_changes:{}'.format(
                            main_seller_variation['sku'],
                            main_seller_variation['seller_id'],
                            self.persist_changes
                        )
                    )
                    continue

                attributes_summary.setdefault(
                    attribute['type'],
                    {
                        'type': attribute['type'],
                        'label': attribute['label'],
                        'values': [],
                    },
                )
                summary_items = attributes_summary[attribute['type']]['values']

                if attribute['value'] not in summary_items:
                    attributes_summary[attribute['type']]['values'].append(
                        attribute['value']
                    )
                    attributes_summary[attribute['type']]['values'] = sorted(
                        attributes_summary[attribute['type']]['values']
                    )

            if not main_product_variation:
                main_product_variation = main_seller_variation
                main_product_variation.update(assembled_variations[0])

        if not main_product_variation:
            return False

        all_categories = []

        for category in all_subs.values():
            """
            Here the list of categories is deduplicated
            """
            all_subcategories = []
            if category in all_categories:
                continue

            for subcategory in category.get('subcategories') or []:
                if subcategory not in all_subcategories:
                    all_subcategories.append(subcategory)

            category['subcategories'] = all_subcategories
            all_categories.append(category)

        if not all_categories:
            sellers = [
                (v[0]['sku'], v[0]['seller_id'])
                for v in grouped_variations.values()
            ]
            logger.error(
                'No categories found for product:{}, sellers {} and '
                'persist_changes:{}'.format(
                    product_id, sellers, self.persist_changes
                )
            )
            return False

        review_score = 0.0

        if review_score_total and review_quantity:
            """
            Here I need to ensure the rounding is made upwards
            using 2 Decimal places. The "+" signal on Decimal
            forces the rounding of the Decimal default context setting.
            """
            review_score = float(
                +Decimal(
                    review_score_total / review_quantity
                )
            )

        canonical_ids, assembled_variations = self._extract_info(
            product_id, assembled_variations
        )

        assembled_product = OrderedDict(
            id=product_id,
            review_count=review_count,
            review_score=review_score,
            url=generate_product_url(
                product_id,
                main_product_variation,
                all_categories,
                self.persist_changes
            ),
            title=main_variation['title'],
            description=main_variation['description'],
            reference=main_variation.get('reference'),
            brand=main_product_variation['brand'],
            variations=assembled_variations,
            attributes=attributes_summary,
            categories=all_categories,
            canonical_ids=canonical_ids
        )

        if main_product_variation.get('type'):
            assembled_product['type'] = main_product_variation['type']

        if main_product_variation.get('selections'):
            assembled_product['selections'] = (
                main_product_variation['selections']
            )

        logger.info(
            'Successfully assembled product:{} with '
            'variations:{} persist_changes:{}'.format(
                product_id,
                [v['id'] for v in assembled_variations],
                self.persist_changes
            )
        )

        return assembled_product

    def _extract_info(
        self,
        product_id: str,
        variations: List
    ) -> Tuple[List, List]:

        skus_infos = []
        ids = set([product_id])

        for variation in variations:
            ids.add(variation['id'])

            skus_infos += [
                {'seller_id': seller['id'], 'sku': seller['sku']}
                for seller in variation['sellers']
            ]

        products = list(self.raw_products.find(
            {'$or': skus_infos},
            {
                '_id': 0,
                'navigation_id': 1,
                'seller_id': 1,
                'sku': 1,
                'fulfillment': 1,
                'matching_uuid': 1,
                'parent_matching_uuid': 1,
                'extra_data': 1
            }
        ))

        products_data = {
            generate_sku_seller_id_key(
                sku=product['sku'],
                seller_id=product['seller_id']
            ): product
            for product in products
        }

        for variation in variations:
            for seller in variation.get('sellers'):
                product = products_data.get(
                    generate_sku_seller_id_key(
                        sku=seller['sku'],
                        seller_id=seller['id']
                    )
                )

                if not product:
                    continue

                if not product.get('navigation_id'):
                    raise NavigationIdNotFound(
                        'Navigation id not found for sku:{} seller:{}'.format(
                            product['sku'], product['seller_id']
                        )
                    )

                ids.add(product['navigation_id'])
                self._adding_info_if_exists(product, seller)

        return sorted(list(ids)), variations

    def _set_attribute_labels(self, attributes: List) -> None:
        for attribute in attributes:
            attr_type = attribute.get('type')
            if not attr_type:
                logger.warning(
                    f'Attribute {attribute} without a type '
                    f'in persist_changes:{self.persist_changes}'
                )
                continue

            attr_type = attr_type.lower()
            if hasattr(constants.ProductSpecification, attr_type):
                attr_label = constants.ProductSpecification[attr_type].label
                attribute['label'] = attr_label
            else:
                try:
                    attribute['label'] = attr_type.capitalize().replace('-', ' ')  # noqa
                except Exception as e:
                    logger.error(
                        f'Unknown type {attr_type} for attribute {attribute} '
                        f'in persist_changes {self.persist_changes} '
                        f'with error {e}'
                    )

    def _find_correlation(self, sku: str, seller_id: str):
        """
        talvez seja melhor ordenar as correlacoes por seller e data, sendo que
        seller magazineluiza deveria ter prioridade sobre os outros

        eu devo eliminar os IDs de correlacao que
        nao pertencem ao conjunto atual
        e manter somente o novo ID
        """
        return self.id_correlations.find({'sku': sku, 'seller_id': seller_id})

    def _update_correlation(
        self,
        product_id: str,
        variation_id: str,
        sku: str,
        seller_id: str,
        force: bool = False
    ):
        logger.debug(
            f'Storing correlation between product:{product_id} '
            f'variation:{variation_id}, sku:{sku} seller_id:{seller_id} '
            f'persist_changes:{self.persist_changes}'
        )

        if not variation_id and not force:
            logger.debug(
                f'Variation is empty, not saved in collection, sku:{sku} '
                f'seller_id:{seller_id} persist_changes:{self.persist_changes}'
            )
            return

        criteria = {
            'sku': sku,
            'seller_id': seller_id
        }

        if self.persist_changes:
            self.id_correlations.update_many(
                criteria,
                {'$set': {
                    'product_id': product_id,
                    'variation_id': variation_id,
                    **criteria,
                }},
                upsert=True
            )

    def find_variation_id(self, sku: str, seller_id: str) -> str:
        logger.debug(
            f'Finding variation correlations for sku:{sku} '
            f'seller_id:{seller_id} persist_changes:{self.persist_changes}'
        )

        if seller_id == constants.MAGAZINE_LUIZA_SELLER_ID:
            variation_id = sku
        else:
            variation_id = self._find_navigation_id(sku, seller_id)

        return variation_id

    def get_product_id(self, grouped_variations: OrderedDict) -> str:
        sorted_variations = sorted(
            [
                {
                    'id': str(variation['_id']),
                    'navigation_id': variation['navigation_id']
                }
                for variations in grouped_variations.values()
                for variation in variations
            ],
            key=lambda item: item['id']
        )

        return sorted_variations[0]['navigation_id']

    def find_product_id(self, variations: List) -> Tuple[str, List]:
        """
        Here we find a valid correlation to the variations
        sent on our input. Because the implemenation without active buybox
        generated one ID for each sku, we need to deal with election based
        on the following criteria:
        - Magazine Luiza SKUs are prioritary
        - Other IDs are sorted (ascending) and the first is elected
        If no correlations are found we generate one ID and save it on the
        variation_id generation/attribution, which happens
        further in the process
        """
        products_ids = []
        for sku, seller_id, parent_sku in variations:
            logger.debug(
                f'Finding product correlations for sku:{sku} '
                f'seller_id:{seller_id} parent_sku:{parent_sku} '
                f'persist_changes:{self.persist_changes}'
            )

            correlations = self._find_correlation(sku, seller_id)
            if correlations.count() <= 0:
                continue

            for correlation in correlations:
                correlation_id = correlation.get('product_id')

                if correlation_id and correlation_id not in products_ids:
                    products_ids.append({
                        'id': correlation_id,
                        'seller_id': correlation['seller_id'],
                        'sku': correlation['sku']
                    })

        if not products_ids:
            if seller_id == constants.MAGAZINE_LUIZA_SELLER_ID:
                correlation_id = convert_id_to_solr_format(sku)
            elif seller_id != constants.MAGAZINE_LUIZA_SELLER_ID:
                correlation_id = self._find_navigation_id(sku, seller_id)

            products_ids.append({
                'id': correlation_id,
                'seller_id': seller_id,
                'sku': sku
            })

        discarded = []
        elected_id = products_ids[0]['id']

        if len(products_ids) > 1:
            for id_info in products_ids:
                seller_id = id_info['seller_id']
                correlation_id = id_info['id']
                if (
                    seller_id and
                    seller_id == constants.MAGAZINE_LUIZA_SELLER_ID
                ):
                    elected_id = correlation_id
                    products_ids.remove(id_info)
                    break

            discarded = [
                id_info['id']
                for id_info in products_ids
                if id_info['id'] != elected_id
            ]

        if discarded:
            self._clean_discarded(discarded)

        return elected_id, discarded

    def _find_navigation_id(self, sku: str, seller_id: str) -> str:
        product = self.raw_products.find_one(
            {
                'sku': sku,
                'seller_id': seller_id
            },
            {'navigation_id': 1}
        )

        return product['navigation_id']

    def _store_unified(self, obj: Dict) -> None:
        if not self.persist_changes:
            return

        logger.debug(
            'Storing unified product:{} with {}'.format(
                obj['id'],
                json_dumps(obj)
            )
        )

        if obj.get('_id'):
            del obj['_id']

        obj['matching_strategy'] = self.strategy_name
        self.unified_objects.update_many(
            {'id': obj['id']},
            {'$set': obj},
            upsert=True
        )

    def _skip_unavailable_variation(self, variation: Dict) -> bool:
        if (
            variation['disable_on_matching'] or
            self._check_unpublished(
                sku=variation.get('sku'),
                seller=variation.get('seller_id'),
                navigation_id=variation.get('navigation_id'),
                product_hash=variation.get('product_hash')
            )
        ):
            return True
        return False

    def _check_unpublished(
        self,
        sku: str,
        seller: str,
        navigation_id: str,
        product_hash: str
    ) -> bool:
        navigation_id = convert_id_to_nine_digits(navigation_id)

        unpublished_product = self.unpublished_products.find_one(
            {'navigation_id': navigation_id},
            {'_id': 0}
        )

        if not unpublished_product:
            return False

        logger.warning(
            'Unpublished product via admin, sku:{sku}, '
            'seller_id:{seller_id} navigation_id:{navigation_id} '
            'product_hash:{product_hash} by user:{user} on:{date}'.format(
                sku=sku,
                seller_id=seller,
                navigation_id=navigation_id,
                user=unpublished_product.get('user'),
                date=unpublished_product.get('created_at'),
                product_hash=product_hash
            )
        )

        unpublished_product.update(
            created_at=(
                unpublished_product.get('created_at') or datetime.now()
            ).strftime('%Y-%m-%dT%H%M%S'),
            updated_at=(
                unpublished_product.get('created_at') or datetime.now()
            ).strftime('%Y-%m-%dT%H%M%S')
        )

        self.notification_sender.send(
            sku=sku,
            seller_id=seller,
            code=constants.UNPUBLISHED_CODE,
            message=constants.UNPUBLISHED_MESSAGE,
            payload=unpublished_product
        )

        return True

    def _filter_by_available_variation(self, grouped_variation: Dict) -> List:
        return [
            variation for variation in grouped_variation
            if not self._skip_unavailable_variation(variation)
        ]

    def _select_winning_variation(self, grouped_variation: List) -> Dict:
        main_seller_variation = grouped_variation[0]

        if (
            main_seller_variation['seller_id'] ==
            constants.MAGAZINE_LUIZA_SELLER_ID
        ):
            return {
                'seller_sku': main_seller_variation['sku'],
                'seller_id': main_seller_variation['seller_id'],
            }

        winning_variation = self._get_highest_score([
            {'sku': v['sku'], 'seller_id': v['seller_id']}
            for v in grouped_variation
        ]) or main_seller_variation

        return {
            'seller_sku': winning_variation['sku'],
            'seller_id': winning_variation['seller_id'],
        }

    @staticmethod
    def _get_variation_category_and_subcategory(
        variation: Dict
    ) -> OrderedDict:
        subs = OrderedDict()
        for category in variation['categories']:
            category_id = category['id']
            subcategories = category['subcategories']
            subs.setdefault(
                category_id,
                {'id': category_id, 'subcategories': []}
            )
            subs[category_id]['subcategories'] += subcategories
        return subs

    @staticmethod
    def _adding_info_if_exists(product: Dict, seller: Dict) -> None:
        fulfillment = product.get('fulfillment')
        if settings.ENABLE_FULFILLMENT and fulfillment is not None:
            seller['fulfillment'] = fulfillment

        matching_uuid = product.get('matching_uuid')
        if matching_uuid:
            seller['matching_uuid'] = matching_uuid

            if settings.ENABLE_PARENT_MATCHING:
                seller.update({
                    'parent_matching_uuid': product.get('parent_matching_uuid')
                })

        extra_data = product.get('extra_data')

        if extra_data:
            seller['extra_data'] = extra_data
