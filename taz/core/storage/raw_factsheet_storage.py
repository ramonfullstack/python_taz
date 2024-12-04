from simple_settings import settings

from taz.core.storage.base_storage import BaseStorage


class RawFactsheetStorage(BaseStorage):

    def __init__(self):
        super().__init__(settings.RAW_FACTSHEET_STORAGE)

    def generate_filename(self, sku, seller_id):
        return f'{seller_id}/factsheet/{sku}.json'
