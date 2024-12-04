from unittest.mock import Mock, call, patch

import pytest
from _pytest.logging import LogCaptureFixture

from taz.consumers.core.maas_product import MaasProductHTTPClient


class TestMaasProductHttpClient:
    @pytest.fixture
    def client(self):
        return MaasProductHTTPClient()

    @pytest.fixture
    def patch_get_token(self):
        return patch.object(MaasProductHTTPClient, 'get_token')

    @pytest.fixture
    def patch_update_token(self):
        return patch.object(MaasProductHTTPClient, 'update_token')

    @pytest.fixture
    def patch_send_factsheet(self):
        return patch.object(MaasProductHTTPClient, '_send_factsheet_to_clean')

    @pytest.fixture
    def patch_get_product(self):
        return patch.object(MaasProductHTTPClient, '_get_product_data')

    @pytest.fixture
    def mock_payload_product(self):
        return {
            'sku': '123456789',
            'seller_id': 'luizalabs',
            'datasheet': [
                {
                    'value': 'Samsung Galaxy Tab A8 Wi-Fi, 64 GB',
                }
            ]
        }

    def test_when_reprocess_and_product_has_factsheet_then_should_return_success( # noqa
        self,
        client: MaasProductHTTPClient,
        patch_requests_post: patch,
        patch_requests_get: patch,
        patch_send_factsheet: patch,
        mock_maas_product_reprocess_payload: dict,
        patch_get_token: patch,
        mock_payload_product: dict
    ):
        with patch_requests_post as mock_requests_post:
            with patch_requests_get as mock_requests_get:
                with patch_get_token as mock_get_token:
                    mock_get_token.return_value = 'fake'

                    mock_post = Mock()
                    mock_post.status_code = 200
                    mock_requests_post.return_value = mock_post

                    mock_get = Mock()
                    mock_get.status_code = 200
                    mock_get.json.return_value = mock_payload_product
                    mock_requests_get.return_value = mock_get
                    with patch_send_factsheet as mock_send_factsheet:
                        success = client.reprocess(
                            mock_maas_product_reprocess_payload
                        )
        headers = {
            'Content-Type': 'application/json',
            'X-Tenant-Id': 'fake',
            'Authorization': 'fake'
        }

        assert mock_requests_post.call_args == call(
            url='https://api-product-staging-origin.luizalabs.com/api/v1/admin/products/reprocess',  # noqa
            headers=headers,
            json={
                'product_skus': ['fake'],
                'operation': 'ALL_PUBLISHING_STEPS'
            },
            timeout=5
        )

        assert mock_requests_get.call_args == call(
            url='https://api-product-staging-origin.luizalabs.com/api/v1/products/fake', # noqa
            headers=headers,
            timeout=5
        )

        assert mock_send_factsheet.call_count == 0
        assert success

    def test_when_reprocess_and_product_no_has_factsheet_then_should_send_empty_factsheet_to_kinesis_with_success( # noqa
        self,
        client: MaasProductHTTPClient,
        patch_requests_post: patch,
        patch_requests_get: patch,
        patch_publish_manager: patch,
        mock_maas_product_reprocess_payload: dict,
        patch_get_token: patch,
        mock_payload_product: dict
    ):
        with patch_requests_post as mock_requests_post:
            with patch_requests_get as mock_requests_get:
                with patch_get_token as mock_get_token:
                    mock_get_token.return_value = 'fake'

                    mock_post = Mock()
                    mock_post.status_code = 200
                    mock_requests_post.return_value = mock_post

                    mock_payload_product['datasheet'] = []
                    mock_get = Mock()
                    mock_get.status_code = 200
                    mock_get.json.return_value = mock_payload_product
                    mock_requests_get.return_value = mock_get
                    with patch_publish_manager as mock_pubsub:
                        success = client.reprocess(
                            mock_maas_product_reprocess_payload
                        )
        headers = {
            'Content-Type': 'application/json',
            'X-Tenant-Id': 'fake',
            'Authorization': 'fake'
        }

        assert mock_requests_post.call_args == call(
            url='https://api-product-staging-origin.luizalabs.com/api/v1/admin/products/reprocess',  # noqa
            headers=headers,
            json={
                'product_skus': ['fake'],
                'operation': 'ALL_PUBLISHING_STEPS'
            },
            timeout=5
        )

        assert mock_requests_get.call_args == call(
            url='https://api-product-staging-origin.luizalabs.com/api/v1/products/fake', # noqa
            headers=headers,
            timeout=5
        )

        assert mock_pubsub.call_args_list[0][1] == {
            'content': {
                'action': 'update',
                'data': {
                    'sku': 'fake', 'seller_id': 'fake', 'items': []
                }
            },
            'topic_name': 'taz-factsheet',
            'project_id': 'maga-homolog'
        }
        assert success

    def test_when_get_product_return_none_then_should_save_log(
        self,
        client: MaasProductHTTPClient,
        patch_requests_post: patch,
        patch_requests_get: patch,
        patch_send_factsheet: patch,
        mock_maas_product_reprocess_payload: dict,
        patch_get_token: patch,
        mock_payload_product: dict,
        caplog: LogCaptureFixture
    ):
        with patch_requests_post as mock_requests_post:
            with patch_requests_get as mock_requests_get:
                with patch_get_token as mock_get_token:
                    mock_get_token.return_value = 'fake'

                    mock_post = Mock()
                    mock_post.status_code = 200
                    mock_requests_post.return_value = mock_post

                    mock_get = Mock()
                    mock_get.status_code = 401
                    mock_requests_get.return_value = mock_get
                    with patch_send_factsheet as mock_send_factsheet:
                        success = client.reprocess(
                            mock_maas_product_reprocess_payload
                        )

        assert (
            'Error to receive product sku:fake '
            'seller_id:fake from maas-product'
            in caplog.text
        )
        assert mock_send_factsheet.call_count == 0
        assert success

    def test_when_reprocess_then_return_failed(
        self,
        client: MaasProductHTTPClient,
        patch_requests_post: patch,
        patch_get_product: patch,
        mock_maas_product_reprocess_payload: dict,
        patch_get_token: patch,
        mock_payload_product: dict
    ):
        with patch_requests_post as mock_requests_post:
            with patch_get_token as mock_get_token:
                with patch_get_product as mock_get_product:
                    mock_get_token.return_value = 'fake'
                    mock_http_response = Mock()
                    mock_http_response.status_code = 403
                    mock_requests_post.side_effect = [mock_http_response]

                    mock_get_product.return_value = mock_payload_product
                    success = client.reprocess(
                        mock_maas_product_reprocess_payload
                    )

        assert mock_requests_post.called
        assert not success

    def test_when_refresh_token_then_return_success(
        self,
        client: MaasProductHTTPClient,
        patch_requests_post: patch,
        patch_update_token: patch
    ):
        with patch_requests_post as mock_requests_post:
            with patch_update_token as mock_update_token:
                mock_http_response = Mock()
                mock_http_response.status_code = 200
                mock_http_response.json = Mock(
                    return_value={'access_token': 'fake'}
                )
                mock_requests_post.return_value = mock_http_response
                success = client.refresh_token()

        assert success
        assert mock_update_token.called_with('Bearer fake')

    def test_when_refresh_token_with_error_in_generate_token_then_return_failed(  # noqa
        self,
        client: MaasProductHTTPClient,
        patch_requests_post: patch,
        patch_update_token: patch
    ):
        with patch_requests_post as mock_requests_post:
            with patch_update_token as mock_update_token:
                mock_http_response = Mock()
                mock_http_response.status_code = 401
                mock_requests_post.return_value = mock_http_response
                success = client.refresh_token()

        assert not success
        assert not mock_update_token.called

    def test_when_refresh_token_with_error_in_set_in_cache_then_return_failed(  # noqa
        self,
        client: MaasProductHTTPClient,
        patch_requests_post: patch,
        patch_update_token: patch
    ):
        with patch_requests_post as mock_requests_post:
            with patch_update_token as mock_update_token:
                mock_http_response = Mock()
                mock_http_response.status_code = 200
                mock_http_response.json = Mock(
                    return_value={'access_token': 'fake'}
                )
                mock_requests_post.return_value = mock_http_response
                mock_update_token.return_value = False
                success = client.refresh_token()

        assert not success
