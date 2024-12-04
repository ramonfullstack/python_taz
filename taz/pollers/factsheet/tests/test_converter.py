from unittest import mock

import pytest

from taz.constants import MAGAZINE_LUIZA_SELLER_ID
from taz.pollers.core.exceptions import DatabaseException
from taz.pollers.factsheet.converter import FactsheetConverter


class TestFactsheetConverter:

    @pytest.fixture
    def batch_key(self):
        return 21650

    @pytest.fixture
    def sku(self):
        return '216501100'

    @pytest.fixture
    def list_sku_db_row(self, batch_key, sku):
        return {
            'batch_key': batch_key,
            'sku': sku,
            'factsheet_id': 289108,
            'product_id': 179035
        }

    @pytest.fixture
    def details_db_rows(self):
        return [
            self._create_db_row(
                int_order=1,
                group_id=1,
                group_name='Apresentação',
                element_id=1000
            ),
            self._create_db_row(
                int_order=2,
                attribute_name='Apresentação do produto',
                attribute_value='Procurando Nemo está de volta',
                element_id=1001,
                parent_id=1000
            ),
            self._create_db_row(
                int_order=3,
                group_id=1,
                group_name='Ficha-Técnica',
                element_id=2000
            ),
            self._create_db_row(
                int_order=4,
                group_id=2,
                group_name='Informações técnicas',
                element_id=2001,
                parent_id=2000
            ),
            self._create_db_row(
                int_order=5,
                attribute_name='Marca',
                attribute_value='Sunny Brinquedos',
                element_id=2002,
                parent_id=2001
            ),
            self._create_db_row(
                int_order=6,
                attribute_name='Cor',
                attribute_value='Branco',
                element_id=2003,
                parent_id=2001
            ),
            self._create_db_row(
                int_order=7,
                attribute_name='Descrição',
                attribute_value='<h2>Título</h2><p>texto</p>',
                element_id=2004,
                parent_id=2001
            ),
            self._create_db_row(
                int_order=8,
                attribute_name='Idade',
                attribute_value='10 anos',
                element_id=2005,
                parent_id=2000
            ),
            self._create_db_row(
                int_order=8,
                attribute_name='Idade',
                attribute_value='12 anos',
                element_id=2005,
                parent_id=2000
            ),
            self._create_db_row(
                int_order=8,
                attribute_name='Idade',
                attribute_value='15 anos',
                element_id=2005,
                parent_id=2000
            ),
            self._create_db_row(
                int_order=9,
                attribute_name='Tipo de brinquedo',
                attribute_description='Plástico',
                element_id=3000,
                parent_id=2000
            ),
            self._create_db_row(
                int_order=10,
                attribute_name='Quantidade de peças',
                attribute_description='10',
                element_id=3001,
                parent_id=2000
            ),
            self._create_db_row(
                int_order=11,
                group_id=1,
                group_name='Destaque Tab (em Branco)',
                element_id=4000
            ),
            self._create_db_row(
                int_order=12,
                attribute_name='Destaque Attribute (em Branco)',
                element_id=4001,
                parent_id=4000
            )
        ]

    @pytest.fixture
    def mock_cursor(self, details_db_rows):
        cursor = mock.Mock()
        cursor.fetchall.return_value = details_db_rows
        return cursor

    @pytest.fixture
    def mock_data_source(self, mock_cursor):
        data_source = mock.Mock()
        data_source.fetch_details.return_value = mock_cursor
        return data_source

    @pytest.fixture
    def converter(self, mock_data_source):
        return FactsheetConverter(mock_data_source)

    @pytest.fixture
    def expected_result(self, sku):
        return {
            'sku': sku,
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'items': [
                {
                    'display_name': 'Apresentação',
                    'elements': [
                        {
                            'key_name': 'Apresentação do produto',
                            'slug': 'apresentacao-do-produto',
                            'position': 2,
                            'elements': [
                                {
                                    'value': 'Procurando Nemo está de volta',
                                    'is_html': False
                                }
                            ]
                        }
                    ],
                    'position': 1,
                    'slug': 'apresentacao'
                },
                {
                    'display_name': 'Ficha-Técnica',
                    'slug': 'ficha-tecnica',
                    'elements': [
                        {
                            'key_name': 'Informações técnicas',
                            'slug': 'informacoes-tecnicas',
                            'position': 4,
                            'elements': [
                                {
                                    'key_name': 'Marca',
                                    'slug': 'marca',
                                    'value': 'Sunny Brinquedos',
                                    'position': 5,
                                    'is_html': False
                                },
                                {
                                    'key_name': 'Cor',
                                    'slug': 'cor',
                                    'value': 'Branco',
                                    'position': 6,
                                    'is_html': False
                                },
                                {
                                    'key_name': 'Descrição',
                                    'slug': 'descricao',
                                    'value': '<h2>Título</h2><p>texto</p>',
                                    'position': 7,
                                    'is_html': True
                                }
                            ]
                        },
                        {
                            'key_name': 'Idade',
                            'slug': 'idade',
                            'position': 8,
                            'elements': [
                                {
                                    'is_html': False,
                                    'slug': '10-anos',
                                    'position': 8,
                                    'value': '10 anos'
                                },
                                {
                                    'is_html': False,
                                    'slug': '12-anos',
                                    'position': 8,
                                    'value': '12 anos'
                                },
                                {
                                    'is_html': False,
                                    'slug': '15-anos',
                                    'position': 8,
                                    'value': '15 anos'
                                }
                            ]
                        },
                        {
                            'key_name': 'Tipo de brinquedo',
                            'slug': 'tipo-de-brinquedo',
                            'position': 9,
                            'elements': [
                                {
                                    'value': 'Plástico',
                                    'is_html': False
                                }
                            ]
                        },
                        {
                            'key_name': 'Quantidade de peças',
                            'slug': 'quantidade-de-pecas',
                            'position': 10,
                            'elements': [
                                {
                                    'value': '10',
                                    'is_html': False
                                }
                            ]
                        },
                    ],
                    'position': 3
                }
            ]
        }

    def _create_db_row(self, **kwargs):
        db_row = {
            'int_order': None,
            'group_id': None,
            'group_name': None,
            'attribute_name': None,
            'attribute_value': None,
            'attribute_description': None,
            'element_id': None,
            'parent_id': None
        }
        db_row.update(kwargs)
        return db_row

    def test_convert_db_rows_to_factsheet(
        self, converter, mock_data_source, mock_cursor, sku, batch_key,
        list_sku_db_row, expected_result
    ):
        converter.from_source([list_sku_db_row])

        mock_data_source.fetch_details.assert_called_once_with(
            list_sku_db_row['factsheet_id'],
            list_sku_db_row['product_id']
        )

        assert mock_cursor.fetchall.called

        items = converter.get_items()
        assert items[batch_key][sku] == expected_result

    def test_raise_error_from_database_on_convert_factsheet(
        self, list_sku_db_row
    ):
        mock_db_error = mock.Mock()
        mock_db_error.fetch_details.side_effect = Exception

        converter = FactsheetConverter(mock_db_error)

        with pytest.raises(DatabaseException):
            converter.from_source([list_sku_db_row])

        assert mock_db_error.fetch_details.called
