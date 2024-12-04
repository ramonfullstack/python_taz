from simple_settings import settings

from taz.core.storage.base_storage import BaseStorage


class FactsheetStorage(BaseStorage):

    def __init__(self):
        super().__init__(settings.FACTSHEET_STORAGE)
        self.__domain = settings.FACTSHEET_DOMAIN

    def generate_filename(self, sku, seller_id):
        return f'{seller_id}/factsheet/{sku}.json'

    def generate_external_url(self, sku, seller_id):
        return f'{self.__domain}/{self.generate_filename(sku, seller_id)}'
