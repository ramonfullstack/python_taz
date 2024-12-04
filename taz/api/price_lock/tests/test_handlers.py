import json
from unittest.mock import patch

import pytest

from taz.api.price_lock.handlers import PriceLockHandler
from taz.core.price_lock.models import PriceLockModel


@pytest.fixture
def price_lock_json():
    return {
        'seller_id': 'whirpool',
        'percent': 30,
        'user': 'foo@luizalabs.com'
    }


@pytest.fixture
def save_price_lock(price_lock_json):
    PriceLockModel(**price_lock_json).save()


@pytest.fixture
def mock_url():
    return '/price_lock'


class TestPriceLockHandler:

    def test_post_price_lock_should_save(
        self, client, price_lock_json, mock_url
    ):
        response = client.post(
            mock_url, body=json.dumps(price_lock_json)

        )
        assert response.status_code == 200

        price_lock = (
            PriceLockModel.objects.get(seller_id=price_lock_json['seller_id'])
        )
        assert price_lock['seller_id'] == price_lock_json['seller_id']
        assert price_lock['percent'] == price_lock_json['percent']

    @pytest.mark.parametrize("payload, status", [
        ({
            'percent': 30,
            'user': 'foo@luizalabs.com'
        }, 400),
        ({
            'seller_id': 'whirpool',
            'user': 'foo@luizalabs.com'
        }, 400),
        ({
            'percent': 30,
            'seller_id': 'whirpool'
        }, 400)
    ])
    def test_post_with_missing_keys_on_payload(
        self, client, payload, status, mock_url
    ):
        response = client.post(
            mock_url, body=json.dumps(payload)
        )
        assert response.status_code == status

    def test_post_with_invalid_percent(
            self, client, price_lock_json, mock_url
    ):
        price_lock_json['percent'] = 'invalid_percent'

        response = client.post(
            mock_url, body=json.dumps(price_lock_json)
        )
        assert response.status_code == 400

    def test_post_price_lock_should_update(
        self, client, save_price_lock, price_lock_json,
        mock_url
    ):
        price_lock_json['percent'] = 20

        response = client.post(
            mock_url, body=json.dumps(price_lock_json)

        )
        assert response.status_code == 200

        price_lock = (
            PriceLockModel.objects.get(seller_id=price_lock_json['seller_id'])
        )
        assert price_lock['seller_id'] == price_lock_json['seller_id']
        assert price_lock['percent'] == price_lock_json['percent']

    def test_get_price_lock_should_return_seller(
            self, client, save_price_lock, mock_url
    ):
        price_lock = PriceLockModel.objects
        price_lock = json.loads(price_lock.to_json())

        response = client.get(
            mock_url + '/seller/{}'.format(price_lock[0]['seller_id'])
        )

        assert response.status_code == 200

        assert (
            price_lock[0]['seller_id'] ==
            response.json['data']['seller_id']
        )
        assert price_lock[0]['percent'] == response.json['data']['percent']

    def test_get_price_lock_returns_not_found(
        self, client, save_price_lock, mock_url
    ):
        response = client.get(
            mock_url + '/seller/xpto'
        )
        assert response.status_code == 404

    @patch.object(PriceLockHandler, 'get_collection', Exception)
    def test_post_returns_error_message(
        self, client, logger_stream, price_lock_json, mock_url
    ):
        with pytest.raises(AttributeError):
            client.post(mock_url, body=json.dumps(price_lock_json))

        assert 'Error price lock with data' in logger_stream.getvalue()


class TestPriceLockListHandler:

    def test_get_price_lock_should_return_all(
        self, client, save_price_lock
    ):

        response = client.get('/price_lock/list')

        assert response.status_code == 200

        price_lock = PriceLockModel.objects

        price_lock = json.loads(price_lock.to_json())

        assert (
            price_lock[0]['seller_id'] ==
            response.json['data'][0]['seller_id']
        )
        assert price_lock[0]['percent'] == response.json['data'][0]['percent']

    def test_get_price_lock_returns_not_found(self, client, save_price_lock):
        response = client.get(
            '/price_lock/seller/xpto'
        )
        assert response.status_code == 404

    @patch.object(PriceLockHandler, 'get_collection', Exception)
    def test_post_returns_error_message(
        self, client, logger_stream, price_lock_json
    ):
        with pytest.raises(AttributeError):
            client.post('/price_lock', body=json.dumps(price_lock_json))

        assert 'Error price lock with data' in logger_stream.getvalue()
