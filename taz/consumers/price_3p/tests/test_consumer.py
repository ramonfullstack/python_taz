import threading
from unittest import mock
from unittest.mock import ANY, patch

import pytest
from simple_settings.utils import settings_stub

import taz.constants as constants
from taz.constants import CREATE_ACTION, UPDATE_ACTION
from taz.consumers.core.notification import Notification
from taz.consumers.price_3p.consumer import Price3pRecordProcessor
from taz.core.price_lock.models import PriceLockModel
from taz.helpers.json import json_loads


class TestPrice3pRecordProcessor:

    @pytest.fixture
    def record_processor(self):
        return Price3pRecordProcessor('price')

    @pytest.fixture
    def mock_price_payload(self):
        return {
            'sku': '0123456789',
            'seller_id': 'luizalabs',
            'list_price': 234.56,
            'price': 123.45,
            'tracking_id': 'bbf11b38-bb18-4555-baa1-2f2616098bc4',
        }

    @pytest.fixture
    def mock_patolino_payload_success(self, mock_price_payload):
        return {
            'sku': mock_price_payload['sku'],
            'seller_id': mock_price_payload['seller_id'],
            'code': constants.PRICE_SUCCESS_CODE,
            'message': constants.PRICE_SUCCESS_MESSAGE,
            'payload': {
                'action': 'create',
                'sku': mock_price_payload['sku'],
                'seller_id': mock_price_payload['seller_id']
            },
            'tracking_id': mock_price_payload['tracking_id'],
            'action': 'update',
            'last_updated_at': ANY,
        }

    @pytest.fixture
    def mock_payload_notification(self, mock_price_payload):
        return {
            'sku': mock_price_payload['sku'],
            'seller_id': mock_price_payload['seller_id'],
            'navigation_id': 'hag92ahjca',
            'action': 'create',
            'type': 'price',
            'origin': 'price',
            'task_id': ANY,
            'tracking_id': mock_price_payload['tracking_id'],
            'timestamp': 0
        }

    @pytest.fixture
    def prices(self, record_processor):
        return record_processor.get_collection('prices')

    @pytest.fixture
    def stocks(self, record_processor):
        return record_processor.get_collection('stocks')

    @pytest.fixture
    def save_raw_products(self, record_processor, mock_price_payload):
        raw_products = record_processor.get_collection('raw_products')
        raw_products.insert_one({
            'sku': mock_price_payload['sku'],
            'navigation_id': 'hag92ahjca',
            'seller_id': mock_price_payload['seller_id'],
            'disable_on_matching': False
        })
        return raw_products

    @pytest.fixture
    def patch_save_price(self):
        return mock.patch.object(Price3pRecordProcessor, '_save')

    @pytest.fixture
    def patch_price_lock(self):
        return patch.object(Price3pRecordProcessor, 'price_lock')

    @pytest.fixture
    def patch_prices(self):
        return patch.object(Price3pRecordProcessor, 'prices')

    @pytest.fixture
    def patch_notification_put(self):
        return patch.object(Notification, 'put')

    def test_when_price_not_exists_then_should_create_price_with_success(
        self,
        record_processor,
        prices,
        mock_price_payload,
        patch_pubsub_client,
        save_raw_products,
        patch_patolino_product_post,
        mock_patolino_payload_success,
        mock_payload_notification
    ):
        with patch_pubsub_client as mock_pubsub:
            with patch_patolino_product_post as mock_patolino:
                record_processor.process_message(mock_price_payload)

        price_db = prices.find_one(
            {}, {'_id': 0, 'md5': 0, 'last_updated_at': 0}
        )

        mock_price_payload['source'] = 'price'
        data = json_loads(mock_pubsub.call_args_list[0][1]['data'].decode())

        assert prices.count_documents({}) == 1
        assert price_db == mock_price_payload
        assert mock_pubsub.called
        assert data == mock_payload_notification
        assert mock_patolino.call_args[0][0] == mock_patolino_payload_success

    def test_when_price_already_exists_then_should_update_price_with_success(
        self,
        record_processor,
        prices,
        mock_price_payload,
        patch_pubsub_client,
        save_raw_products,
        patch_patolino_product_post,
        mock_patolino_payload_success,
        mock_payload_notification
    ):
        prices.insert_one(mock_price_payload)
        del mock_price_payload['_id']

        mock_price_payload['price'] = 500
        mock_price_payload['list_price'] = 499

        with patch_pubsub_client as mock_pubsub:
            with patch_patolino_product_post as mock_patolino:
                record_processor.process_message(mock_price_payload)

        price_db = prices.find_one(
            {}, {'_id': 0, 'md5': 0, 'last_updated_at': 0}
        )

        mock_patolino_payload_success['payload']['action'] = constants.UPDATE_ACTION # noqa
        mock_payload_notification['action'] = constants.UPDATE_ACTION

        mock_price_payload['source'] = 'price'
        data = json_loads(mock_pubsub.call_args_list[0][1]['data'].decode())

        assert prices.count_documents({}) == 1
        assert price_db == mock_price_payload
        assert mock_pubsub.called
        assert data == mock_payload_notification
        assert mock_patolino.call_args[0][0] == mock_patolino_payload_success

    def test_when_price_is_lower_than_value_accept_then_should_block_product(
        self,
        record_processor,
        prices,
        mock_price_payload,
        save_raw_products,
        patch_pubsub_client,
        patch_patolino_product_post
    ):
        prices.insert_one(mock_price_payload)
        del mock_price_payload['_id']

        PriceLockModel(seller_id='luizalabs', percent=70.00).save()
        mock_price_payload['price'] = mock_price_payload['price'] * .69

        with patch_pubsub_client as mock_pubsub:
            with patch_patolino_product_post as mock_patolino:
                record_processor.process_message(mock_price_payload)

        sku = mock_price_payload['sku']
        seller_id = mock_price_payload['seller_id']

        raw_product = save_raw_products.find_one(
            {
                'sku': sku,
                'seller_id': seller_id
            },
            {
                'disable_on_matching': 1,
                '_id': 0
            }
        )

        assert raw_product['disable_on_matching'] is True
        assert mock_pubsub.called
        assert mock_patolino.call_args[0][0] == {
            'action': constants.UPDATE_ACTION,
            'code': constants.PRICE_ERROR_CODE,
            'last_updated_at': ANY,
            'message': 'Blocking product because lowest price accepted violated price ' # noqa
            f'update for sku:{sku} seller_id:{seller_id} current_price: 123.45'
            ' new price:85.1805 max_percent:0.7 lowest price '
            'accepted:86.41499999999999',
            'payload': {
                'action': constants.UPDATE_ACTION,
                'navigation_id': None
            },
            'seller_id': seller_id,
            'sku': sku
        }

    @settings_stub(ENABLE_PRICE_LOCK_PERCENT=False)
    def test_when_price_lock_percent_disabled_then_should_not_process_block_product( # noqa
        self,
        record_processor,
        prices,
        mock_price_payload,
        save_raw_products,
        patch_pubsub_client,
        patch_patolino_product_post,
        patch_price_lock,
        mock_payload_notification,
        mock_patolino_payload_success
    ):
        prices.insert_one(mock_price_payload)
        del mock_price_payload['_id']

        mock_price_payload['price'] = mock_price_payload['price'] * .69
        with patch_pubsub_client as mock_pubsub:
            with patch_patolino_product_post as mock_patolino:
                with patch_price_lock as mock_price_lock:
                    record_processor.process_message(mock_price_payload)

        mock_patolino_payload_success['payload']['action'] = constants.UPDATE_ACTION  # noqa
        mock_payload_notification['action'] = constants.UPDATE_ACTION
        data = json_loads(mock_pubsub.call_args_list[0][1]['data'].decode())

        assert data == mock_payload_notification
        assert mock_patolino.call_args[0][0] == mock_patolino_payload_success
        mock_price_lock.assert_not_called()

    def test_should_block_product_using_50_percent_if_dont_have_config(
        self,
        record_processor,
        prices,
        mock_price_payload,
        save_raw_products,
        patch_pubsub_client,
        patch_patolino_product_post
    ):
        prices.insert_one(mock_price_payload)
        del mock_price_payload['_id']

        mock_price_payload['price'] = mock_price_payload['price'] * .49
        with patch_pubsub_client as mock_pubsub:
            with patch_patolino_product_post as mock_patolino:
                record_processor.process_message(mock_price_payload)

        raw_product = save_raw_products.find_one({
            'sku': mock_price_payload['sku'],
            'seller_id': mock_price_payload['seller_id']
        })

        assert raw_product['disable_on_matching'] is True
        assert mock_pubsub.called
        assert mock_patolino.called

    def test_when_update_price_already_exists_with_same_info_then_should_skip_process( # noqa
        self,
        record_processor,
        prices,
        mock_price_payload,
        logger_stream,
        save_raw_products,
        patch_pubsub_client,
        patch_patolino_product_post
    ):
        with patch_pubsub_client as mock_pubsub:
            with patch_patolino_product_post as mock_patolino:
                record_processor.process_message(mock_price_payload)

        assert prices.count_documents({}) == 1
        assert mock_pubsub.called
        assert mock_patolino.called

        with patch_pubsub_client as mock_pubsub:
            with patch_patolino_product_post as mock_patolino:
                record_processor.process_message(mock_price_payload)

        log = logger_stream.getvalue()
        sku = mock_price_payload['sku']
        seller_id = mock_price_payload['seller_id']

        assert f'Skip price update for sku:{sku} seller_id:{seller_id}' in log
        mock_pubsub.assert_not_called()

    def test_when_update_price_then_should_update_md5_value(
        self,
        record_processor,
        prices,
        mock_price_payload,
        save_raw_products,
        patch_pubsub_client,
        patch_patolino_product_post
    ):
        with patch_pubsub_client as mock_pubsub:
            with patch_patolino_product_post as mock_patolino:
                record_processor.process_message(mock_price_payload)

        product_created = prices.find_one()
        mock_pubsub.assert_called_once()
        mock_patolino.assert_called_once()

        mock_price_payload['price'] = 898

        with patch_pubsub_client as mock_pubsub:
            with patch_patolino_product_post as mock_patolino:
                record_processor.process_message(mock_price_payload)

        product_updated = prices.find_one()

        assert product_created['md5'] != product_updated['md5']
        mock_pubsub.assert_called_once()
        mock_patolino.assert_called_once()

    @pytest.mark.parametrize(
        'price, new_price, expected', [
            (
                {
                    'sku': '012345678',
                    'seller_id': 'magazineluiza',
                    'list_price': 89.90,
                    'price': 79.90
                },
                {
                    'sku': '012345678',
                    'seller_id': 'magazineluiza',
                    'list_price': 99.90,
                    'price': 99.90
                },
                {
                    'sku': '012345678',
                    'seller_id': 'magazineluiza',
                    'list_price': 99.90,
                    'price': 99.90
                }
            ),
            (
                {
                    'sku': '012345678',
                    'seller_id': 'magazineluiza',
                    'list_price': 89.90,
                    'price': 79.90
                },
                {
                    'sku': '012345678',
                    'seller_id': 'magazineluiza',
                    'list_price': 89.90,
                    'price': 90.90
                },
                {
                    'sku': '012345678',
                    'seller_id': 'magazineluiza',
                    'list_price': 89.90,
                    'price': 90.90
                }
            ),
        ]
    )
    def test_merge_prices(
        self,
        record_processor,
        price,
        new_price,
        expected
    ):
        response = record_processor._merge(price, new_price)

        assert response['list_price'] == expected['list_price']
        assert response['price'] == expected['price']
        assert response['sku'] == expected['sku']
        assert response['seller_id'] == expected['seller_id']

    def test_when_price_has_payload_without_price_info_then_should_ignore_message( # noqa
        self,
        record_processor,
        prices,
        mock_price_payload,
        logger_stream,
        patch_pubsub_client,
        patch_patolino_product_post
    ):
        sku = mock_price_payload['sku']
        seller_id = mock_price_payload['seller_id']

        payload = {
            'sku': sku,
            'seller_id': seller_id
        }
        with patch_pubsub_client as mock_pubsub:
            with patch_patolino_product_post as mock_patolino:
                record_processor.process_message(payload)

        assert prices.count_documents({}) == 0
        assert (
            f'Discarding price for sku:{sku} seller_id:{seller_id} because '
            'price is NULL' in logger_stream.getvalue()
        )

        mock_pubsub.assert_not_called()
        mock_patolino.assert_not_called()

    @pytest.mark.parametrize('price,list_price', [
        ('', 10),
        (10, ''),
        (0, 10),
        (10, 0),
        (None, 10),
        (10, None)
    ])
    def test_when_price_has_empty_value_or_less_then_zero_then_should_ignore_message( # noqa
        self,
        record_processor,
        mock_price_payload,
        logger_stream,
        price,
        list_price,
        patch_pubsub_client,
        patch_patolino_product_post
    ):
        mock_price_payload['price'] = price
        mock_price_payload['list_price'] = list_price

        with patch_pubsub_client as mock_pubsub:
            with patch_patolino_product_post as mock_patolino:
                record_processor.process_message(mock_price_payload)

        sku = mock_price_payload['sku']
        seller_id = mock_price_payload['seller_id']

        mock_pubsub.assert_not_called()
        mock_patolino.assert_not_called()
        assert (
            f'Discarding price for sku:{sku} seller_id:{seller_id} '
            f'because is a invalid price. payload:{mock_price_payload}'
        ) in logger_stream.getvalue()

    @pytest.mark.parametrize('processor_method', ['update', 'create'])
    def test_when_price_payload_has_tracking_id_field_then_should_add_value_notification( # noqa
        self,
        record_processor,
        mock_price_payload,
        mongo_database,
        save_raw_products,
        processor_method,
        patch_pubsub_client,
        patch_patolino_product_post
    ):
        if processor_method != 'create':
            mongo_database.prices.insert_one(mock_price_payload)
            del mock_price_payload['_id']
            mock_price_payload['price'] = 555.00
            mock_price_payload['list_price'] = 444.00

        with patch_patolino_product_post:
            with patch_pubsub_client as mock_pubsub:
                record_processor.process_message(mock_price_payload)

        tracking_id = mock_price_payload['tracking_id']
        data = json_loads(mock_pubsub.call_args_list[0][1]['data'].decode())

        assert data['tracking_id'] == tracking_id

    def test_when_create_price_happen_exception_then_should_send_notification_error( # noqa
        self,
        record_processor,
        mock_price_payload,
        save_raw_products,
        mongo_database,
        patch_pubsub_client,
        patch_patolino_product_post,
        patch_prices
    ):

        with patch_pubsub_client:
            with patch_patolino_product_post as patolino_mock:
                with patch_prices as mock_prices:
                    mock_prices.find_one.return_value = {}
                    mock_prices.update_many.side_effect = Exception
                    with pytest.raises(Exception):
                        record_processor.process_message(mock_price_payload)

        assert patolino_mock.call_args[0][0] == {
            'sku': mock_price_payload['sku'],
            'seller_id': mock_price_payload['seller_id'],
            'code': constants.PRICE_ERROR_CODE,
            'message': constants.PRICE_ERROR_MESSAGE,
            'action': constants.UPDATE_ACTION,
            'last_updated_at': ANY,
            'payload': {
                'action': constants.CREATE_ACTION,
                'sku': mock_price_payload['sku'],
                'seller_id': mock_price_payload['seller_id']
            },
            'tracking_id': mock_price_payload['tracking_id']
        }

    def test_when_update_price_happen_exception_then_should_send_notification_error( # noqa
        self,
        record_processor,
        mock_price_payload,
        save_raw_products,
        mongo_database,
        patch_pubsub_client,
        patch_patolino_product_post,
        patch_prices
    ):
        mongo_database.prices.insert_one(mock_price_payload)
        mock_price_payload['price'] = 1000.00
        mock_price_payload['list_price'] = 900.00

        with patch_pubsub_client:
            with patch_patolino_product_post as patolino_mock:
                with patch_prices as mock_prices:
                    mock_prices.update_many.side_effect = Exception
                    with pytest.raises(Exception):
                        record_processor.process_message(mock_price_payload)

        assert patolino_mock.call_args[0][0] == {
            'sku': mock_price_payload['sku'],
            'seller_id': mock_price_payload['seller_id'],
            'code': constants.PRICE_ERROR_CODE,
            'message': constants.PRICE_ERROR_MESSAGE,
            'action': constants.UPDATE_ACTION,
            'last_updated_at': ANY,
            'payload': {
                'action': constants.UPDATE_ACTION,
                'sku': mock_price_payload['sku'],
                'seller_id': mock_price_payload['seller_id']
            },
            'tracking_id': mock_price_payload['tracking_id']
        }

    @pytest.mark.parametrize(
        'prices, dimensions, should_log', [
            (
                {
                    'list_price': 0.06,
                    'price': 0.06,
                },
                {
                    'width': 0.11,
                    'depth': 0.16,
                    'weight': 0.1,
                    'height': 0.02
                },
                False
            ),
            (
                {
                    'list_price': 0.06,
                    'price': 0.06,
                },
                {
                    'width': 0.11,
                    'depth': 0.16,
                    'weight': 0.1,
                    'height': 0.02
                },
                False
            ),
            (
                {
                    'list_price': 0.05,
                    'price': 0.05,
                },
                {
                    'width': 0.3,
                    'depth': 0.2,
                    'weight': 0.3,
                    'height': 0.3
                },
                True
            ),
            (
                {
                    'list_price': 0.05,
                    'price': 0.05,
                },
                {
                    'width': 0.3,
                    'depth': 0.2,
                    'weight': 0.3,
                    'height': 0.3
                },
                True
            ),
            (
                {
                    'list_price': 0.05,
                    'price': 0.06,
                },
                {
                    'width': 0.3,
                    'depth': 0.2,
                    'weight': 0.3,
                    'height': 0.3
                },
                False
            ),
            (
                {
                    'list_price': 0.05,
                    'price': 0.04,
                },
                {
                    'width': 0.1,
                    'depth': 0.1,
                    'weight': 0.3,
                    'height': 0.1
                },
                False
            ),
        ]
    )
    def test_processor_wrong_price_vs_cubage_log(
        self,
        record_processor,
        mongo_database,
        mock_price_payload,
        patch_pubsub_client,
        patch_patolino_product_post,
        prices,
        dimensions,
        should_log,
        logger_stream
    ):
        sku = mock_price_payload['sku']
        seller_id = mock_price_payload['seller_id']

        price_dict = {
            'sku': sku,
            'seller_id': seller_id,
            'list_price': prices['list_price'],
            'price': prices['price']
        }

        mongo_database.raw_products.insert_one({
            'sku': sku,
            'navigation_id': sku,
            'seller_id': seller_id,
            'disable_on_matching': False,
            'dimensions': dimensions
        })

        with patch_pubsub_client:
            with patch_patolino_product_post:
                record_processor.process_message(price_dict)

        log = logger_stream.getvalue()

        if should_log:
            assert 'Wrong Price X Cubage' in log
        else:
            assert 'Wrong Price X Cubage' not in log

    def test_when_receive_many_messages_at_the_same_time_with_same_sku_and_seller_id_then_should_throw_exception_lock_active_error( # noqa
        self,
        record_processor,
        mock_price_payload,
        patch_pubsub_client,
        save_raw_products,
        patch_patolino_product_post,
        caplog
    ):
        exception_threads = []

        def custom_except_hook(args):
            exception_threads.append({
                'type': args.exc_type,
                'value': args.exc_value
            })

        threading.excepthook = custom_except_hook

        threads = []
        for _ in range(5):
            threads.append(
                threading.Thread(
                    target=record_processor.process_message,
                    args=[mock_price_payload]
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
        assert str(exception_threads[0]['value']) == 'For key prices-0123456789-luizalabs'  # noqa

    @pytest.mark.parametrize(
        'action', [
            CREATE_ACTION,
            UPDATE_ACTION
        ]
    )
    def test_when_receive_navigation_id_on_message_then_should_notify(
        self,
        record_processor,
        prices,
        mock_price_payload,
        patch_notification_put,
        patch_pubsub_client,
        save_raw_products,
        patch_patolino_product_post,
        action,
        mongo_database
    ):
        if action == UPDATE_ACTION:
            mongo_database.prices.insert_one(mock_price_payload)
            del mock_price_payload['_id']
            mock_price_payload['list_price'] = 1000

        navigation_id = {'navigation_id': '999999999'}
        mock_price_payload.update(navigation_id)

        with patch_pubsub_client, patch_patolino_product_post:
            with patch_notification_put as mock_notification:
                record_processor.process_message(mock_price_payload)

        price_db = prices.find_one(
            {}, {'_id': 0, 'md5': 0, 'last_updated_at': 0}
        )

        mock_price_payload['source'] = 'price'
        assert prices.count_documents({}) == 1
        assert price_db == mock_price_payload
        mock_notification.assert_called_once_with(
            data={
                'sku': mock_price_payload['sku'],
                'seller_id': mock_price_payload['seller_id'],
                'tracking_id': mock_price_payload['tracking_id'],
                **navigation_id
            },
            scope='price',
            action=action
        )

    def test_when_navigation_id_is_none_then_should_not_send_event_with_field_on_payload( # noqa
        self,
        record_processor,
        patch_notification_put
    ):
        sku = '123456789'
        seller_id = 'netshoes'
        tracking_id = '123'

        with patch_notification_put as mock_notification:
            record_processor._catalog_notification(
                action=CREATE_ACTION,
                sku=sku,
                seller_id=seller_id,
                tracking_id=tracking_id
            )

        mock_notification.assert_called_once_with(
            data={
                'sku': sku,
                'seller_id': seller_id,
                'tracking_id': tracking_id
            },
            scope='price',
            action=CREATE_ACTION
        )
