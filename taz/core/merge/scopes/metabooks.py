import logging
from typing import Dict

logger = logging.getLogger(__name__)


class MetabooksScope:

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
        self._normalize_title()
        self._normalize_brand()

        self.raw_product['description'] = self.enriched_product['description']
        self.raw_product['attributes'] = []

    def _normalize_title(self):
        title = 'Livro - {}'.format(self.enriched_product['title'])

        self.raw_product['title'] = title
        self.raw_product['offer_title'] = title
        self.raw_product['reference'] = ''

    def _normalize_brand(self):
        if not self.enriched_product.get('metadata', {}).get('Editora'):
            logger.warning(
                'Normalized brand not found, metadata:{metadata}'.format(
                    metadata=self.enriched_product.get('metadata')
                )
            )
            return

        publishers = self.enriched_product['metadata']['Editora']
        self.raw_product['brand'] = publishers
