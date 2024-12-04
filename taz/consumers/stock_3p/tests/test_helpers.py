import pytest

from taz.consumers.stock_3p.helpers import Stock3pHelper


class TestStock3pHelper:

    @pytest.fixture
    def payload_stock(self):
        return {
            'sku': '012345678',
            'seller_id': 'netshoes',
            'list_price': 234.56,
            'price': 123.45,
            'delivery_availability': 'nationwide',
            'stock_count': 321,
            'stock_type': 'on_seller',
            'checkout_price': 234.56
        }

    def test_when_product_payload_doesnt_have_stock_count_field_then_should_return_true( # noqa
        self,
        payload_stock
    ):
        del payload_stock['stock_count']
        assert Stock3pHelper.is_missing_stock(payload_stock)

    def test_when_product_payload_have_stock_count_field_then_should_return_false( # noqa
        self,
        payload_stock
    ):
        assert not Stock3pHelper.is_missing_stock(payload_stock)

    @pytest.mark.parametrize(
        'price, new_price, expected', [
            (
                {
                    'sku': '012345678',
                    'seller_id': 'magazineluiza',
                    'list_price': 89.90,
                    'price': 79.90,
                    'delivery_availability': 'nationwide',
                    'stock_count': 321,
                    'stock_type': 'on_seller',
                    'checkout_price': 234.56,
                },
                {
                    'sku': '012345678',
                    'seller_id': 'magazineluiza',
                    'list_price': 99.90,
                    'price': 99.90,
                },
                {
                    'sku': '012345678',
                    'seller_id': 'magazineluiza',
                    'list_price': 99.90,
                    'price': 99.90,
                    'delivery_availability': 'nationwide',
                    'stock_count': 321,
                    'stock_type': 'on_seller',
                    'checkout_price': 234.56,
                }
            ),
            (
                {
                    'sku': '012345678',
                    'seller_id': 'magazineluiza',
                    'list_price': 89.90,
                    'price': 79.90,
                    'delivery_availability': 'regional',
                    'stock_count': 0,
                    'stock_type': 'on_seller',
                    'checkout_price': 234.56,
                },
                {
                    'sku': '012345678',
                    'seller_id': 'magazineluiza',
                    'delivery_availability': 'regional',
                    'stock_count': 0,
                },
                {
                    'sku': '012345678',
                    'seller_id': 'magazineluiza',
                    'list_price': 89.90,
                    'price': 79.90,
                    'delivery_availability': 'regional',
                    'stock_count': 0,
                    'stock_type': 'on_seller',
                    'checkout_price': 234.56,
                }
            ),
            (
                {
                    'sku': '012345678',
                    'seller_id': 'magazineluiza',
                    'list_price': 89.90,
                    'price': 79.90,
                    'delivery_availability': 'regional',
                    'stock_count': 0,
                    'stock_type': 'on_seller',
                    'checkout_price': 234.56,
                },
                {
                    'sku': '012345678',
                    'seller_id': 'magazineluiza',
                },
                {
                    'sku': '012345678',
                    'seller_id': 'magazineluiza',
                    'list_price': 89.90,
                    'price': 79.90,
                    'delivery_availability': 'regional',
                    'stock_count': 0,
                    'stock_type': 'on_seller',
                    'checkout_price': 234.56,
                }
            ),
            (
                {
                    'sku': '012345678',
                    'seller_id': 'magazineluiza',
                    'list_price': 89.90,
                    'price': 79.90,
                    'delivery_availability': 'regional',
                    'stock_count': 0,
                    'stock_type': 'on_seller',
                    'checkout_price': 234.56,
                },
                {
                    'sku': '012345678',
                    'seller_id': 'magazineluiza',
                    'list_price': 89.90,
                    'price': 79.90,
                    'delivery_availability': 'regional',
                    'stock_count': 0,
                    'stock_type': 'on_seller',
                    'checkout_price': 234.56,
                },
                {
                    'sku': '012345678',
                    'seller_id': 'magazineluiza',
                    'list_price': 89.90,
                    'price': 79.90,
                    'delivery_availability': 'regional',
                    'stock_count': 0,
                    'stock_type': 'on_seller',
                    'checkout_price': 234.56,
                }
            ),
        ]
    )
    def test_merge_prices_payload(
        self,
        price,
        new_price,
        expected
    ):
        response = Stock3pHelper.merge(price, new_price)
        assert response == expected

    def test_when_call_mount_payload_method_then_should_return_payload_with_success( # noqa
        self,
        payload_stock
    ):
        navigation_id = '123456789'
        response = Stock3pHelper.mount_payload_stocks(
            sku=payload_stock['sku'],
            seller_id=payload_stock['seller_id'],
            navigation_id=navigation_id,
            stock_count=payload_stock['stock_count']
        )

        del payload_stock['price']
        del payload_stock['list_price']
        del payload_stock['checkout_price']
        payload_stock['navigation_id'] = navigation_id

        assert response == payload_stock
