import random
import string
from unittest.mock import Mock, patch

import jwt
import pytest
import requests

from taz.helpers.test_utils import mock_response


@pytest.fixture
def apiluiza_response_not_found():
    return {
        'developerMessage': 'Products not found at catalog: 123',
        'userMessage': 'Product not found',
        'errorCode': 20061,
        'moreInfo': 'http://dev-magazineluiza.devportal.apigee.com/codigos-de-erro' # noqa
    }


@pytest.fixture
def patch_requests_get():
    return patch.object(requests, 'get')


@pytest.fixture
def fake_jwt_token():
    secret_key = ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=32,
        )
    )

    payload = {
        'app_name': 'NationalAppStaging',
        'aud': [
            'XPTO',
            'access'
        ],
        'iss': 'http://stage.apiluiza.com.br/oauth/jwt/client_credential',
        'exp': 0,
        'iat': 0,
        'client_id': 'xpto',
        'jti': '259b893b-0a5f-4bed-844a-fa5f9c0d0134'
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token.decode()


@pytest.fixture
def mock_oauth_token(fake_jwt_token):
    mock = Mock()
    mock.status_code = 200
    mock.json = Mock(
        return_value={'access_token': fake_jwt_token}
    )
    return mock


@pytest.fixture
def mock_not_found_store_pickup(apiluiza_response_not_found):
    mock = Mock()
    mock.status_code = 404
    mock.json = Mock(
        return_value=apiluiza_response_not_found
    )
    return mock


@pytest.fixture
def mock_bad_request_store_pickup(apiluiza_response_not_found):
    mock = Mock()
    mock.status_code = 400
    mock.json = Mock(
        return_value={
            'developerMessage': 'Product dimensions not compatible with Pick Up Store',  # noqa
            'userMessage': 'You are not allowed to pick up theses products in store due to the dimensions of one of them',  # noqa
            'errorCode': 20059,
            'moreInfo': 'http://dev-magazineluiza.devportal.apigee.com/codigos-de-erro'  # noqa
        }
    )
    return mock


@pytest.fixture
def mock_valid_product_store_pickup(apiluiza_response_content):
    mock = Mock()
    mock.status_code = 200
    mock.json = Mock(
        return_value=apiluiza_response_content
    )
    return mock


@pytest.fixture
def mock_error_store_pickup(apiluiza_response_not_found):
    mock = mock_response(
        status=500,
        raise_for_status=Exception('Internal Server Error')
    )
    return mock
