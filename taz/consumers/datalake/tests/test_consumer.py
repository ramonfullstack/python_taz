import importlib
from unittest.mock import patch

import pytest
from simple_settings.utils import settings_stub

from taz.constants import MAGAZINE_LUIZA_SELLER_ID
from taz.consumers.datalake.consumer import DataLakeProcessor
from taz.consumers.datalake.tests.scopes import fake_scope
from taz.consumers.datalake.tests.scopes.fake_scope import Scope
from taz.helpers.json import json_dumps


class TestDataLakeConsumer:

    @pytest.fixture
    def consumer(self):
        return DataLakeProcessor('datalake')

    @pytest.fixture
    def patch_import_module_scope(self):
        return patch.object(importlib, 'import_module')

    @pytest.fixture
    def patch_get_data(self):
        return patch.object(Scope, 'get_data')

    def test_when_process_with_success_then_should_send_message_to_all_streams(
        self,
        consumer,
        patch_import_module_scope,
        patch_publish_manager,
        patch_kafka_producer,
        patch_get_data,
        caplog
    ):
        data = {
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'sku': '123'
        }

        with patch_import_module_scope as mock_scope:
            with patch_get_data as mock_get_data:
                with patch_publish_manager as mock_publish_pubsub:
                    with patch_kafka_producer as mock_kafka_producer:
                        mock_scope.return_value = fake_scope
                        mock_get_data.return_value = data
                        response = consumer.process_message({
                            **data,
                            'navigation_id': '123456789',
                            'type': 'fake_scope'
                        })

        assert response
        mock_publish_pubsub.assert_called_once_with(
            content={'data': {**data}, 'schema': 'fake_scope'},
            topic_name='fake',
            project_id='maga-homolog'
        )
        mock_kafka_producer.produce.assert_called_once_with(
            topic='fake',
            value=json_dumps(data).encode('utf-8'),
            key=None
        )
        assert mock_scope.call_args[0][0] == (
            'taz.consumers.datalake.scopes.fake_scope'
        )

        for stream in ['niagara', 'tetrix']:
            assert (
                f'Successfully sent sku:123 '
                f'seller_id:magazineluiza navigation_id:123456789 '
                f'with scope fake_scope to Datalake stream:{stream}'
            ) in caplog.text

    def test_when_schema_is_invalid_then_should_not_publish_message(
        self,
        consumer,
        patch_publish_manager,
        patch_kafka_producer,
        caplog
    ):
        with patch_publish_manager as mock_publish_pubsub:
            with patch_kafka_producer as mock_kafka_producer:
                result = consumer.process_message({
                    'seller_id': 'xablau',
                    'sku': '123456789',
                    'navigation_id': '123456789',
                    'type': 'invalid_scope'
                })

        assert not result
        mock_publish_pubsub.assert_not_called()
        mock_kafka_producer.produce.assert_not_called()

        assert (
            'Error sending data to datalake sku:123456789 '
            'seller_id:xablau with scope:invalid_scope '
            'error:Unknown scope name:invalid_scope '
        ) in caplog.text

    def test_when_payload_is_empty_then_should_not_publish_message(
        self,
        consumer,
        patch_import_module_scope,
        patch_publish_manager,
        patch_kafka_producer,
        patch_get_data
    ):
        with patch_import_module_scope as mock_scope:
            with patch_publish_manager as mock_publish_pubsub:
                with patch_kafka_producer as mock_kafka_producer:
                    with patch_get_data as mock_get_data:
                        mock_scope.return_value = fake_scope
                        mock_get_data.return_value = []

                        response = consumer.process_message({
                            'sku': '2027604',
                            'seller_id': 'dbestshop-online',
                            'navigation_id': '7623510',
                            'action': 'update',
                            'type': 'product',
                            'origin': 'product',
                            'task_id': '3f08006f9fb94770bdfe0f27c18adf17',
                            'timestamp': 0
                        })

        assert response is True
        mock_publish_pubsub.assert_not_called()
        mock_kafka_producer.produce.assert_not_called()

    def test_when_payload_is_list_then_should_process_with_success(
        self,
        consumer,
        patch_import_module_scope,
        patch_publish_manager,
        patch_kafka_producer,
        patch_get_data
    ):
        with patch_import_module_scope as mock_scope:
            with patch_publish_manager as mock_publish_pubsub:
                with patch_kafka_producer as mock_kafka_producer:
                    with patch_get_data as mock_get_data:
                        mock_scope.return_value = fake_scope
                        mock_get_data.return_value = [
                            {
                                'foo': 'bar',
                                'seller_id': 'dbestshop-online',
                                'sku': '2027604',
                                'scope_name': 'fake_scope'
                            },
                            None
                        ]

                        response = consumer.process_message({
                            'sku': '2027604',
                            'seller_id': 'dbestshop-online',
                            'navigation_id': '7623510',
                            'action': 'update',
                            'type': 'product',
                            'origin': 'product',
                            'task_id': '3f08006f9fb94770bdfe0f27c18adf17',
                            'timestamp': 0
                        })

        assert response is True
        mock_publish_pubsub.assert_called_once()
        mock_kafka_producer.produce.assert_called_once()

    @settings_stub(
        DATALAKE={'fake_scope': {
            'niagara': {
                'topic_name': 'fake',
                'project_id': 'maga-homolog',
                'enabled': True
            },
            'tetrix': {
                'topic_name': 'fake',
                'enabled': False
            }
        }}
    )
    def test_when_stream_not_enabled_then_should_not_publish_message(
        self,
        consumer,
        patch_import_module_scope,
        patch_publish_manager,
        patch_kafka_producer,
        patch_get_data,
    ):
        data = {
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'sku': '123'
        }

        with patch_import_module_scope as mock_scope:
            with patch_get_data as mock_get_data:
                with patch_publish_manager as mock_publish_pubsub:
                    with patch_kafka_producer as mock_kafka_producer:
                        mock_scope.return_value = fake_scope
                        mock_get_data.return_value = data
                        response = consumer.process_message({
                            **data,
                            'navigation_id': '123456789',
                            'type': 'fake_scope'
                        })

        assert response is True
        mock_publish_pubsub.assert_called_once()
        mock_kafka_producer.produce.assert_not_called()
