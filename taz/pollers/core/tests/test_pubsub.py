import json

import pytest
from simple_settings import settings

from taz.pollers.core.brokers.pubsub import StreamPublisherManager


class TestStreamPublisherManager:

    @pytest.fixture
    def stream_publisher_manager(self):
        return StreamPublisherManager()

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
