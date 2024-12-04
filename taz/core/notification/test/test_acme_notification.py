from datetime import datetime
from unittest.mock import patch

import pytest

from taz.constants import (
    CREATE_ACTION,
    FAILURE_FACTSHEET_CODE,
    FAILURE_FACTSHEET_MESSAGE,
    SUCCESS_FACTSHEET_CODE,
    SUCCESS_FACTSHEET_MESSAGE
)
from taz.core.notification.acme_notification import AcmeNotificationSender
from taz.helpers.json import json_dumps


class TestAcmeNotificationSender:

    @pytest.fixture
    def notification_sender(self):
        return AcmeNotificationSender()

    @pytest.fixture
    def mock_timestamp(self):
        return 12345

    def test_when_process_factsheet_then_should_send_payload_with_success_and_notify_patolino( # noqa
        self,
        notification_sender,
        patch_pubsub_client,
        patch_patolino_product_post,
        mock_factsheet_seller_id,
        mock_factsheet_sku,
        mock_factsheet_payload,
        mock_timestamp,
        patch_factsheet_url,
        patch_datetime
    ):
        mock_factsheet_payload.update({
            'message_timestamp': mock_timestamp
        })

        factsheet_url = 'factsheet_fake_url'
        datetime_utcnow = datetime(2022, 1, 24, 0, 0, 0)

        with patch_patolino_product_post as patolino_mock:
            with patch_pubsub_client as mock_pubsub:
                with patch('time.time', return_value=mock_timestamp), patch_datetime as mock_datetime: # noqa
                    with patch_factsheet_url as mock_factsheet_url:
                        mock_datetime.utcnow.return_value = datetime_utcnow
                        mock_factsheet_url.return_value = factsheet_url

                        notification_sender.send_factsheet(
                            action=CREATE_ACTION,
                            seller_id=mock_factsheet_seller_id,
                            sku=mock_factsheet_sku,
                            payload=mock_factsheet_payload
                        )

                        mock_pubsub.assert_called_with(
                            data=json_dumps(mock_factsheet_payload).encode('utf-8'), # noqa
                            topic='projects/maga-homolog/topics/taz-factsheet-export-sandbox', # noqa
                            ordering_key='{}/{}'.format(
                                mock_factsheet_seller_id,
                                mock_factsheet_sku
                            ).lower()
                        )

                        assert patolino_mock.call_count == 1
                        assert patolino_mock.call_args_list[0][0][0] == {
                            'sku': mock_factsheet_sku,
                            'seller_id': mock_factsheet_seller_id,
                            'code': SUCCESS_FACTSHEET_CODE,
                            'message': SUCCESS_FACTSHEET_MESSAGE,
                            'payload': {
                                'url': factsheet_url,
                                'action': CREATE_ACTION
                            },
                            'action': 'update',
                            'last_updated_at': '2022-01-24T00:00:00'
                        }

    def test_when_send_factsheet_failed_then_should_notify_patolino(
        self,
        notification_sender,
        patch_pubsub_client,
        patch_patolino_product_post,
        mock_factsheet_seller_id,
        mock_factsheet_sku,
        mock_factsheet_payload,
        mock_timestamp,
        patch_factsheet_url
    ):
        mock_factsheet_payload.update({
            'message_timestamp': mock_timestamp
        })
        factsheet_url = 'fake_url'
        with patch_patolino_product_post as patolino_mock:
            with patch_pubsub_client as mock_pubsub:
                with patch('time.time', return_value=mock_timestamp):
                    with patch_factsheet_url as mock_factsheet_url:
                        with pytest.raises(Exception):
                            mock_factsheet_url.return_value = factsheet_url

                            notification_sender.send_factsheet(
                                action=CREATE_ACTION,
                                seller_id=mock_factsheet_seller_id,
                                sku=mock_factsheet_sku,
                                payload=mock_factsheet_payload
                            )

                            mock_pubsub.assert_called_with(
                                data=json_dumps(mock_factsheet_payload).encode('utf-8'),  # noqa
                                topic='projects/maga-homolog/topics/taz-factsheet-export-sandbox',  # noqa
                                ordering_key='{}/{}'.format(
                                    mock_factsheet_seller_id,
                                    mock_factsheet_sku
                                ).lower()
                            )

                            assert patolino_mock.call_count == 1
                            patolino_mock.assert_called_with({
                                'sku': mock_factsheet_sku,
                                'seller_id': mock_factsheet_seller_id,
                                'code': FAILURE_FACTSHEET_CODE,
                                'message': FAILURE_FACTSHEET_MESSAGE,
                                'payload': {
                                    'url': factsheet_url,
                                    'action': CREATE_ACTION
                                }
                            })
