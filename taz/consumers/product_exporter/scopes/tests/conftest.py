from datetime import datetime

import pytest
from redis import Redis
from simple_settings import settings

from taz import constants
from taz.core.matching.common.enriched_products import EnrichedProductSamples
from taz.core.matching.common.samples import ProductSamples


@pytest.fixture
def cache():
    return Redis(
        host=settings.REDIS_LOCK_SETTINGS['host'],
        port=settings.REDIS_LOCK_SETTINGS['port']
    )


@pytest.fixture
def product_dict(mongo_database):
    product = ProductSamples.magazineluiza_sku_213445900()

    del product['main_category']

    return product


@pytest.fixture
def enriched_product(product_dict):
    payload = EnrichedProductSamples.magazineluiza_sku_0233847()

    payload['sku'] = product_dict['sku']
    payload['seller_id'] = product_dict['seller_id']
    payload['navigation_id'] = product_dict['navigation_id']

    return payload


@pytest.fixture
def enriched_wakko(product_dict):
    payload = EnrichedProductSamples.magazineluiza_sku_0233847()

    payload['sku'] = product_dict['sku']
    payload['seller_id'] = product_dict['seller_id']
    payload['navigation_id'] = product_dict['navigation_id']
    payload['source'] = constants.SOURCE_WAKKO
    payload['metadata'] = {
        'normalized': {
            'Volume': ['90g']
        },
        'descriptive': {
            'Volume': ['90 g']
        },
        'classified': {
            'nsfw': {
                'safe': 0.5,
                'illustration': 0.35,
                'hentai': 0.80,
                'sensual': 0.82,
                'porn': 0.85
            },
            'category_id': 'IN'
        }
    }

    return payload


@pytest.fixture
def enriched_pickupstore(product_dict):
    payload = {
        'sku': product_dict['sku'],
        'seller_id': product_dict['seller_id'],
        'source': constants.SOURCE_API_LUIZA_PICKUPSTORE
    }

    return payload


@pytest.fixture
def id_correlation_dict(mongo_database, product_dict):
    id_correlation = {
        'sku': product_dict['sku'],
        'seller_id': product_dict['seller_id'],
        'product_id': '1234567',
        'variation_id': '213445900'
    }

    mongo_database.id_correlations.insert_one(id_correlation)


@pytest.fixture
def raw_products_dict(mongo_database):
    raw_product = {
        'type': 'product',
        'sku': 'E86-2541-007-04',
        'navigation_id': 'dfd5ck1fc0',
        'seller_id': 'zattini',
        'ean': '312312312312',
        'disable_on_matching': False,
    }

    mongo_database.raw_products.insert_one(raw_product)


@pytest.fixture
def prices_product_dict(mongo_database):
    to_insert = [
        {
            'stock_type': 'on_seller',
            'seller_id': 'zattini',
            'sku': 'E86-2541-007-04',
            'stock_count': 200
        },
        {
            'stock_type': 'on_seller',
            'seller_id': 'zattini',
            'sku': 'E86-2541-002-08',
            'stock_count': 102
        }
    ]

    mongo_database.prices.insert_many(to_insert)


@pytest.fixture
def unified_objects_dict(mongo_database):
    to_insert = {
        'reference': 'La Prairie',
        'description': '',
        'id': '9941810',
        'brand': 'La Prairie',
        'attributes': {},
        'url': '',
        'title': 'White Caviar Illuminating Cream La Prairie',
        'review_score': 5,
        'canonical_ids': [
            'afgj7c7978',
            'ageba5fgk6',
            'ak2ca4kje5',
            'bjhde21dh0',
            'ddagg49dkf',
            'dfd5ck1fc0'
        ],
        'type': 'product',
        'review_count': 0,
        'categories': []
    }

    mongo_database.unified_objects.insert_one(to_insert)
    return to_insert


@pytest.fixture
def id_correlations_products_dict(mongo_database):
    to_insert = [
        {
            'sku': 'E86-2541-006-02',
            'seller_id': 'zattini',
            'product_id': '9941810',
            'variation_id': 'hd83e2begc'
        },
        {
            'sku': 'E86-2541-007-04',
            'seller_id': 'zattini',
            'product_id': '9941810',
            'variation_id': 'cckbk9gc99'
        },
        {
            'sku': 'E86-2541-002-08',
            'seller_id': 'zattini',
            'product_id': '9941810',
            'variation_id': 'bdjj6h6g83'
        }
    ]

    mongo_database.id_correlations.insert_many(to_insert)


@pytest.fixture
def rating_dict(mongo_database):
    price = {
        'product_id': '2134459',
        'type': 'product_average_rating',
        'value': 4.3
    }

    mongo_database.customer_behaviors.insert_one(price)


@pytest.fixture
def review_dict(mongo_database, product_dict):
    price = {
        'product_id': '2134459',
        'type': 'product_total_review_count',
        'value': 83
    }

    mongo_database.customer_behaviors.insert_one(price)


@pytest.fixture
def categories_dicts(mongo_database):
    category = {
        'url': 'eletrodomesticos/l/ed/',
        'parent_id': 'ML',
        'slug': 'eletrodomesticos',
        'description': 'Eletrodomésticos',
        'id': 'ED',
        'active': True
    }

    subcategory = {
        'description': 'Máquina de Lavar',
        'slug': 'maquina-de-lavar',
        'id': 'LAVA',
        'parent_id': 'ED',
        'url': 'maquina-de-lavar/eletrodomesticos/s/ed/lava/',
        'active': True
    }

    mongo_database.categories.insert_one(category)
    mongo_database.categories.insert_one(subcategory)


@pytest.fixture
def store_media(mongo_database, product_dict):
    mongo_database.medias.insert_many([
        {
            'seller_id': product_dict['seller_id'],
            'sku': product_dict['sku'],
            'images': [
                {
                    'url': 'http://img.magazineluiza.com.br/1500x1500/x-213445900.jpg',  # noqa
                    'hash': 'd4b4755b9ee658406f6e40f1d6e6129c'
                },
                {
                    'url': 'http://img.magazineluiza.com.br/1500x1500/x-213445900a.jpg',  # noqa
                    'hash': 'ce86964b8543828d1433cb1e029770e5'
                },
                '213445900.jpg',
                '213445900-A.jpg'
            ]
        }
    ])


@pytest.fixture
def save_unpublished_product(mongo_database, product_dict):

    payload = {
        'navigation_id': product_dict['navigation_id'],
        'user': 'xablau',
        'updated_at': datetime.now(),
        'created_at': datetime.now()
    }

    mongo_database.unpublished_products.insert_one(payload)
