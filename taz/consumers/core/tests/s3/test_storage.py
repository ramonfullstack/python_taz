import pytest
from simple_settings import settings

from taz.consumers.core.s3.storage import S3CloudManager


class TestS3CloudManager:

    @pytest.fixture
    def storage_manager(self):
        return S3CloudManager(settings.MEDIA_BUCKET)

    @pytest.fixture
    def filename(self):
        return 'hello.txt'

    @pytest.fixture
    def filename_failed(self):
        return '404.txt'

    def test_upload(
            self,
            filename,
            storage_manager=S3CloudManager):
        storage_manager.upload(self, filename)
        storage_manager.delete(self, filename)

    def test_upload_failed(
            self,
            filename_failed,
            storage_manager=S3CloudManager):
        assert storage_manager.upload(self, filename_failed) is False

    def test_delete(
            self,
            filename,
            storage_manager=S3CloudManager):
        storage_manager.delete(self, filename)

    def test_delete_failed(
            self,
            filename_failed,
            storage_manager=S3CloudManager):
        assert storage_manager.delete(self, filename_failed) is False

    def test_get_file(
            self,
            filename,
            storage_manager=S3CloudManager):
        storage_manager.get_file(self, filename)

    def test_get_file_failed(
            self,
            filename_failed,
            storage_manager=S3CloudManager):
        assert storage_manager.get_file(self, filename_failed) is False

    def test_get_object(
            self,
            filename,
            storage_manager=S3CloudManager):
        storage_manager.get_object(self, filename)

    def test_get_object_failed(
            self,
            filename_failed,
            storage_manager=S3CloudManager):
        assert storage_manager.get_object(self, filename_failed) is False
