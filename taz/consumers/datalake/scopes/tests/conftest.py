import pytest

from taz.core.matching.common.samples import ProductSamples


@pytest.fixture
def product_inactive():
    product = ProductSamples.magazineluiza_sku_193389600()
    product['disable_on_matching'] = True
    return product


@pytest.fixture
def mock_sku():
    return '123456789'


@pytest.fixture
def price():
    return {
        'sku': '193389600',
        'seller_id': 'magazineluiza',
        'list_price': 234.56,
        'price': 123.45,
        'delivery_availability': 'nationwide',
        'stock_count': 321,
        'stock_type': 'on_seller',
        'checkout_price': 234.56,
    }


@pytest.fixture
def price_with_currency():
    return {
        'sku': '193389601223',
        'seller_id': 'foreign_seller',
        'list_price': 234.56,
        'price': 123.45,
        'currency': 'USD',
        'delivery_availability': 'nationwide',
        'stock_count': 321,
        'stock_type': 'on_seller',
        'checkout_price': 234.56
    }


@pytest.fixture
def category():
    return {
        'id': 'ET',
        'description': 'Tv e Video',
        'slug': 'tv-video',
        'parent_id': 'ML',
        'active': True
    }


@pytest.fixture
def sub_category():
    return {
        'id': 'ELIT',
        'description': 'Tv e Video Sub',
        'slug': 'tv-video',
        'parent_id': 'ET',
        'active': True
    }


@pytest.fixture
def sub_category_other():
    return {
        'id': 'TLED',
        'description': 'Tv e Video Sub Other',
        'slug': 'tv-video',
        'parent_id': 'ET',
        'active': True
    }


@pytest.fixture
def save_product_inactive(mongo_database, product_inactive):
    mongo_database.raw_products.insert_one(product_inactive)


@pytest.fixture
def save_price(mongo_database, price):
    mongo_database.prices.insert_one(price)


@pytest.fixture
def save_category(mongo_database, category):
    mongo_database.categories.insert_one(category)


@pytest.fixture
def save_sub_category(mongo_database, sub_category, sub_category_other):
    mongo_database.categories.insert_one(sub_category)
    mongo_database.categories.insert_one(sub_category_other)


@pytest.fixture
def categories_expected():
    return [{
        'subcategories': [
            {'id': 'ELIT'},
            {'id': 'LE55'},
            {'id': 'LE6Z'},
            {'id': 'LEAI'},
            {'id': 'LECI'},
            {'id': 'LESM'},
            {'id': 'PECO'},
            {'id': 'S60H'},
            {'id': 'SM55'},
            {'id': 'SMAI'},
            {'id': 'SMCD'},
            {'id': 'SMLD'},
            {'id': 'TD55'},
            {'id': 'TLED'}
        ],
        'id': 'ET'
    }]
