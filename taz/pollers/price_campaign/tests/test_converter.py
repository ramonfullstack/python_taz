import pytest

from taz.constants import MAGAZINE_LUIZA_SELLER_ID
from taz.pollers.price_campaign.converter import PriceConverter


class TestPriceConverter:

    @pytest.fixture
    def database_row(self):
        return {
            'batch_key': '01234',
            'sku': '012345678',
            'prices': '6386;299.00;299.00|7949;299.00;284.05'
        }

    @pytest.fixture
    def converter(self):
        return PriceConverter()

    @pytest.fixture
    def expected_transformed_set(self):
        return {
            '01234': {
                '012345678': {
                    'sku': '012345678',
                    'seller_id': MAGAZINE_LUIZA_SELLER_ID,
                    'prices': '6386;299.00;299.00|7949;299.00;284.05'
                }
            }
        }

    def test_price_campaign_converter(
        self,
        converter,
        database_row,
        expected_transformed_set
    ):
        converter.from_source([database_row])

        assert len(converter.get_items()) > 0
        assert expected_transformed_set == converter.get_items()
