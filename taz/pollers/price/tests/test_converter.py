from decimal import Decimal

import pytest

from taz.constants import MAGAZINE_LUIZA_SELLER_ID
from taz.pollers.price.converter import PriceConverter


class TestPriceConverter:

    @pytest.fixture
    def database_row(self):
        return {
            'batch_key': '01234',
            'sku': '012345678',
            'list_price': Decimal('234.56'),
            'price': Decimal('123.45'),
            'nationwide_delivery': None,
            'regional_delivery': None,
            'stock_count': None,
            'stock_type': None,
            'checkout_price': Decimal('234.56'),
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
                    'list_price': Decimal('234.56'),
                    'price': Decimal('123.45'),
                    'delivery_availability': None,
                    'stock_count': 321,
                    'stock_type': None,
                    'campaign_code': 0,
                    'checkout_price': Decimal('234.56'),
                }
            }
        }

    @pytest.mark.parametrize(
        'delivery_availability,stock_count,nationwide,regional,stock_type,campaign_code', [  # noqa
            ('nationwide', 321, 1, 0, 'on_seller', 0),
            ('regional', 321, 0, 1, 'on_supplier', 0),
            ('unavailable', 0, 0, 0, 'on_seller', 0),
            ('unavailable', 0, 0, 0, 'on_seller', 1234),
        ]
    )
    def test_delivery_availability_database_convertion(
        self,
        converter,
        database_row,
        delivery_availability,
        stock_count,
        expected_transformed_set,
        nationwide,
        regional,
        stock_type,
        campaign_code
    ):
        expected_transformed_set['01234']['012345678'].update({
            'delivery_availability': delivery_availability,
            'stock_count': stock_count,
            'stock_type': stock_type,
            'campaign_code': campaign_code,
        })

        database_row.update({
            'nationwide_delivery': nationwide,
            'regional_delivery': regional,
            'stock_count': stock_count,
            'stock_type': stock_type,
            'campaign_code': campaign_code
        })

        converter.from_source([database_row])

        assert len(converter.get_items()) > 0
        assert expected_transformed_set == converter.get_items()
