import logging
import re
from copy import copy
from typing import Dict

from simple_settings import settings

from taz.core.merge.scopes.helpers import normalize_attributes
from taz.core.storage.raw_products_storage import RawProductsStorage
from taz.utils import diacriticless

logger = logging.getLogger(__name__)


class SmartContentScope:

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

    def apply(self):
        main_category = self.raw_product['main_category'].get('id')

        if self._is_allowed_normalized(main_category):
            self._normalize_attributes()
            self._normalize_title(main_category)

        self.raw_product['description'] = self.enriched_product['description']
        self.raw_product['brand'] = self.enriched_product['brand']

    def _normalize_attributes(self):
        attributes = normalize_attributes(
            self.enriched_product.get('metadata') or {}
        )
        self.raw_product['attributes'] = attributes

        if not attributes:
            storage_product = self.__raw_products_storage.get_bucket_data(
                sku=self.enriched_product.get('sku'),
                seller_id=self.enriched_product.get('seller_id')
            )

            if storage_product:
                self.raw_product['attributes'] = (
                    storage_product.get('attributes')
                )

        logger.debug(
            f'Attributes {attributes} normalized in smartcontent scope'
        )

    @staticmethod
    def _is_allowed_normalized(main_category):
        return main_category in (
            settings.ENABLE_SMARTCONTENT_ENRICHMENT_BY_CATEGORY
        ) or '*' in settings.ENABLE_SMARTCONTENT_ENRICHMENT_BY_CATEGORY

    def _normalize_title(self, main_category):
        if self.enriched_product.get('title'):
            self.raw_product['title'] = self.enriched_product['title']

            if (
                main_category in
                settings.SMARTCONTENT_CATEGORY_NOT_ALLOWED_REFERENCE
            ):
                self._apply_title_cleanup()

    def _apply_title_cleanup(self):
        reference = copy(self.raw_product['reference'])
        title_enriched = copy(self.enriched_product['title'])

        if diacriticless(reference) in diacriticless(title_enriched):
            word_length = len(title_enriched) - len(reference)
            self.raw_product['title'] = (
                self.enriched_product['title'][:word_length]
            )
            self.raw_product['title'] = re.sub(
                r'(\s|-)*$', '', self.raw_product['title']
            )
            self.raw_product['offer_title'] = (
                '{} - {}'.format(
                    self.raw_product['title'],
                    self.raw_product['reference']
                )
                if self.raw_product['reference'] else
                self.raw_product['title']
            )
        else:
            self.raw_product['reference'] = ''
