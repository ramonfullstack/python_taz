import pytest

from taz.core.notification.notification_sender import NotificationSender


class TestNotificationSender:

    @pytest.fixture
    def notification_sender(self):
        return NotificationSender()

    @pytest.fixture
    def notification_dict(self):
        return {
            'sku': '030910800',
            'seller_id': 'magazineluiza',
            'code': 'SUCCESS',
            'message': 'Successfully published',
            'payload': {
                'navigation_id': '030910800',
                'title': 'Headphone Bluetooth JBL T500BT com Microfone',
                'reference': 'Preto',
                'price': '213.90'
            }
        }

    def test_should_send_notification_to_patolino(
        self,
        notification_sender,
        patch_publish_manager,
        notification_dict
    ):
        with patch_publish_manager as mock_pubsub:
            mock_pubsub.return_value = notification_dict

            notification_sender.send(**notification_dict)

        assert mock_pubsub.called

    def test_should_raise_error_on_send_notification_to_patolino(
        self,
        notification_sender,
        patch_publish_manager,
        notification_dict,
        logger_stream
    ):
        with pytest.raises(Exception):
            with patch_publish_manager as mock_pubsub:
                mock_pubsub.side_effect = Exception()
                notification_sender.send(**notification_dict)

        log = logger_stream.getvalue()

        assert mock_pubsub.called
        assert 'Error sending notification to Patolino' in log
