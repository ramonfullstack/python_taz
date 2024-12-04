import json

import pytest


class TestNotificationHandler:

    @pytest.fixture
    def source(self):
        return 'omnilogic'

    def test_post_notification_with_payload(
        self,
        client,
        omnilogic_message,
        source,
        patch_publish_manager,
        logger_stream
    ):

        with patch_publish_manager as mock_pubsub:
            response = client.post(
                f'/notification/{source}',
                body=json.dumps(omnilogic_message)
            )

            omnilogic_message.update({'source': source})

            mock_pubsub.assert_called_once()
            call_args = mock_pubsub.call_args_list[0][1]['content']
            assert call_args == omnilogic_message
            assert response.status_code == 200
            assert (
                'Send request to notification with' in logger_stream.getvalue()
            )

    def test_post_notification_without_payload(
        self,
        client,
        source,
        patch_publish_manager
    ):
        with patch_publish_manager as mock_pubsub:
            response = client.post(f'/notification/{source}')
            assert not mock_pubsub.called
            assert response.status_code == 400

    def test_post_notification_datasheet_with_a_invalid_identifier(
        self,
        client,
    ):
        response = client.post(
            '/notification/datasheet',
            body=json.dumps({
                'seller_id': 'test',
                'sku': 'test',
                'identifier': '094820983E+23'
            })
        )
        assert response.status_code == 400
        assert json.loads(response.json['error_message'])['_schema'][0] == 'Invalid identifier' # noqa

    def test_post_notification_schema_accepts_unknown_fields(
        self,
        client
    ):
        response = client.post(
            '/notification/magalu',
            body=json.dumps({
                'seller_id': 'test',
                'sku': 'test',
                'test': 'test'
            })
        )
        assert response.status_code == 200

    def test_datasheet_when_identifier_does_not_exist_on_gpc_bucket(
        self,
        client
    ):
        response = client.post(
            '/notification/datasheet',
            body=json.dumps({
                'seller_id': 'test',
                'sku': 'test',
                'identifier': '09482098323'
            })
        )
        assert response.status_code == 404
        assert response.json['error_message'] == 'Datasheet not found'
