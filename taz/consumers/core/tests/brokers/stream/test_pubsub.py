from json import dumps
from unittest.mock import patch

import pytest
from simple_settings.utils import settings_stub

from taz.consumers.core.brokers.stream.pubsub import (
    PubSubBroker,
    PubSubRecordProcessor
)

methods_actions = [
    ('create', 'create'),
    ('update', 'update'),
    ('delete', 'remove')
]


class TestPubSubPubSubRecordProcessor:

    @pytest.fixture
    def record_processor(self):
        return PubSubRecordProcessor('test')

    def test_process_record_call_with_data(
        self, record_processor
    ):
        data = dumps({'action': 'test', 'data': 'data_test'})
        result = record_processor.process_message(message=data)
        assert result is None
        assert record_processor.scope == 'test'


class FakePubSubBroker(PubSubBroker):
    record_processor_class = PubSubRecordProcessor
    scope = 'fake'
    project_name = scope
    topic_name = 'fake_topic'


class TestPubSubPubSubBroker:

    @pytest.fixture
    def pubsub_broker(self, logger_stream):
        fake = FakePubSubBroker()

        log = logger_stream.getvalue()

        assert 'Listening pubsub on subscription fake\n' in log
        return fake

    @patch('time.sleep', return_value=None)
    def test_run_start(self, mock_time, pubsub_broker):
        pubsub_broker.start()
        assert mock_time.called

    @settings_stub(PUBSUB_SUBSCRIPTION_ID="")
    def test_pubsub_broker_without_sub_name(self, monkeypatch, pubsub_broker):
        with pytest.raises(AttributeError):
            FakePubSubBroker()
