from unittest.mock import ANY

import pytest

from taz.consumers.pricing.consumer import PricingRecordProcessor
from taz.helpers.json import json_loads


class TestPricingConsumer:

    @pytest.fixture
    def consumer(self):
        return PricingRecordProcessor('pricing')

    @pytest.fixture
    def save_prices(self, consumer, mongo_database):
        mongo_database.prices.insert_one({
            'last_updated_at': '2016-12-22T17:21:25.866255',
            'stock_count': 25,
            'delivery_availability': 'nationwide',
            'sku': '223313100',
            'seller_id': 'magazineluiza',
            'list_price': 100,
            'stock_type': 'on_seller',
            'price': 100
        })

    @pytest.fixture
    def save_raw_products(self, consumer):
        raw_products = consumer.get_collection('raw_products')
        raw_products.insert_one({
            'sku': '223313100',
            'navigation_id': '223313100',
            'seller_id': 'magazineluiza',
            'disable_on_matching': False
        })

        return raw_products

    @pytest.fixture
    def message(self):
        return {
            'schema': 'pricing_update',
            'data': {
                'sku': '223313100',
                'seller_id': 'magazineluiza',
                'campaign_code': '0',
                'channel_id': '*',
                'base_price': 200,
                'price': 200,
                'action': 'update',
                'origin': 'adm-site',
                'campaign_id': '',
                'campaign_name': '',
                'username': '',
                'modified_at': 1592857403
            }
        }

    def test_should_process_message_and_update_price(
        self,
        message,
        consumer,
        save_prices,
        save_raw_products,
        patch_pubsub_client,
        mongo_database
    ):
        before_update = mongo_database.prices.find_one(
            {'seller_id': 'magazineluiza', 'sku': '223313100'}
        )
        old_price = before_update['price']

        with patch_pubsub_client as mock_pubsub:
            consumer.process_message(message)

        after_update = mongo_database.prices.find_one(
            {'seller_id': 'magazineluiza', 'sku': '223313100'}
        )
        new_price = after_update['price']
        data = json_loads(mock_pubsub.call_args_list[0][1]['data'].decode())

        assert new_price != old_price
        assert after_update['md5']
        assert after_update['source'] == 'pricing'
        assert mock_pubsub.called
        assert data == {
            'sku': '223313100',
            'seller_id': 'magazineluiza',
            'navigation_id': '223313100',
            'action': 'update',
            'type': 'price',
            'origin': 'price',
            'task_id': ANY,
            'timestamp': 0
        }

    def test_should_process_message_and_create_price(
        self,
        message,
        consumer,
        save_raw_products,
        patch_pubsub_client,
        mongo_database
    ):
        with patch_pubsub_client as mock_pubsub:
            consumer.process_message(message)

        price_loaded = mongo_database.prices.find_one(
            {'sku': '223313100', 'seller_id': 'magazineluiza'},
            {'_id': 0, 'last_updated_at': 0}
        )

        assert price_loaded == {
            'list_price': 200,
            'md5': 'a334b793262caac12c06c3fd4a1eec5a',
            'price': 200,
            'seller_id': 'magazineluiza',
            'sku': '223313100',
            'source': 'pricing'
        }

        assert mock_pubsub.called

    def test_should_discard_message_because_seller_is_not_magazineluiza(
        self,
        message,
        consumer,
        patch_pubsub_client,
    ):
        message['data']['seller_id'] = 'qualquer'

        with patch_pubsub_client as mock_pubsub:
            consumer.process_message(message)

        assert not mock_pubsub.called

    def test_should_discard_message_because_campaign_code_is_not_zero(
        self,
        message,
        consumer,
        patch_pubsub_client,
    ):
        message['data']['campaign_code'] = '1234'

        with patch_pubsub_client as mock_pubsub:
            consumer.process_message(message)

        assert not mock_pubsub.called

    def test_should_discard_message_because_channel_id_is_not_asterisk(
        self,
        message,
        consumer,
        patch_pubsub_client,
    ):
        message['data']['channel_id'] = '99'

        with patch_pubsub_client as mock_pubsub:
            consumer.process_message(message)

        assert not mock_pubsub.called
