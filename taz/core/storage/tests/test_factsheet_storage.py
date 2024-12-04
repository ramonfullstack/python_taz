from unittest.mock import call

import pytest
from simple_settings import settings

from taz.core.storage.factsheet_storage import FactsheetStorage


class TestFactsheetStorage:

    @pytest.fixture
    def mock_factsheet_storage(self):
        return FactsheetStorage()

    def test_when_get_factsheet_then_should_return_factsheet_payload_with_success( # noqa
        self,
        mock_factsheet_storage,
        mock_factsheet_payload,
        patch_storage_manager_get_json,
        mock_factsheet_seller_id,
        mock_factsheet_sku,
        mock_factsheet_filename
    ):
        with patch_storage_manager_get_json as mock_storage:
            mock_storage.return_value = mock_factsheet_payload
            payload = mock_factsheet_storage.get_bucket_data(
                sku=mock_factsheet_sku,
                seller_id=mock_factsheet_seller_id
            )

            assert payload == mock_factsheet_payload
            mock_storage.assert_called_with(mock_factsheet_filename)

    def test_when_get_factsheet_then_should_return_factsheet_empty(
        self,
        mock_factsheet_storage,
        patch_storage_manager_get_json,
        mock_factsheet_seller_id,
        mock_factsheet_sku,
        mock_factsheet_filename
    ):
        with patch_storage_manager_get_json as mock_storage:
            mock_storage.return_value = {}

            payload = mock_factsheet_storage.get_bucket_data(
                sku=mock_factsheet_sku,
                seller_id=mock_factsheet_seller_id
            )

            assert payload == {}
            mock_storage.assert_called_with(mock_factsheet_filename)

    def test_when_upload_factsheet_then_should_process_with_success(
        self,
        mock_factsheet_storage,
        mock_factsheet_payload,
        patch_storage_manager_upload,
        mock_factsheet_seller_id,
        mock_factsheet_sku,
        mock_factsheet_filename,
        logger_stream
    ):
        with patch_storage_manager_upload as mock_storage:
            mock_factsheet_storage.upload_bucket_data(
                sku=mock_factsheet_sku,
                seller_id=mock_factsheet_seller_id,
                payload=mock_factsheet_payload
            )

            assert 'Successfully upload' in logger_stream.getvalue()
            assert mock_storage.call_args == call(
                mock_factsheet_payload,
                mock_factsheet_filename,
                'application/json; charset=utf-8'
            )

    def test_when_delete_factsheet_then_should_process_with_success(
        self,
        mock_factsheet_storage,
        patch_storage_manager_delete,
        mock_factsheet_seller_id,
        mock_factsheet_sku,
        mock_factsheet_filename,
        logger_stream
    ):
        with patch_storage_manager_delete as mock_storage:
            mock_factsheet_storage.delete_bucket_data(
                sku=mock_factsheet_sku,
                seller_id=mock_factsheet_seller_id
            )

            assert 'Successfully deleted' in logger_stream.getvalue()
            mock_storage.assert_called_with(mock_factsheet_filename)

    def test_generate_filename_with_success(
        self,
        mock_factsheet_storage,
        mock_factsheet_seller_id,
        mock_factsheet_sku,
        mock_factsheet_filename
    ):
        factsheet_file_name = mock_factsheet_storage.generate_filename(
            sku=mock_factsheet_sku,
            seller_id=mock_factsheet_seller_id
        )
        assert mock_factsheet_filename == factsheet_file_name

    def test_get_factsheet_url_with_success(
        self,
        mock_factsheet_storage,
        mock_factsheet_seller_id,
        mock_factsheet_sku,
        mock_factsheet_filename
    ):
        url = mock_factsheet_storage.generate_external_url(
            sku=mock_factsheet_sku,
            seller_id=mock_factsheet_seller_id
        )

        assert url == f'{settings.FACTSHEET_DOMAIN}/{mock_factsheet_filename}'
