import uuid
from typing import Dict

from maaslogger import base_logger
from simple_settings import settings

from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.google.stream import StreamPublisherManager

logger = base_logger.get_logger(__name__)


class Notification(MongodbMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.publisher = StreamPublisherManager()

    @property
    def raw_products(self):
        return self.get_collection('raw_products')

    def put(
        self,
        data: Dict,
        scope: str,
        action: str,
        origin: str = None,
        navigation_id_required: bool = True
    ):
        sku = data['sku']
        seller_id = data['seller_id']
        navigation_id = self.__get_navigation_id(data)

        if not navigation_id:
            logger.warning(
                f'Product not found from notification with sku:{sku} '
                f'seller_id:{seller_id} and scope:{scope}'
            )

            if navigation_id_required:
                return

        payload = self.format_payload(
            sku=sku,
            seller_id=seller_id,
            navigation_id=navigation_id,
            action=action,
            scope=scope,
            origin=origin,
            tracking_id=data.get('tracking_id'),
            source=data.get('source')
        )

        self._publish_to_pubsub(payload)

        logger.info(
            f'Send notification for action:{action} and type:{scope} with '
            f'sku:{sku} seller_id:{seller_id} navigation_id:{navigation_id}'
        )

    def _publish_to_pubsub(self, payload):
        attributes = {
            'seller_id': payload['seller_id'],
            'action': payload['action'],
            'type': payload['type']
        }

        self.publisher.publish(
            content=payload,
            topic_name=settings.PUBSUB_PUBLISHER_NOTIFY_TOPIC,
            project_id=settings.PUBSUB_NOTIFY_PROJECT_ID,
            attributes=attributes
        )

    def __get_navigation_id(self, data: Dict):
        if data.get('navigation_id'):
            return data['navigation_id']

        criteria = {
            'sku': data['sku'],
            'seller_id': data['seller_id']
        }

        product = self.raw_products.find_one(
            criteria,
            {'navigation_id': 1}
        ) or {}

        return product.get('navigation_id')

    @staticmethod
    def format_payload(
        sku: str,
        seller_id: str,
        navigation_id: str,
        action: str,
        scope: str,
        origin: str = None,
        tracking_id: str = None,
        source: str = None
    ):
        payload = {
            'sku': sku,
            'seller_id': seller_id,
            'navigation_id': navigation_id,
            'action': action,
            'type': scope,
            'origin': origin or scope,
            'task_id': uuid.uuid4().hex,
            'timestamp': 0
        }

        if tracking_id:
            payload['tracking_id'] = tracking_id

        if source:
            payload['source'] = source

        return payload
