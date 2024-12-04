from datetime import datetime
from functools import cached_property
from typing import Dict, List

from maaslogger import base_logger
from simple_settings import settings

from taz import constants
from taz.constants import MAGAZINE_LUIZA_SELLER_ID, SOURCE_GENERIC_CONTENT
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.product_exporter.scopes.helpers import ScopeHelper

logger = base_logger.get_logger(__name__)


class Scope(MongodbMixin):
    name = 'product_features'

    def __init__(self, seller_id, sku):
        self.seller_id = seller_id
        self.sku = sku

        self.scope_helper = ScopeHelper()

    @cached_property
    def categories(self):
        return self.get_collection('categories')

    @cached_property
    def enriched_products(self):
        return self.get_collection('enriched_products')

    @cached_property
    def raw_products(self):
        return self.get_collection('raw_products')

    def get_data(self):
        if self.seller_id == MAGAZINE_LUIZA_SELLER_ID:
            return {}

        product = self.raw_products.find_one(
            {'sku': self.sku, 'seller_id': self.seller_id},
            {
                '_id': 0,
                'categories': 1,
                'product_type': 1,
                'matching_uuid': 1,
                'parent_matching_uuid': 1,
                'navigation_id': 1
            }
        )

        if not product:
            logger.info(
                f'Product with sku:{self.sku} and seller_id:{self.seller_id}'
                'not found in raw products'
            )
            return {}

        enriched_products = self.scope_helper.get_enriched_products(
            self.seller_id,
            self.sku,
            skip=settings.SKIP_ENRICHED_SOURCE_IN_PRODUCT_FEATURES,
            fields={
                '_id': 0,
                'entity': 1,
                'classifications': 1,
                'source': 1,
                'product_type': 1,
                'metadata': 1,
                'active': 1
            }
        )

        return self.format_payload(product, enriched_products)

    def format_payload(
        self,
        product: Dict,
        enriched_products: List[Dict]
    ):
        payload = {
            'sku': self.sku,
            'seller': self.seller_id,
            'navigation_id': product['navigation_id'],
            'metadata': self.get_metadata(enriched_products),
            'datasheet': self.contains_datasheet(enriched_products),
            'timestamp': datetime.now().timestamp(),
            'source': constants.SOURCE_TAZ
        }

        product_type = (
            product.get('product_type') or
            self.select_product_type(enriched_products)
        )

        if product_type:
            payload['product_type'] = product_type
            payload['categories'] = self.scope_helper.get_categories_detail(
                product.get('categories')
            )

        if product.get('matching_uuid'):
            payload['matching_uuid'] = product['matching_uuid']

        if product.get('parent_matching_uuid'):
            payload['parent_matching_uuid'] = product['parent_matching_uuid']

        return payload

    @staticmethod
    def contains_datasheet(enriched_products: List[Dict]) -> bool:
        for product in enriched_products:
            if product['source'] in [
                constants.SOURCE_DATASHEET,
                constants.SOURCE_BACKOFFICE_DATASHEET
            ]:
                return True
        return False

    @staticmethod
    def select_product_type(enriched_products: List[Dict]) -> str:
        ordered_sources = [
            constants.SOURCE_RECLASSIFICATION_PRICE_RULE,
            constants.SOURCE_METABOOKS,
            constants.SOURCE_OMNILOGIC,
            constants.SOURCE_HECTOR,
        ]

        for source in ordered_sources:
            for enriched in enriched_products:
                if enriched['source'] == source:
                    if enriched.get('product_type'):
                        return enriched['product_type']
                    if enriched.get('entity'):
                        return enriched['entity']
                    if enriched.get('classifications'):
                        return enriched['classifications'][0]['product_type']
        return ''

    @staticmethod
    def get_metadata(enriched_products: List[Dict]) -> List:
        for enriched in enriched_products:
            if (
                enriched['source'] == SOURCE_GENERIC_CONTENT and
                enriched['active']
            ):
                return [
                    {
                        'name': key,
                        'value': value,
                        'source': SOURCE_GENERIC_CONTENT
                    }
                    for key, value in enriched['metadata'].items()
                    if enriched['metadata']
                ]

        return []
