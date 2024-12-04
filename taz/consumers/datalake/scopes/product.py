import logging
from functools import cached_property

from taz.consumers.core.database.mongodb import MongodbMixin
from taz.core.storage.raw_products_storage import RawProductsStorage

logger = logging.getLogger(__name__)


class Scope(MongodbMixin):
    name = 'product_original'

    def __init__(
        self,
        sku: str,
        seller_id: str,
        navigation_id: str = None,
        **kwargs
    ) -> None:
        self.__sku = sku
        self.__seller_id = seller_id
        self.__navigation_id = navigation_id

    @cached_property
    def raw_products_storage(self):
        return RawProductsStorage()

    def get_data(self):
        original_product = self.raw_products_storage.get_bucket_data(
            sku=self.__sku,
            seller_id=self.__seller_id
        )

        if not original_product:
            return None

        original_product['scope_name'] = self.name

        return original_product
