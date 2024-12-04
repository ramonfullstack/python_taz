import copy
import logging
import time

from simple_settings import settings

import taz.constants as constants
from taz.consumers.core.google.stream import StreamPublisherManager
from taz.core.notification.notification_sender import NotificationSender
from taz.core.storage.factsheet_storage import FactsheetStorage

logger = logging.getLogger(__name__)


class AcmeNotificationSender:

    def __init__(self):
        self.__notification_sender = NotificationSender()
        self.__factsheet_storage = FactsheetStorage()
        self.__pubsub = StreamPublisherManager()

    def send_factsheet(self, action, seller_id, sku, payload):
        message = copy.copy(payload)

        factsheet_url = self.__factsheet_storage.generate_external_url(
            sku=sku,
            seller_id=seller_id
        )

        if '_id' in message:
            del message['_id']

        message.update({
            'sku': sku,
            'seller_id': seller_id,
            'message_timestamp': time.time()
        })

        try:
            self.__pubsub.publish(
                content=message,
                topic_name=settings.PUBSUB_FACTSHEET_EXPORT_TOPIC_NAME,
                project_id=settings.PUBSUB_NOTIFY_PROJECT_ID,
                ordering_key='{}/{}'.format(seller_id, sku).lower()
            )

            self.__notification_sender.send(
                sku=sku,
                seller_id=seller_id,
                code=constants.SUCCESS_FACTSHEET_CODE,
                message=constants.SUCCESS_FACTSHEET_MESSAGE,
                payload={
                    'url': factsheet_url,
                    'action': action
                }
            )

            logger.info(
                f'Factsheet sku:{sku} seller_id:{seller_id} '
                f'sent to successfully for pub-sub topic:'
                f'{settings.PUBSUB_FACTSHEET_EXPORT_TOPIC_NAME}'
                f' with action:{action}'
            )
        except Exception as e:
            self.__notification_sender.send(
                sku=sku,
                seller_id=seller_id,
                code=constants.FAILURE_FACTSHEET_CODE,
                message=constants.FAILURE_FACTSHEET_MESSAGE,
                payload={
                    'url': factsheet_url,
                    'action': action
                }
            )

            logger.error(
                f'Failed to sent factsheet sku:{sku} seller_id:{seller_id} '
                f'on pub-sub topic:'
                f'{settings.PUBSUB_FACTSHEET_EXPORT_TOPIC_NAME} and '
                f'error:{e} payload:{message}'
            )
            raise
