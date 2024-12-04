import logging
from typing import Dict

from simple_settings import settings

from taz.constants import ProductSpecification

logger = logging.getLogger(__name__)


class WakkoScope:

    def __init__(
        self,
        raw_product: Dict,
        enriched_product: Dict,
        *args,
        **kwargs
    ):
        self.enriched_product = enriched_product
        self.raw_product = raw_product

    def apply(self):
        if bool(settings.ENABLE_WAKKO_SCOPE):
            logger.debug('Wakko enrichment disabled')
            return

        self._normalize_attributes()
        self._normalize_brand()

        source = self.enriched_product.get('source')
        if source:
            self.raw_product['source'] = source

    def _normalize_brand(self):
        metadata = self.enriched_product.get('metadata') or {}
        normalized = metadata.get('normalized') or {}

        if normalized.get('Marca'):
            self.raw_product['brand'] = (
                self.enriched_product['metadata']['normalized']['Marca'][0]
            )

            return

        if normalized.get('Editora'):
            self.raw_product['brand'] = (
                self.enriched_product['metadata']['normalized']['Editora'][0]
            )

            return

        logger.warning(
            'Normalized brand not found, metadata:{metadata}'.format(
                metadata=self.enriched_product.get('metadata')
            )
        )

    def _normalize_attributes(self):
        attributes = self.raw_product.get('attributes') or []

        metadata = self.enriched_product.get('metadata') or {}
        normalized = metadata.get('normalized') or {}

        if not attributes or not normalized:
            logger.debug(
                'Wakko attributes enrichment was ignored'
                ' because attributes:{attributes} '
                'or normalized:{normalized} is empty '
                'for sku:{sku} seller_id:{seller_id}'.format(
                    attributes=attributes,
                    normalized=normalized,
                    sku=self.raw_product['sku'],
                    seller_id=self.raw_product['seller_id']
                )
            )
            return

        for attrs in attributes:
            attr_type = attrs['type']

            attr_label = (
                ProductSpecification[attr_type].label
                if attr_type in ProductSpecification.__members__
                else attr_type
            )

            if not normalized.get(attr_label):
                continue

            normalized_value = normalized.get(attr_label)
            if not normalized_value:
                continue

            attrs['value'] = ', '.join(normalized_value)
