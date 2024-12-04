import logging

from taz import constants
from taz.consumers.core.database.mongodb import MongodbMixin

logger = logging.getLogger(__name__)


class ApiLuizaPickupStoreScope(MongodbMixin):

    def __init__(self, raw_product):
        self.raw_product = raw_product

    @property
    def enriched_products(self):
        return self.get_collection('enriched_products')

    def apply(self):
        pickupstore_product_count = self.enriched_products.count({
            'sku': self.raw_product['sku'],
            'seller_id': self.raw_product['seller_id'],
            'source': constants.SOURCE_API_LUIZA_PICKUPSTORE
        })

        if pickupstore_product_count == 0:
            self.raw_product['store_pickup_available'] = False
            return

        self.raw_product['store_pickup_available'] = True
