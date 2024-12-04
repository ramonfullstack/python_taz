import logging
from concurrent.futures import ThreadPoolExecutor, wait

from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.notification import Notification
from taz.consumers.rebuild.scopes.base import BaseRebuild

logger = logging.getLogger(__name__)


class RebuildCatalogNotification(MongodbMixin, BaseRebuild):
    poller_scope = 'complete_products'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notification = Notification()

    @property
    def raw_products(self):
        return self.get_collection('raw_products')

    def _rebuild(self, action, data):
        logger.info(
            'Starting catalog notification rebuild with request:{}'.format(
                data
            )
        )

        criteria = {
            'seller_id': data['seller_id'],
            'disable_on_matching': False
        }

        raw_products = self.raw_products.find(
            criteria,
            {'sku': 1, 'seller_id': 1, 'navigation_id': 1, '_id': 0},
            no_cursor_timeout=True
        )

        raw_products = list(raw_products)

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(self._send, product, action)
                for product in raw_products
            ]

        wait(futures)

        logger.info('Finish catalog notification rebuild')
        return True

    def _send(self, product, action):
        seller_id = product['seller_id']
        sku = product['sku']
        navigation_id = product['navigation_id']
        scope = 'product'

        payload = {
            'sku': sku,
            'seller_id': seller_id,
            'navigation_id': navigation_id
        }

        self.notification.put(payload, scope, action)

        logger.info(
            'Rebuild to product notification for sku:{sku} '
            'seller_id:{seller_id} navigation_id:{navigation_id} '
            'scope:{scope} action:{action}'.format(
                action=action,
                scope=scope,
                **payload
            )
        )
