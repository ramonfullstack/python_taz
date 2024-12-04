from unittest.mock import patch

import pytest
from simple_settings.utils import settings_stub

from taz.constants import SOURCE_SMARTCONTENT
from taz.consumers.core.exceptions import NotFound
from taz.consumers.metadata_verify.scopes.smartcontent.scope import Scope
from taz.utils import get_identifier


class TestMetadataVerifySmartContentScope:

    @pytest.fixture
    def scope(self):
        return Scope()

    @pytest.fixture
    def patch_get_metadata(self):
        return patch.object(Scope, 'get_metadata')

    def test_when_enriched_smartcontent_scope_then_save_in_enriched_and_return_payload(  # noqa
        self,
        scope,
        patch_get_metadata,
        product,
        product_smartcontent,
        mongo_database,
        mock_expected_smartcontent_scope_payload
    ):
        identifier = get_identifier(product)
        with patch_get_metadata as mock_get_metadata:
            mock_get_metadata.return_value = product_smartcontent
            response = scope.process(identifier, product)

        assert response == mock_expected_smartcontent_scope_payload
        assert mongo_database.enriched_products.count_documents({
            'seller_id': product['seller_id'],
            'sku': product['sku'],
            'source': SOURCE_SMARTCONTENT
        }) == 1

    def test_when_smartcontent_metadata_not_found_then_return_none(
        self,
        scope,
        patch_data_storage,
        patch_storage_manager_get_json,
        product
    ):
        identifier = get_identifier(product)
        with patch_data_storage as mock_data_storage:
            with patch_storage_manager_get_json as mock_storage_get_json:
                mock_data_storage.get_json = mock_storage_get_json
                mock_storage_get_json.side_effect = NotFound
                response = scope.process(identifier, product)

        assert response is None
        assert mock_storage_get_json.called

    @pytest.mark.parametrize(
        'allowed_smartcontent_category,allowed_smartcontent_seller',
        [
            ('AF', 'magazineluiza'),
            ('*', 'magazineluiza'),
            ('AF', '*'),
            ('*', '*')
        ]
    )
    def test_when_smartcontent_is_allowed_enabled_then_return_true(
        self,
        scope,
        product,
        allowed_smartcontent_category,
        allowed_smartcontent_seller
    ):
        product['seller_id'] = 'magazineluiza'
        product['categories'][0]['id'] = 'AF'
        identifier = get_identifier(product)

        with settings_stub(
            ALLOWED_SMARTCONTENT_CATEGORY=[
                allowed_smartcontent_category
            ],
            ALLOWED_SMARTCONTENT_SELLER=[
                allowed_smartcontent_seller
            ]
        ):
            allowed, identifier_enabled = scope.is_allowed(product)

        assert allowed
        assert identifier_enabled == identifier

    @pytest.mark.parametrize(
        'allowed_smartcontent_category,allowed_smartcontent_seller',
        [
            ('AF', 'fake'),
            ('*', 'fake'),
            ('MD', '*')
        ]
    )
    def test_when_smartcontent_is_allowed_disabled_then_return_false(
        self,
        scope,
        product,
        allowed_smartcontent_category,
        allowed_smartcontent_seller
    ):
        product['seller_id'] = 'magazineluiza'
        product['categories'][0]['id'] = 'AF'
        identifier = get_identifier(product)

        with settings_stub(
            ALLOWED_SMARTCONTENT_CATEGORY=[
                allowed_smartcontent_category
            ],
            ALLOWED_SMARTCONTENT_SELLER=[
                allowed_smartcontent_seller
            ]
        ):
            allowed, identifier_enabled = scope.is_allowed(product)

        assert not allowed
        assert identifier_enabled == identifier

    def test_when_smartcontent_enable_and_product_without_identifier_then_return_false(  # noqa
        self,
        scope,
        product
    ):
        product.pop('isbn', None)
        product['ean'] = ''
        with settings_stub(
            ALLOWED_SMARTCONTENT_CATEGORY=['*'],
            ALLOWED_SMARTCONTENT_SELLER=['*']
        ):
            allowed, identifier_enabled = scope.is_allowed(product)

        assert not allowed
        assert identifier_enabled == ''
