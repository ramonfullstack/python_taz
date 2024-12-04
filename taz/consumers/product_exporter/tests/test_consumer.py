import json

import pytest
from simple_settings.utils import settings_stub

from taz.consumers.core.exceptions import InvalidScope
from taz.consumers.product_exporter.consumer import (
    SCOPE,
    ProductExporterProcessor
)
from taz.consumers.product_exporter.tests.scopes import (
    empty_fake_scope,
    fake_scope,
    fake_scope_with_categories,
    fulfillment_fake_scope
)

TEST_SCOPES = {
    'fake_scope': fake_scope.Scope,
    'empty_fake_scope': empty_fake_scope.Scope,
    'fulfillment_fake_scope': fulfillment_fake_scope.Scope,
    'fake_scope_with_categories': fake_scope_with_categories.Scope,
}


class TestProductExporterConsumer:

    @pytest.fixture
    def consumer(self):
        return ProductExporterProcessor(scope=SCOPE)

    @pytest.fixture
    def mock_message_with_category_field(self):
        return {
            'seller_id': 'xablau',
            'sku': '123456789',
            'type': 'product',
            'categories': [
                {
                    'id': 'IN',
                    'subcategories': [
                        {
                            'id': 'MRAM',
                            'name': 'Memória RAM'
                        }
                    ]
                }
            ]
        }

    @pytest.fixture
    def mock_message(self):
        return {
            'seller_id': 'xablau',
            'sku': '123456789',
            'type': 'product'
        }

    @pytest.fixture
    def mock_message_with_fulfillment(self):
        return {
            'seller_id': 'xablau',
            'sku': '123456789',
            'type': 'product',
            'fulfillment': True
        }

    def get_test_scope(self, scope_name='fake_scope', seller_id='', sku=''):
        return TEST_SCOPES[scope_name](seller_id, sku)

    def get_fulfillment_scope(
        self,
        scope_name='fake_scope',
        seller_id='',
        sku=''
    ):
        return self.get_test_scope(
            scope_name='fulfillment_fake_scope',
            seller_id=seller_id,
            sku=sku
        )

    def get_category_scope(
        self,
        scope_name='fake_scope',
        seller_id='',
        sku=''
    ):
        return TEST_SCOPES['fake_scope_with_categories'](seller_id, sku)

    def test_should_send_to_pubsub_calling_fake_scope_module(
        self,
        consumer,
        patch_pubsub_client,
        patch_patolino_product_post,
        mock_message
    ):
        sku = mock_message['sku']
        seller_id = mock_message['seller_id']
        with patch_pubsub_client as mock_pubsub:
            with patch_patolino_product_post as patolino_mock:
                consumer._get_scope = self.get_test_scope
                response = consumer.process_message(mock_message)

        assert patolino_mock.call_count == 1

        patolino_payload = patolino_mock.call_args[0][0]
        assert patolino_payload['sku'] == sku
        assert patolino_payload['seller_id'] == seller_id
        assert patolino_payload['code'] == 'PRODUCT_EXPORTER_FAKE_SCOPE_SUCCESS' # noqa
        assert patolino_payload['message'] == (
            'Successfully processed on product_exporter '
            'with scope fake_scope'
        )
        assert patolino_payload['payload'] == {
            'navigation_id': 'bar'
        }

        assert response is True

        assert mock_pubsub.call_args[1]['scope'] == 'fake_scope'
        assert mock_pubsub.call_args[1]['entity'] == ''
        assert mock_pubsub.call_args[1]['seller_id'] == 'xablau'
        assert mock_pubsub.call_args[1]['ordering_key'] == '{}/{}'.format(
            mock_message['seller_id'],
            mock_message['sku']
        ).lower()

        payload = json.loads(mock_pubsub.call_args[1]['data'].decode('utf-8'))
        assert payload == {
            'foo': 'bar',
            'seller_id': 'xablau',
            'sku': '123456789',
            'navigation_id': 'bar'
        }

    def test_should_not_send_to_pubsub_and_notification_if_scope_is_invalid(
        self,
        consumer,
        patch_pubsub_client,
        caplog,
        patch_patolino_product_post,
        mock_message
    ):
        mock_message['type'] = 'enriched_product'
        with patch_pubsub_client as mock_pubsub:
            with patch_patolino_product_post as notification_mock:
                with pytest.raises(InvalidScope) as e:
                    consumer.process_message(mock_message)

        assert e
        assert mock_pubsub.call_count == 0
        assert notification_mock.call_count == 0

        assert (
            'Invalid scope "invalid_scope" from product exporter'
        ) in caplog.records[0].getMessage()

    def test_should_not_send_to_pubsub_and_notification_if_type_is_invalid(
        self,
        consumer,
        patch_pubsub_client,
        caplog,
        patch_patolino_product_post,
        mock_message
    ):
        mock_message['type'] = 'invalid_type'
        with patch_pubsub_client as mock_pubsub:
            with patch_patolino_product_post as patolino_mock:
                result = consumer.process_message(mock_message)

        assert not result
        assert mock_pubsub.call_count == 0
        assert patolino_mock.call_count == 0

        assert (
            'Type "invalid_type" not found in settings from sku:123456789 '
            'seller_id:xablau error:\'invalid_type\''
        ) in caplog.records[0].getMessage()

    def test_should_notify_when_error_sending_to_pubsub(
        self,
        consumer,
        patch_pubsub_client,
        patch_patolino_product_post,
        caplog,
        mock_message
    ):
        with patch_pubsub_client as mock_pubsub:
            with patch_patolino_product_post as patolino_mock:
                consumer._get_scope = self.get_test_scope
                mock_pubsub.side_effect = Exception(
                    'Error sending to pubsub'
                )

                response = consumer.process_message(mock_message)

        assert response is False

        assert mock_pubsub.call_count == 1
        error_log = caplog.records[0].getMessage()

        assert 'Error sending to pubsub' in error_log

        assert 'sku:123456789' in error_log
        assert 'seller_id:xablau' in error_log
        assert 'scope:fake_scope' in error_log

        assert patolino_mock.call_count == 1

        patolino_payload = patolino_mock.call_args[0][0]
        assert patolino_payload['sku'] == mock_message['sku']
        assert patolino_payload['seller_id'] == mock_message['seller_id']
        assert patolino_payload['code'] == 'PRODUCT_EXPORTER_FAKE_SCOPE_ERROR'
        assert patolino_payload['message'] == (
            'Error processing on product export consumer '
            'with scope fake_scope error: Error sending to pubsub'
        )
        assert patolino_payload['payload'] == {
            'navigation_id': 'bar'
        }

    @settings_stub(ENABLE_FULFILLMENT=True)
    def test_when_calling_fulfillment_fake_scope_and_enabled_option_then_include_attribute_fulfillment( # noqa
        self,
        consumer,
        patch_pubsub_client,
        patch_patolino_product_post,
        mock_message_with_fulfillment
    ):
        with patch_pubsub_client as mock_pubsub:
            with patch_patolino_product_post as patolino_mock:
                consumer._get_scope = self.get_fulfillment_scope
                consumer.process_message(mock_message_with_fulfillment)

        assert mock_pubsub.call_args[1]['fulfillment']
        assert patolino_mock.call_args[0][0]['payload'] == {
            'navigation_id': 'bar',
            'fulfillment': True
        }

        payload = json.loads(mock_pubsub.call_args[1]['data'].decode('utf-8'))
        assert payload == {
            'foo': 'bar',
            'seller_id': 'xablau',
            'sku': '123456789',
            'navigation_id': 'bar',
            'fulfillment': True
        }

    @settings_stub(ENABLE_FULFILLMENT=False)
    def test_when_calling_fulfillment_fake_scope_and_disabled_option_then_not_include_attribute_fulfillment( # noqa
        self,
        consumer,
        patch_pubsub_client,
        patch_patolino_product_post,
        mock_message
    ):
        with patch_pubsub_client as mock_pubsub:
            with patch_patolino_product_post as patolino_mock:
                consumer._get_scope = self.get_test_scope
                consumer.process_message(mock_message)

        assert 'fulfillment' not in mock_pubsub.call_args[1]
        assert patolino_mock.call_args[0][0]['payload'] == {
            'navigation_id': 'bar'
        }

    def test_should_send_to_pubsub_with_attribute_category(
        self,
        consumer,
        patch_pubsub_client,
        patch_patolino_product_post,
        mock_message_with_category_field
    ):
        with patch_pubsub_client as mock_pubsub:
            with patch_patolino_product_post as patolino_mock:
                consumer._get_scope = self.get_category_scope
                consumer.process_message(mock_message_with_category_field)

        assert patolino_mock.call_count == 1
        assert mock_pubsub.call_args[1]['category'] == 'IN'
