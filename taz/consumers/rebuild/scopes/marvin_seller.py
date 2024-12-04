import logging
from concurrent.futures import ThreadPoolExecutor, wait

from marshmallow import Schema, fields, validate
from simple_settings import settings

from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.rebuild.scopes.base import BaseRebuild

logger = logging.getLogger(__name__)


class MarvinSellerDataSchema(Schema):
    seller_id = fields.String(
        validate=[validate.Length(min=1, max=250)],
        required=True
    )

    min_sku = fields.String()
    max_sku = fields.String()


class RebuildMarvinSeller(MongodbMixin, BaseRebuild):
    schema_class = MarvinSellerDataSchema
    poller_scope = 'marvin_seller'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.raw_products = self.get_collection('raw_products')

    def _rebuild(self, action, data):
        logger.info(
            f'Starting marvin seller rebuild with action:{action} '
            f'request:{data}'
        )

        if action not in ['update', 'delete']:
            logger.warning(
                f'Invalid action [{action}] on '
                'rebuild marvin sellers'
            )
            return True

        seller_id = data.get('seller_id')
        min_sku = data.get('min_sku')
        max_sku = data.get('max_sku')

        criteria = {
            'seller_id': seller_id,
            'disable_on_matching': False,
            'sku': {'$gte': min_sku, '$lte': max_sku}
        }

        products = self.raw_products.find(criteria)

        if not products:
            logger.warning(
                'Raw products not found on '
                f'rebuild marvin sellers with criteria:{criteria} '
            )
            return True

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(self._send, product, action)
                for product in products
            ]

        wait(futures)
        return True

    def _send(self, product, action):
        seller_id = product['seller_id']
        sku = product['sku']
        navigation_id = product['navigation_id']

        payload = {
            'action': action,
            'seller_id': seller_id,
            'sku': sku,
            'type': 'product',
            'navigation_id': navigation_id,
            'origin': 'force-taz'
        }

        try:
            self.pubsub_manager.publish(
                content=payload,
                topic_name=settings.MARVIN_NOTIFICATION['topic_name'],
                project_id=settings.MARVIN_NOTIFICATION['project_id'],
                attributes={
                    'subscription_id': 'marvin-gateway-force-taz-sub'
                }
            )
        except Exception as e:
            logger.error(
                'An error occurred while rebuild marvin on pubsub '
                f'with error:{e} payload:{payload}'
            )

            raise

        logger.info(
            f'Rebuild to marvin seller for sku:{sku} '
            f'seller_id:{seller_id} action:{action}'
        )
