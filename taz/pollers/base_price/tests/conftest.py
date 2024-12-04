from decimal import Decimal

import pytest

from taz.constants import MAGAZINE_LUIZA_SELLER_ID
from taz.pollers.base_price.converter import BasePriceConverter


@pytest.fixture
def database_row():
    return {
        'batch_key': '01234',
        'sku': '012345678',
        'list_price': Decimal('234.56'),
        'gemco_id': '5034529',
        'bundles': '1234;4|3232;2'
    }


@pytest.fixture
def database_row_without_bundle(database_row):
    database_row['bundles'] = None
    return database_row


@pytest.fixture
def converter():
    return BasePriceConverter()


@pytest.fixture
def expected_transformed_set():
    return {
        '01234': {
            '012345678': {
                'sku': '012345678',
                'seller_id': MAGAZINE_LUIZA_SELLER_ID,
                'list_price': '234.56',
                'gemco_id': '5034529',
                'bundles': '1234;4|3232;2'
            }
        }
    }


@pytest.fixture
def expected_transformed_set_without_bundle(expected_transformed_set):
    expected_transformed_set['01234']['012345678']['bundles'] = None
    return expected_transformed_set
