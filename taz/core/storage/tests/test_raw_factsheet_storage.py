from logging import StreamHandler
from typing import Dict
from unittest.mock import call, patch

import pytest

from taz.core.storage.raw_factsheet_storage import RawFactsheetStorage


class TestRawFactsheetStorage:

    @pytest.fixture
    def mock_raw_factsheet_storage(self):
        return RawFactsheetStorage()

    def test_when_get_factsheet_then_should_return_factsheet_payload_with_success(  # noqa
        self,
        mock_raw_factsheet_storage: RawFactsheetStorage,
        mock_factsheet_payload: Dict,
        patch_storage_manager_get_json: patch,
        mock_factsheet_seller_id: str,
        mock_factsheet_sku: str,
        mock_factsheet_filename: str
    ):
        with patch_storage_manager_get_json as mock_storage:
            mock_storage.return_value = mock_factsheet_payload
            payload = mock_raw_factsheet_storage.get_bucket_data(
                sku=mock_factsheet_sku,
                seller_id=mock_factsheet_seller_id
            )

            assert payload == mock_factsheet_payload
            mock_storage.assert_called_with(mock_factsheet_filename)

    def test_when_get_factsheet_then_should_return_factsheet_empty(
        self,
        mock_raw_factsheet_storage: RawFactsheetStorage,
        patch_storage_manager_get_json,
        mock_factsheet_seller_id: str,
        mock_factsheet_sku: str,
        mock_factsheet_filename: str
    ):
        with patch_storage_manager_get_json as mock_storage:
            mock_storage.return_value = {}

            payload = mock_raw_factsheet_storage.get_bucket_data(
                sku=mock_factsheet_sku,
                seller_id=mock_factsheet_seller_id
            )

            assert payload == {}
            mock_storage.assert_called_with(mock_factsheet_filename)

    def test_when_upload_factsheet_then_should_process_with_success(
        self,
        mock_raw_factsheet_storage: RawFactsheetStorage,
        mock_factsheet_payload,
        patch_storage_manager_upload,
        mock_factsheet_seller_id: str,
        mock_factsheet_sku: str,
        mock_factsheet_filename: str,
        logger_stream: StreamHandler
    ):
        with patch_storage_manager_upload as mock_storage:
            mock_raw_factsheet_storage.upload_bucket_data(
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
        mock_raw_factsheet_storage: RawFactsheetStorage,
        patch_storage_manager_delete,
        mock_factsheet_seller_id: str,
        mock_factsheet_sku: str,
        mock_factsheet_filename: str,
        logger_stream: StreamHandler
    ):
        with patch_storage_manager_delete as mock_storage:
            mock_raw_factsheet_storage.delete_bucket_data(
                sku=mock_factsheet_sku,
                seller_id=mock_factsheet_seller_id
            )

            assert 'Successfully deleted' in logger_stream.getvalue()
            mock_storage.assert_called_with(mock_factsheet_filename)

    def test_generate_filename_with_success(
        self,
        mock_raw_factsheet_storage: RawFactsheetStorage,
        mock_factsheet_seller_id: str,
        mock_factsheet_sku: str,
        mock_factsheet_filename: str
    ):
        factsheet_file_name = mock_raw_factsheet_storage.generate_filename(
            sku=mock_factsheet_sku,
            seller_id=mock_factsheet_seller_id
        )
        assert mock_factsheet_filename == factsheet_file_name
