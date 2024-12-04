from unittest.mock import ANY, call

import pytest
from simple_settings import settings

from taz.consumers.core.notification import Notification
from taz.core.matching.common.samples import ProductSamples


class TestNotification:

    @pytest.fixture
    def notification(self):
        return Notification()

    @pytest.fixture
    def product(self):
        return ProductSamples.magazineluiza_sku_193389600()

    @pytest.fixture
    def payload(self, product):
        return {
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'navigation_id': product['navigation_id']
        }

    @pytest.fixture
    def mock_notification(self, product):
        return {
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'navigation_id': product['navigation_id'],
            'action': 'create',
            'type': 'product',
            'origin': 'product',
            'task_id': ANY,
            'timestamp': 0
        }

    @pytest.mark.parametrize('origin', [('test')])
    def test_put_notification_from_product(
        self,
        payload,
        notification,
        patch_publish_manager,
        mock_notification,
        origin
    ):
        mock_notification['origin'] = origin
        with patch_publish_manager as mock_publish:  # noqa
            notification.put(payload, 'product', 'create', origin=origin)

        mock_publish.call_args.assert_called_with(
            mock_notification, {
                'seller_id': {
                    'DataType': 'String',
                    'StringValue': 'magazineluiza'
                },
                'action': {
                    'DataType': 'String',
                    'StringValue': 'create'
                },
                'type': {
                    'DataType': 'String',
                    'StringValue': 'product'
                },
                'has_tracking': {
                    'DataType': 'String',
                    'StringValue': 'false'
                }
            }
        )
        assert mock_publish.called

    def test_put_notification_not_found_returns_not_notify(
        self,
        payload,
        patch_pubsub_client,
        notification,
        patch_publish_manager
    ):
        del payload['navigation_id']

        with patch_publish_manager, patch_pubsub_client as mock_pubsub:
            notification.put(payload, 'product', 'create')

        assert not mock_pubsub.called

    def test_when_put_notification_for_existing_product_then_call_pubsub_publisher(  # noqa
        self,
        patch_notification_raw_products,
        payload,
        notification,
        product,
        patch_publish_manager,
        mock_notification
    ):
        payload['action'] = 'fake'
        del payload['navigation_id']

        with patch_publish_manager as mock_stream_publisher_publish:
            with patch_notification_raw_products as mock_raw_products_collection:  # noqa
                mock_raw_products_collection.find_one.return_value = product  # noqa
                notification.put(payload, 'product', 'create')

        mock_stream_publisher_publish.assert_has_calls([
            call(
                attributes={
                    'seller_id': 'magazineluiza',
                    'action': 'create',
                    'type': 'product'
                },
                content=mock_notification,
                project_id=settings.PUBSUB_NOTIFY_PROJECT_ID,
                topic_name=settings.PUBSUB_PUBLISHER_NOTIFY_TOPIC
            )
        ])

    def test_when_put_notification_for_non_existing_product_then_call_publishers(  # noqa
        self,
        patch_notification_raw_products,
        payload,
        notification,
        patch_publish_manager
    ):
        with patch_publish_manager as mock_stream_publisher_publish:
            with patch_notification_raw_products as mock_raw_products_collection:  # noqa
                mock_raw_products_collection.find_one.return_value = None
                notification.put(payload, 'product', 'create', 'product', False)  # noqa

        assert mock_stream_publisher_publish.called
