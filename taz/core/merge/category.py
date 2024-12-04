import logging
from typing import Dict, List, Optional, Tuple

from simple_settings import settings

from taz import constants

FALLBACK_MISSING_CATEGORY = settings.FALLBACK_MISSING_CATEGORY

logger = logging.getLogger(__name__)


class CategoryMerger:

    def merge(
        self,
        sku: str,
        seller_id: str,
        categories: List,
        enriched_products: List[Dict]
    ) -> Tuple[List, Optional[str], str]:
        logger.debug(
            f'Category Merger received to merge sku:{sku} '
            f'seller_id:{seller_id} categories:{categories} '
            f'enriched_product:{enriched_products}'
        )

        enriched_product = self.filter_classification_enrichment(
            enriched_product_from_db=enriched_products
        )

        if not enriched_product:
            return categories, None, ''

        categories, product_type = self._mount_data(enriched_product)

        logger.info(
            f'Category Merger done successfully from sku:{sku} '
            f'seller_id:{seller_id} categories:{categories}'
        )

        return categories, product_type, enriched_product['source']

    @staticmethod
    def _mount_data(enriched_product: Dict) -> Tuple[List, Optional[str]]:
        category_id = (
            enriched_product.get('category_id') or
            enriched_product.get('classifications', [{}])[0].get('category_id')
        )

        subcategories = (
            enriched_product.get('subcategory_ids', []) or
            enriched_product.get('classifications', [{}])[0].get(
                'subcategories', []
            )
        )

        product_type = (
            enriched_product.get('product_type') or
            enriched_product.get('entity') or
            enriched_product.get('classifications', [{}])[0].get(
                'product_type', None
            )
        )

        return [
            {
                'id': category_id,
                'subcategories': [
                    {
                        'id': subcategory
                    } for subcategory in subcategories
                ]
            }
        ], product_type

    def filter_classification_enrichment(self, enriched_product_from_db):
        enriched_product = {
            enriched_source.get('source'): enriched_source
            for enriched_source in enriched_product_from_db or []
        }

        for source in [
            constants.SOURCE_RECLASSIFICATION_PRICE_RULE,
            constants.SOURCE_METABOOKS,
            constants.SOURCE_OMNILOGIC,
            constants.SOURCE_HECTOR
        ]:
            enriched = enriched_product.get(source)
            if not enriched:
                continue

            if (
                source == constants.SOURCE_METABOOKS and
                enriched.get('category_id') == FALLBACK_MISSING_CATEGORY
            ):
                continue

            if enriched.get('entity') != constants.DEFAULT_ENTITY:
                return enriched
