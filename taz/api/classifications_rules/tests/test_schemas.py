from typing import Dict

import pytest
from marshmallow import EXCLUDE

from taz.api.classifications_rules.schemas import (
    FIELDS_ENABLED_INPUT,
    ClassificationsRules
)


class TestClassificationsRules:

    @pytest.fixture
    def schema(self):
        return ClassificationsRules(only=FIELDS_ENABLED_INPUT, unknown=EXCLUDE)

    def test_when_validate_classification_rule_input_then_successfully(
        self,
        mock_classification_rule_refrigerador_menor_400: Dict,
        schema: ClassificationsRules
    ):
        assert schema.validate(
            mock_classification_rule_refrigerador_menor_400
        ) == {}

    @pytest.mark.parametrize('field', [
        ('product_type'), ('operation'), ('price'), ('to'), ('user')
    ])
    def test_when_validate_classification_rule_input_without_required_field_then_raise_exception(  # noqa
        self,
        mock_classification_rule_refrigerador_menor_400: Dict,
        schema: ClassificationsRules,
        field: str
    ):
        mock_classification_rule_refrigerador_menor_400.pop(field, None)
        assert schema.validate(
            mock_classification_rule_refrigerador_menor_400
        ) == {field: ['Missing data for required field.']}

    @pytest.mark.parametrize('field', [
        ('product_type'), ('operation'), ('price'), ('to'), ('user')
    ])
    def test_when_validate_classification_rule_input_none_required_field_then_raise_exception(  # noqa
        self,
        mock_classification_rule_refrigerador_menor_400: Dict,
        schema: ClassificationsRules,
        field: str
    ):
        mock_classification_rule_refrigerador_menor_400[field] = None
        assert schema.validate(
            mock_classification_rule_refrigerador_menor_400
        ) == {field: ['Field may not be null.']}

    def test_when_validate_classification_rule_input_with_invalid_operation_then_raise_exception(  # noqa
        self,
        mock_classification_rule_refrigerador_menor_400: Dict,
        schema: ClassificationsRules,
    ):
        mock_classification_rule_refrigerador_menor_400.update(
            {'operation': 'FAKE'}
        )
        assert schema.validate(
            mock_classification_rule_refrigerador_menor_400
        ) == {'operation': ['Must be one of: MENOR_IGUAL, MAIOR_IGUAL.']}

    @pytest.mark.parametrize('field', [
        ('product_type'), ('category_id'), ('subcategory_ids')
    ])
    def test_when_validate_classification_rule_input_without_required_field_on_to_field_then_raise_exception(  # noqa
        self,
        mock_classification_rule_refrigerador_menor_400: Dict,
        schema: ClassificationsRules,
        field: str
    ):
        mock_classification_rule_refrigerador_menor_400['to'].pop(field, str)
        assert schema.validate(
            mock_classification_rule_refrigerador_menor_400
        ) == {'to': {field: ['Missing data for required field.']}}

    @pytest.mark.parametrize('field', [
        ('product_type'), ('category_id'), ('subcategory_ids')
    ])
    def test_when_validate_classification_rule_input_none_required_field_on_to_field_then_raise_exception(  # noqa
        self,
        mock_classification_rule_refrigerador_menor_400: Dict,
        schema: ClassificationsRules,
        field: str
    ):
        mock_classification_rule_refrigerador_menor_400['to'][field] = None
        assert schema.validate(
            mock_classification_rule_refrigerador_menor_400
        ) == {'to': {field: ['Field may not be null.']}}

    def test_when_validate_classification_rule_input_with_subcategory_empty_then_raise_exception(  # noqa
        self,
        mock_classification_rule_refrigerador_menor_400: Dict,
        schema: ClassificationsRules
    ):
        mock_classification_rule_refrigerador_menor_400['to']['subcategory_ids'] = []  # noqa
        assert schema.validate(
            mock_classification_rule_refrigerador_menor_400
        ) == {
            'to': {'subcategory_ids': ['Shorter than minimum length 1.']}
        }

    def test_when_validate_not_allowed_product_type_classification_rule_input_then_raise_exception(  # noqa
        self,
        mock_classification_rule_refrigerador_menor_400: Dict,
        schema: ClassificationsRules
    ):
        product_type: str = 'Livro'
        mock_classification_rule_refrigerador_menor_400.update(
            {'product_type': product_type}
        )
        assert schema.validate(
            mock_classification_rule_refrigerador_menor_400
        ) == {'product_type': [f'product_type:{product_type} is not valid.']}
