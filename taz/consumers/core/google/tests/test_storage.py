from unittest.mock import Mock, patch

import pytest
from simple_settings.utils import settings_stub

from taz.consumers.core.google.storage import StorageManager


class TestStorage:

    BUCKET_NAME = 'bucket_name'
    DATA = 'data'
    FILENAME = 'filename'

    @pytest.fixture
    def mock_storage_client(self):
        return patch(
            'taz.consumers.core.google.storage.StorageManager.get_gcp_client',
            autospec=True
        )

    @settings_stub(ENABLED_RETRY_STORAGE=True)
    def test_when_retry_is_active_on_upload_method_then_should_use_data_from_get_blob( # noqa
        self,
        mock_storage_client
    ):
        with mock_storage_client as mock_client:
            mock_bucket = Mock()
            mock_client().get_bucket.return_value = mock_bucket
            StorageManager(self.BUCKET_NAME).upload(self.DATA, self.FILENAME)

            assert mock_bucket.get_blob.call_count == 1
            assert mock_bucket.blob.call_count == 0
            assert mock_bucket.get_blob.return_value.upload_from_string.call_count == 1  # noqa

    @settings_stub(ENABLED_RETRY_STORAGE=False)
    def test_when_retry_not_active_then_should_use_data_from_blob(
        self,
        mock_storage_client
    ):
        with mock_storage_client as mock_client:
            mock_bucket = Mock()
            mock_client().get_bucket.return_value = mock_bucket
            mock_bucket.get_blob.return_value = None

            StorageManager(
                self.BUCKET_NAME
            ).upload(self.DATA, self.FILENAME)

            assert mock_bucket.get_blob.call_count == 0
            assert mock_bucket.blob.call_count == 1
            assert mock_bucket.blob.return_value.upload_from_string.call_count == 1 # noqa

    @settings_stub(ENABLED_RETRY_STORAGE=True)
    def test_when_retry_is_active_but_get_blob_is_empty_then_should_use_data_from_blob(  # noqa
        self,
        mock_storage_client
    ):
        with mock_storage_client as mock_client:
            mock_bucket = Mock()
            mock_client().get_bucket.return_value = mock_bucket
            mock_bucket.get_blob.return_value = None

            StorageManager(
                self.BUCKET_NAME
            ).upload(self.DATA, self.FILENAME)

            assert mock_bucket.get_blob.call_count == 1
            assert mock_bucket.blob.call_count == 1
            assert mock_bucket.blob.return_value.upload_from_string.call_count == 1  # noqa