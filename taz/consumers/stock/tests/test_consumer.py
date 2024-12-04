import pytest

from taz.consumers.stock.consumer import StockRecordProcessor
from taz.helpers.json import json_loads


class TestStockConsumer:

    @pytest.fixture
    def consumer(self):
        return StockRecordProcessor('stock')

    @pytest.fixture
    def product(self):
        return {
            'sku': '044359000',
            'seller_id': 'magazineluiza',
            'navigation_id': '044359000'
        }

    @pytest.fixture
    def save_product(self, product, mongo_database):
        return mongo_database.raw_products.insert_one(product)

    def test_should_discard_message_for_type_not_is_v1(self, consumer):
        message = {'entity_type': 'murcho'}

        response = consumer.process_message(message)
        assert response is True

    def test_should_save_success(
        self,
        consumer,
        magazineluiza_sku_044359000_cd_300,
        magazineluiza_sku_044359000_cd_350,
        magazineluiza_sku_044359000_store_595,
        magazineluiza_sku_044359000_cd_50,
        mongo_database,
        patch_pubsub_client,
        save_product,
    ):
        mongo_database.prices.insert_one({
            'seller_id': 'magazineluiza',
            'sku': '044359000'
        })

        with patch_pubsub_client as mock_pubsub:
            consumer.process_message(magazineluiza_sku_044359000_store_595)

        assert mock_pubsub.called

        with patch_pubsub_client as mock_pubsub:
            consumer.process_message(magazineluiza_sku_044359000_cd_350)

        assert mock_pubsub.called

        payload = json_loads(mock_pubsub.call_args_list[1][1]['data'].decode())
        del payload['task_id']

        assert payload == {
            'sku': '044359000',
            'seller_id': 'magazineluiza',
            'navigation_id': '044359000',
            'action': 'update',
            'type': 'stock',
            'origin': 'stock',
            'timestamp': 0
        }

        with patch_pubsub_client as mock_pubsub:
            consumer.process_message(magazineluiza_sku_044359000_cd_300)

        assert mock_pubsub.called

        with patch_pubsub_client as mock_pubsub:
            consumer.process_message(magazineluiza_sku_044359000_cd_50)

        assert mock_pubsub.called

        stock_saved = mongo_database.stocks.find_one(
            {
                'seller_id': 'magazineluiza',
                'sku': '044359000',
                'branch_id': 300
            },
            {'_id': 0}
        )

        assert stock_saved['last_updated_at']
        del stock_saved['last_updated_at']

        assert stock_saved == {
            'seller_id': 'magazineluiza',
            'sku': '044359000',
            'branch_id': 300,
            'latitude': -23.131369,
            'longitude': -46.95137,
            'delivery_availability': 'nationwide',
            'position': {
                'physic': {
                    'amount': 33,
                    'reserved': 2,
                    'available': 31
                },
                'logic': {
                    'amount': 0,
                    'reserved': 0,
                    'available': 0
                }
            },
            'type': 'DC',
            'navigation_id': '044359000'
        }

        assert mock_pubsub.called
        assert mock_pubsub.call_args[1]['seller_id'] == 'magazineluiza'

        payload = json_loads(mock_pubsub.call_args_list[0][1]['data'].decode())
        assert payload == {
            'sku': '044359000',
            'seller_id': 'magazineluiza',
            'stock_count': 36,
            'stock_type': 'on_seller',
            'delivery_availability': 'nationwide',
            'stock_details': {
                '350': [{
                    'stock_type': 'on_seller',
                    'quantity': 5
                }],
                '300': [{
                    'stock_type': 'on_seller',
                    'quantity': 31
                }]
            },
            'navigation_id': '044359000'
        }

        price = mongo_database.prices.find_one(
            {},
            {'_id': 0, 'last_updated_at': 0}
        )

        assert price == {
            'seller_id': 'magazineluiza',
            'sku': '044359000',
            'delivery_availability': 'nationwide',
            'stock_type': 'on_seller',
            'stock_count': 1
        }

    def test_should_availability_regional_for_cd_995(
        self,
        consumer,
        magazineluiza_sku_044359000_cd_995,
        mongo_database,
        patch_pubsub_client,
        save_product,
    ):
        with patch_pubsub_client as mock_pubsub:
            consumer.process_message(magazineluiza_sku_044359000_cd_995)

        stock_saved = mongo_database.stocks.find_one(
            {
                'seller_id': 'magazineluiza',
                'sku': '044359000',
                'branch_id': 995
            },
            {'_id': 0}
        )

        del stock_saved['last_updated_at']
        assert stock_saved == {
            'seller_id': 'magazineluiza',
            'sku': '044359000',
            'branch_id': 995,
            'latitude': -23.131369,
            'longitude': -46.95137,
            'delivery_availability': 'regional',
            'position': {
                'physic': {
                    'amount': 6,
                    'reserved': 2,
                    'available': 5
                },
                'logic': {
                    'amount': 0,
                    'reserved': 0,
                    'available': 0
                }
            },
            'type': 'DC',
            'navigation_id': '044359000'
        }

        assert mock_pubsub.called

        payload = json_loads(mock_pubsub.call_args_list[0][1]['data'].decode())
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
        consumer,
        magazineluiza_sku_044359000_store_595,
        magazineluiza_sku_044359000_cd_300,
        mongo_database,
        patch_pubsub_client,
        save_product,
    ):
        with patch_pubsub_client as mock_pubsub:
            consumer.process_message(magazineluiza_sku_044359000_store_595)

        stock_saved = mongo_database.stocks.find_one(
            {
                'seller_id': 'magazineluiza',
                'sku': '044359000',
                'branch_id': 595
            },
            {'_id': 0}
        )

        del stock_saved['last_updated_at']
        assert stock_saved == {
            'seller_id': 'magazineluiza',
            'sku': '044359000',
            'branch_id': 595,
            'latitude': -23.131369,
            'longitude': -46.95137,
            'delivery_availability': 'regional',
            'position': {
                'physic': {
                    'amount': 6,
                    'reserved': 2,
                    'available': 5
                },
                'logic': {
                    'amount': 0,
                    'reserved': 0,
                    'available': 0
                }
            },
            'type': 'STORE',
            'navigation_id': '044359000'
        }

        assert mock_pubsub.called

        payload = json_loads(mock_pubsub.call_args_list[0][1]['data'].decode())
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

    def test_when_product_hasnt_navigation_id_then_should_discard_message(
        self,
        consumer,
        magazineluiza_sku_044359000_cd_300,
        patch_pubsub_client,
        caplog
    ):
        with patch_pubsub_client as mock_pubsub:
            consumer.process_message(magazineluiza_sku_044359000_cd_300)

        mock_pubsub.assert_not_called()
        assert (
            'Product of sku:044359000 seller_id:magazineluiza '
            'without navigation_id' in caplog.text
        )

    def test_should_return_not_pubsub_called_for_other_stock_type(
        self,
        consumer,
        magazineluiza_sku_044359000_other_62,
        mongo_database,
        patch_pubsub_client,
        save_product,
    ):
        with patch_pubsub_client as mock_pubsub:
            consumer.process_message(magazineluiza_sku_044359000_other_62)

        assert not mock_pubsub.called

    def test_should_save_success_but_not_notify_when_stocks_equal(
        self,
        consumer,
        magazineluiza_sku_044359000_cd_300,
        mongo_database,
        patch_pubsub_client,
        save_product
    ):
        mongo_database.prices.insert_one({
            'seller_id': 'magazineluiza',
            'sku': '044359000',
            'stock_count': 1
        })

        with patch_pubsub_client as mock_pubsub:
            consumer.process_message(magazineluiza_sku_044359000_cd_300)

        assert mock_pubsub.called

    def test_should_save_success_notify_when_no_price_in_database(
        self,
        consumer,
        magazineluiza_sku_044359000_cd_300,
        mongo_database,
        patch_pubsub_client,
        save_product
    ):
        with patch_pubsub_client as mock_pubsub:
            consumer.process_message(magazineluiza_sku_044359000_cd_300)

        assert mock_pubsub.called
