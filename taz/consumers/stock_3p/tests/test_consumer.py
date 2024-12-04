import threading
from unittest.mock import ANY, patch
from uuid import uuid4

import pytest

from taz.constants import (
    CREATE_ACTION,
    MAGAZINE_LUIZA_SELLER_ID,
    PRODUCT_UNFINISHED_PROCESS_MESSAGE,
    STOCK_SUCCESS_CODE,
    STOCK_SUCCESS_MESSAGE,
    STOCK_UNFINISHED_PROCESS,
    UPDATE_ACTION
)
from taz.consumers.core.notification import Notification
from taz.consumers.stock_3p.consumer import Stock3pRecordProcessor
from taz.helpers.json import json_loads


class TestStock3pRecordProcessor:

    @pytest.fixture
    def record_processor(self):
        return Stock3pRecordProcessor('stock')

    @pytest.fixture
    def prices(self, record_processor):
        return record_processor.get_collection('prices')

    @pytest.fixture
    def stocks(self, record_processor):
        return record_processor.get_collection('stocks')

    @pytest.fixture
    def save_prices(self, record_processor, price_dict):
        prices = record_processor.get_collection('prices')
        prices.insert_one(price_dict)

    @pytest.fixture
    def save_raw_products(self, record_processor):
        raw_products = record_processor.get_collection('raw_products')

        raw_products.insert_many([
            {
                'sku': '012345678',
                'navigation_id': '012345678',
                'seller_id': 'netshoes',
                'disable_on_matching': False
            },
            {
                'sku': '1232323323',
                'navigation_id': '12312311',
                'seller_id': 'murcho',
                'disable_on_matching': False
            }
        ])

    @pytest.fixture
    def price_dict(self):
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

    @pytest.fixture
    def mock_patolino_notification_success(self, price_dict):
        return {
            'sku': price_dict['sku'],
            'seller_id': price_dict['seller_id'],
            'code': STOCK_SUCCESS_CODE,
            'message': STOCK_SUCCESS_MESSAGE,
            'last_updated_at': ANY,
            'payload': {
                'action': 'update',
                'sku': price_dict['sku'],
                'seller_id': price_dict['seller_id']
            },
            'action': 'update'
        }

    @pytest.fixture
    def mock_notification_success(self, price_dict):
        return {
            'sku': price_dict['sku'],
            'seller_id': price_dict['seller_id'],
            'navigation_id': '012345678',
            'action': 'update',
            'type': 'stock',
            'origin': 'stock',
            'task_id': ANY,
            'timestamp': 0
        }

    @pytest.fixture
    def patch_stocks(self):
        return patch.object(Stock3pRecordProcessor, 'stocks')

    @pytest.fixture
    def patch_notification_put(self):
        return patch.object(Notification, 'put')

    def test_when_product_stock_doesnt_exist_then_should_create_stock_with_success(  # noqa
        self,
        record_processor,
        prices,
        stocks,
        price_dict,
        save_raw_products,
        patch_patolino_product_post,
        patch_pubsub_client,
        mock_patolino_notification_success,
        mock_notification_success
    ):
        mock_patolino_notification_success['payload']['action'] = 'create'
        mock_notification_success['action'] = 'create'

        with patch_pubsub_client as mock_pubsub:
            with patch_patolino_product_post as mock_patolino:
                record_processor.process_message(price_dict)

        assert stocks.count_documents({}) == 1
        assert prices.count_documents({}) == 1
        assert prices.find_one({}, {'source': 1, '_id': 0}) == {
            'source': 'stock'
        }

        pubsub_data = json_loads(mock_pubsub.call_args.kwargs['data'].decode())

        assert mock_notification_success == pubsub_data
        assert mock_patolino_notification_success == mock_patolino.call_args[0][0]  # noqa

    def test_when_product_stock_exists_then_should_update_with_success(
        self,
        record_processor,
        prices,
        price_dict,
        save_raw_products,
        save_prices,
        patch_patolino_product_post,
        patch_pubsub_client,
        mock_patolino_notification_success,
        mock_notification_success
    ):

        price_dict['stock_count'] = 100

        with patch_pubsub_client as mock_pubsub:
            with patch_patolino_product_post as mock_patolino:
                record_processor.process_message(price_dict)

        price_updated = prices.find_one(
            {
                'sku': price_dict['sku'],
                'seller_id': price_dict['seller_id']
            }
        )

        assert price_updated['stock_count'] == 100
        assert mock_pubsub.called
        assert mock_patolino_notification_success == mock_patolino.call_args[0][0]  # noqa]

        data = json_loads(mock_pubsub.call_args.kwargs['data'].decode())
        assert mock_notification_success == data

    def test_when_update_stock_but_payload_not_change_then_should_skip_process(
        self,
        record_processor,
        prices,
        price_dict,
        logger_stream,
        save_raw_products,
        patch_pubsub_client,
        patch_patolino_product_post,
        mock_patolino_notification_success
    ):
        sku = price_dict['sku']
        seller_id = price_dict['seller_id']

        mock_patolino_notification_success['code'] = (
            STOCK_UNFINISHED_PROCESS
        )

        mock_patolino_notification_success['message'] = (
            PRODUCT_UNFINISHED_PROCESS_MESSAGE.format(
                sku=sku,
                seller_id=seller_id,
                reason='Values did not change'
            )
        )

        mock_patolino_notification_success['payload'] = {
            'navigation_id': None,
            'action': 'update'
        }

        with patch_pubsub_client:
            with patch_patolino_product_post:
                record_processor.process_message(price_dict)

        assert prices.count_documents({}) == 1

        with patch_pubsub_client as mock_pubsub:
            with patch_patolino_product_post as mock_patolino:
                record_processor.process_message(price_dict)

        log = logger_stream.getvalue()

        assert (
            'Skip stock 3p update for sku:{} seller_id:{}'.format(
                sku,
                seller_id
            ) in log
        )
        assert mock_patolino_notification_success == mock_patolino.call_args[0][0]  # noqa
        assert not mock_pubsub.called

    @pytest.mark.parametrize('action', [
        'create',
        'update'
    ])
    def test_record_processor_price_should_send_tracking_id(
        self,
        record_processor,
        price_dict,
        mongo_database,
        save_raw_products,
        patch_pubsub_client,
        patch_patolino_product_post,
        action
    ):
        if action == 'update':
            record_processor.get_collection('prices').insert_one(
                price_dict
            )

        price_dict['price'] = 1000
        price_dict['list_price'] = 900

        tracking_id = str(uuid4())
        price_dict['tracking_id'] = tracking_id

        with patch_patolino_product_post:
            with patch_pubsub_client as mock_pubsub:
                record_processor.process_message(price_dict)

        data = json_loads(mock_pubsub.call_args_list[0][1]['data'].decode())
        assert data['tracking_id'] == tracking_id

    def test_when_seller_id_is_magazineluiza_then_should_skip_process(
        self,
        record_processor,
        patch_pubsub_client,
        patch_patolino_product_post,
        price_dict
    ):
        price_dict['seller_id'] = MAGAZINE_LUIZA_SELLER_ID

        with patch_pubsub_client as mock_pubsub:
            with patch_patolino_product_post as mock_patolino:
                record_processor.process_message(price_dict)

        assert not mock_pubsub.called
        assert not mock_patolino.called

    def test_when_payload_doesnt_have_stock_count_field_then_should_skip_process(  # noqa
        self,
        record_processor,
        patch_pubsub_client,
        patch_patolino_product_post,
        price_dict,
        logger_stream
    ):
        del price_dict['stock_count']

        with patch_pubsub_client as mock_pubsub:
            with patch_patolino_product_post as mock_patolino:
                record_processor.process_message(price_dict)

        assert not mock_pubsub.called
        assert not mock_patolino.called
        assert 'Discarding stock for sku:{} seller_id:{}'.format(
            price_dict['sku'],
            price_dict['seller_id']
        ) in logger_stream.getvalue()

    def test_when_save_but_product_doest_have_navigation_id_then_not_send_notification(  # noqa
        self,
        record_processor,
        patch_pubsub_client,
        patch_patolino_product_post,
        price_dict,
        logger_stream,
        patch_stocks,
        stocks,
        prices,
        mock_patolino_notification_success
    ):
        mock_patolino_notification_success['payload']['action'] = 'create'

        with patch_pubsub_client as mock_pubsub:
            with patch_patolino_product_post as mock_patolino:
                record_processor.process_message(price_dict)

        sku = price_dict['sku']
        seller_id = price_dict['seller_id']
        log = logger_stream.getvalue()

        assert (
            f'Product not found from notification with sku:{sku} '
            f'seller_id:{seller_id} and scope:stock'
        ) in log

        mock_pubsub.assert_not_called()
        assert stocks.count_documents({}) == 1
        assert prices.count_documents({}) == 1
        assert mock_patolino_notification_success == mock_patolino.call_args[0][0]  # noqa

    def test_when_receive_many_messages_at_the_same_time_with_same_sku_and_seller_id_then_should_throw_exception_lock_active_error(  # noqa
        self,
        record_processor,
        price_dict,
        save_raw_products,
        patch_patolino_product_post,
        patch_pubsub_client,
        caplog
    ):
        exception_threads = []

        def custom_except_hook(args):
            exception_threads.append({
                'type': args.exc_type,
                'value': args.exc_value
            })

        threading.excepthook = custom_except_hook

        price_dict.update({'tracking_id': '123'})

        threads = []
        for _ in range(5):
            threads.append(
                threading.Thread(
                    target=record_processor.process_message,
                    args=[price_dict]
                )
            )

        with patch_pubsub_client:
            with patch_patolino_product_post:
                for thread in threads:
                    thread.start()

                for thread in threads:
                    thread.join()

        assert len(exception_threads) > 0
        assert 'LockActiveError' in str(exception_threads[0]['type'])
        assert str(exception_threads[0]['value']) == 'For key prices-012345678-netshoes' # noqa

    @pytest.mark.parametrize(
        'action', [
            CREATE_ACTION,
            UPDATE_ACTION
        ]
    )
    def test_when_receive_navigation_id_on_message_then_should_not_search_on_db_and_send_notification(  # noqa
        self,
        record_processor,
        prices,
        stocks,
        price_dict,
        patch_patolino_product_post,
        patch_notification_put,
        patch_pubsub_client,
        mock_patolino_notification_success,
        mock_notification_success,
        action,
        mongo_database
    ):
        if action == UPDATE_ACTION:
            mongo_database.prices.insert_one(price_dict)
            price_dict['stock_count'] = 10

        mock_patolino_notification_success['payload']['action'] = action
        mock_notification_success['action'] = action

        navigation_id = {'navigation_id': '999999999'}

        price_dict.update(navigation_id)
        mock_notification_success.update(navigation_id)

        with patch_pubsub_client, patch_patolino_product_post:
            with patch_notification_put as mock_notification:
                record_processor.process_message(price_dict)

        assert stocks.count_documents({}) == 1
        assert prices.count_documents({}) == 1
        assert prices.find_one({}, {'source': 1, '_id': 0}) == {
            'source': 'stock'
        }

        mock_notification.assert_called_once_with(
            data={
                'sku': price_dict['sku'],
                'seller_id': price_dict['seller_id'],
                'tracking_id': None,
                **navigation_id
            },
            scope='stock',
            action=action
        )

    @pytest.mark.parametrize(
        'action', [
            CREATE_ACTION,
            UPDATE_ACTION
        ]
    )
    def test_when_navigation_id_on_message_is_empty_then_should_find_value_db_and_send_notification(  # noqa
        self,
        record_processor,
        prices,
        stocks,
        price_dict,
        patch_patolino_product_post,
        patch_notification_put,
        patch_pubsub_client,
        mock_patolino_notification_success,
        mock_notification_success,
        action,
        mongo_database,
        save_raw_products
    ):
        if action == UPDATE_ACTION:
            mongo_database.prices.insert_one(price_dict)
            price_dict['stock_count'] = 10

        mock_patolino_notification_success['payload']['action'] = action
        mock_notification_success['action'] = action

        with patch_pubsub_client, patch_patolino_product_post:
            with patch_notification_put as mock_notification:
                record_processor.process_message(price_dict)

        assert stocks.count_documents({}) == 1
        assert prices.count_documents({}) == 1
        assert prices.find_one({}, {'source': 1, '_id': 0}) == {
            'source': 'stock'
        }

        mock_notification.assert_called_once_with(
            data={
                'sku': price_dict['sku'],
                'seller_id': price_dict['seller_id'],
                'tracking_id': None,
                'navigation_id': '012345678'
            },
            scope='stock',
            action=action
        )

    def test_when_navigation_id_is_none_then_should_not_send_event_with_field_on_payload( # noqa
        self,
        record_processor,
        patch_notification_put
    ):
        sku = '123456789'
        tracking_id = '123'

        with patch_notification_put as mock_notification:
            record_processor._catalog_notification(
                action=CREATE_ACTION,
                sku=sku,
                seller_id=MAGAZINE_LUIZA_SELLER_ID,
                tracking_id=tracking_id
            )

        mock_notification.assert_called_once_with(
            data={
                'sku': sku,
                'seller_id': MAGAZINE_LUIZA_SELLER_ID,
                'tracking_id': tracking_id
            },
            scope='stock',
            action=CREATE_ACTION
        )
