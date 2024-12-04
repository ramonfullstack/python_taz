import logging
from concurrent.futures import ThreadPoolExecutor, wait

from taz.constants import (
    MAGAZINE_LUIZA_SELLER_ID,
    SOURCE_API_LUIZA_PICKUPSTORE
)
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.crontabs.base import CronBase
from taz.crontabs.store_pickup_checker.http_client import (
    PickupStoresHttpClient
)

logger = logging.getLogger(__name__)


class StorePickupCheckerCrontab(CronBase, MongodbMixin):

    cron_name = 'StorePickupChecker'
    MAX_WORKERS = 10

    def __init__(self):
        self.client = PickupStoresHttpClient()
        self.raw_products = self.get_collection('raw_products')
        self.enriched_products = self.get_collection('enriched_products')

    def run(self):
        logger.info('StorePickupCheckerCrontab crontab started')
        products = self.raw_products.find(
            {
                'disable_on_matching': False,
                'seller_id': MAGAZINE_LUIZA_SELLER_ID
            },
            {
                'sku': 1,
                '_id': 0
            }
        )

        products = list(products)
        if not products:
            logger.warning(
                f'Products not found for seller:{MAGAZINE_LUIZA_SELLER_ID}'
            )
            return

        with ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as executor:
            futures = [
                executor.submit(self._save_or_delete_pickup_stores, product)
                for product in products
            ]

        wait(futures)

        logger.info('Cron successfully completed')

    def _save_or_delete_pickup_stores(self, product):
        response = self.client.get_pickup_stores(product['sku'])
        criteria = {
            'sku': product['sku'],
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'source': SOURCE_API_LUIZA_PICKUPSTORE
        }

        if response:
            self._save_pickup_stores(
                product=product,
                response=response,
                criteria=criteria
            )
        else:
            self.enriched_products.remove(criteria)

            logger.warning(
                'Product sku:{sku} seller_id:{seller_id} not available '
                'for pickup store, so it will be deleted'.format(
                    sku=product['sku'],
                    seller_id=MAGAZINE_LUIZA_SELLER_ID,
                ))

    def _save_pickup_stores(self, product, response, criteria):
        payload = {
            'sku': product['sku'],
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'source': SOURCE_API_LUIZA_PICKUPSTORE
        }

        payload.update(response)

        self.get_collection('enriched_products').update(
            criteria,
            {'$set': payload},
            upsert=True
        )

        logger.info(
            'Successfully save pickup store information for product '
            'sku:{sku} seller_id:{seller_id}'.format(
                sku=product['sku'],
                seller_id=MAGAZINE_LUIZA_SELLER_ID,
            )
        )


if __name__ == '__main__':  # pragma: no cover
    crontab = StorePickupCheckerCrontab()
    crontab.start()
