from unittest.mock import patch

import pytest
from simple_settings import settings

from taz.consumers.core.google.storage import StorageManager
from taz.core.storage.cloud_storage_manager import CloudStorageManager


class TestCloudStorageManager:

    @pytest.fixture
    def file_name(self):
        return 'test_file.jpg'

    @pytest.fixture
    def mock_settings(self):
        with patch(
            'taz.core.storage.cloud_storage_manager.settings'
        ) as mock_settings:
            yield mock_settings

    @pytest.fixture
    def manager(self):
        return CloudStorageManager(bucket_config=settings.BUCKET_CONFIG)

    def test_write_bucket_data(self, manager, file_name):
        with patch.object(StorageManager, 'upload') as mock_gcp_upload:
            manager_instance = manager
            data = b'test data'

            manager_instance.write_bucket_data(data, file_name)

            mock_gcp_upload.assert_called_with(data=data, filename=file_name)

    def test_read_bucket_data(self, manager, file_name):
        with patch.object(StorageManager, 'get_file') as mock_gcp_get_file:
            manager_instance = manager
            manager_instance.read_bucket_data(file_name)

            mock_gcp_get_file.assert_called_with(filename=file_name)

    def test_invalid_storage_type(self, manager, file_name, mock_settings):
        mock_settings.BUCKET_CONFIG = {
            'read': [
                {
                    'storage': 'azure',
                    'bucket_name': 'image-test',
                    'active': True,
                }
            ]
        }

        invalid_cloud = mock_settings.BUCKET_CONFIG['read'][0]['storage']
        expected_msg = f'Unsupported storage type: {invalid_cloud}'

        manager_instance = manager
        with pytest.raises(ValueError) as error:
            manager_instance.read_bucket_data(file_name)

        assert str(error.value) == expected_msg
