import json

import pytest
from simple_settings import settings

from taz.consumers.core.google.stream import (
    PubSubSubscriber,
    StreamPublisherManager
)
from taz.consumers.core.locks import LockActiveError


class FakeEventPubSub:

    def __init__(self):
        self.data = json.dumps({'message': 'fake'})
        self.ordering_key = 'fake_key'

    def nack(self):  # pragma: no cover
        pass


class TestStreamPublisherManager:

    @pytest.fixture
    def stream_publisher_manager(self):
        return StreamPublisherManager()

    @pytest.fixture
    def pubsub_subscriber(self):
        return PubSubSubscriber('fake_project_id', 'fake_sub_name')

    def test_should_publish_event(
        self,
        stream_publisher_manager,
        patch_pubsub_client
    ):
        payload = {'name': 'murcho'}
        with patch_pubsub_client as mock:
            stream_publisher_manager.publish(
                payload,
                settings.TEST_TOPIC_NAME
            )

        assert mock.called

        content = json.loads(mock.call_args[1]['data'].decode('utf-8'))

        assert content == {'name': 'murcho'}

    def test_when_catch_exception_lock_active_error_then_should_save_log(
        self,
        pubsub_subscriber,
        caplog
    ):
        pubsub_subscriber.subscribe(self.handler_function_exception)
        pubsub_subscriber._wrapper(FakeEventPubSub())

        assert 'already lock in redis:Error' in caplog.text

    def handler_function_exception(self, event):
        raise LockActiveError('Error')
