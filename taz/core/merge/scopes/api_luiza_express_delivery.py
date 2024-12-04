import logging

from taz import constants
from taz.consumers.core.database.mongodb import MongodbMixin

logger = logging.getLogger(__name__)


class ApiLuizaExpressDelivery(MongodbMixin):

    def __init__(self, raw_product):
        self.raw_product = raw_product

    @property
    def enriched_products(self):
        return self.get_collection('enriched_products')

    def apply(self):
        criteria = {
            'sku': self.raw_product['sku'],
            'seller_id': self.raw_product['seller_id'],
            'source': constants.SOURCE_API_LUIZA_EXPRESS_DELIVERY
        }

        enriched_product = self.enriched_products.find_one(criteria)

        if not enriched_product:
            logger.warning(
                'Enriched product not found from sku:{sku} '
                'seller_id:{seller_id} source:{source}'.format(**criteria)
            )

            return

        if enriched_product['delivery_days'] in [1, 2]:
            self.raw_product['delivery_plus_1'] = True
            self.raw_product['delivery_plus_2'] = False
