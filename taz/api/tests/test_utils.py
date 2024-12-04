import pytest

from taz.api.utils import (
    convert_fields_to_list,
    format_fields_filtered,
    format_response_with_fields
)


class TestUtilsApi:

    @pytest.fixture
    def mock_list_input(self):
        return ['A', 'B', 'C']

    def test_convert_fields_when_receive_string_separated_by_comma_then_return_list_of_string( # noqa
        self,
        mock_list_input
    ):
        result = convert_fields_to_list(','.join(mock_list_input))
        assert result == mock_list_input

    def test_convert_fields_when_receive_null_field_then_return_empty_list(
        self
    ):
        assert convert_fields_to_list(None) == []

    def test_format_fields_when_receive_list_of_fields_then_return_dict_with_fields( # noqa
        self,
        mock_list_input
    ):
        result = format_fields_filtered(mock_list_input)
        assert result == {'A': 1, 'B': 1, 'C': 1, '_id': 0}

    def test_format_fields_when_not_receive_value_then_return_dict_with_id_field_only( # noqa
        self
    ):
        assert format_fields_filtered() == {'_id': 0}

    def test_format_response_when_receive_payload_then_return_only_fields_required( # noqa
        self
    ):
        mock = [{'A': 'value A', 'B': 'value B'}]
        result = format_response_with_fields('A', {'results': mock})
        assert result == {'results': [{'A': 'value A'}]}
