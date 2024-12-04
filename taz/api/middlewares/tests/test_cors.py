import pytest

from taz.api.middlewares.cors import CORSMiddleware


class FakeRequest:
    def __init__(self, headers=None, relative_uri='/foo', query_string=''):
        self.method = 'OPTIONS'
        self.token_owner = 'Unknown'
        self.headers = headers or {}
        self.relative_uri = relative_uri
        self.query_string = query_string
        self.status = '200 OK'

    def get_header(self, key, default=None):
        return self.headers.get(key) or default


class FakeResponse:
    def __init__(self):
        self.headers = {}

    def set_header(self, name, value):
        self.headers.update({name: value})

    def get_headers(self):
        return self.headers

    def get_header(self, header):
        return self.headers.get(header)

    def delete_header(self, header):
        self.headers.pop(header, None)


class Fake:
    pass


class TestCORS:

    @pytest.fixture
    def cors(self):
        return CORSMiddleware()

    def test_middlware_return_reponse_headers(self, cors):
        request = FakeRequest(headers={
            'Origin': 'example.com.br',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': '*'
        })
        response = FakeResponse()

        cors.process_response(request, response, Fake(), Fake())
        assert response.headers == {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Max-Age': '86400'
        }

    @pytest.mark.parametrize('allow_origin,origin', [
        ('fake.com.br', 'exemple.com.br'),
        ('test', 'exemple.com.br')
    ])
    def test_middlware_invalid_origin_return_none(
        self,
        allow_origin,
        origin
    ):
        request = FakeRequest(headers={
            'Origin': origin,
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': '*'
        })
        response = FakeResponse()

        cors = CORSMiddleware(allow_origins=allow_origin)
        cors.process_response(request, response, Fake(), Fake())
        assert response.headers == {}
