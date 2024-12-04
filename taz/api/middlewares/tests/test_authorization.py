from unittest.mock import patch

import pytest

from taz.api.common.exceptions import Unauthorized
from taz.api.middlewares.authorization import AuthorizationMiddleware


class FakeRequest:
    def __init__(
        self,
        headers=None,
        path='/foo',
        query_string='',
        method='GET'
    ):
        self.headers = headers or {}
        self.path = path
        self.query_string = query_string
        self.method = method

    def get_header(self, key):
        return self.headers.get(key)


class FakeResponse:
    pass


class TestAuthorizationMiddleware:

    @pytest.fixture
    def authorization(self):
        return AuthorizationMiddleware()

    @pytest.fixture
    def patch_validate_jwt_gcp(self):
        return patch.object(AuthorizationMiddleware, '_validate_jwt')

    def test_middlware_return_http_status_401(self, authorization):
        with pytest.raises(Unauthorized) as error:
            authorization.process_request(FakeRequest(), FakeResponse())

        assert error.value.code == 401

    def test_middleware_return_success_for_token_in_headers(
        self, token, authorization
    ):
        authorization_header = {
            'Authorization': 'Token {}'.format(token.token)
        }

        response = authorization.process_request(
            FakeRequest(authorization_header), FakeResponse
        )

        assert response is None

    def test_middleware_return_http_status_401_for_invalid_token(
        self, authorization
    ):
        authorization_header = {
            'Authorization': 'invalid token'
        }

        with pytest.raises(Unauthorized) as error:
            authorization.process_request(
                FakeRequest(authorization_header), FakeResponse
            )

        assert error.value.code == 401

    def test_middleware_ignore_validation_in_some_endpoints(
        self, authorization
    ):
        response = authorization.process_request(
            FakeRequest(path='/monitor'), FakeResponse
        )

        assert response is None

    def test_middlware_return_success_for_gcp_token_jwt_in_headers(
        self, authorization, patch_validate_jwt_gcp
    ):
        authorization_header = {
            'Authorization': 'fake-token-with-more-of-30-chars'
        }

        with patch_validate_jwt_gcp as mock_validate_jwt:
            response = authorization.process_request(
                FakeRequest(authorization_header), FakeResponse
            )

        assert response is None
        assert mock_validate_jwt.called
