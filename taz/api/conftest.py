from unittest.mock import patch

import pytest
from falcon import testing
from mongoengine import connect
from simple_settings import settings

from taz.api import app
from taz.api.medias.models import MediaModel
from taz.api.models.token import TokenModel
from taz.api.pending.models import PendingProductModel
from taz.api.prices.models import PriceModel
from taz.api.products.models import RawProductModel
from taz.consumers.core.aws.sqs import SQSManager
from taz.core.matching.common.samples import ProductSamples


class Client(testing.TestClient):

    def get_header_token(self):
        token = TokenModel.generate('TazApi')
        return {
            'Authorization': 'Token {}'.format(token.token)
        }

    def get(self, path='/', **kwargs):
        kwargs.update({'headers': self.get_header_token()})
        return self.simulate_get(path, **kwargs)

    def delete(self, path='/', **kwargs):
        kwargs.update({'headers': self.get_header_token()})
        return self.simulate_delete(path, **kwargs)

    def put(self, path='/', **kwargs):
        kwargs.update({'headers': self.get_header_token()})
        return self.simulate_put(path, **kwargs)

    def post(self, path='/', **kwargs):
        kwargs.update({'headers': self.get_header_token()})
        return self.simulate_post(path, **kwargs)


@pytest.fixture(scope='module')
def client():
    return Client(app)


@pytest.fixture(autouse=True)
def mongo_db():
    return connect('acme', host=settings.MONGO_URI)


@pytest.fixture
def patch_sqs_put():
    return patch.object(SQSManager, 'put')


@pytest.fixture(autouse=True)
def clean_database(mongo_db):
    mongo_db.drop_database(settings.MONGO_DATABASE)


@pytest.fixture
def token():
    return TokenModel.generate('TazApi')


@pytest.fixture
def save_raw_products():
    raw_products = [
        ProductSamples.seller_a_variation_with_parent(),
        ProductSamples.seller_b_variation_with_parent(),
        ProductSamples.seller_c_variation_with_parent()
    ]

    for product in raw_products:
        RawProductModel(**product).save()


@pytest.fixture
def save_raw_products_with_inactive(save_raw_products):
    inactive_product = ProductSamples.seller_a_variation_with_parent()
    inactive_product['disable_on_matching'] = True
    RawProductModel(**inactive_product).save()


@pytest.fixture
def save_raw_products_without_attributes():
    raw_products = [
        ProductSamples.seller_a_variation_with_parent()
    ]

    for product in raw_products:
        del product['attributes']
        RawProductModel(**product).save()


@pytest.fixture
def save_pending_products():
    raw_products = [
        ProductSamples.seller_a_variation_with_parent(),
        ProductSamples.seller_b_variation_with_parent(),
        ProductSamples.seller_c_variation_with_parent()
    ]

    for product in raw_products:
        PendingProductModel(**product).save()


@pytest.fixture
def save_prices():
    raw_products = [
        ProductSamples.seller_a_variation_with_parent(),
        ProductSamples.seller_b_variation_with_parent(),
        ProductSamples.seller_c_variation_with_parent(),
        ProductSamples.seller_d_variation_with_parent(),
    ]

    for product in raw_products:
        price = {
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'list_price': '234.56',
            'price': '123.45',
            'delivery_availability': 'nationwide',
            'stock_count': 321,
            'stock_type': 'on_seller'
        }

        PriceModel(**price).save()


@pytest.fixture
def save_prices_duplicated():
    raw_products = [
        ProductSamples.seller_a_variation_with_parent(),
        ProductSamples.seller_a_variation_with_parent()
    ]

    for product in raw_products:
        price = {
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'list_price': '234.56',
            'price': '123.45',
            'delivery_availability': 'nationwide',
            'stock_count': 321,
            'stock_type': 'on_seller'
        }

        PriceModel(**price).save()


@pytest.fixture
def save_medias():
    raw_products = [
        ProductSamples.seller_a_variation_with_parent(),
        ProductSamples.seller_b_variation_with_parent(),
        ProductSamples.seller_c_variation_with_parent(),
        ProductSamples.seller_d_variation_with_parent(),
    ]

    for product in raw_products:
        media = {
            'images': [
                'd2e14e48997a911745931e6a2991b2cf.jpg'
            ],
            'seller_id': product['seller_id'],
            'sku': product['sku']
        }

        MediaModel(**media).save()


@pytest.fixture
def product_dict():
    return {
        'ean': '1234567890123456',
        'seller_id': 'murcho',
        'seller_description': 'Murcho Store',
        'sku': '123456789',
        'parent_sku': '987654321',
        'type': 'product',
        'title': 'iPhone Murcho 64 GB',
        'description': 'iPhone Murcho 64 GB Bla Bla Bla',
        'reference': 'iClone, iPony, etc',
        'brand': 'Murcho Inc',
        'sold_count': 50,
        'sells_to_company': True,
        'dimensions': {
            'width': 0.18,
            'depth': 0.18,
            'weight': 0.18,
            'height': 0.18,
        },
        'attributes': [
            {
                'type': 'color',
                'value': 'Azul'
            },
            {
                'type': 'voltage',
                'value': 'Bivolt'
            }
        ],
        'categories': [
            {
                'id': 'TB',
                'subcategories': [
                    {
                        'id': 'KIND',
                    }
                ]
            }
        ],
    }
