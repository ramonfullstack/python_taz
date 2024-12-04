from typing import Dict
from unittest.mock import ANY

import pytest
from pymongo import MongoClient
from simple_settings import settings

from taz.constants import MAGAZINE_LUIZA_SELLER_ID, UPDATE_ACTION


@pytest.fixture
def mock_minimum_order_quantity():
    return {
        'sku': '237216200',
        'seller_id': MAGAZINE_LUIZA_SELLER_ID,
        'navigation_id': '237216200',
        'value': 5,
        'active': True,
        'user': 'catalogo@luizalabs.com',
        'created_at': '2024-05-17T14:15:00.160+00:00'
    }


@pytest.fixture
def mock_prices():
    return {
        'sku': '237216200',
        'seller_id': MAGAZINE_LUIZA_SELLER_ID,
        'price': 58.98,
        'list_price': 109.8,
        'delivery_availability': 'nationwide',
        'stock_type': 'on_supplier',
        'last_updated_at': '2024-05-17T20:39:00.066333'
    }


@pytest.fixture
def mock_raw_products():
    return {
        'sku': '237216200',
        'seller_id': MAGAZINE_LUIZA_SELLER_ID,
        'navigation_id': '237216200'
    }


@pytest.fixture
def mock_prices_with_minimum_order_quantity(mock_prices):
    return {
        **mock_prices,
        'minimum_order_quantity': 5
    }


@pytest.fixture
def sku(mock_minimum_order_quantity: Dict):
    return mock_minimum_order_quantity['sku']


@pytest.fixture
def seller_id(mock_minimum_order_quantity: Dict):
    return mock_minimum_order_quantity['seller_id']


@pytest.fixture
def navigation_id(mock_minimum_order_quantity: Dict):
    return mock_minimum_order_quantity['navigation_id']


@pytest.fixture
def save_minimum_order_quantity(
    mongo_database: MongoClient,
    mock_minimum_order_quantity: Dict
):
    mongo_database.minimum_order_quantity.insert_one(
        mock_minimum_order_quantity
    )


@pytest.fixture
def save_prices(
    mongo_database: MongoClient,
    mock_prices: Dict
):
    mongo_database.prices.insert_one(mock_prices)


@pytest.fixture
def save_products(
    mongo_database: MongoClient,
    mock_prices: Dict,
    mock_raw_products: Dict
):
    mongo_database.raw_products.insert_one(mock_raw_products)


@pytest.fixture
def save_prices_with_minimum_order_quantity(
    mongo_database: MongoClient,
    mock_prices_with_minimum_order_quantity: Dict
):
    mongo_database.prices.insert_one(mock_prices_with_minimum_order_quantity)


@pytest.fixture
def pubsub_payload_expected(mock_minimum_order_quantity: Dict):
    return {
        'content': {
            'sku': mock_minimum_order_quantity['sku'],
            'seller_id': mock_minimum_order_quantity['seller_id'],
            'navigation_id': mock_minimum_order_quantity['navigation_id'],
            'action': UPDATE_ACTION,
            'type': 'stock',
            'origin': 'api_minimum_order_quantity',
            'task_id': ANY,
            'timestamp': ANY
        },
        'topic_name': settings.PUBSUB_PUBLISHER_NOTIFY_TOPIC,
        'project_id': settings.GOOGLE_PROJECT_ID,
        'attributes': {
            'seller_id': mock_minimum_order_quantity['seller_id'],
            'action': UPDATE_ACTION,
            'type': 'stock'
        }
    }
