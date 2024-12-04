import logging

from taz.core.merge.scopes.helpers import normalize_attributes

logger = logging.getLogger(__name__)


class DatasheetScope:

    def __init__(
        self,
        raw_product: dict,
        enriched_product: dict,
        *args,
        **kwargs
    ):
        self.enriched_product = enriched_product
        self.raw_product = raw_product

    def apply(self) -> None:
        self.raw_product.update(self.get_result())

    def get_result(self):
        result = {
            field: self.enriched_product[field]
            for field in ['description', 'metadata']
            if self.enriched_product.get(field)
        }

        if 'metadata' in result:
            metatada = result.pop('metadata') or {}
            result.update({
                'attributes': normalize_attributes(metatada)
            })
        return result
