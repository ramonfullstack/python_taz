import pytest


@pytest.fixture
def product_200238300():
    return {
        'dimensions': {
            'width': 0.2,
            'height': 0.23,
            'weight': 0.78,
            'depth': 0.11
        },
        'images_count': 7,
        'active': True,
        'created_at': '2011-08-27T05:13:16.857000',
        'categories': [{
            'subcategories': [{
                'id': 'PSAV'
            }],
            'id': 'EP'
        }],
        'seller_id': 'magazineluiza',
        'brand': 'Cadence',
        'full_title': 'Passadeira a Vapor Portátil Cadence Lisser VAP901 - 200ml 700W Branco',  # noqa
        'sku': '200238300',
        'offer_title': 'Passadeira a Vapor Portátil Cadence Lisser VAP901 - 200ml 700W Branco',  # noqa
        'main_category': {
            'subcategory': {
                'id': 'PSAV'
            },
            'id': 'EP'
        },
        'md5': 'a67b3cd87e6726cfbf3bdfd9d0cd8c5e',
        'description': 'Passadeira que higieniza as roupas, eliminando odore em poucos minutos e evitando a proliferação de ácaros e outros microorganismos. Muito prática, ela é ideal para qualquer tipo de tecido, roupas ou cortinas. É portátil e fácil de levar nas viagens. Possui escovas especiais para retirar fiapos e pelos.',  # noqa
        'attributes': [{
            'type': 'voltage',
            'value': '220V'
        }],
        'last_updated_at': '2019-05-02T15:50:07.145558',
        'reviews_count': 10,
        'disable_on_matching': False,
        'grade': 10,
        'parent_sku': '2002382',
        'seller_description': 'Magazine Luiza',
        'ean': '7898221451861',
        'navigation_id': '200238300',
        'entity': 'Passadeira a Vapor',
        'reference': '200ml 700W Branco',
        'updated_at': '2019-05-02T12:43:35.273000',
        'main_variation': False,
        'sold_count': 0,
        'type': 'product',
        'review_rating': 2.9,
        'title': 'Passadeira a Vapor Portátil Cadence Lisser VAP901',
        'selections': {
            '0': ['17637', '24166', '7291', '8218', '8387'],
            '12966': ['16734', '16737']
        },
        'matching_strategy': 'SINGLE_SELLER',
        'sells_to_company': True,
        'category_id': 'EP'
    }


@pytest.fixture
def enriched_product_200238300():
    return {
        'sku': '200238300',
        'entity': 'Passadeira a Vapor',
        'metadata': {
            'Marca': 'Cadence',
            'Potência': '700 W',
            'Voltagem': '220V'
        },
        'seller_id': 'magazineluiza',
        'navigation_id': '200238300',
        'category_id': 'EP',
        'subcategory_ids': ['PSAV'],
        'product_hash': None,
        'product_name': None,
        'product_matching_metadata': [],
        'product_name_metadata': [],
        'sku_metadata': [],
        'filters_metadata': ['Marca', 'Capacidade', 'Voltagem', 'Potência'],
        'source': 'magalu',
        'timestamp': 1554989750.800389
    }


@pytest.fixture
def media_product_200238300(mock_product_videos_message_data):
    return {
        'images': [
            '8b5ae762cd50df712106a89c879865f9.jpg',
            '6d6ede217a6a94d5d6cd68915221f858.jpg',
            '6ebd58ffb55e912104a26c863103de04.jpg',
            'd562c798fac2cd2994a3c256d8326a24.jpg',
            '27de830f188c7489b2f112e762ed6e92.jpg',
            'b3ba5b29d6f9d723db6aa51d98a57738.jpg',
            'b445072a0b1320d2c7fc0e29aad59340.jpg'
        ],
        'videos': mock_product_videos_message_data,
        'seller_id': 'magazineluiza',
        'sku': '200238300'
    }


@pytest.fixture
def customer_behavior_200238300():
    return [
        {
            'product_id': '200238300',
            'type': 'product_total_review_count',
            'value': 10
        },
        {
            'product_id': '200238300',
            'type': 'product_average_rating',
            'value': 2.9
        }
    ]
