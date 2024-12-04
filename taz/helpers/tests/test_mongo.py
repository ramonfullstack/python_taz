from decimal import Decimal

import pytest

from taz.helpers.mongo import _unpack, decode_body


@pytest.fixture
def price_dict():
    return {
        'sku': '012345678',
        'seller_id': 'magazineluiza',
        'list_price': Decimal(234.56),
        'price': Decimal(123.45),
        'delivery_availability': 'nationwide',
        'stock_count': 321,
        'stock_type': 'on_seller',
        'checkout_price': Decimal(234.56),
    }


def test_decode_body_with_decimal(price_dict):
    data = decode_body(price_dict)

    assert isinstance(data, dict)


def test_decode_body_without_decimal(price_dict):
    data = decode_body({
        'sku': price_dict['sku'],
        'seller_id': price_dict['seller_id'],
        'delivery_availability': price_dict['delivery_availability'],
        'stock_count': price_dict['stock_count'],
        'stock_type': price_dict['stock_type'],
    })

    assert isinstance(data, dict)


def test_unpack_should_return_number():
    unpacked_data = _unpack(1)

    assert unpacked_data == 1


def test_unpack_should_return_key_value():
    data = _unpack({"a": "b"})

    assert list(data)[0][0] == "a"
    assert list(data)[0][1] == "b"
