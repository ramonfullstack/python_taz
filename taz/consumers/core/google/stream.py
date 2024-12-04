import json
import signal
import threading
import time

from google.cloud import pubsub, pubsub_v1
from maaslogger import base_logger
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from simple_settings import settings

from taz.consumers.core.locks import LockActiveError
from taz.helpers.json import json_dumps, json_loads
from taz.settings.otel import start_as_current_span

logger = base_logger.get_logger(__name__)


class StreamPublisherManager:

    def __init__(self):
        self.client = pubsub.PublisherClient(
            publisher_options=pubsub_v1.types.PublisherOptions(
                enable_message_ordering=True
            )
        )

    @staticmethod
    def _try_create_ordering_key(attributes: dict, content: any):
        if isinstance(content, bytes):
            try:
                content = json_loads(content)
            except Exception as e:
                logger.warning(
                    f'can not load content: {content} to dict: {str(e)}'
                )

        if isinstance(content, dict):
            seller_id = (
                content.get('seller_id', '') or
                attributes.get('seller_id', '')
            )
            sku = (
                content.get('sku') or
                attributes.get('sku', '')
            )
        else:
            seller_id = attributes.get('seller_id', '')
            sku = attributes.get('sku', '')

        if not seller_id or not sku:
            return ''

        return '{}/{}'.format(seller_id, sku).lower()

    def publish(
        self,
        content,
        topic_name,
        project_id=settings.GOOGLE_PROJECT_ID,
        attributes=None,
        ordering_key=None
    ):
        attributes = attributes or {}
        ordering_key = (
            ordering_key or self._try_create_ordering_key(
                attributes=attributes,
                content=content,
            )
        )

        if not isinstance(content, bytes):
            content = json_dumps(content).encode('utf-8')

        topic_path = self.client.topic_path(project_id, topic_name)

        with start_as_current_span(
            'pubsub.producer.publish',
            kind=trace.SpanKind.CONSUMER,
            attributes={
                'message.topic': topic_name or '',
                'message.ordering_key': ordering_key or '',
                'message.project_id': project_id or ''
            }
        ) as span:
            self.client.publish(
                topic=topic_path,
                data=content,
                ordering_key=ordering_key,
                **attributes
            )
            span.set_status(Status(StatusCode.OK))

        logger.debug(
            f'Successfully sent on topic:{topic_name} '
            f'project_id:{project_id}'
        )


class StopSubscriber(Exception):
    """Force exit from subscriber consume."""


class SubscriptionBuilder:
    def _build_subscription(self):
        subscription_path = self.client.subscription_path(
            self.project_id,
            self.subscription_name
        )
        return subscription_path


class DeadlineManager(SubscriptionBuilder):
    def __init__(self, project_id, subscription_name):
        self.client = pubsub_v1.SubscriberClient()
        self.project_id = project_id
        self.subscription_name = subscription_name
        self.subscription_path = self._build_subscription()

    def try_modify_ack_deadline(self, ack_id, new_deadline_in_seconds=60):
        try:
            self.client.modify_ack_deadline(
                request={
                    "subscription": self.subscription_path,
                    "ack_ids": [ack_id],
                    "ack_deadline_seconds": new_deadline_in_seconds,
                }
            )
        except Exception as e:
            logger.warning(
                f'can not modify ack deadline: {ack_id}: {e}'
            )


class PubSubSubscriber(SubscriptionBuilder):
    def __init__(self, project_id, subscription_name):
        self.project_id = project_id
        self.client = pubsub.SubscriberClient()
        self.subscription_name = subscription_name
        self.subscription_path = self._build_subscription()

        self._stop = threading.Event()
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def stop(self, *_):  # pragma: no cover
        if self.is_stopped():
            return
        self._stop.set()

    def is_stopped(self):  # pragma: no cover
        return self._stop.is_set()

    def subscribe(self, handler_function, max_messages=100, **kwargs):
        try:
            self.handler_function = handler_function
            subscription = self.client.subscribe(
                subscription=self.subscription_path,
                callback=self._wrapper,
                flow_control=pubsub_v1.types.FlowControl(
                    max_messages=max_messages, **kwargs
                )
            )
            logger.info(
                'Listening for messages on "{subscription_name}" '.format(
                    subscription_name=self.subscription_name
                )
            )
            if settings.PUBSUB_LOOP_ENABLED:
                self._loop()
            subscription.cancel()
        except Exception as error:
            logger.error(
                'Failed to close subscription gracefully '
                f'with error {error}'
            )

    def _wrapper(self, event):
        payload = {}
        with start_as_current_span(
            'pubsub.consumer.process_message',
            kind=trace.SpanKind.CONSUMER,
            attributes={
                'message.subscription_name': self.subscription_name or '',
                'message.ordering_key': event.ordering_key or '',
                'message.project_id': self.project_id or ''
            }
        ) as span:
            try:
                self._wrapper_process(event)

                span.set_status(Status(StatusCode.OK))

            except StopSubscriber as e:
                logger.warning(
                    'Forced stop of subscriber by '
                    f'callback:{self.handler_function}'
                )
                span.set_status(Status(StatusCode.ERROR))
                span.record_exception(e)
                event.nack()
                self.stop()
            except LockActiveError as e:
                logger.warning(
                    'Event with sku:{sku} seller_id:{seller_id} '
                    'tracking_id:{tracking_id} already lock in '
                    'redis:{error}'.format(
                        sku=payload.get('sku'),
                        seller_id=payload.get('seller_id'),
                        tracking_id=payload.get('tracking_id'),
                        error=e
                    )
                )
                span.set_status(Status(StatusCode.ERROR))
                span.record_exception(e)
                event.nack()
            except Exception as e:
                logger.exception(
                    f'Error while processing event:{e}',
                    exc_info=True,
                    stack_info=True,
                    stacklevel=2
                )
                span.set_status(Status(StatusCode.ERROR))
                span.record_exception(e)
                event.nack()

                raise

    def _wrapper_process(self, event):
        response = self.handler_function(
            json.loads(event.data)
        )
        if response is False:
            event.nack()
        else:
            event.ack()

    def _loop(self):  # pragma: no cover
        while True:
            try:
                if self.is_stopped():
                    break
                time.sleep(1)
            except KeyboardInterrupt:
                break


class PubSubSubscriberRawEvent(PubSubSubscriber):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _wrapper_process(self, event):
        response = self.handler_function(event)
        if response is False:
            event.nack()
        else:
            event.ack()
