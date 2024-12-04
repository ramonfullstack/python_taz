import logging
from typing import Dict

from simple_settings import settings

from taz.constants import (
    MAGAZINE_LUIZA_SELLER_ID,
    PRODUCT_ORIGIN,
    SOURCE_OMNILOGIC
)
from taz.core.merge.scopes.helpers import normalize_attributes
from taz.core.storage.raw_products_storage import RawProductsStorage

logger = logging.getLogger(__name__)


class OmnilogicScope:

    def __init__(
        self,
        raw_product: Dict,
        enriched_product: Dict,
        *args,
        **kwargs
    ):
        self.enriched_product = enriched_product
        self.raw_product = raw_product
        self.__raw_products_storage = RawProductsStorage()
        self.original_product = None
        self.origin = kwargs.get('origin')

    def apply(self):
        if (
            self.enriched_product.get('product_hash') and
            self.enriched_product.get('entity') in settings.ENABLE_MATCHING_FROM_ENTITY  # noqa
        ):
            logger.info(
                'Product has product_hash:{product_hash} apply merge '
                'rules for sku:{sku} seller_id:{seller_id}'.format(
                    product_hash=self.enriched_product['product_hash'],
                    sku=self.raw_product['sku'],
                    seller_id=self.raw_product['seller_id'],
                )
            )

            self._normalize_title()

            self.raw_product['product_hash'] = self.enriched_product['product_hash']  # noqa
            self.raw_product['source'] = SOURCE_OMNILOGIC

        self._normalize_attributes()
        self._normalize_brand()

    def _normalize_title(self):
        if self.raw_product['seller_id'] != MAGAZINE_LUIZA_SELLER_ID:
            self.raw_product['title'] = (
                self.enriched_product['product_name'] or
                self.raw_product['title']
            )
            self.raw_product['reference'] = (
                self.enriched_product.get('sku_name') or ''
            )

    def _normalize_brand(self):
        if self.origin != PRODUCT_ORIGIN:
            raw_product = self.get_original_product()
            if raw_product:
                self.raw_product['brand'] = raw_product.get('brand', None)

    def _normalize_attributes(self):
        attributes = []
        if self._enable_enrichment():
            metadata = self.enriched_product.get('metadata') or {}
            metadata = {
                attribute_name: metadata.get(attribute_name)
                for attribute_name in self.enriched_product['sku_metadata']
            }
            attributes = normalize_attributes(metadata)

            if attributes:
                self.raw_product['attributes'] = attributes
        elif self.origin != PRODUCT_ORIGIN:
            raw_product = self.get_original_product()
            if raw_product:
                attributes = raw_product.get('attributes') or []
                self.raw_product['attributes'] = attributes
                logger.info(
                    'Including original attributes to product of sku:{sku} '
                    'seller_id:{seller_id} navigation_id:{navigation_id} '
                    'attributes:{attributes}'.format(
                        sku=self.raw_product.get('sku'),
                        seller_id=self.raw_product.get('seller_id'),
                        navigation_id=self.raw_product.get('navigation_id'),
                        attributes=attributes
                    )
                )

    def get_original_product(self):
        if self.original_product is None:
            self.original_product = self.__raw_products_storage.get_bucket_data( # noqa
                sku=self.enriched_product.get('sku'),
                seller_id=self.enriched_product.get('seller_id')
            )

        return self.original_product

    def _enable_enrichment(self):
        category_id = self.enriched_product['category_id']
        return (
            self.enriched_product.get('sku_metadata') and not (
                category_id in settings.KEEP_CATEGORIES_ATTRIBUTES or
                '*' in settings.KEEP_CATEGORIES_ATTRIBUTES
            )
        )
