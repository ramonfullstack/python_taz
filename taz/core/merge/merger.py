import logging
from functools import cached_property
from typing import Dict, List

from simple_settings import settings

from taz import constants
from taz.constants import (
    CHESTER_STRATEGY,
    OMNILOGIC_STRATEGY,
    SINGLE_SELLER_STRATEGY
)
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.core.merge.category import CategoryMerger
from taz.core.merge.factsheet import FactsheetMerger
from taz.core.merge.matching_strategy import (
    ChesterMatchingStrategy,
    OmnilogicMatchingStrategy
)
from taz.core.merge.scopes.api_luiza_express_delivery import (
    ApiLuizaExpressDelivery
)
from taz.core.merge.scopes.api_luiza_pickupstore import (
    ApiLuizaPickupStoreScope
)
from taz.core.merge.scopes.datasheet import DatasheetScope
from taz.core.merge.scopes.metabooks import MetabooksScope
from taz.core.merge.scopes.omnilogic import OmnilogicScope
from taz.core.merge.scopes.smartcontent import SmartContentScope
from taz.core.merge.scopes.wakko import WakkoScope

logger = logging.getLogger(__name__)

SCOPES = {
    constants.SOURCE_METABOOKS: MetabooksScope,
    constants.SOURCE_SMARTCONTENT: SmartContentScope,
    constants.SOURCE_OMNILOGIC: OmnilogicScope,
    constants.SOURCE_WAKKO: WakkoScope,
    constants.SOURCE_DATASHEET: DatasheetScope
}


