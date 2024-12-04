from maaslogger import base_logger
from simple_settings import settings

from taz.consumers.catalog_notification import SCOPE
from taz.consumers.catalog_notification.router import CatalogNotificationRouter
from taz.consumers.core.brokers.stream import (
    PubSubBrokerRawEvent,
    PubSubRecordProcessor
)
from taz.consumers.core.google.stream import StreamPublisherManager

logger = base_logger.get_logger(__name__)


class CatalogNotificationProcessor(PubSubRecordProcessor):
    scope = SCOPE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.router = CatalogNotificationRouter(
            publisher=StreamPublisherManager()
        )

    def process_message(self, message):
        try:
            self.router.route(message=message)
            return True
        except Exception as e:
            logger.error(
                f'error:{str(e)} on route message:{str(message.attributes)}'
            )

            return False


class CatalogNotificationConsumer(PubSubBrokerRawEvent):
    scope = SCOPE
    record_processor_class = CatalogNotificationProcessor
    project_name = settings.GOOGLE_PROJECT_ID
