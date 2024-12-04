import pytest

from taz.api.middlewares.version import VersionMiddleware
from taz.api.version import __version__


class FakeResponse:
    def __init__(self):
        self.headers = {}

    def set_header(self, name, value):
        self.headers.update({name: value})

    def get_headers(self):
        return self.headers


class Fake:
    pass


class TestVersion:

    @pytest.fixture()
    def version(self):
        return VersionMiddleware()

    def test_middlware_return_api_version_in_reponse_headers(self, version):
        response = FakeResponse()

        version.process_response(Fake(), response, Fake(), Fake())
        assert response.headers['version'] == __version__
