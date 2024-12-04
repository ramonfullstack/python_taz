import logging
from concurrent.futures import ThreadPoolExecutor, as_completed, wait

from google.cloud import pubsub, pubsub_v1
from simple_settings import settings

from taz.helpers.json import json_dumps
from taz.pollers.core.exceptions import SendRecordsException

from .base import BaseBroker
from .exceptions import MissingPollerSettingException

logger = logging.getLogger(__name__)


class PubSubBroker(BaseBroker):

    def __init__(self, scope):
        if scope not in settings.POLLERS.keys():
            raise MissingPollerSettingException(
                'Poller {} is not properly set on settings file'.format(scope)
            )

        super().__init__()

        self.scope = scope
        self.waits = {}
        self.halt_requested = False
        self.executor = ThreadPoolExecutor(
            max_workers=settings.SENDER_MAX_WORKERS
        )
        self.pubsub = StreamPublisherManager()

    def put_many(self, action, dataset):
        if self.halt_requested:
            return

        self.waits = {
            self.executor.submit(
                self._process_record,
                action,
                item
            ): item
            for item in dataset if not self.halt_requested
        }

        process_fail = False
        completed, _ = wait(self.waits)
        for future in completed:
            item = self.waits[future]
            try:
                future.result()
            except Exception:
                logger.exception(
                    'Encountered an exception while send many records to '
                    'Scope "{}" with action "{}": {}'.format(
                        self.scope, action, item
                    )
                )
                process_fail = True

        if process_fail:
            raise SendRecordsException()

    def shutdown(self):
        if not self.waits:
            return

        logger.warning('Requesting executor shutdown...')

        self.executor.shutdown(wait=True)
        self.halt_requested = True

        for future in as_completed(self.waits):
            logger.warning(
                'Thread with item {} was completed'.format(self.waits[future])
            )

            try:
                future.result()
            except Exception as e:
                logger.error(e)

    def _publish(self, action, payload, ordering_key):
        self.pubsub.publish(
            content=payload,
            topic_name=settings.POLLERS[self.scope]['topic_name'],
            project_id=settings.POLLERS[self.scope]['project_id'],
            ordering_key=ordering_key,
        )
        logger.info(
            'Sent to scope:{scope} with action:{action} '
            'topic_name:{topic_name} project_id:{project_id}'.format(
                scope=self.scope,
                action=action,
                topic_name=settings.POLLERS[self.scope]['topic_name'],
                project_id=settings.POLLERS[self.scope]['project_id']
            )
        )

    def _process_record(self, action, item):
        if self.halt_requested:
            return

        payload = {
            'action': action,
            'item': item,
        }

        ordering_key = None
        seller_id = item.get('seller_id', '')
        sku = item.get('sku', '')
        if seller_id and sku:
            ordering_key = f'{seller_id}/{sku}'

        self._publish(action, payload, ordering_key)


class PubSubBrokerWithData(PubSubBroker):

    def __init__(self, scope, ordering_key=None):
        super().__init__(scope)
        self.ordering_key = ordering_key

    def _process_record(self, action, item):
        if self.halt_requested:
            return

        payload = {
            'action': action,
            'data': item,
        }

        ordering_key = None
        seller_id = item.get('seller_id', '')
        sku = item.get('sku', '')
        ordering_key_value = item.get(self.ordering_key, '')
        if seller_id and sku:
            ordering_key = f'{seller_id}/{sku}'
        elif ordering_key_value:
            ordering_key = f'{ordering_key_value}'

        self._publish(action, payload, ordering_key)


class StreamPublisherManager:

    def __init__(self):
        self.client = pubsub.PublisherClient(
            publisher_options=pubsub_v1.types.PublisherOptions(
                enable_message_ordering=True
            )
        )

    def publish(
        self,
        content,
        topic_name,
        project_id=settings.GOOGLE_PROJECT_ID,
        ordering_key=None
    ):
        content = json_dumps(content).encode('utf-8')
        topic_path = self.client.topic_path(project_id, topic_name)
        future = self.client.publish(
            topic=topic_path,
            data=content,
            ordering_key=ordering_key,
        )
        logger.debug(
            'Successfully sent:{content} on topic:{topic_name} '
            'project_id:{project_id} topic_path:{topic_path} '
            'result:{result}'.format(
                content=content,
                topic_name=topic_name,
                project_id=project_id,
                topic_path=topic_path,
                result=future.result()
            )
        )
