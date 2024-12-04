from unittest.mock import patch

import pytest

from taz.consumers.core.kafka.producer import KafkaProducer
from taz.helpers.json import json_dumps


class TestKafkaProducer:

    @pytest.fixture
    def kafka_producer(self):
        return KafkaProducer('datalake')

    @pytest.fixture
    def mock_message(self):
        return {'sku': '123', 'seller_id': 'luizalabs'}

    @pytest.fixture
    def patch_producer_publish(self):
        return patch.object(KafkaProducer, 'producer')

    def test_publish_message_with_success(
        self,
        kafka_producer,
        patch_producer_publish,
        mock_message,
        caplog
    ):
        caplog.set_level('DEBUG')

        with patch_producer_publish as mock_publish:
            kafka_producer.publish(
                topic='test',
                message=mock_message
            )

        mock_publish.produce.assert_called_with(
            topic='test',
            value=json_dumps(mock_message).encode('utf-8'),
            key=None
        )

        assert (
            'Successfully sent message to Kafka topic:test'
            in caplog.text
        )

    def test_when_publish_throws_exception_then_should_save_log_and_raise_exception( # noqa
        self,
        kafka_producer,
        patch_producer_publish,
        mock_message,
        caplog
    ):
        with patch_producer_publish as mock_publish:
            with pytest.raises(Exception):
                mock_publish.produce.side_effect = Exception
                kafka_producer.publish(
                    topic='test',
                    message=mock_message
                )

        mock_publish.assert_not_called()

        assert (
            'Error to publish message on Kafka topic:test with error:'
            in caplog.text
        )
