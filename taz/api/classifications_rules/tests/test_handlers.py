import json
from typing import Dict

import pytest
from falcon.testing.client import Result
from pymongo.database import Database

from taz.api.classifications_rules.schemas import ClassificationsRulesStatus
from taz.api.common.json import custom_json_encoder


class TestClassificationsRulesHandler:

    @pytest.fixture
    def mock_url(self) -> str:
        return '/classifications_rules'

    def test_when_list_classifications_rules_return_empty(
        self,
        mock_url: str,
        client
    ):
        response: Result = client.get(mock_url)
        assert response.status_code == 200
        assert response.json == {'data': []}

    def test_when_list_classifications_rules_return_all_classifications_rules(
        self,
        mock_url: str,
        client,
        save_classification_rule,
        mock_classification_rule_refrigerador_menor_400,
        mock_classification_rules_response_data: Dict
    ):
        response: Result = client.get(mock_url)
        assert response.status_code == 200
        assert response.json == {'data': [
            mock_classification_rules_response_data
        ]}

    def test_when_create_classification_rule_then_return_success(
        self,
        mock_url: str,
        client,
        mock_classification_rule_refrigerador_menor_400: Dict,
        mongo_database: Database,
        mock_classification_rules_body_data: str
    ):
        response: Result = client.post(
            mock_url,
            body=mock_classification_rules_body_data
        )
        assert response.status_code == 201
        assert mongo_database.classifications_rules.count_documents({}) == 1

    @pytest.mark.parametrize('field', [
        ('product_type'), ('operation'), ('price'), ('to')
    ])
    def test_when_create_invalid_classification_rule_then_return_bad_request(
        self,
        mock_url: str,
        client,
        mock_classification_rule_refrigerador_menor_400: Dict,
        field: str,
        mongo_database: Database
    ):
        mock_classification_rule_refrigerador_menor_400.pop(field, None)
        response: Result = client.post(
            mock_url,
            body=json.dumps(
                mock_classification_rule_refrigerador_menor_400,
                default=custom_json_encoder
            )
        )

        assert response.status_code == 400
        assert json.loads(response.json['error_message']) == {
            field: ['Missing data for required field.']
        }
        assert mongo_database.classifications_rules.count_documents({}) == 0

    def test_when_update_classification_rule_then_return_success(
        self,
        mock_url: str,
        client,
        save_classification_rule,
        mock_classification_rule_refrigerador_menor_400: Dict,
        mongo_database: Database,
        mock_classification_rules_body_data: str
    ):
        d = json.loads(mock_classification_rules_body_data)
        d['id'] = d.pop('_id')
        mock_classification_rules_body_data = json.dumps(d)

        response: Result = client.put(
            mock_url,
            body=mock_classification_rules_body_data
        )
        assert response.status_code == 200
        assert mongo_database.classifications_rules.count_documents({}) == 1

    def test_when_there_is_already_a_classification_rule_created(
        self,
        mock_url,
        client,
        mongo_database: Database,
        mock_classification_rules_body_data: str,
        mock_classification_rule_refrigerador_menor_400
    ):
        mongo_database.classifications_rules.insert_one(
            mock_classification_rule_refrigerador_menor_400
        )
        response: Result = client.post(
            mock_url,
            body=mock_classification_rules_body_data,
        )
        assert response.status_code == 400
        assert mongo_database.classifications_rules.count_documents({}) == 1


class TestClassificationsRulesByIdHandler:

    @pytest.fixture
    def mock_url(
        self,
        mock_classification_rule_refrigerador_menor_400: Dict
    ) -> str:
        id: str = mock_classification_rule_refrigerador_menor_400['_id']
        return f'/classifications_rules/{id}'

    def test_when_delete_classification_rule_then_return_bad_request(
        self,
        mock_url: str,
        client,
        mongo_database: Database
    ):
        response: Result = client.delete(mock_url)
        assert response.status_code == 400
        assert mongo_database.classifications_rules.count_documents({}) == 0

    def test_when_delete_classification_rule_then_return_success(
        self,
        mock_url: str,
        client,
        mock_classification_rule_refrigerador_menor_400: Dict,
        mongo_database: Database
    ):
        mock_classification_rule_refrigerador_menor_400.update({
            'active': True,
            'status': ClassificationsRulesStatus.created.value
        })
        mongo_database.classifications_rules.insert_one(
            mock_classification_rule_refrigerador_menor_400
        )
        response: Result = client.delete(mock_url)

        classification_rule: Dict = mongo_database.classifications_rules.find_one({})  # noqa

        assert response.status_code == 200
        assert mongo_database.classifications_rules.count_documents({}) == 1
        assert not classification_rule['active']
        assert classification_rule['status'] == ClassificationsRulesStatus.deleted.value  # noqa

    def test_when_get_classification_rule_by_id_then_return_success(
        self,
        mock_url: str,
        client,
        save_classification_rule,
        mock_classification_rules_response_data: Dict
    ):
        response: Result = client.get(mock_url)
        assert response.status_code == 200
        assert response.json == {
            'data': mock_classification_rules_response_data
        }

    def test_when_get_classification_rule_by_id_then_return_not_found(
        self,
        mock_url: str,
        client
    ):
        response: Result = client.get(mock_url)
        assert response.status_code == 404
