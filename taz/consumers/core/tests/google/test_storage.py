import io
import json

import pytest
from simple_settings import settings

from taz.consumers.core.exceptions import NotFound
from taz.consumers.core.google.storage import StorageManager


class TestStorageManager:

    @pytest.fixture
    def storage_manager(self):
        return StorageManager(settings.MEDIA_BUCKET)

    @pytest.fixture
    def filename(self):
        return 'hello.json'

    @pytest.fixture
    def file_content(self):
        return 'string_test'

    @pytest.fixture
    def content_type(self):
        return 'application/json'

    @pytest.fixture
    def text_file(self):
        return 'get_file.txt'

    def test_storage_upload_file(
        self,
        storage_manager,
        filename,
        file_content
    ):
        storage_manager.upload(file_content, filename)
        storage_manager.delete(filename)

    def test_storage_upload_bytes(
        self,
        storage_manager,
        filename,
        file_content
    ):
        with io.BytesIO() as f:
            f.write(b' '.join(100 * (b'plaintext', )))
            storage_manager.upload(f, filename)
        storage_manager.delete(filename)

    def test_storage_upload_file_with_content_type(
        self,
        storage_manager,
        filename,
        file_content,
        content_type
    ):
        storage_manager.upload(file_content, filename, content_type)
        storage_manager.delete(filename)

    def test_storage_get_file(
        self,
        text_file,
        storage_manager,
        filename,
        file_content,
        content_type
    ):
        storage_manager.delete(text_file)
        storage_manager.upload(
            file_content,
            text_file,
            content_type
        )

        payload = storage_manager.get_file(text_file)

        assert payload == file_content

    def test_storage_get_json_of_file(
        self,
        storage_manager,
        filename,
        content_type,
        patch_storage_manager_get_file
    ):

        file_content = '{"murcho": "murchao"}'

        storage_manager.upload(
            file_content,
            'get_json_of_file.json',
            content_type
        )
        payload = storage_manager.get_json('get_json_of_file.json')

        assert payload == json.loads(file_content)

        storage_manager.delete(filename)

    def test_storage_delete_file(self, storage_manager, filename):
        storage_manager.delete(filename)

    def test_storage_get_json_of_file_returns_not_found(
        self,
        storage_manager,
        filename,
        patch_storage_manager_get_file
    ):
        with pytest.raises(NotFound) as e:
            storage_manager.get_json('filename.json')
        storage_manager.delete(filename)

        assert e.value.args[0] == 'Storage file:filename.json not found'
