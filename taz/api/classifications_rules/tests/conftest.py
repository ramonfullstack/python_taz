from json import dumps, loads
from typing import Dict

import pytest
from pymongo.database import Database

from taz.api.common.json import custom_json_encoder


@pytest.fixture
def save_classification_rule(
    mongo_database: Database,
    mock_classification_rule_refrigerador_menor_400: Dict
):
    mongo_database.classifications_rules.insert_one(
        mock_classification_rule_refrigerador_menor_400
    )


@pytest.fixture
def mock_classification_rules_body_data(
    mock_classification_rule_refrigerador_menor_400: Dict
) -> str:
    return dumps(
        mock_classification_rule_refrigerador_menor_400,
        default=custom_json_encoder
    )


@pytest.fixture
def mock_classification_rules_response_data(
    mock_classification_rule_refrigerador_menor_400: Dict
):
    mock_classification_rule_refrigerador_menor_400['id'] = mock_classification_rule_refrigerador_menor_400.pop('_id')  # noqa
    return loads(dumps(
        mock_classification_rule_refrigerador_menor_400,
        default=custom_json_encoder
    ))
