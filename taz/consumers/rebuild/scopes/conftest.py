from unittest.mock import Mock

import pytest


@pytest.fixture
def mock_kinesis():
    return Mock()


@pytest.fixture
def populated_products(mongo_database):
    mongo_database.raw_products.insert_many([
        {
            '_id': '111',
            'sku': '13203400',
            'seller_id': 'magazineluiza',
            'categories': [{'id': 'AA'}],
            'disable_on_matching': False
        },
        {
            '_id': '222',
            'sku': '51009933',
            'seller_id': 'magazineluiza',
            'categories': [{'id': 'BB'}],
            'disable_on_matching': False
        },
        {
            '_id': '333',
            'sku': '33343400',
            'seller_id': 'magazineluiza',
            'categories': [{'id': 'CC'}],
            'disable_on_matching': False
        },
        {
            '_id': '444',
            'sku': '84390300',
            'seller_id': 'epocacosmeticos',
            'categories': [{'id': 'DD', 'subcategories': [{'id': 'AA'}]}],
            'disable_on_matching': False
        }
    ])


@pytest.fixture
def expected_products():
    return [
        {
            'sku': '13203400',
            'seller_id': 'magazineluiza',
            'categories': [{'id': 'AA'}],
            'disable_on_matching': False
        },
        {
            'sku': '51009933',
            'seller_id': 'magazineluiza',
            'categories': [{'id': 'BB'}],
            'disable_on_matching': False
        },
        {
            'sku': '33343400',
            'seller_id': 'magazineluiza',
            'categories': [{'id': 'CC'}],
            'disable_on_matching': False
        },
        {
            'sku': '84390300',
            'seller_id': 'epocacosmeticos',
            'categories': [{'id': 'DD', 'subcategories': [{'id': 'AA'}]}],
            'disable_on_matching': False
        }
    ]
