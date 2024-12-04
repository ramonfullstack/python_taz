from unittest.mock import patch

import pytest

from taz.constants import MAGAZINE_LUIZA_SELLER_ID
from taz.core.matching.common.enriched_products import EnrichedProductSamples
from taz.core.merge.factsheet import FactsheetMerger
from taz.helpers.json import json_dumps, json_loads


class TestFactsheetMerger:

    @pytest.fixture
    def merger(self):
        return FactsheetMerger()

    @pytest.fixture
    def seller_id(self):
        return 'shoploko'

    @pytest.fixture
    def sku(self):
        return '74471'

    @pytest.fixture
    def patch_add_metadata_factsheet(self):
        return patch.object(FactsheetMerger, '_add_metadata_to_factsheet')

    @pytest.fixture
    def enriched_product_notfound(self, mongo_database):
        enriched_product = EnrichedProductSamples.shoploko_sku_74471()

        mongo_database.enriched_products.delete_one({
            'sku': enriched_product['sku'],
            'seller_id': enriched_product['seller_id']
        })

        return enriched_product

    @pytest.fixture
    def enriched_product(self, mongo_database):
        enriched_product = EnrichedProductSamples.shoploko_sku_74471()
        mongo_database.enriched_products.insert_one(enriched_product)
        return enriched_product

    @pytest.fixture
    def factsheet_empty(self):
        return {
            'items': [],
        }

    @pytest.fixture
    def mock_factsheet_empty_elements(self):
        return {
            'items': [{
                'display_name': 'Ficha Técnica',
                'slug': 'ficha-tecnica',
                'position': 1,
                'elements': []
            }]
        }

    @pytest.fixture
    def factsheet_with_items(self):
        return {
            'items': [
                {
                    'slug': 'other',
                    'position': 1,
                    'display_name': 'Other',
                    'elements': []
                }
            ]
        }

    def template_technical_info(self, elements):
        return {
            'slug': 'informacoes-complementares-magazineluiza',
            'position': 1,
            'key_name': 'Informações complementares',
            'elements': elements
        }

    @pytest.fixture
    def factsheet_with_old_metadata(self):
        return {
            'items': [
                {
                    'display_name': 'Ficha Técnica',
                    'slug': 'ficha-tecnica',
                    'position': 1,
                    'elements': [
                        self.template_technical_info(
                            [
                                {
                                    'key_name': 'Capacidade',
                                    'slug': 'capacidade',
                                    'value': '3,2L',
                                    'position': 1,
                                    'is_html': False
                                }
                            ]
                        )
                    ]
                }
            ]
        }

    @pytest.fixture
    def factsheet_element(self):
        return [
            self.template_technical_info(
                [
                    {
                        'key_name': 'Capacidade',
                        'slug': 'capacidade',
                        'value': '3,2L',
                        'position': 1,
                        'is_html': False
                    },
                    {
                        'key_name': 'Cor',
                        'slug': 'cor',
                        'value': 'Inox Vermelho',
                        'position': 2,
                        'is_html': False
                    },
                    {
                        'key_name': 'Marca',
                        'slug': 'marca',
                        'value': 'Mondial',
                        'position': 3,
                        'is_html': False
                    },
                    {
                        'key_name': 'Modelo',
                        'slug': 'modelo',
                        'value': 'AF-14',
                        'position': 4,
                        'is_html': False
                    },
                    {
                        'key_name': 'Modelo Nominal',
                        'slug': 'modelo-nominal',
                        'value': 'Family',
                        'position': 5,
                        'is_html': False
                    },
                    {
                        'key_name': 'Produto',
                        'slug': 'produto',
                        'value': 'Fritadeira Elétrica',
                        'position': 6,
                        'is_html': False
                    },
                    {
                        'key_name': 'Tipo',
                        'slug': 'tipo',
                        'value': 'Sem óleo',
                        'position': 7,
                        'is_html': False
                    },
                    {
                        'key_name': 'Voltagem',
                        'slug': 'voltagem',
                        'value': '110 volts',
                        'position': 8,
                        'is_html': False
                    }
                ]
            )
        ]

    @pytest.fixture
    def factsheet_with_metadata(self, factsheet_element):
        return {
            'items': [
                {
                    'display_name': 'Ficha Técnica',
                    'slug': 'ficha-tecnica',
                    'position': 1,
                    'elements': factsheet_element
                }
            ]
        }

    @pytest.fixture
    def factsheet_with_items_and_metadata(self, factsheet_element):
        return {
            'items': [
                {
                    'slug': 'other',
                    'position': 1,
                    'display_name': 'Other',
                    'elements': []
                },
                {
                    'display_name': 'Ficha Técnica',
                    'slug': 'ficha-tecnica',
                    'position': 2,
                    'elements': factsheet_element
                }
            ]
        }

    @pytest.fixture
    def factsheet_with_technical_specification(self):
        return {
            'items': [
                {
                    'display_name': 'Ficha Técnica',
                    'slug': 'ficha-tecnica',
                    'position': 1,
                    'elements': [
                        self.template_technical_info(
                            [
                                {
                                    'key_name': 'Capacidade da Memória',
                                    'slug': 'capacidade-da-memoria',
                                    'position': 1,
                                    'value': '32GB',
                                    'is_html': False
                                },
                                {
                                    'key_name': 'Cor',
                                    'slug': 'cor',
                                    'position': 2,
                                    'value': 'Platinum',
                                    'is_html': False
                                },
                                {
                                    'key_name': 'Marca',
                                    'slug': 'marca',
                                    'position': 3,
                                    'value': 'Motorola',
                                    'is_html': False
                                },
                                {
                                    'key_name': 'Memória RAM',
                                    'slug': 'memoria-ram',
                                    'position': 4,
                                    'value': '3GB',
                                    'is_html': False
                                },
                                {
                                    'key_name': 'Quantidade de Chips',
                                    'slug': 'quantidade-de-chips',
                                    'position': 5,
                                    'value': 'Dual Chip',
                                    'is_html': False
                                },
                                {
                                    'key_name': 'Resolução da Câmera Traseira',
                                    'slug': 'resolucao-da-camera-traseira',
                                    'position': 6,
                                    'value': '13MP',
                                    'is_html': False
                                },
                                {
                                    'key_name': 'Sistema Operacional',
                                    'slug': 'sistema-operacional',
                                    'position': 7,
                                    'value': 'Android Nougat',
                                    'is_html': False
                                },
                                {
                                    'key_name': 'Tamanho da Tela',
                                    'slug': 'tamanho-da-tela',
                                    'position': 8,
                                    'value': '5.5 polegadas',
                                    'is_html': False
                                }
                            ]
                        )
                    ]
                }
            ]
        }

    @pytest.fixture
    def mock_expected_factsheet_only_technical_info_code_anatel(
        self
    ):
        return {
            'items': [{
                'display_name': 'Ficha Técnica',
                'slug': 'ficha-tecnica',
                'position': 1,
                'elements': [
                    self.template_technical_info(
                        [{
                            'key_name': 'Certificado homologado pela Anatel número',  # noqa
                            'slug': 'certificado-homologado-pela-anatel-numero',  # noqa
                            'position': 1,
                            'value': 'HHHHH-AA-FFFFF',
                            'is_html': False
                        }]
                    )
                ]
            }]
        }

    def test_process_factsheet_merge_with_success(
        self,
        merger,
        seller_id,
        sku,
        patch_storage_manager_get_file,
        patch_storage_manager_upload,
        enriched_product,
        factsheet_empty,
        factsheet_with_metadata,
        patch_publish_manager
    ):
        with patch_storage_manager_get_file as mock_get:
            with patch_storage_manager_upload as mock_upload:
                with patch_publish_manager as mock_pubsub:
                    mock_get.return_value = json_dumps(
                        factsheet_empty, ensure_ascii=False
                    )
                    merger.merge(sku, seller_id)

        factsheet, filename, content_type = mock_upload.call_args[0]
        assert filename == f'{seller_id}/factsheet/{sku}.json'
        assert json_loads(factsheet) == factsheet_with_metadata
        assert mock_pubsub.called

    def test_when_should_process_is_false_then_not_process_event(
        self,
        merger,
        sku,
        patch_add_metadata_factsheet
    ):
        with patch_add_metadata_factsheet as mock_process:
            merger.merge(sku, MAGAZINE_LUIZA_SELLER_ID)

        mock_process.assert_not_called()

    def test_when_seller_id_is_magazineluiza_then_should_ignore_event(
        self,
        merger,
        sku
    ):
        should_process, _ = merger.validate_if_should_process(
            sku=sku,
            seller_id=MAGAZINE_LUIZA_SELLER_ID
        )
        assert not should_process

    def test_when_product_dont_have_enriched_product_then_should_ignore_event(
        self,
        merger,
        sku,
        seller_id,
        logger_stream
    ):
        should_process, _ = merger.validate_if_should_process(
            sku=sku,
            seller_id=seller_id
        )

        assert not should_process
        assert (
            'Product dont have enriched product '
            f'sku:{sku} seller_id:{seller_id}'
        ) in logger_stream.getvalue()

    def test_when_product_has_datasheet_then_should_ignore_event(
        self,
        merger,
        patch_add_metadata_factsheet,
        mongo_database,
        logger_stream
    ):
        enriched_product = EnrichedProductSamples.magazineluiza_sku_0233847_datasheet() # noqa
        enriched_product['seller_id'] = 'luizalabs'
        sku = enriched_product['sku']
        seller_id = enriched_product['seller_id']

        enriched = EnrichedProductSamples._1000store_sku_55316()
        enriched['sku'] = sku
        enriched['seller_id'] = seller_id

        mongo_database.enriched_products.insert_many([
            enriched_product,
            enriched
        ])

        should_process, _ = merger.validate_if_should_process(
            sku=sku,
            seller_id=seller_id
        )

        assert (
            f'Ignore product with sku:{sku} seller_id:{seller_id} '
            f'because it has datasheet on enriched products'
        ) in logger_stream.getvalue()

    def test_factsheet_merge_if_factsheet_not_exists(
        self,
        merger,
        seller_id,
        sku,
        patch_storage_manager_get_file,
        patch_storage_manager_upload,
        enriched_product,
        factsheet_with_metadata,
        patch_publish_manager
    ):
        with patch_storage_manager_get_file as mock_get:
            with patch_storage_manager_upload as mock_upload:
                with patch_publish_manager as mock_pubsub:
                    mock_get.return_value = None
                    merger.merge(sku, seller_id)

        factsheet, filename, content_type = mock_upload.call_args[0]
        assert filename == f'{seller_id}/factsheet/{sku}.json'
        assert json_loads(factsheet) == factsheet_with_metadata
        assert mock_pubsub.called

    def test_factsheet_merge_should_replace_old_metadata(
        self,
        merger,
        seller_id,
        sku,
        patch_storage_manager_get_file,
        patch_storage_manager_upload,
        enriched_product,
        factsheet_with_old_metadata,
        factsheet_with_metadata,
        patch_publish_manager
    ):
        with patch_storage_manager_get_file as mock_get:
            with patch_storage_manager_upload as mock_upload:
                with patch_publish_manager as mock_pubsub:
                    mock_get.return_value = json_dumps(
                        factsheet_with_old_metadata,
                        ensure_ascii=False
                    )
                    merger.merge(sku, seller_id)

        factsheet, filename, content_type = mock_upload.call_args[0]
        assert filename == f'{seller_id}/factsheet/{sku}.json'
        assert json_loads(factsheet) == factsheet_with_metadata
        assert mock_pubsub.called

    def test_factsheet_merge_should_preserve_old_items(
        self,
        merger,
        seller_id,
        sku,
        patch_storage_manager_get_file,
        patch_storage_manager_upload,
        enriched_product,
        factsheet_with_items,
        factsheet_with_items_and_metadata,
        patch_publish_manager
    ):
        with patch_storage_manager_get_file as mock_get:
            with patch_storage_manager_upload as mock_upload:
                with patch_publish_manager as mock_pubsub:
                    mock_get.return_value = json_dumps(
                        factsheet_with_items,
                        ensure_ascii=False
                    )
                    merger.merge(sku, seller_id)

        factsheet, filename, content_type = mock_upload.call_args[0]
        assert filename == f'{seller_id}/factsheet/{sku}.json'
        assert json_loads(factsheet) == factsheet_with_items_and_metadata
        assert mock_pubsub.called

    def test_factsheet_merge_should_not_upload_in_factsheet_consumer(
        self,
        merger,
        seller_id,
        sku,
        patch_storage_manager_get_file,
        patch_storage_manager_upload,
        enriched_product,
        factsheet_empty,
        factsheet_with_metadata,
        patch_publish_manager
    ):
        with patch_storage_manager_get_file as mock_get:
            with patch_storage_manager_upload as mock_upload:
                with patch_publish_manager as mock_pubsub:
                    mock_get.return_value = json_dumps(
                        factsheet_empty,
                        ensure_ascii=False
                    )
                    merger.merge(
                        sku,
                        seller_id,
                        factsheet=factsheet_empty
                    )

        mock_get.assert_not_called()
        mock_upload.assert_not_called()
        mock_pubsub.assert_not_called()
        assert factsheet_empty == factsheet_with_metadata

    def test_factsheet_merge_with_technical_specification_in_factsheet(
        self,
        merger,
        factsheet_with_technical_specification,
        factsheet_empty,
        patch_storage_manager_get_file,
        patch_storage_manager_upload,
        patch_publish_manager,
        mongo_database
    ):
        enriched = EnrichedProductSamples.shoploko_sku_155536300_with_technical_specification() # noqa
        enriched['source'] = 'magalu'
        mongo_database.enriched_products.insert_one(enriched)

        sku = enriched['sku']
        seller_id = enriched['seller_id']

        with patch_storage_manager_get_file as mock_get:
            with patch_storage_manager_upload as mock_upload:
                with patch_publish_manager as mock_pubsub:
                    mock_get.return_value = json_dumps(
                        factsheet_empty, ensure_ascii=False
                    )
                    merger.merge(sku, seller_id)

        factsheet, filename, content_type = mock_upload.call_args[0]

        assert content_type == 'application/json; charset=utf-8'
        assert filename == f'{seller_id}/factsheet/{sku}.json'
        assert json_loads(factsheet) == factsheet_with_technical_specification
        assert mock_pubsub.called

    def test_factsheet_merge_with_value_in_list(
        self,
        merger,
        mongo_database,
        factsheet_empty,
        patch_storage_manager_get_file,
        patch_storage_manager_upload,
        patch_publish_manager
    ):
        enriched_product = EnrichedProductSamples.ifcat_sku_24ng0002xx()
        enriched_product['source'] = 'magalu'
        mongo_database.enriched_products.insert_one(enriched_product)

        sku = enriched_product['sku']
        seller_id = enriched_product['seller_id']

        with patch_storage_manager_get_file as mock_get:
            with patch_storage_manager_upload as mock_upload:
                with patch_publish_manager as mock_pubsub:
                    mock_get.return_value = json_dumps(
                        factsheet_empty, ensure_ascii=False
                    )
                    merger.merge(sku, seller_id)

        factsheet, filename, content_type = mock_upload.call_args[0]

        assert mock_pubsub.called
        assert content_type == 'application/json; charset=utf-8'
        assert filename == f'{seller_id}/factsheet/{sku}.json'
        assert json_loads(factsheet) == {
            'items': [{
                'display_name': 'Ficha Técnica',
                'elements': [{
                    'elements': [
                        {
                            'is_html': False,
                            'key_name': 'Gênero',
                            'position': 1,
                            'slug': 'genero',
                            'value': 'Unissex'
                        },
                        {
                            'is_html': False,
                            'key_name': 'Idade Recomendada',
                            'position': 2,
                            'slug': 'idade-recomendada',
                            'value': '09 Anos, 10 Anos, A Partir de 11 Anos'
                        },
                        {
                            'is_html': False,
                            'key_name': 'Marca',
                            'position': 3,
                            'slug': 'marca',
                            'value': 'Nig Brinquedos'
                        }
                    ],
                    'key_name': 'Informações complementares',
                    'position': 1,
                    'slug': 'informacoes-complementares-magazineluiza'
                }],
                'position': 1,
                'slug': 'ficha-tecnica'
            }]
        }

    def test_when_factsheet_merger_with_generic_content_then_return_included_code_anatel(  # noqa
        self,
        merger,
        mongo_database,
        factsheet_empty,
        patch_storage_manager_get_file,
        patch_storage_manager_upload,
        patch_publish_manager,
        mock_expected_factsheet_only_technical_info_code_anatel
    ):
        enriched_product = EnrichedProductSamples.shoploko_sku_74471_generic_content()  # noqa
        sku = enriched_product['sku']
        seller_id = enriched_product['seller_id']
        mongo_database.enriched_products.insert_one(enriched_product)
        with patch_storage_manager_get_file as mock_get:
            with patch_storage_manager_upload as mock_upload:
                with patch_publish_manager as mock_pubsub:
                    mock_get.return_value = json_dumps(
                        factsheet_empty, ensure_ascii=False
                    )
                    merger.merge(sku, seller_id)

        factsheet, filename, content_type = mock_upload.call_args[0]

        assert mock_pubsub.called
        assert content_type == 'application/json; charset=utf-8'
        assert filename == f'{seller_id}/factsheet/{sku}.json'
        assert json_loads(factsheet) == mock_expected_factsheet_only_technical_info_code_anatel  # noqa

    def test_when_factsheet_merger_with_disabled_generic_content_then_return_factsheet_without_technical_info(  # noqa
        self,
        merger,
        mongo_database,
        patch_storage_manager_get_file,
        patch_storage_manager_upload,
        patch_publish_manager,
        mock_expected_factsheet_only_technical_info_code_anatel,
        mock_factsheet_empty_elements
    ):
        enriched_product = EnrichedProductSamples.shoploko_sku_74471_generic_content()  # noqa
        enriched_product.update({'active': False})
        sku = enriched_product['sku']
        seller_id = enriched_product['seller_id']
        mongo_database.enriched_products.insert_one(enriched_product)
        with patch_storage_manager_get_file as mock_get:
            with patch_storage_manager_upload as mock_upload:
                with patch_publish_manager as mock_pubsub:
                    mock_get.return_value = json_dumps(
                        mock_expected_factsheet_only_technical_info_code_anatel,  # noqa
                        ensure_ascii=False
                    )
                    merger.merge(sku, seller_id)

        factsheet, filename, content_type = mock_upload.call_args[0]

        assert mock_pubsub.called
        assert content_type == 'application/json; charset=utf-8'
        assert filename == f'{seller_id}/factsheet/{sku}.json'
        assert json_loads(factsheet) == mock_factsheet_empty_elements
