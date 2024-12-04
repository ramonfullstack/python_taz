import logging
from concurrent.futures import ThreadPoolExecutor, wait

from simple_settings import settings

from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.rebuild.scopes.base import BaseRebuild

logger = logging.getLogger(__name__)


class RebuildCompleteProductBySeller(MongodbMixin, BaseRebuild):
    poller_scope = 'complete_products_by_seller'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def raw_products(self):
        return self.get_collection('raw_products')

    def _rebuild(self, action, data):
        logger.info(
            'Starting complete products by seller rebuild '
            'with request:{}'.format(data)
        )

        raw_products = self.raw_products.find(
            {'seller_id': data['seller_id']}
        )

        raw_products = list(raw_products)

        if not raw_products:
            logger.warning(
                'Rebuild complete product by seller not found with '
                'request:{}'.format(data)
            )

            return

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(self._send, product, action)
                for product in raw_products
            ]

        wait(futures)

        logger.info('Finish complete product by Seller rebuild')
        return True

    def _send(self, product, action):
        seller_id = product['seller_id']
        sku = product['sku']
        payload = {
            'action': action,
            'seller_id': seller_id,
            'sku': sku,
            'origin': __name__
        }
        self.pubsub_manager.publish(
            content=payload,
            topic_name=settings.PUBSUB_COMPLETE_PRODUCT_TOPIC_NAME,
            project_id=settings.GOOGLE_PROJECT_ID
        )

        logger.info(
            'Rebuild to complete product for sku:{} seller:{}'.format(
                sku, seller_id
            )
        )


class RebuildCompleteProductBySku(MongodbMixin, BaseRebuild):
    poller_scope = 'complete_products_by_sku'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _rebuild(self, action, data):
        logger.info(
            'Starting complete products by sku rebuild with '
            'request:{}'.format(data)
        )

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(self._send, product, action)
                for product in data
            ]

        wait(futures)

        logger.info('Finish complete product by SKU rebuild')
        return True

    def _send(self, product, action):
        seller_id = product['seller_id']
        sku = product['sku']

        payload = {
            'action': action,
            'seller_id': seller_id,
            'sku': sku,
            'origin': __name__
        }
        self.pubsub_manager.publish(
            content=payload,
            topic_name=settings.PUBSUB_COMPLETE_PRODUCT_TOPIC_NAME,
            project_id=settings.GOOGLE_PROJECT_ID
        )

        logger.info(
            'Rebuild to complete product for sku:{} seller:{}'.format(
                sku, seller_id
            )
        )
