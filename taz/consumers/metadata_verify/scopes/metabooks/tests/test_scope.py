from unittest.mock import ANY, call, patch

import pytest

from taz.constants import SOURCE_METABOOKS
from taz.consumers.core.exceptions import NotFound
from taz.consumers.metadata_verify.scopes.metabooks.scope import Scope
from taz.utils import get_identifier


class TestMetadataVerifyMetabooksScope:

    @pytest.fixture
    def scope(self):
        return Scope()

    @pytest.fixture
    def patch_get_metadata(self):
        return patch.object(Scope, 'get_metadata')

    @pytest.fixture
    def patch_get_media(self):
        return patch.object(Scope, 'get_media')

    @pytest.fixture
    def patch_metabooks_enriched_product_process(self):
        return patch.object(Scope, '_enriched_product_process')

    @pytest.fixture
    def patch_metabooks_factsheet_process(self):
        return patch.object(Scope, '_factsheet_process')

    @pytest.fixture
    def enriched_product_message(self):
        return {
            'sku': '1515489',
            'seller_id': 'magazineluiza',
            'navigation_id': '6211054',
            'metadata': {
                'Editora': 'Editora Unesp, Oxford University Press',
                'Edição': '1ª edição',
                'Autor': 'Blackburn, Simon',
                'Data de publicação': '30.12.2050',
                'Tipo de produto': 'pbook',
                'Número de páginas': '120',
                'Idiomas do produto': 'Português, Inglês'
            },
            'title': 'Ética',
            'subtitle': 'Uma brevíssima introdução',
            'description': 'Nossa autoimagem como criaturas morais',
            'source': 'metabooks',
            'entity': 'Livro',
            'category_id': 'LI',
            'subcategory_ids': [
                'LIFS',
                'LVFT'
            ]
        }

    def test_when_not_found_metabooks_metadata_then_remove_old_metabooks_enrichment(  # noqa
        self,
        scope,
        patch_data_storage,
        patch_storage_manager_get_json,
        product,
        mongo_database,
        enriched_product_message
    ):
        mongo_database.enriched_products.insert_one(
            enriched_product_message
        )
        identifier = get_identifier(product)
        with patch_data_storage as mock_data_storage:
            with patch_storage_manager_get_json as mock_storage_get_json:
                mock_data_storage.get_json = mock_storage_get_json
                mock_storage_get_json.side_effect = NotFound
                payload = scope.process(identifier, product)

        assert mongo_database.enriched_products.count_documents({
            'seller_id': product['seller_id'],
            'sku': product['sku'],
            'source': SOURCE_METABOOKS
        }) == 0
        assert payload is None
        assert mock_storage_get_json.call_args == call(
            'metabooks/9788582604663.json'
        )

    def test_when_not_found_metabooks_medias_then_return_payload_without_medias(  # noqa
        self,
        scope,
        patch_get_metadata,
        patch_storage_manager_get_json,
        patch_image_storage,
        product,
        patch_metabooks_enriched_product_process,
        patch_metabooks_factsheet_process
    ):
        identifier = get_identifier(product)
        with patch_get_metadata:
            with patch_image_storage as mock_image_storage:
                with patch_storage_manager_get_json as mock_storage_get_json:
                    with patch_metabooks_factsheet_process as mock_factsheet_process:  # noqa
                        with patch_metabooks_enriched_product_process as mock_enriched_product_process:  # noqa
                            mock_image_storage.get_json = mock_storage_get_json
                            mock_storage_get_json.side_effect = NotFound
                            payload = scope.process(identifier, product)

        assert payload == {
            'factsheet': ANY,
            'media': None,
            'enriched_product': ANY
        }
        assert mock_storage_get_json.called
        assert mock_factsheet_process.called
        assert mock_enriched_product_process.called

    def test_when_process_metabooks_scope_then_create_payload_with_success(
        self,
        scope,
        product,
        sku,
        seller_id,
        isbn,
        metadata,
        expected_metadata,
        mock_expected_metabooks_enriched_product,
        mock_metabooks_images,
        patch_get_media,
        mock_expected_metabooks_images,
        patch_get_metadata,
        metabooks_save_categories
    ):
        product.update({'sku': sku, 'seller_id': seller_id, 'isbn': isbn})
        mock_expected_metabooks_enriched_product.update({
            'subcategory_ids': ['LGTA', 'LDSO', 'LVDW', 'LCCO']
        })
        with patch_get_metadata as mock_get_metadata:
            with patch_get_media as mock_get_media:
                mock_get_metadata.return_value = metadata
                mock_get_media.return_value = mock_metabooks_images
                payload = scope.process(isbn, product)

        assert payload == {
            'factsheet': expected_metadata,
            'media': mock_expected_metabooks_images,
            'enriched_product': mock_expected_metabooks_enriched_product
        }

    def test_when_product_with_isbn_then_allowed(
        self,
        scope,
        product
    ):
        product.update({'isbn': 'isbn', 'ean': 'ean'})
        is_allowed, identifier = scope.is_allowed(product)
        assert is_allowed
        assert identifier == 'isbn'

    def test_when_product_with_ean_then_allowed(
        self,
        scope,
        product
    ):
        product.pop('isbn', None)
        product.update({'ean': 'ean'})
        is_allowed, identifier = scope.is_allowed(product)
        assert is_allowed
        assert identifier == 'ean'

    def test_when_product_without_identifier_then_not_allowed(
        self,
        scope,
        product
    ):
        product.pop('isbn', None)
        product.update({'ean': ''})
        is_allowed, identifier = scope.is_allowed(product)
        assert not is_allowed
        assert identifier == ''
