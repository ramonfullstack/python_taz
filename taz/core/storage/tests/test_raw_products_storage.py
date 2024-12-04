from unittest.mock import call

import pytest

from taz.core.storage.raw_products_storage import RawProductsStorage


class TestRawProductsStorage:

    @pytest.fixture
    def mock_raw_products_storage(self):
        return RawProductsStorage()

    @pytest.fixture
    def mock_sku_raw_products(self, mock_raw_products_payload):
        return mock_raw_products_payload['sku']

    @pytest.fixture
    def mock_seller_id_raw_products(self, mock_raw_products_payload):
        return mock_raw_products_payload['seller_id']

    def test_when_get_raw_products_then_should_return_payload_with_success(
        self,
        mock_raw_products_storage,
        mock_raw_products_payload,
        patch_storage_manager_get_json,
        mock_raw_products_filename,
        mock_sku_raw_products,
        mock_seller_id_raw_products
    ):
        with patch_storage_manager_get_json as mock_storage:
            mock_storage.return_value = mock_raw_products_payload
            payload = mock_raw_products_storage.get_bucket_data(
                sku=mock_sku_raw_products,
                seller_id=mock_seller_id_raw_products
            )

            assert payload == mock_raw_products_payload
            mock_storage.assert_called_with(mock_raw_products_filename)

    def test_when_get_raw_products_then_should_return_empty_payload(
        self,
        mock_raw_products_storage,
        mock_raw_products_payload,
        patch_storage_manager_get_json,
        mock_raw_products_filename,
        mock_sku_raw_products,
        mock_seller_id_raw_products
    ):
        with patch_storage_manager_get_json as mock_storage:
            mock_storage.return_value = {}

            payload = mock_raw_products_storage.get_bucket_data(
                sku=mock_sku_raw_products,
                seller_id=mock_seller_id_raw_products
            )

            assert payload == {}
            mock_storage.assert_called_with(mock_raw_products_filename)

    def test_when_upload_raw_products_then_should_process_with_success(
        self,
        mock_raw_products_storage,
        mock_raw_products_payload,
        patch_storage_manager_upload,
        mock_raw_products_filename,
        logger_stream,
        mock_seller_id_raw_products,
        mock_sku_raw_products
    ):
        with patch_storage_manager_upload as mock_storage:
            mock_raw_products_storage.upload_bucket_data(
                sku=mock_sku_raw_products,
                seller_id=mock_seller_id_raw_products,
                payload=mock_raw_products_payload
            )

            assert 'Successfully upload' in logger_stream.getvalue()
            assert mock_storage.call_args == call(
                mock_raw_products_payload,
                mock_raw_products_filename,
                'application/json; charset=utf-8'
            )

    def test_when_delete_raw_products_then_should_process_with_success(
        self,
        mock_raw_products_storage,
        mock_raw_products_payload,
        patch_storage_manager_delete,
        mock_raw_products_filename,
        mock_seller_id_raw_products,
        mock_sku_raw_products,
        logger_stream
    ):
        with patch_storage_manager_delete as mock_storage:
            mock_raw_products_storage.delete_bucket_data(
                sku=mock_sku_raw_products,
                seller_id=mock_seller_id_raw_products
            )

            assert 'Successfully deleted' in logger_stream.getvalue()
            mock_storage.assert_called_with(mock_raw_products_filename)

    def test_generate_filename_with_success(
        self,
        mock_raw_products_storage,
        mock_raw_products_filename,
        mock_seller_id_raw_products,
        mock_sku_raw_products
    ):
        filename = mock_raw_products_storage.generate_filename(
            sku=mock_sku_raw_products,
            seller_id=mock_seller_id_raw_products
        )
        assert mock_raw_products_filename == filename
