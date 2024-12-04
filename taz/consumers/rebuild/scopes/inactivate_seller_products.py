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


class RebuildInactivateSellerProducts(MongodbMixin, BaseRebuild):
    poller_scope = 'inactivate_seller_products'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notification = Notification()
        self.notification_sender = NotificationSender()
        self.pagination = Pagination(self.raw_products)

    @property
    def raw_products(self):
        return self.get_collection('raw_products')

    def _rebuild(self, action, data):
        logger.info(
            'Starting inactivate seller products rebuild '
            'with request:{}'.format(data)
        )

        if data['seller_id'] in settings.UNBLOCKABLE_SELLERS:
            logger.warning(
                'Rebuild inactive products cant inactive '
                'seller:{} products'.format(data['seller_id'])
            )

            return True

        seller_id = data.get('seller_id')
        sku = data.get('sku')

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
            logger.warning(
                'Rebuild inactive products found no active products '
                'request:{}'.format(data)
            )
            return True
        elif not products:
            logger.info(
                'Finish inactivate seller products rebuild for '
                'seller_id:{seller_id}'.format(
                    seller_id=seller_id
                )
            )
            return True

        logger.warning(
            'Rebuild inactive products found {quantity} active products '
            'for seller_id:{seller_id}'.format(
                quantity=len(products),
                seller_id=data['seller_id']
            )
        )

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(
                    self._save_and_notify_product, product,
                    data.get('inactive_reason')
                )
                for product in products
            ]

        wait(futures)

        payload = {
            'scope': 'inactivate_seller_products',
            'action': action,
            'data': {
                'seller_id': seller_id,
                'sku': products[-1]['sku']
            }
        }

        self.pubsub_manager.publish(
            content=payload,
            topic_name=settings.PUBSUB_REBUILD_TOPIC_NAME,
            project_id=settings.GOOGLE_PROJECT_ID
        )
        return True

    def _save_and_notify_product(self, product, inactive_reason):
        self._inactivate_product(product)
        self._notification(product, inactive_reason)

    def _notification(self, product, inactive_reason):
        payload = {
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'navigation_id': product['navigation_id']
        }

        self.notification.put(payload, 'product', constants.UPDATE_ACTION)

        if inactive_reason:
            self.notification_sender.send(
                sku=product['sku'],
                seller_id=product['seller_id'],
                code=constants.MAAS_PRODUCT_INACTIVATION_SELLER_SUCCESS_CODE,
                message=inactive_reason,
                payload=payload
            )

    def _inactivate_product(self, product):
        seller_id = product['seller_id']
        sku = product['sku']

        now = datetime.utcnow().isoformat()

        self.raw_products.update_many(
            {'sku': sku, 'seller_id': seller_id},
            {
                '$set': {
                    'disable_on_matching': True,
                    'updated_at': now,
                    'md5': ''
                }
            }
        )
