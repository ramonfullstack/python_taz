import pytest

from taz.consumers.datalake.scopes.price import Scope


class TestPriceScope:

    @pytest.fixture
    def save_price(self, mongo_database, price):
        price['last_updated_at'] = '2016-12-22T17:21:25.866255'
        mongo_database.prices.insert_one(price)

    @pytest.fixture
    def save_currency_price(self, mongo_database, price_with_currency):
        price_with_currency['last_updated_at'] = '2024-06-01T00:21:25.866255'
        mongo_database.prices.insert_one(price_with_currency)

    def test_when_scope_price_process_then_should_return_payload_with_success(
        self,
        save_price,
        price
    ):

        price = Scope(
            sku=price['sku'],
            seller_id=price['seller_id']
        ).get_data()

        assert {
            'sku': price['sku'],
            'seller_id': price['seller_id'],
            'price': price['price'],
            'list_price': price['list_price'],
            'last_updated_at': '2016-12-22T17:21:25.866255'
        } == price

    def test_when_scope_price_should_return_currency_payload_with_success(
        self,
        save_currency_price,
        price_with_currency
    ):
        price = price_with_currency

        get_price_data = Scope(
            sku=price['sku'],
            seller_id=price['seller_id']
        ).get_data()

        assert {
            'sku': price['sku'],
            'seller_id': price['seller_id'],
            'price': price['price'],
            'list_price': price['list_price'],
            'currency': price['currency'],
            'last_updated_at': '2024-06-01T00:21:25.866255'
        } == get_price_data

    def test_when_price_not_found_then_should_log_error_and_return_none(
        self,
        price,
        logger_stream
    ):
        result = Scope(
            sku=price['sku'],
            seller_id=price['seller_id']
        ).get_data()

        assert not result
        assert (
            'Price not found with scope:price sku:{} seller_id:{}'.format(
                price['sku'],
                price['seller_id']
            )
        ) in logger_stream.getvalue()
