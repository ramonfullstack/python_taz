import time

from maaslogger import base_logger
from simple_settings import settings

from taz.constants import (
    PRODUCT_EXPORT_ERROR_CODE,
    PRODUCT_EXPORT_ERROR_MESSAGE,
    PRODUCT_EXPORT_SUCCESS_CODE,
    PRODUCT_EXPORT_SUCCESS_MESSAGE
)
from taz.consumers.core.brokers.stream import (
    PubSubBroker,
    PubSubRecordProcessor
)
from taz.consumers.core.exceptions import InvalidScope
from taz.consumers.core.google.stream import StreamPublisherManager
from taz.consumers.product_exporter.helpers import contains_fulfillment
from taz.consumers.product_exporter.scopes import (
    PRODUCT_FEATURES,
    SIMPLE_PRODUCT,
    SOURCE_PRODUCT
)
from taz.core.notification.notification_sender import NotificationSender

SCOPE = 'product_exporter'
EXPORT_SCOPES = {
    'product_features': PRODUCT_FEATURES,
    'simple_product': SIMPLE_PRODUCT,
    'source_product': SOURCE_PRODUCT
}

logger = base_logger.get_logger(__name__)


class ProductExporterProcessor(PubSubRecordProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pubsub_manager = StreamPublisherManager()
        self.notification_sender = NotificationSender()

    def process_message(self, message):
        sku, seller_id, _type = (
            message['sku'],
            message['seller_id'],
            message['type']
        )

        try:
            product_exporter_scopes = settings.PRODUCT_EXPORTER_SCOPES[_type]
        except KeyError as error:
            logger.error(
                'Type "{type}" not found in settings from '
                'sku:{sku} seller_id:{seller_id} error:{error}'.format(
                    sku=sku,
                    seller_id=seller_id,
                    type=_type,
                    error=error
                )
            )

            return False

        for product_exporter_scope in product_exporter_scopes:
            scope_name = product_exporter_scope['scope']

            scope = self._get_scope(
                scope_name=scope_name,
                seller_id=seller_id,
                sku=sku
            )
            payload = scope.get_data()

            if not payload:
                continue

            payloads = (
                [payload]
                if not isinstance(payload, list)
                else payload
            )

            for payload in payloads:
                logger.debug(
                    'Sending data sku:{sku} '
                    'seller_id:{seller_id} scope:{scope} '
                    'to product exporter: {payload}'.format(
                        sku=sku,
                        seller_id=seller_id,
                        scope=scope.name,
                        payload=payload
                    )
                )

                try:
                    start = time.time()
                    categories = payload.get('categories', '')
                    category_id = categories[0].get('id','') if len(categories) else '' # noqa
                    publish_attributes = {
                        'seller_id': seller_id,
                        'scope': scope.name,
                        'entity': message.get('entity', ''),
                        'type': message['type'],
                        'category': category_id
                    }

                    if (
                        settings.ENABLE_FULFILLMENT and
                        contains_fulfillment(payload)
                    ):
                        publish_attributes.update(
                            {'fulfillment': str(payload['fulfillment'])}
                        )

                    self.pubsub_manager.publish(
                        content=payload,
                        topic_name=product_exporter_scope['topic_name'],
                        project_id=product_exporter_scope['project_id'],
                        attributes=publish_attributes,
                        ordering_key='{}/{}'.format(seller_id, sku).lower()
                    )

                    notification_code = PRODUCT_EXPORT_SUCCESS_CODE.format(
                        scope=scope.name.upper()
                    )

                    notification_message = PRODUCT_EXPORT_SUCCESS_MESSAGE.format(  # noqa
                        scope=scope.name
                    )

                    fulfillment = None
                    if (
                        settings.ENABLE_FULFILLMENT and
                        contains_fulfillment(payload)
                    ):
                        fulfillment = payload['fulfillment']

                    self.notification_sender.send(
                        sku=sku,
                        seller_id=seller_id,
                        code=notification_code,
                        message=notification_message,
                        payload=self._create_notification_payload(
                            payload.get('navigation_id'),
                            fulfillment
                        )
                    )

                    logger.info(
                        'Successfully sent sku:{sku} '
                        'seller_id:{seller_id} with scope {scope} '
                        'offer_id:{offer_id} to product exporter '
                        'category: {category_id} '
                        'stream in {duration} seconds'
                        .format(
                            sku=sku,
                            seller_id=seller_id,
                            offer_id=payload.get('offer_id'),
                            duration='{0:.3f}'.format(time.time() - start),
                            scope=scope.name,
                            category_id=category_id
                        )
                    )
                except Exception as error:
                    notification_code = PRODUCT_EXPORT_ERROR_CODE.format(
                        scope=scope.name.upper()
                    )

                    notification_message = PRODUCT_EXPORT_ERROR_MESSAGE.format(
                        scope=scope.name,
                        error=error
                    )

                    self.notification_sender.send(
                        sku=sku,
                        seller_id=seller_id,
                        code=notification_code,
                        message=notification_message,
                        payload=self._create_notification_payload(
                            payload.get('navigation_id')
                        )
                    )

                    logger.error(
                        'Error sending data to product exporter '
                        'sku:{sku} seller_id:{seller_id} with scope:{scope} '
                        'payload:{payload} message:{message} '
                        'error:{error}'.format(
                            sku=sku,
                            seller_id=seller_id,
                            scope=scope_name,
                            error=error,
                            message=message,
                            payload=payload
                        )
                    )

                    return False
        return True

    def _get_scope(self, scope_name, seller_id, sku):
        try:
            return EXPORT_SCOPES[scope_name](seller_id, sku)
        except Exception:
            logger.error(
                'Invalid scope "{}" from product exporter'.format(scope_name)
            )

            raise InvalidScope(scope_name=scope_name)

    def _create_notification_payload(self, navigation_id, fulfillment=None):
        payload = {'navigation_id': navigation_id} if navigation_id else {}
        if fulfillment is not None:
            payload.update({'fulfillment': fulfillment})

        return payload


class ProductExporterConsumer(PubSubBroker):
    scope = SCOPE
    record_processor_class = ProductExporterProcessor
    project_name = settings.GOOGLE_PROJECT_ID
    subscription_name = settings.PUBSUB_PRODUCT_EXPORTER_SUB_NAME
