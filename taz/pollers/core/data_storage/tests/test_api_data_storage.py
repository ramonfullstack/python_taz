import pytest
from simple_settings.utils import settings_stub

from taz.pollers.core.data_storage.api import ApiDataStorage
from taz.pollers.core.exceptions import UrlNotProvided


class FakeApiDataStorage(ApiDataStorage):

    def batch_key(self):
        return 'batch_key'


class TestApiDataStorage:

    @pytest.fixture
    def data_storage(self):
        return ApiDataStorage(url='http://www.apiurl.com/')

    @pytest.fixture
    def data_storage_with_scope(self):
        ApiDataStorage.scope = 'fake'
        return ApiDataStorage()

    def test_data_storage_should_use_url_passed_in_constructor(
        self,
        data_storage
    ):
        assert data_storage.url == 'http://www.apiurl.com/'

    @settings_stub(
        POLLERS={
            'fake': {
                'api': {
                    'url': 'http://www.settings-url.com/'
                }
            }
        }
    )
    def test_data_storage_should_use_url_from_settings(self):
        expected_url = 'http://www.settings-url.com/'
        ApiDataStorage.scope = 'fake'
        data_storage = ApiDataStorage()

        assert data_storage.url == expected_url

    def test_should_raise_when_url_is_not_provided(self, data_storage):
        data_storage.url = None

        with pytest.raises(UrlNotProvided):
            data_storage.fetch()

    def test_fake_implementation_should_return_batch_key(self):
        fake_data_storage = FakeApiDataStorage()
        assert fake_data_storage.batch_key() == 'batch_key'

    def test_scope_should_be_the_same_for_api_and_data_storage(self):
        ApiDataStorage.scope = 'test_scope'
        data_storage = ApiDataStorage('http://www.apiurl.com/')
        assert data_storage.scope == data_storage.api.scope

    def test_when_batch_key_is_not_implemented_should_raise(
        self,
        data_storage
    ):
        with pytest.raises(NotImplementedError):
            data_storage.batch_key()
