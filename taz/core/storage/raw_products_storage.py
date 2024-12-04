from simple_settings import settings

from taz.core.storage.base_storage import BaseStorage


class RawProductsStorage(BaseStorage):

    def __init__(self):
        super().__init__(settings.RAW_PRODUCT_STORAGE)

    def generate_filename(self, sku, seller_id):
        return f'{seller_id}/{sku}.json'

    def generate_external_url(self, sku, seller_id):  # pragma: no cover
        pass
