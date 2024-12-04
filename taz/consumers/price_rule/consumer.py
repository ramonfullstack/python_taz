from functools import cached_property
from time import perf_counter
from typing import Dict, List, Optional

from maaslogger import base_logger
from simple_settings import settings

from taz.constants import (
    PRICE_RULE_ORIGIN,
    SOURCE_HECTOR,
    SOURCE_OMNILOGIC,
    SOURCE_RECLASSIFICATION_PRICE_RULE,
    UPDATE_ACTION
)
from taz.consumers.core.brokers.stream import PubSubRecordProcessor
from taz.consumers.core.brokers.stream.pubsub import PubSubBroker
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.notification import Notification
from taz.consumers.core.taz import TazRequest
from taz.consumers.price_rule import SCOPE
from taz.core.merge.category import CategoryMerger

logger = base_logger.get_logger(__name__)

MAIOR_IGUAL = 'MAIOR_IGUAL'
MENOR_IGUAL = 'MENOR_IGUAL'

TYPE_ENRICHED_PRODUCT = 'enriched_product'


class PriceRuleProcessor(MongodbMixin, PubSubRecordProcessor):
    scope = SCOPE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category_merger = CategoryMerger()

    @cached_property
    def prices(self):
        return self.get_collection('prices')

    @cached_property
    def taz_request(self):
        return TazRequest()

    @cached_property
    def enriched_products(self):
        return self.get_collection('enriched_products')

    @cached_property
    def classifications_rules(self):
        return self.get_collection('classifications_rules')

    @cached_property
    def notification(self):
        return Notification()

    def process_message(self, message: Dict) -> bool:
        elapsed_time = perf_counter()
        sku = message['sku']
        seller_id = message['seller_id']
        navigation_id = message['navigation_id']
        source = message.get('source', '')
        tracking_id = message.get('tracking_id')
        origin = message.get('origin', 'UNKNOWN')

        is_type_enriched_product = message.get('type') == TYPE_ENRICHED_PRODUCT

        logger.info(
            f'Request price rule sku:{sku} seller_id:{seller_id} '
            f'navigation_id:{navigation_id} source:{source} from '
            f'origin:{origin}'
        )

        if (
            is_type_enriched_product and
            source == SOURCE_RECLASSIFICATION_PRICE_RULE
        ):
            self._send_notification(
                action=UPDATE_ACTION,
                sku=sku,
                seller_id=seller_id,
                navigation_id=navigation_id,
                tracking_id=tracking_id,
            )
            return True

        enriched_products = list(self.enriched_products.find(
            {
                'sku': sku,
                'seller_id': seller_id,
                'source': {
                    '$in': [
                        SOURCE_HECTOR,
                        SOURCE_OMNILOGIC,
                        SOURCE_RECLASSIFICATION_PRICE_RULE,
                    ]
                },
            }
        ))

        if not enriched_products:
            logger.debug(
                f'Not found enriched products sku:{sku} seller_id:{seller_id} '
                f'navigation_id:{navigation_id} source:{source}'
            )
            if is_type_enriched_product:
                self._send_notification(
                    action=UPDATE_ACTION,
                    sku=sku,
                    seller_id=seller_id,
                    navigation_id=navigation_id,
                    tracking_id=tracking_id,
                )
            return True

        enriched_filtered_products = [
            product for product in enriched_products
            if product['source'] in [SOURCE_OMNILOGIC, SOURCE_HECTOR]
        ]

        categories, product_type, source = self.category_merger.merge(
            sku=sku,
            seller_id=seller_id,
            categories=[],
            enriched_products=enriched_filtered_products,
        )

        rules = list(self.classifications_rules.find(
            {
                'product_type': product_type,
                'active': True,
            }
        ))

        enriched_product_reclassification = self.__get_source_reclassification(
            enriched_products
        )

        if not rules:
            logger.debug(
                'Not found price rule for product '
                f'sku:{sku} seller_id:{seller_id} '
                f'navigation_id:{navigation_id} '
                f'source:{source}'
            )
            if enriched_product_reclassification:
                logger.debug(
                    'Delete reclassification price rule for product '
                    f'sku:{sku} seller_id:{seller_id} '
                    f'navigation_id:{navigation_id} '
                    f'source:{source}'
                )
                self.delete_taz_enriched_product(
                    sku=sku,
                    seller_id=seller_id,
                    source=SOURCE_RECLASSIFICATION_PRICE_RULE,
                )
                return True

            if is_type_enriched_product:
                self._send_notification(
                    action=UPDATE_ACTION,
                    sku=sku,
                    seller_id=seller_id,
                    navigation_id=navigation_id,
                    tracking_id=tracking_id,
                )
            return True

        price = (
            self.prices.find_one(
                {
                    'sku': sku,
                    'seller_id': seller_id,
                },
                {'_id': 0, 'price': 1},
            ) or {}
        )
        if not price or not price.get('price'):
            logger.debug(
                'Not found price for product '
                f'sku:{sku} seller_id:{seller_id} '
                f'navigation_id:{navigation_id} '
                f'source:{source}'
            )
            if enriched_product_reclassification:
                logger.debug(
                    'Delete reclassification price rule for product '
                    f'sku:{sku} seller_id:{seller_id} '
                    f'navigation_id:{navigation_id} '
                    f'source:{source}'
                )
                self.delete_taz_enriched_product(
                    sku=sku,
                    seller_id=seller_id,
                    source=SOURCE_RECLASSIFICATION_PRICE_RULE,
                )

            if is_type_enriched_product:
                self._send_notification(
                    action=UPDATE_ACTION,
                    sku=sku,
                    seller_id=seller_id,
                    navigation_id=navigation_id,
                    tracking_id=tracking_id,
                )
            return True

        payload = {
            'sku': sku,
            'seller_id': seller_id,
            'navigation_id': navigation_id,
            'price': price['price'],
            'from': {
                'product_type': product_type,
                'category_id': categories[0]['id'],
                'subcategory_ids': [
                    c['id'] for c in categories[0]['subcategories']
                ],
                'source': source,
            },
        }

        rule_id = None
        for rule in rules:
            if (
                rule['operation'] == MAIOR_IGUAL and
                price.get('price', 0) >= rule['price']
            ) or (
                rule['operation'] == MENOR_IGUAL and
                price.get('price', 0) <= rule['price']
            ):
                rule_id = rule['_id']
                logger.debug(
                    f'Apply price rule to product '
                    f'sku:{sku} seller_id:{seller_id} '
                    f'navigation_id:{navigation_id} '
                    f'source:{source} rule_id:{rule_id}')
                payload.update(
                    {
                        'rule_id': rule_id,
                        'category_id': rule['to']['category_id'],
                        'subcategory_ids': rule['to']['subcategory_ids'],
                        'product_type': rule['to']['product_type'],
                        'source': SOURCE_RECLASSIFICATION_PRICE_RULE,
                    }
                )
                if self._has_changed_classification_rule(
                    rule=rule,
                    enriched=enriched_product_reclassification
                ):
                    self.post_taz_enriched_product(payload)
                break

        if enriched_product_reclassification and rule_id is None:
            logger.debug(
                'Delete reclassification price rule for product '
                f'sku:{sku} seller_id:{seller_id} '
                f'navigation_id:{navigation_id} '
                f'source:{source}'
            )
            self.delete_taz_enriched_product(
                sku=sku,
                seller_id=seller_id,
                source=SOURCE_RECLASSIFICATION_PRICE_RULE,
            )

        if is_type_enriched_product and rule_id is None:
            elapsed_time = perf_counter() - elapsed_time
            self._send_notification(
                action=UPDATE_ACTION,
                sku=sku,
                seller_id=seller_id,
                navigation_id=navigation_id,
                tracking_id=tracking_id,
            )
            logger.info(
                'Successfully processed price rule to product '
                f'sku:{sku} seller_id:{seller_id} '
                f'navigation_id:{navigation_id} '
                f'source:{source} in {elapsed_time:.3f}s'
            )

        return True

    def delete_taz_enriched_product(self, seller_id, sku, source):
        self.taz_request.delete_enriched_product(
            sku=sku, seller_id=seller_id, source=source
        )

    def post_taz_enriched_product(self, payload):
        self.taz_request.post_notification(
            SOURCE_RECLASSIFICATION_PRICE_RULE,
            payload
        )

    def _send_notification(
        self,
        action: str,
        seller_id: str,
        sku: str,
        navigation_id: str,
        tracking_id: str = None,
    ) -> None:
        payload = {
            'sku': sku,
            'seller_id': seller_id,
            'navigation_id': navigation_id,
            'tracking_id': tracking_id
        }

        self.notification.put(
            data=payload,
            scope=self.scope,
            action=action,
            origin=PRICE_RULE_ORIGIN
        )

    def _has_changed_classification_rule(
        self,
        rule: Dict,
        enriched: Dict
    ) -> bool:
        return (
            not enriched or
            rule['_id'] != enriched['rule_id'] or
            rule['to']['product_type'] != enriched['product_type'] or
            rule['to']['category_id'] != enriched['category_id'] or
            rule['to']['subcategory_ids'] != enriched['subcategory_ids']
        )

    def __get_source_reclassification(
        self,
        enriched_products: List[Dict]
    ) -> Optional[Dict]:
        for enriched in enriched_products:
            if enriched['source'] == SOURCE_RECLASSIFICATION_PRICE_RULE:
                return enriched
        return None


class PriceRuleConsumer(PubSubBroker):
    scope = SCOPE
    record_processor_class = PriceRuleProcessor
    project_name = settings.GOOGLE_PROJECT_ID
