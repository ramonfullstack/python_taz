import datetime
import logging
from typing import Optional

from simple_settings import settings

from taz import constants
from taz.consumers.core.google.stream import StreamPublisherManager

logger = logging.getLogger(__name__)


class NotificationSender:

    def __init__(self):
        self.__pubsub_manager = StreamPublisherManager()

    def send(self, sku, seller_id, code, message, payload, tracking_id=None):
        notification = {
            'sku': sku,
            'seller_id': seller_id,
            'code': code,
            'message': message,
            'payload': payload,
            'action': constants.UPDATE_ACTION,
            'last_updated_at': datetime.datetime.utcnow().isoformat()
        }

        if tracking_id:
            notification['tracking_id'] = tracking_id

        logger.debug(
            f'Send notification to Patolino with sku:{sku} '
            f'seller_id:{seller_id} payload:{notification}'
        )

        publish_attributes = {
            'seller_id': notification['seller_id'],
            'code': notification['code'],
            'has_tracking': 'true' if tracking_id else 'false'
        }

        self._send_stream(notification, publish_attributes)

    def _send_stream(self, data, attributes):
        try:
            self.__pubsub_manager.publish(
                content=data,
                topic_name=settings.PATOLINO_STREAM_TOPIC_NAME,
                project_id=settings.PATOLINO_STREAM_PROJECT_ID,
                attributes=attributes
            )

            logger.debug(
                'Notification sent successfully with sku:{sku} '
                'and seller_id:{seller_id}'.format(
                    sku=data['sku'],
                    seller_id=data['seller_id']
                )
            )
        except Exception as e:
            logger.error(
                'Error sending notification to Patolino with sku:{sku} '
                'seller_id:{seller_id} '
                'payload:{payload} '
                'error:{error}'.format(
                    sku=data['sku'],
                    seller_id=data['seller_id'],
                    payload=data,
                    error=e
                )
            )
            raise e

    def notify_patolino_about_error(
        self,
        product: dict,
        action: str,
        reason: str,
        code: str
    ):
        self.send(
            sku=product['sku'],
            seller_id=product['seller_id'],
            code=code,
            message=reason,
            payload={
                'navigation_id': product.get('navigation_id'),
                'action': action
            }
        )

    def notify_patolino_about_unfinished_process(
        self,
        product: dict,
        action: str,
        reason: str,
        code: str,
        tracking_id: Optional[str] = None
    ):
        self.send(
            sku=product['sku'],
            seller_id=product['seller_id'],
            code=code,
            message=constants.PRODUCT_UNFINISHED_PROCESS_MESSAGE.format(
                sku=product['sku'],
                seller_id=product['seller_id'],
                reason=reason,
                code=code
            ),
            payload={
                'navigation_id': product.get('navigation_id'),
                'action': action
            },
            tracking_id=tracking_id
        )
