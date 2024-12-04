from unittest.mock import patch

import pytest

from taz.constants import SOURCE_DATASHEET
from taz.consumers.core.exceptions import NotFound
from taz.consumers.metadata_verify.scopes.datasheet.scope import Scope


class TestMetadataVerifyDatasheetScope:

    @pytest.fixture
    def scope(self):
        return Scope()

    @pytest.fixture
    def patch_get_metadata(self):
        return patch.object(Scope, 'get_metadata')

    @pytest.fixture
    def mock_datasheet_enriched_payload(self, product):
        return {
            'seller_id': product['seller_id'],
            'sku': product['sku'],
            'navigation_id': product['navigation_id'],
            'source': 'datasheet',
            'identifier': 'other'
        }

    def test_when_product_with_isbn_then_allowed(
        self,
        scope,
        product,
        mock_datasheet_enriched_payload,
        mongo_database
    ):
        mongo_database.enriched_products.insert_one(
            mock_datasheet_enriched_payload
        )
        is_allowed, identifier = scope.is_allowed(product)
        assert is_allowed
        assert identifier == 'other'

    def test_when_product_not_linked_to_datasheet_then_not_allowed(
        self,
        scope,
        product
    ):
        is_allowed, identifier = scope.is_allowed(product)
        assert not is_allowed
        assert identifier is None

    def test_when_process_datasheet_scope_then_create_payload_with_success(
        self,
        scope,
        product,
        isbn,
        patch_get_metadata,
        product_smartcontent,
        mock_expected_smartcontent_scope_payload,
        mock_datasheet_enriched_payload,
        mongo_database
    ):
        mongo_database.enriched_products.insert_one(
            mock_datasheet_enriched_payload
        )
        product.update({'isbn': isbn})
        mock_expected_smartcontent_scope_payload.update({'media': None})
        mock_expected_smartcontent_scope_payload['enriched_product'].update({
            'source': SOURCE_DATASHEET
        })

        with patch_get_metadata as mock_get_metadata:
            mock_get_metadata.return_value = product_smartcontent
            response = scope.process(isbn, product)

        assert response == mock_expected_smartcontent_scope_payload
        assert mongo_database.enriched_products.count_documents({
            'seller_id': product['seller_id'],
            'sku': product['sku'],
            'source': SOURCE_DATASHEET
        }) == 1

    def test_when_datasheet_metadata_not_found_then_return_none(
        self,
        scope,
        isbn,
        patch_data_storage,
        patch_storage_manager_get_json,
        product
    ):
        product.update({'isbn': isbn})
        with patch_data_storage as mock_data_storage:
            with patch_storage_manager_get_json as mock_storage_get_json:
                mock_data_storage.get_json = mock_storage_get_json
                mock_storage_get_json.side_effect = NotFound
                response = scope.process(isbn, product)

        assert response is None
        assert mock_storage_get_json.called

    def test_when_product_not_linked_with_datasheet_then_raise_exception(
        self,
        scope,
        mock_datasheet_enriched_payload,
        isbn,
        product
    ):
        with pytest.raises(NotFound):
            scope._enriched_product_process(
                product['sku'],
                product['seller_id'],
                product['navigation_id'],
                {}
            )
