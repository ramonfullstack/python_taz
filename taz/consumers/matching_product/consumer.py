from functools import cached_property
from typing import Dict

from maaslogger import base_logger
from simple_settings import settings

from taz.constants import UPDATE_ACTION
from taz.consumers.core.brokers.stream import (
    PubSubBroker,
    PubSubRecordProcessor
)
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.google.stream import StreamPublisherManager

logger = base_logger.get_logger(__name__)


class MatchingProductProcessor(PubSubRecordProcessor, MongodbMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @cached_property
    def raw_products(self):
        return self.get_collection('raw_products')

    @cached_property
    def pubsub(self):
        return StreamPublisherManager()

    def publish(self, content: Dict, attributes):
        self.pubsub.publish(
            content=content,
            attributes=attributes,
            topic_name=settings.PUBSUB_MATCHING_PRODUCT_TOPIC_NAME,
            project_id=settings.GOOGLE_PROJECT_ID
        )

    def process_message(self, message):
        navigation_id = message['navigation_id']
        sku = message['sku']
        seller_id = message['seller_id']
        matching_uuid = message.get('matching_uuid')
        matching_type = message.get('matching_type')
        parent_matching_uuid = message.get('parent_matching_uuid')

        payload = {
            'matching_uuid': matching_uuid,
            'matching_type': matching_type
        } if matching_uuid else {
            'parent_matching_uuid': parent_matching_uuid
        }

        result = self.raw_products.update_one(
            {'sku': sku, 'seller_id': seller_id},
            {'$set': payload}
        )

        if result.modified_count == 0:
            logger.warning(
                f'sku:{sku} seller_id:{seller_id} navigation_id:'
                f'{navigation_id} matching_uuid:{matching_uuid} matching_type:'
                f'{matching_type} parent_matching_uuid:{parent_matching_uuid} '
                'cannot update the product',
                detail={
                    "sku": sku,
                    "seller_id": seller_id,
                    "navigation_id": navigation_id,
                    "matching_uuid": matching_uuid,
                    "matching_type": matching_type,
                    "parent_matching_uuid": parent_matching_uuid
                }
            )
            return True

        attributes = {
            'scope': self.scope,
            'action': UPDATE_ACTION
        }
        content = {
            'sku': sku,
            'seller_id': seller_id,
            'navigation_id': navigation_id,
            'tracking_id': None,
            **attributes
        }
        self.publish(
            content=content,
            attributes=attributes
        )
        logger.info(
            f'sku:{sku} seller_id:{seller_id} navigation_id:{navigation_id} '
            f'matching_uuid:{matching_uuid} matching_type:{matching_type} '
            f'parent_matching_uuid:{parent_matching_uuid} was updated '
            'and pubsub stream successfully',
            detail={
                "sku": sku,
                "seller_id": seller_id,
                "navigation_id": navigation_id,
                "matching_uuid": matching_uuid,
                "matching_type": matching_type,
                "parent_matching_uuid": parent_matching_uuid
            }
        )


class MatchingProductConsumer(PubSubBroker):
    project_name = settings.GOOGLE_PROJECT_ID
    scope = 'matching_product'
    record_processor_class = MatchingProductProcessor