class Merger(MongodbMixin):

    def __init__(
        self,
        raw_product: Dict,
        enriched_product: Dict,
        action: str,
        origin: str = None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.action = action
        self.origin = origin
        self.enriched_product = enriched_product
        self.raw_product = raw_product
        self.category_merger = CategoryMerger()
        self.STRATEGIES = {
            CHESTER_STRATEGY: ChesterMatchingStrategy(),
            OMNILOGIC_STRATEGY: OmnilogicMatchingStrategy()
        }

    @cached_property
    def enriched_products(self):
        return self.get_collection('enriched_products')

    @cached_property
    def raw_products(self):
        return self.get_collection('raw_products')

    @cached_property
    def factsheet_merger(self) -> FactsheetMerger:
        return FactsheetMerger()

    def merge(self):
        logger.debug(
            'Enriched payload received to merge, '
            f'payload:{self.enriched_product}'
        )

        sku = self.raw_product['sku']
        seller_id = self.raw_product['seller_id']
        navigation_id = self.raw_product.get('navigation_id')

        enriched_products = list(
            self.enriched_products.find(
                {'sku': sku, 'seller_id': seller_id},
                {'_id': 0}
            )
        )

        if self.enriched_product:
            enriched_products = [
                enriched for enriched in enriched_products or []
                if enriched['source'] != self.enriched_product['source']
            ]
            enriched_products.append(self.enriched_product)

        enriched_products = self.execution_priority(enriched_products)
        for enriched_product in enriched_products:
            scope = enriched_product['source']

            if (
                scope == constants.SOURCE_METABOOKS and
                not self.raw_product.get('isbn')
            ):
                continue

            scope_cls = SCOPES.get(scope)

            if not scope_cls:
                continue

            scope_cls(
                self.raw_product,
                enriched_product,
                origin=self.origin
            ).apply()

            logger.debug(
                f'Using scope:{scope} to enrich the product sku:{sku} '
                f'seller_id:{seller_id} navigation_id:{navigation_id}'
            )

        if enriched_products:
            self._merge_category(enriched_products)

        self.set_matching_strategy(enriched_products)

        if seller_id == constants.MAGAZINE_LUIZA_SELLER_ID:
            ApiLuizaPickupStoreScope(self.raw_product).apply()
            ApiLuizaExpressDelivery(self.raw_product).apply()

        self._remove_empty_selector()
        self._save_raw_product()
        self._merge_factsheet()

        logger.info(
            'Merge successfully completed for sku:{sku} '
            'seller_id:{seller_id} navigation_id:{navigation_id} '
            'attributes:{attributes} main_category:{main_category}'.format(
                sku=self.raw_product.get('sku'),
                seller_id=self.raw_product.get('seller_id'),
                navigation_id=self.raw_product.get('navigation_id'),
                attributes=self.raw_product.get('attributes'),
                main_category=self.raw_product.get('main_category')
            )
        )

    def _save_raw_product(self):
        try:
            criteria = {
                'sku': self.raw_product['sku'],
                'seller_id': self.raw_product['seller_id'],
            }

            if self.raw_product.get('_id'):
                del self.raw_product['_id']

            self.raw_products.update_many(
                criteria,
                {'$set': self.raw_product},
                upsert=True
            )
        except Exception as e:
            logger.exception(
                'An error occurred saving raw_products with sku:{sku} '
                'seller_id:{seller_id} navigation_id:{navigation_id} '
                'error:{error}'.format(
                    sku=self.raw_product['sku'],
                    seller_id=self.raw_product['seller_id'],
                    navigation_id=self.raw_product.get('navigation_id'),
                    error=e
                )
            )
            raise

    def _remove_empty_selector(self):
        attributes = [
            attr
            for attr in self.raw_product.get('attributes') or []
            if attr.get('value', '') != ''
        ]
        self.raw_product['attributes'] = attributes

    def _merge_category(
        self,
        enriched_products: List[Dict]
    ):
        categories, product_type, _ = self.category_merger.merge(
            categories=self.raw_product.get('categories') or [],
            enriched_products=enriched_products or [],
            sku=self.raw_product['sku'],
            seller_id=self.raw_product['seller_id']
        )

        self.raw_product['categories'] = categories

        if product_type:
            self.raw_product['product_type'] = product_type

        try:
            self.raw_product['main_category'] = {
                'id': categories[0]['id'],
                'subcategory': {
                    'id': categories[0]['subcategories'][0]['id']
                }
            }
        except Exception as e:
            logger.error(
                'Could not generate main_category to sku:{sku} '
                'seller_id:{seller_id} navigation_id:{navigation_id} '
                'error:{error}'.format(
                    sku=self.raw_product['sku'],
                    seller_id=self.raw_product['seller_id'],
                    navigation_id=self.raw_product.get('navigation_id'),
                    error=e
                )
            )

    def _merge_factsheet(self) -> None:
        try:
            self.factsheet_merger.merge(
                sku=self.raw_product['sku'],
                seller_id=self.raw_product['seller_id']
            )
        except Exception as e:
            logger.exception(
                'An error occurred applying merger on factsheet with '
                'sku:{sku} seller_id:{seller_id} '
                'navigation_id:{navigation_id} error:{error}'.format(
                    sku=self.raw_product['sku'],
                    seller_id=self.raw_product['seller_id'],
                    navigation_id=self.raw_product.get('navigation_id'),
                    error=e
                )
            )
            raise

    def execution_priority(
        self,
        enriched_products: List[Dict]
    ) -> List[Dict]:
        if not enriched_products and self.enriched_product:
            return [self.enriched_product]

        return sorted(
            enriched_products,
            key=lambda enriched: settings.PRIORITY_EXECUTION_MERGER.get(
                enriched['source'], len(settings.PRIORITY_EXECUTION_MERGER)
            )
        )

    def set_matching_strategy(self, enriched_products: List):
        self.raw_product.update({'matching_strategy': SINGLE_SELLER_STRATEGY})

        for strategy in [CHESTER_STRATEGY, OMNILOGIC_STRATEGY]:
            payload = self.STRATEGIES[strategy].validate_and_get_matching_strategy( # noqa
                product=self.raw_product,
                enriched_products=enriched_products
            )

            if payload:
                self.raw_product.update(payload)
                break
