import logging
from concurrent.futures import ThreadPoolExecutor, wait
from datetime import datetime

from simple_settings import settings

from taz import constants
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.notification import Notification
from taz.consumers.rebuild.scopes.base import BaseRebuild
from taz.core.notification.notification_sender import NotificationSender
from taz.helpers.pagination import Pagination

logger = logging.getLogger(__name__)


class RebuildSellerSellsToCompany(MongodbMixin, BaseRebuild):
    poller_scope = 'seller_sells_to_company'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notification = Notification()
        self.notification_sender = NotificationSender()
        self.pagination = Pagination(self.raw_products)

    @property
    def raw_products(self):
        return self.get_collection('raw_products')

    def _rebuild(self, action, data):
        seller_id = data.get('id')
        sku = data.get('sku')
        sells_to_company = data.get('sells_to_company')

        logger.info(
            'Starting sells_to_company rebuild for '
            'seller_id:{seller_id}'.format(seller_id=seller_id)
        )

        criteria = {
            'seller_id': seller_id,
            'disable_on_matching': False
        }

        products = self.pagination._paginate_keyset(
            criteria=criteria,
            fields={'sku': 1, 'seller_id': 1, 'navigation_id': 1, '_id': 0},
            limit_size=int(settings.LIMIT_REBUILD_SELLER_PRODUCTS),
            sort=[('sku', 1)],
            field_offset='sku',
            offset=sku
        )

        products = list(products)

        if not products and not sku:
            logger.info(
                'Rebuild sells_to_company found no active products for '
                'seller_id:{seller_id}'.format(seller_id=seller_id)
            )
            return True

        elif not products:
            logger.info(
                'Finish rebuild sells_to_company for '
                'seller_id:{seller_id}'.format(seller_id=seller_id)
            )
            return True

        logger.info(
            'Rebuild sells_to_company found {quantity} active products '
            'for seller_id:{seller_id}'.format(
                quantity=len(products),
                seller_id=seller_id
            )
        )

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(
                    self._save_and_notify_product, product, sells_to_company
                )
                for product in products
            ]

        wait(futures)

        payload = {
            'scope': 'seller_sells_to_company',
            'action': action,
            'data': {
                'id': seller_id,
                'sku': products[-1]['sku']
            }
        }

        self.pubsub_manager.publish(
            content=payload,
            topic_name=settings.PUBSUB_REBUILD_TOPIC_NAME,
            project_id=settings.GOOGLE_PROJECT_ID
        )
        return True

    def _save_and_notify_product(self, product, sells_to_company):
        self._update_sells_to_company(product, sells_to_company)
        self._notification(product)

    def _update_sells_to_company(self, product, sells_to_company):
        seller_id = product['seller_id']
        sku = product['sku']

        now = datetime.utcnow().isoformat()

        self.raw_products.update_many(
            {'sku': sku, 'seller_id': seller_id},
            {
                '$set': {
                    'sells_to_company': sells_to_company,
                    'updated_at': now,
                    'md5': ''
                }
            }
        )

    def _notification(self, product):
        payload = {
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'navigation_id': product['navigation_id']
        }

        self.notification.put(payload, 'product', constants.UPDATE_ACTION)
