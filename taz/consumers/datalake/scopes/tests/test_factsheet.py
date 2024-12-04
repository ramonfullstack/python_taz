import datetime
from unittest.mock import Mock

import pytest

from taz.constants import CREATE_ACTION, DELETE_ACTION, UPDATE_ACTION
from taz.consumers.datalake.scopes.factsheet import Scope


class TestFactsheetScope:

    @pytest.fixture
    def mock_current_datetime(self):
        return datetime.datetime(2022, 1, 24, 0, 0, 0)

    @pytest.fixture
    def mock_expected_factsheet(
        self,
        mock_factsheet_sku,
        mock_factsheet_seller_id,
        mock_factsheet_navigation_id,
        mock_current_datetime
    ):
        return {
            'sku': mock_factsheet_sku,
            'seller_id': mock_factsheet_seller_id,
            'navigation_id': mock_factsheet_navigation_id,
            'action': CREATE_ACTION,
            'updated_at': mock_current_datetime.isoformat(),
            'items': [
                {
                    'element_group': '<h2>Apresentação</h2>',
                    'element_key': 'Apresentação do produto',
                    'element_values': [
                        {
                            'key': 'Apresentação do produto',
                            'value': 'Procurando Nemo está de volta agora'
                        }
                    ]
                },
                {
                    'element_group': '<h2>Apresentação</h2>',
                    'element_key': 'Apresentação do produto',
                    'element_values': [
                        {
                            'key': 'Apresentação do produto',
                            'value': '<h2>Procurando Nemo está de volta</h2>'
                        }
                    ]
                },
                {
                    'element_group': 'Ficha-Técnica',
                    'element_key': 'Informações complementares',
                    'element_values': [
                        {
                            'key': 'Marca',
                            'value': 'Sunny Brinquedos'
                        },
                        {
                            'key': 'Cor',
                            'value': 'Branco'
                        },
                        {
                            'key': 'Desenvolvimento',
                            'value': 'Capacidade visual'
                        },
                        {
                            'key': 'Desenvolvimento',
                            'value': 'Percepção cromática'
                        },
                        {
                            'key': 'Desenvolvimento',
                            'value': '<h2>Diversão</h2><p>criança</p>'
                        }
                    ]
                }
            ]
        }

    @pytest.mark.parametrize('action', [
        CREATE_ACTION,
        UPDATE_ACTION
    ])
    def test_get_data_should_factsheet_payload(
        self,
        mock_factsheet_navigation_id,
        mock_factsheet_sku,
        mock_factsheet_seller_id,
        action,
        patch_storage_manager_get_json,
        mock_factsheet_payload,
        mock_current_datetime,
        mock_expected_factsheet,
        patch_datetime
    ):
        factsheet_scope = Scope(
            sku=mock_factsheet_sku,
            seller_id=mock_factsheet_seller_id,
            navigation_id=mock_factsheet_navigation_id,
            action=action
        )
        mock_expected_factsheet.update({'action': action})

        with patch_storage_manager_get_json as mock_get_json:
            with patch_datetime as mock_datetime:
                mock_datetime.now.return_value = mock_current_datetime
                mock_get_json.return_value = mock_factsheet_payload
                payload = factsheet_scope.get_data()

        assert payload == mock_expected_factsheet

    def test_get_data_action_delete_should_factsheet_payload(
        self,
        mock_factsheet_navigation_id,
        mock_factsheet_sku,
        mock_factsheet_seller_id,
        patch_storage_manager_get_json,
        mock_factsheet_payload,
        mock_current_datetime,
        mock_expected_factsheet,
        patch_mongo_collection,
        patch_datetime
    ):
        action = DELETE_ACTION
        factsheet_scope = Scope(
            sku=mock_factsheet_sku,
            seller_id=mock_factsheet_seller_id,
            navigation_id=mock_factsheet_navigation_id,
            action=action
        )
        mock_expected_factsheet.update({'action': action, 'items': []})

        with patch_storage_manager_get_json as mock_get_json:
            with patch_datetime as mock_datetime:
                with patch_mongo_collection as mock_collection:
                    mock_find_one = Mock()
                    mock_collection.return_value = mock_find_one
                    mock_find_one.find_one.side_effect = [
                        {'navigation_id': mock_factsheet_navigation_id}
                    ]

                    mock_datetime.now.return_value = mock_current_datetime
                    mock_get_json.return_value = mock_factsheet_payload

                    payload = factsheet_scope.get_data()

        assert payload == mock_expected_factsheet

    def test_get_data_invalid_factsheet_should_payload_empty(
        self,
        mock_factsheet_sku,
        mock_factsheet_seller_id,
        patch_storage_manager_get_json
    ):
        action = CREATE_ACTION
        factsheet_scope = Scope(
            sku=mock_factsheet_sku,
            seller_id=mock_factsheet_seller_id,
            action=action
        )
        with patch_storage_manager_get_json as mock_get_json:
            mock_get_json.return_value = {
                'items': [{}]
            }
            payload = factsheet_scope.get_data()
            assert not payload

    def test_get_data_without_value_in_field_should_return_factsheet_with_none_value( # noqa
        self,
        mock_factsheet_navigation_id,
        mock_factsheet_sku,
        mock_factsheet_seller_id,
        patch_storage_manager_get_json,
        mock_factsheet_payload,
        mock_current_datetime,
        mock_expected_factsheet,
        patch_datetime
    ):
        factsheet_scope = Scope(
            sku=mock_factsheet_sku,
            seller_id=mock_factsheet_seller_id,
            navigation_id=mock_factsheet_navigation_id,
            action=UPDATE_ACTION
        )
        mock_expected_factsheet.update({'action': UPDATE_ACTION})
        del mock_factsheet_payload['items'][1]['elements'][0]['elements'][0]['value'] # noqa
        mock_expected_factsheet['items'][2]['element_values'][0]['value'] = None # noqa

        with patch_storage_manager_get_json as mock_get_json:
            with patch_datetime as mock_datetime:
                mock_datetime.now.return_value = mock_current_datetime
                mock_get_json.return_value = mock_factsheet_payload
                payload = factsheet_scope.get_data()

        assert payload == mock_expected_factsheet

    def test_when_factsheet_not_hierarchical_then_correct_factsheet(
        self,
        mock_factsheet_navigation_id,
        mock_factsheet_sku,
        mock_factsheet_seller_id,
        patch_storage_manager_get_json,
        mock_factsheet_payload,
        mock_current_datetime,
        mock_expected_factsheet,
        patch_datetime
    ):
        factsheet_payload = {
            'items': [
                {
                    'display_name': 'Ficha-Técnica',
                    'slug': 'ficha-tecnica',
                    'elements': [
                        {
                            'key_name': 'Marca',
                            'slug': 'marca',
                            'elements': [
                                {
                                    'value': 'Camesa',
                                    'is_html': False
                                },
                                {
                                    'value': 'Falsa',
                                    'is_html': False
                                }
                            ]
                        },
                        {
                            'key_name': 'Referência',
                            'slug': 'referencia',
                            'elements': [
                                {
                                    'value': '1.12581.02.1007',
                                    'is_html': False
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        factsheet_scope = Scope(
            sku=mock_factsheet_sku,
            seller_id=mock_factsheet_seller_id,
            navigation_id=mock_factsheet_navigation_id,
            action=UPDATE_ACTION
        )
        mock_expected_factsheet.update({'action': UPDATE_ACTION})

        with patch_storage_manager_get_json as mock_get_json:
            with patch_datetime as mock_datetime:
                mock_datetime.now.return_value = mock_current_datetime
                mock_get_json.return_value = factsheet_payload
                payload = factsheet_scope.get_data()

        assert payload == {
            'sku': '123456789',
            'seller_id': 'epoca',
            'navigation_id': '123456789',
            'action': 'update',
            'updated_at': '2022-01-24T00:00:00',
            'items': [
                {
                    'element_group': 'Ficha-Técnica',
                    'element_key': 'Marca',
                    'element_values': [
                        {'key': 'Marca', 'value': 'Camesa'},
                        {'key': 'Marca', 'value': 'Falsa'}
                    ]
                },
                {
                    'element_group': 'Ficha-Técnica',
                    'element_key': 'Referência',
                    'element_values': [
                        {'key': 'Referência', 'value': '1.12581.02.1007'}
                    ]
                }
            ]
        }
