import pytest

from taz.pollers.partner.converter import PartnerConverter


class TestPartnerConverter:

    @pytest.fixture
    def database_row(self):
        return {
            'batch_key': '01',
            'id': '01234',
            'strdescricao': 'bacon ipsum'
        }

    @pytest.fixture
    def converter(self):
        return PartnerConverter()

    @pytest.fixture
    def expected_transformed_set(self):
        return {
            '01': {
                '01234': {
                    'id': '01234',
                    'description': 'bacon ipsum',
                }
            }
        }

    def test_converter_category(
        self,
        converter,
        database_row,
        expected_transformed_set
    ):

        converter.from_source([database_row])

        assert len(converter.get_items()) > 0
        assert expected_transformed_set == converter.get_items()
