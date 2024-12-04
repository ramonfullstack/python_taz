import pytest

from taz.consumers.core.stock import StockHelper


class TestStockHelper:

    @pytest.fixture
    def stock_helper(self):
        return StockHelper()

    @pytest.fixture
    def seller_id(self):
        return 'magazineluiza'

    def _stock_payload(
        self,
        sku,
        seller_id,
        navigation_id,
        stock_count=0,
        branch_id=300,
        delivery_availability='nationwide',
        _type='DC'
    ):
        return {
            'seller_id': seller_id,
            'sku': sku,
            'branch_id': branch_id,
            'latitude': -23.131369,
            'longitude': -46.95137,
            'delivery_availability': delivery_availability,
            'position': {
                'physic': {
                    'amount': stock_count,
                    'reserved': 0,
                    'available': stock_count
                },
                'logic': {
                    'amount': 0,
                    'reserved': 0,
                    'available': 0
                }
            },
            'type': _type,
            'navigation_id': navigation_id
        }

    def test_should_availability_regional_for_cd_995(
        self,
        stock_helper,
        mongo_database,
        seller_id
    ):
        sku = '044359000'
        navigation_id = '044359000'
        stock = self._stock_payload(sku, seller_id, navigation_id, 5, 995, 'regional')  # noqa

        mongo_database.stocks.save(stock)

        payload = stock_helper.mount('044359000', seller_id, '044359000')

        assert payload == {
            'sku': '044359000',
            'seller_id': 'magazineluiza',
            'stock_count': 5,
            'stock_type': 'on_seller',
            'delivery_availability': 'regional',
            'stock_details': {
                '995': [{
                    'stock_type': 'on_seller',
                    'quantity': 5
                }]
            },
            'navigation_id': '044359000'
        }

    def test_should_return_stock_for_store(
        self,
        stock_helper,
        mongo_database,
        seller_id
    ):
        sku = '044359000'
        navigation_id = '044359000'
        stock = self._stock_payload(sku, seller_id, navigation_id, 5, 595, 'regional', 'STORE')  # noqa

        mongo_database.stocks.save(stock)

        payload = stock_helper.mount(
            '044359000',
            seller_id,
            '044359000',
            'STORE',
            595
        )

        assert payload == {
            'sku': '044359000',
            'seller_id': 'magazineluiza',
            'stock_count': 5,
            'stock_type': 'on_seller',
            'delivery_availability': 'regional',
            'stock_details': {
                '595': [{
                    'stock_type': 'on_seller',
                    'quantity': 5
                }]
            },
            'navigation_id': '044359000'
        }
