from decimal import Context, Decimal

import pytest
from simple_settings import settings

from taz.helpers.json import json_dumps, json_loads


class TestJsonHelper:

    @pytest.fixture
    def expected_dict(self):
        return {
            'a': Decimal('1.0'),
            'b': Decimal('0.9'),
            'c': Decimal('0.83'),
            'd': +Decimal(0.91),
        }

    @pytest.fixture
    def expected_string(self):
        return '{"a": 1.0, "b": 0.9, "c": 0.83, "d": 0.91}'

    def test_context_must_be_loaded_and_defined_on_settings(self):
        """
        This test was made only to load Decimal context from settings.
        Without it, the assertions would fail because it follows
        default precision, not the one the defined on settings.
        """
        assert isinstance(settings.context, Context)

    def test_json_dumps_and_loads_must_follow_precision(
        self, expected_dict, expected_string
    ):
        assert expected_dict == json_loads(expected_string)

        dumped = json_dumps(expected_dict)
        assert '"a": 1.0' in dumped
        assert '"b": 0.9' in dumped
        assert '"c": 0.83' in dumped
        assert '"d": 0.91' in dumped

    def test_json_loads_must_deal_with_bytes(
        self, expected_dict, expected_string
    ):
        byte_obj = bytes(expected_string.encode('utf-8'))
        assert expected_dict == json_loads(byte_obj)

    def test_json_with_special_characters(self):
        payload = {
            'Resolução da Câmera': '12MP'
        }

        response = json_dumps(payload, False)
        assert response == '{"Resolução da Câmera": "12MP"}'

    def test_json_ordered(self):
        payload = {'b': 1, 'a': 1, 'c': {'b': 1, 'a': 1}}
        response = json_dumps(payload, True, True)
        assert response == '{"a": 1, "b": 1, "c": {"a": 1, "b": 1}}'
