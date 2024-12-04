import pytest

from taz import constants
from taz.constants import (
    AVAILABILITY_NATIONWIDE,
    AVAILABILITY_REGIONAL,
    MAGAZINE_LUIZA_SELLER_ID,
    STOCK_TYPE_DC,
    STOCK_TYPE_ON_SELLER
)
from taz.consumers.datalake.scopes.stock import Scope
from taz.utils import convert_id_to_nine_digits


class TestStockScope:

    @pytest.fixture
    def mock_price(self):
        return {
            'sku': '088894700',
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'price': 0,
            'list_price': 0,
            'minimum_order_quantity': 10
        }

    @pytest.fixture
    def mock_stock_3p(self):
        return {
            'seller_id': 'luizalabs',
            'sku': '012345678',
            'navigation_id': 'abcdefgh',
            'branch_id': 0,
            'stock_count': 156,
            'stock_type': STOCK_TYPE_ON_SELLER,
            'delivery_availability': AVAILABILITY_NATIONWIDE
        }

    @pytest.fixture
    def mock_stock_1p(self):
        return {
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'sku': '088894700',
            'branch_id': 300,
            'latitude': -23.131369,
            'longitude': -46.95137,
            'delivery_availability': AVAILABILITY_REGIONAL,
            'position': {
                'physic': {
                    'amount': 100,
                    'reserved': 0,
                    'available': 100
                },
                'logic': {
                    'amount': 0,
                    'reserved': 0,
                    'available': 0
                }
            },
            'type': STOCK_TYPE_DC,
            'navigation_id': '0888947'
        }

    @pytest.fixture
    def save_stock(self, mock_stock_1p, mock_stock_3p, mongo_database):
        return mongo_database.stocks.insert_many([
            mock_stock_1p,
            mock_stock_3p
        ])

    @pytest.mark.parametrize('stock_payload', [
        'mock_stock_1p',
        'mock_stock_3p'
    ])
    def test_when_called_get_data_then_should_return_stock_payload_with_success( # noqa
        self,
        mongo_database,
        save_stock,
        stock_payload,
        mock_price,
        request
    ):
        stock_payload = request.getfixturevalue(stock_payload)
        sku = stock_payload['sku']
        seller_id = stock_payload['seller_id']
        navigation_id = stock_payload['navigation_id']

        if seller_id == MAGAZINE_LUIZA_SELLER_ID:
            stock_count = stock_payload['position']['physic']['amount']
            navigation_id = convert_id_to_nine_digits(navigation_id)
            moq = mock_price['minimum_order_quantity']
        else:
            stock_count = stock_payload['stock_count']
            moq = 0
            mock_price.pop('minimum_order_quantity', None)

        mock_price['sku'] = sku
        mock_price['seller_id'] = seller_id
        mongo_database.prices.insert_one(mock_price)

        scope_stock = Scope(
            seller_id=seller_id,
            sku=sku,
            navigation_id=navigation_id
        ).get_data()

        assert scope_stock == {
            'sku': sku,
            'seller_id': seller_id,
            'navigation_id': navigation_id,
            'stock_count': stock_count,
            'minimum_order_quantity': moq
        }

    @pytest.mark.parametrize('stock_payload', [
        'mock_stock_1p',
        'mock_stock_3p'
    ])
    def test_when_stock_not_found_then_should_return_payload_with_stock_count_zero( # noqa
        self,
        stock_payload,
        request
    ):
        stock_payload = request.getfixturevalue(stock_payload)

        sku = stock_payload['sku']
        seller_id = stock_payload['seller_id']
        navigation_id = stock_payload['navigation_id']

        result = Scope(
            seller_id=seller_id,
            sku=sku,
            navigation_id=navigation_id
        ).get_data()

        if seller_id == constants.MAGAZINE_LUIZA_SELLER_ID:
            navigation_id = convert_id_to_nine_digits(navigation_id)

        assert result == {
            'sku': sku,
            'seller_id': seller_id,
            'stock_count': 0,
            'navigation_id': navigation_id,
            'minimum_order_quantity': 0
        }

    def test_when_stock_not_receive_navigation_id_then_should_discard_message(
        self,
        mock_stock_3p,
        caplog
    ):
        sku = mock_stock_3p['sku']
        seller_id = mock_stock_3p['seller_id']

        result = Scope(
            seller_id=seller_id,
            sku=sku,
        ).get_data()

        assert not result
        assert (
            f'Stock event with sku:{sku} and '
            f'seller_id:{seller_id} without navigation_id'
            in caplog.text
        )
