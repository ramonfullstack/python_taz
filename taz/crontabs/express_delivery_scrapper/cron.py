import copy
import logging
from concurrent.futures import ThreadPoolExecutor, wait

from simple_settings import settings

from taz import constants
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.crontabs.base import CronBase
from taz.crontabs.express_delivery_scrapper.http_client import HttpClient

logger = logging.getLogger(__name__)


class ExpressDeliveryScrapperCrontab(CronBase, MongodbMixin):

    cron_name = 'ExpressDeliveryScrapper'
    zipcode = settings.EXPRESS_DELIVERY_ZIPCODE

    MAX_WORKERS = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.client = HttpClient()

        self.enriched_products = self.get_collection('enriched_products')
        self.raw_products = self.get_collection('raw_products')
        self.prices = self.get_collection('prices')

    def run(self):
        products = self.raw_products.find({
            'seller_id': constants.MAGAZINE_LUIZA_SELLER_ID,
            'disable_on_matching': False
        })

        products = list(products)
        if not products:
            logger.warning('Products not found for seller:{}'.format(
                constants.MAGAZINE_LUIZA_SELLER_ID
            ))

            return

        logger.info('{} products found'.format(len(products)))

        with ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as executor:
            futures = [
                executor.submit(self._get_product, product)
                for product in products
            ]

        wait(futures)

        logger.info('Cron successfully completed')

    def _get_product(self, product):
        criteria = {
            'sku': product['sku'],
            'seller_id': product['seller_id']
        }

        price = self.prices.find_one(criteria)
        if not price:
            logger.warning(
                'Price not found for sku:{sku} '
                'seller_id:{seller_id}'.format(**criteria)
            )

            return

        response = self.client.post(
            product['sku'],
            price['price'],
            self.zipcode
        )

        delivery_days = self._get_delivery_days(response)

        criteria.update({
            'source': constants.SOURCE_API_LUIZA_EXPRESS_DELIVERY
        })

        payload = copy.copy(criteria)
        payload.update({'delivery_days': delivery_days})

        self.enriched_products.remove(criteria)
        self.enriched_products.update(criteria, payload, upsert=True)

        logger.info(
            'Calculation information obtained for '
            'the product:{sku} with:{payload}'.format(
                sku=product['sku'],
                payload=payload
            )
        )

    def _get_delivery_days(self, response):
        modal = response['records'][0]['deliveries'][0]['modals'][0]
        return modal['shippingTime']['businessDays']


if __name__ == '__main__':  # pragma: no cover
    crontab = ExpressDeliveryScrapperCrontab()
    crontab.start()
