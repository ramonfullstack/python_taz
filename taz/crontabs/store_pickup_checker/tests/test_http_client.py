from unittest.mock import MagicMock, patch

import pytest
import requests

from taz.crontabs.store_pickup_checker.http_client import (
    PickupStoresHttpClient
)
from taz.http_status import HTTP_401_UNAUTHORIZED


class TestPickupStoresHttpClient:

    @pytest.fixture
    def http_client(self):
        return PickupStoresHttpClient()

    @patch.object(requests, 'post')
    def test_get_oauth_token(
        self,
        mock_post,
        fake_jwt_token,
        http_client,
        mock_oauth_token,
    ):
        mock_post.return_value = mock_oauth_token
        response = http_client.get_oauth_token()

        assert mock_post.call_count == 1
        assert response == f'Bearer {fake_jwt_token}'

    @patch.object(requests, 'post')
    def test_get_pickup_store_should_refresh_token(
        self,
        mock_post,
        fake_jwt_token,
        http_client,
        patch_requests_get,
        mock_oauth_token,
        mock_valid_product_store_pickup,
    ):
        mock_post.return_value = mock_oauth_token
        with patch_requests_get as mock_get:
            mock_respose_401 = MagicMock()
            mock_respose_401.status_code = HTTP_401_UNAUTHORIZED

            mock_get.side_effect = [
                mock_respose_401,
                mock_valid_product_store_pickup
            ]
            response = http_client.get_pickup_stores(sku='12345678')

        assert mock_get.call_count == 2
        assert mock_post.call_count == 1
        assert mock_get.call_args[0][0] == (
            'https://stage.apiluiza.com.br/v1/pickupstores?'
            'products[0].quantity=1&products[0].sku=12345678'
        )
        assert mock_get.call_args[1]['headers'] == {
            'Authorization': f'Bearer {fake_jwt_token}'
        }
        assert response == {'has_pickustore': True}

    def test_get_pickup_store_should_return_ok(
        self,
        http_client,
        patch_requests_get,
        mock_valid_product_store_pickup,
    ):
        with patch_requests_get as mock_get:
            mock_get.return_value = mock_valid_product_store_pickup
            response = http_client.get_pickup_stores(sku='12345678')

        assert mock_get.call_count == 1
        assert mock_get.call_args[0][0] == (
            'https://stage.apiluiza.com.br/v1/pickupstores?'
            'products[0].quantity=1&products[0].sku=12345678'
        )
        assert response == {'has_pickustore': True}

    def test_get_pickup_store_should_return_empty_list_when_not_found(
        self,
        http_client,
        patch_requests_get,
        mock_not_found_store_pickup,
        caplog
    ):
        with patch_requests_get as mock_get:
            mock_get.return_value = mock_not_found_store_pickup
            response = http_client.get_pickup_stores(sku='123')

        assert mock_get.call_count == 1
        assert mock_get.call_args[0][0] == (
            'https://stage.apiluiza.com.br/v1/pickupstores?'
            'products[0].quantity=1&products[0].sku=123'
        )
        assert caplog.records[0].getMessage() == (
            'No pickup stores found for sku:123 '
            'url:https://stage.apiluiza.com.br'
            '/v1/pickupstores?products[0].quantity=1&products[0].sku=123'
        )
        assert response == {}

    def test_get_pickup_store_should_return_empty_list_when_error(
        self,
        http_client,
        patch_requests_get,
        mock_error_store_pickup,
        caplog
    ):
        with patch_requests_get as mock_get:
            mock_get.return_value = mock_error_store_pickup
            response = http_client.get_pickup_stores(sku='123')

        assert mock_get.call_count == 1
        assert mock_get.call_args[0][0] == (
            'https://stage.apiluiza.com.br/v1/pickupstores?'
            'products[0].quantity=1&products[0].sku=123'
        )
        assert caplog.records[0].getMessage() == (
            'Error requesting ApiLuiza pickup store for sku:123 '
            'error:Internal Server Error '
            'url:https://stage.apiluiza.com.br'
            '/v1/pickupstores?products[0].quantity=1&products[0].sku=123'
        )
        assert response == {}

    def test_get_pickup_store_should_return_empty_list_when_bad_request(
        self,
        http_client,
        patch_requests_get,
        mock_bad_request_store_pickup,
        caplog
    ):
        with patch_requests_get as mock_get:
            mock_get.return_value = mock_bad_request_store_pickup
            response = http_client.get_pickup_stores(sku='123')

        assert mock_get.call_count == 1
        assert mock_get.call_args[0][0] == (
            'https://stage.apiluiza.com.br/v1/pickupstores?'
            'products[0].quantity=1&products[0].sku=123'
        )
        assert caplog.records[0].getMessage() == (
            'No pickup stores found for sku:123 '
            'url:https://stage.apiluiza.com.br'
            '/v1/pickupstores?products[0].quantity=1&products[0].sku=123'
        )
        assert response == {}
