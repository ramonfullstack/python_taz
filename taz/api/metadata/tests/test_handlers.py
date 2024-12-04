import pytest
from simple_settings import settings

from taz.constants import SOURCE_SMARTCONTENT


class TestMetadataInputHandler:

    @pytest.fixture
    def source(self):
        return SOURCE_SMARTCONTENT

    @pytest.fixture
    def message(self, source):
        return {'source': source, 'identified': '123456789'}

    @pytest.fixture
    def base64(self):
        return 'ewoJInNvdXJjZSI6ICJzbWFydGNvbnRlbnQiLAoJImlkZW50aWZpZWQiOiAiMTIzNDU2Nzg5Igp9'  # noqa

    @pytest.fixture
    def mock_url(self):
        return '/metadatainput/notification/'

    def test_post_notification_with_payload(
        self,
        client,
        message,
        mock_url,
        patch_publish_manager
    ):
        with patch_publish_manager as mock_pubsub:
            response = client.post(mock_url, json=message)

        assert response.json == message
        assert response.status_code == 200

        mock_pubsub.assert_called_with(
            topic_name=settings.PUBSUB_METADATA_INPUT_TOPIC_NAME,
            project_id=settings.GOOGLE_PROJECT_ID,
            content=message
        )

    def test_post_notification_with_base64(
        self,
        client,
        base64,
        message,
        mock_url,
        patch_publish_manager
    ):
        with patch_publish_manager as mock_pubsub:
            response = client.post(
                mock_url,
                json={'message': {'data': base64}}
            )

        assert response.json == message
        assert response.status_code == 200
        assert mock_pubsub.called

    def test_post_notification_without_payload(self, client, mock_url):
        response = client.post(mock_url)
        assert response.status_code == 400
