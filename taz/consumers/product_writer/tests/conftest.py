import pytest
from pymongo import MongoClient

from taz.constants import (
    AVAILABILITY_NATIONWIDE,
    MAGAZINE_LUIZA_SELLER_ID,
    STOCK_TYPE_DC
)


@pytest.fixture
def expected_product_matched_builded():
    return {
        'id': '212415800',
        'attributes': [{
            'label': 'Voltagem',
            'type': 'voltage',
            'values': ['110 Volts', '220 Volts']
        }],
        'brand': 'hamilton beach',
        'canonical_ids': ['2022250', '212415700', '212415800'],
        'categories': [{
            'composite_name': 'EP|Eletroportáteis',
            'id': 'EP',
            'name': 'Eletroportáteis',
            'subcategories': [{
                'composite_name': 'ELCO|Eletroportáteis '
                'para Cozinha',
                'id': 'ELCO',
                'name': 'Eletroportáteis para Cozinha',
                'url': 'eletroportateis-para-cozinha/eletroportateis/s/ep/elco/'  # noqa
            }, {
                'composite_name': 'LIQU|Liquidificadores',
                'id': 'LIQU',
                'name': 'Liquidificadores',
                'url': 'lquidificadores/eletroportateis/s/ep/liqu/'
            }, {
                'composite_name': 'LIQU|Liquidificadores',
                'id': 'LIQU',
                'name': 'Liquidificadores',
                'url': 'lquidificadores/eletroportateis/s/ep/liqu/'
            }, {
                'composite_name': 'ELCO|Eletroportáteis '
                'para Cozinha',
                'id': 'ELCO',
                'name': 'Eletroportáteis para Cozinha',
                'url': 'eletroportateis-para-cozinha/eletroportateis/s/ep/elco/'  # noqa
            }],
            'url': 'eletroportateis/l/ep/'
        }],
        'title': 'Liquidificador Hamilton Beach Multifuncional Plus',
        'type': 'product',
        'url': 'liquidificador-hamilton-beach-multifuncional-plus-5-velocidades-com-filtro-inox-500w/p/2124158/ep/elco/',  # noqa
        'variations': [{
            'media': {
                'images': ['/{w}x{h}/liquidificador-multifuncional-plus-54229-hamilton-beach-hamilton-beach/dbestshop/2022250/2022250.jpg', '/{w}x{h}/liquidificador-multifuncional-plus-54229-hamilton-beach-hamilton-beach/dbestshop/2022250/2022250-A.jpg'],  # noqa
                'podcasts': ['/dbestshop/podcasts/2022250/2022250.mp3'],
                'videos': ['2022250'],
                'audios': ['/dbestshop/audios/2022250/2022250.mp3']
            },
            'sellers': [{
                'status': 'published',
                'list_price': 349.9,
                'description': 'DBestShop',
                'price': 267.9,
                'sells_to_company': False,
                'stock_type': 'on_seller',
                'delivery_availability': 'nationwide',
                'id': 'dbestshop',
                'sku': '2022250',
                'stock_count': 23,
                'sold_count': 0
            }],
            'is_delivery_available': True,
            'id': '2022250',
            'categories': [{
                'url': 'eletroportateis/l/ep/',
                'composite_name': 'EP|Eletroport\xc3\xa1teis',
                'subcategories': [{
                    'url': 'eletroportateis-para-cozinha/eletroportateis/s/ep/elco/',  # noqa
                    'composite_name': 'ELCO|Eletroport\xc3\xa1teis para Cozinha',  # noqa
                    'id': 'ELCO',
                    'name': 'Eletroport\xc3\xa1teis para Cozinha'
                }, {
                    'url': 'lquidificadores/eletroportateis/s/ep/liqu/',
                    'composite_name': 'LIQU|Liquidificadores',
                    'id': 'LIQU',
                    'name': 'Liquidificadores'
                }],
                'id': 'EP',
                'name': 'Eletroport\xc3\xa1teis'
            }]
        }, {
            'media': {
                'images': ['/{w}x{h}/liquidificador-hamilton-beach-multifuncional-plus-5-velocidades-com-filtro-inox-500w/magazineluiza/212415800/212415800.jpg', '/{w}x{h}/liquidificador-hamilton-beach-multifuncional-plus-5-velocidades-com-filtro-inox-500w/magazineluiza/212415800/212415800-A.jpg'],  # noqa
                'podcasts': ['/magazineluiza/podcasts/212415800/212415800.mp3'],  # noqa
                'videos': ['212415800'],
                'audios': ['/magazineluiza/audios/212415800/212415800.mp3']
            },
            'sellers': [{
                'status': 'published',
                'list_price': 349.9,
                'description': 'Magazine Luiza',
                'price': 267.9,
                'sells_to_company': False,
                'stock_type': 'on_seller',
                'delivery_availability': 'nationwide',
                'id': 'magazineluiza',
                'sku': '212415800',
                'stock_count': 23,
                'sold_count': 0
            }],
            'is_delivery_available': True,
            'attributes': [{
                'name': 'voltage',
                'value': '220 Volts'
            }],
            'id': '212415800',
            'categories': [{
                'url': 'eletroportateis/l/ep/',
                'composite_name': 'EP|Eletroport\xc3\xa1teis',
                'subcategories': [{
                    'url': 'eletroportateis-para-cozinha/eletroportateis/s/ep/elco/',  # noqa
                    'composite_name': 'ELCO|Eletroport\xc3\xa1teis para Cozinha',  # noqa
                    'id': 'ELCO',
                    'name': 'Eletroport\xc3\xa1teis para Cozinha'
                }, {
                    'url': 'lquidificadores/eletroportateis/s/ep/liqu/',
                    'composite_name': 'LIQU|Liquidificadores',
                    'id': 'LIQU',
                    'name': 'Liquidificadores'
                }],
                'id': 'EP',
                'name': 'Eletroport\xc3\xa1teis'
            }]
        }, {
            'media': {
                'images': ['/{w}x{h}/liquidificador-hamilton-beach-multifuncional-plus-5-velocidades-com-filtro-inox-500w/magazineluiza/212415700/212415700.jpg', '/{w}x{h}/liquidificador-hamilton-beach-multifuncional-plus-5-velocidades-com-filtro-inox-500w/magazineluiza/212415700/212415700-A.jpg'],  # noqa
                'podcasts': ['/magazineluiza/podcasts/212415700/212415700.mp3'],  # noqa
                'videos': ['212415700'],
                'audios': ['/magazineluiza/audios/212415700/212415700.mp3']
            },
            'sellers': [{
                'status': 'published',
                'list_price': 349.9,
                'description': 'Magazine Luiza',
                'price': 267.9,
                'sells_to_company': False,
                'stock_type': 'on_seller',
                'delivery_availability': 'nationwide',
                'id': 'magazineluiza',
                'sku': '212415700',
                'stock_count': 23,
                'sold_count': 0
            }],
            'is_delivery_available': True,
            'attributes': [{
                'name': 'voltage',
                'value': '110 Volts'
            }],
            'id': '212415700',
            'categories': [{
                'url': 'eletroportateis/l/ep/',
                'composite_name': 'EP|Eletroport\xc3\xa1teis',
                'subcategories': [{
                    'url': 'eletroportateis-para-cozinha/eletroportateis/s/ep/elco/',  # noqa
                    'composite_name': 'ELCO|Eletroport\xc3\xa1teis para Cozinha',  # noqa
                    'id': 'ELCO',
                    'name': 'Eletroport\xc3\xa1teis para Cozinha'
                }, {
                    'url': 'lquidificadores/eletroportateis/s/ep/liqu/',
                    'composite_name': 'LIQU|Liquidificadores',
                    'id': 'LIQU',
                    'name': 'Liquidificadores'
                }],
                'id': 'EP',
                'name': 'Eletroport\xc3\xa1teis'
            }]
        }]
    }


@pytest.fixture
def custom_attributes_dict():
    return {
        'sku': '123456789',
        'seller_id': 'magazineluiza',
        'short_title': 'A short title',
        'short_description': 'A brief description'
    }


@pytest.fixture
def priceless_product(database):
    categories = [
        {
            'id': 'PF',
            'description': 'Perfumaria',
            'slug': 'perfumaria',
            'parent_id': 'ML'
        },
        {
            'id': 'PFPF',
            'description': 'Perfumes Femininos',
            'slug': 'perfumes-femininos',
            'parent_id': 'PF'
        },
        {
            'id': 'PFPM',
            'description': 'Perfumes Masculinos',
            'slug': 'perfumes-masculinos',
            'parent_id': 'PF'
        }
    ]

    for category in categories:
        database.categories.insert_one(category)

    return {
        'title': 'Caneca Xablau Branca',
        'review_count': 2,
        'type': 'product',
        'review_score': 4.3,
        'release_date': '2014-11-04T00:00:00',
        'categories': [
            {
                'id': 'PF',
                'subcategories': [
                    {'id': 'PFPF'},
                    {'id': 'PFPM'}
                ]
            }
        ],
        'variations': [
            {
                'id': '723829300',
                'created_at': '2008-05-10T08:20:44.900000',
                'updated_at': '2008-05-10T08:20:44.900000',
                'title': 'Caneca Xablau Branca - 250ml',
                'reference': 'CXB250ML',
                'sellers': [
                    {
                        'id': 'magazineluiza',
                        'description': 'Magazine Luiza',
                        'sku': '723829300',
                        'sells_to_company': True,
                        'sold_count': 10,
                        'fulfillment': True
                    }
                ],
                'categories': [
                    {
                        'id': 'PF',
                        'subcategories': [
                            {'id': 'PFPF'},
                            {'id': 'PFPM'}
                        ]
                    }
                ],
                'dimensions': {
                    'width': 0.18,
                    'depth': 0.13,
                    'weight': 0.47,
                    'height': 0.44
                },
                'selections': {
                    '7985': ['12669'],
                    '0': ['10709', '10811', '12416', '8079']
                },
            },
            {
                'title': 'Caneca Xablau Branca - 350ml',
                'reference': 'CXB350ML',
                'id': '8weuwe88we',
                'created_at': '2008-05-10T08:20:44.900000',
                'updated_at': '2008-05-10T08:20:44.900000',
                'sellers': [
                    {
                        'id': 'magazineluiza',
                        'description': 'Magazine Luiza',
                        'sku': '8weuwe88we',
                        'sells_to_company': True,
                        'sold_count': 10,
                        'fulfillment': False,
                        'matching_uuid': 'a0069aee16d441cab4030cce086debbc',
                        'extra_data': [{'name': 'is_magalu_indica', 'value': 'true'}],  # noqa
                        'parent_matching_uuid': '5c2275661d8f11ed861d0242ac120002' # noqa

                    }
                ],
                'categories': [
                    {
                        'id': 'PF',
                        'subcategories': [
                            {'id': 'PFPF'},
                            {'id': 'PFPM'}
                        ]
                    }
                ],
                'dimensions': {
                    'width': 0.18,
                    'depth': 0.13,
                    'weight': 0.47,
                    'height': 0.44
                },
                'selections': {
                    '7985': ['12669'],
                    '0': ['10709', '10811', '12416', '8079']
                },
            },
            {
                'title': 'Caneca Xablau Branca - 200ml',
                'reference': 'CXB200ML',
                'id': '623728900',
                'created_at': '2008-05-10T08:20:44.900000',
                'updated_at': '2008-05-10T08:20:44.900000',
                'sellers': [
                    {
                        'id': 'magazineluiza',
                        'description': 'Magazine Luiza',
                        'sku': '623728900',
                        'sells_to_company': True,
                        'sold_count': 10,
                        'fulfillment': True,
                        'matching_uuid': 'a0069aee16d441cab4030cce086debbc',
                        'extra_data': [{'name': 'is_magalu_indica', 'value': 'true'}],  # noqa
                        'parent_matching_uuid': '5c2275661d8f11ed861d0242ac120002' # noqa

                    },
                    {
                        'id': 'seuzeh',
                        'description': 'Seu Zeh',
                        'sku': '819283iqw',
                        'sells_to_company': True,
                        'sold_count': 10,
                        'fulfillment': False,
                        'matching_uuid': '57f5031ad56949ac92bff1873b3f5b4a',
                        'parent_matching_uuid': '5c2275661d8f11ed861d0242ac120002', # noqa
                        'extra_data': None
                    }
                ],
                'categories': [
                    {
                        'id': 'PF',
                        'subcategories': [
                            {'id': 'PFPF'},
                            {'id': 'PFPM'}
                        ]
                    }
                ],
                'dimensions': {
                    'width': 0.18,
                    'depth': 0.13,
                    'weight': 0.47,
                    'height': 0.44
                },
                'selections': {
                    '7985': ['12669'],
                    '0': ['10709', '10811', '12416', '8079']
                },
            },
            {
                'title': 'Caneca Xablau Branca - 450ml',
                'reference': 'CXB450ML',
                'id': '82323jjjj3',
                'created_at': '2008-05-10T08:20:44.900000',
                'updated_at': '2008-05-10T08:20:44.900000',
                'sellers': [
                    {
                        'id': 'seller_a',
                        'description': 'Seller A',
                        'sku': '82323jjjj3',
                        'sells_to_company': True,
                        'sold_count': 10,
                        'matching_uuid': 'af6f8d9cb9a64bcd8023e21c5a797b85',
                        'extra_data': [{'name': 'is_magalu_indica', 'value': 'true'}],  # noqa
                        'parent_matching_uuid': '5c2275661d8f11ed861d0242ac120002' # noqa

                    },
                    {
                        'id': 'seller_b',
                        'description': 'Seller B',
                        'sku': '098asdwe28',
                        'sells_to_company': True,
                        'sold_count': 10
                    },
                    {
                        'id': 'seller_c',
                        'description': 'Seller C',
                        'sku': 'ou23ou23ou',
                        'sells_to_company': True,
                        'sold_count': 10,
                        'fulfillment': False,
                        'matching_uuid': 'af6f8d9cb9a64bcd8023e21c5a797b85',
                        'extra_data': [{'name': 'is_magalu_indica', 'value': 'true'}],  # noqa
                        'parent_matching_uuid': '5c2275661d8f11ed861d0242ac120002' # noqa


                    }
                ],
                'categories': [
                    {
                        'id': 'PF',
                        'subcategories': [
                            {'id': 'PFPF'},
                            {'id': 'PFPM'}
                        ]
                    }
                ],
                'dimensions': {
                    'width': 0.18,
                    'depth': 0.13,
                    'weight': 0.47,
                    'height': 0.44
                },
                'selections': {
                    '7985': ['12669'],
                    '0': ['10709', '10811', '12416', '8079']
                },
            },
            {
                'title': 'Caneca Xablau Branca - 150ml',
                'reference': 'CXB150ML',
                'id': '723uwej2u3',
                'created_at': '2008-05-10T08:20:44.900000',
                'updated_at': '2008-05-10T08:20:44.900000',
                'sellers': [
                    {
                        'id': 'casaamerica',
                        'description': 'Casa America',
                        'sku': '723uwej2u3',
                        'sells_to_company': True,
                        'sold_count': 10
                    }
                ],
                'categories': [
                    {
                        'id': 'PF',
                        'subcategories': [
                            {'id': 'PFPF'},
                            {'id': 'PFPM'}
                        ]
                    }
                ],
                'dimensions': {
                    'width': 0.18,
                    'depth': 0.13,
                    'weight': 0.47,
                    'height': 0.44
                },
                'selections': {
                    '7985': ['12669'],
                    '0': ['10709', '10811', '12416', '8079']
                },
            }
        ],
    }


@pytest.fixture
def save_stocks(mongo_database: MongoClient):
    mongo_database.stocks.insert_many([
        {
            'sku': '723829300',
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'type': STOCK_TYPE_DC,
            'position': {
                'physic': {
                    'available': 2
                },
                'logic': {
                    'available': 3
                }
            },
            'delivery_availability': AVAILABILITY_NATIONWIDE,
            'branch_id': '123'
        },
        {
            'sku': '623728900',
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'type': STOCK_TYPE_DC,
            'position': {
                'physic': {
                    'available': 1
                },
                'logic': {
                    'available': 0
                }
            },
            'delivery_availability': AVAILABILITY_NATIONWIDE,
            'branch_id': '123'
        }
    ])


@pytest.fixture
def prices():
    return [
        {
            'sku': '212415700',
            'seller_id': 'magazineluiza',
            'list_price': 349.90,
            'price': 267.90,
            'delivery_availability': 'nationwide',
            'stock_count': 1,
            'stock_type': 'on_seller',
            'sold_count': 0
        },
        {
            'sku': '212415800',
            'seller_id': 'magazineluiza',
            'list_price': 349.90,
            'price': 267.90,
            'delivery_availability': 'nationwide',
            'stock_count': 1,
            'stock_type': 'on_seller',
            'sold_count': 0
        },
        {
            'sku': '2022250',
            'seller_id': 'dbestshop',
            'list_price': 349.90,
            'price': 267.90,
            'delivery_availability': 'nationwide',
            'stock_count': 23,
            'stock_type': 'on_seller',
            'sold_count': 0
        },
        {
            'sku': '723829300',
            'seller_id': 'magazineluiza',
            'list_price': 234.56,
            'price': 123.45,
            'minimum_order_quantity': 5
        },
        {
            'sku': '723829300',
            'seller_id': 'magazineluiza',
            'delivery_availability': 'nationwide',
            'stock_count': 1,
            'stock_type': 'on_seller',
            'sold_count': 0
        },
        {
            'sku': '623728900',
            'seller_id': 'magazineluiza',
            'list_price': 434.56,
            'price': 323.45,
            'delivery_availability': 'nationwide',
            'stock_count': 1,
            'stock_type': 'on_seller',
            'sold_count': 0,
            'minimum_order_quantity': 10
        },
        {
            'sku': '819283iqw',
            'seller_id': 'seuzeh',
            'list_price': 134.56,
            'price': 23.45,
            'delivery_availability': 'nationwide',
            'stock_count': 31,
            'stock_type': 'on_seller',
            'sold_count': 0,
        },
        {
            'sku': '82323jjjj3',
            'seller_id': 'seller_a',
            'list_price': 64.56,
            'price': 33.45,
            'delivery_availability': 'nationwide',
            'stock_count': 3,
            'stock_type': 'on_supplier',
            'sold_count': 0,
        },
        {
            'sku': '098asdwe28',
            'seller_id': 'seller_b',
            'list_price': 14.56,
            'price': 13.45,
            'delivery_availability': 'unavailable',
            'stock_count': 0,
            'stock_type': 'on_supplier',
            'sold_count': 3,
        },
        {
            'sku': 'ou23ou23ou',
            'seller_id': 'seller_c',
            'list_price': 74.56,
            'price': 53.45,
            'delivery_availability': 'nationwide',
            'stock_count': 18,
            'stock_type': 'on_supplier',
            'sold_count': 2,
        },
        {
            'sku': '723uwej2u3',
            'seller_id': 'casaamerica',
            'list_price': 44.56,
            'price': 33.45,
            'delivery_availability': 'nationwide',
            'stock_count': 0,
            'stock_type': 'on_supplier',
            'sold_count': 1,
        },
    ]


@pytest.fixture
def expected_verified_sellers():
    return [
        {
            'sku': '723829300',
            'seller_id': 'magazineluiza',
            'list_price': 234.56,
            'price': 123.45,
            'delivery_availability': 'nationwide',
            'stock_count': 21,
            'stock_type': 'on_seller',
            'sold_count': 0,
            'status': 'published'
        },
        {
            'sku': '623728900',
            'seller_id': 'magazineluiza',
            'list_price': 434.56,
            'price': 323.45,
            'delivery_availability': 'nationwide',
            'stock_count': 10,
            'stock_type': 'on_seller',
            'sold_count': 0,
            'status': 'published'
        },
        {
            'sku': '819283iqw',
            'seller_id': 'seuzeh',
            'list_price': 134.56,
            'price': 23.45,
            'delivery_availability': 'unavailable',
            'stock_count': 31,
            'stock_type': 'on_seller',
            'sold_count': 0,
            'status': 'published'
        },
        {
            'sku': '82323jjjj3',
            'seller_id': 'seller_a',
            'list_price': 64.56,
            'price': 33.45,
            'delivery_availability': 'unavailable',
            'stock_count': 3,
            'stock_type': 'on_supplier',
            'sold_count': 0,
            'status': 'published'
        },
        {
            'sku': '098asdwe28',
            'seller_id': 'seller_b',
            'list_price': 14.56,
            'price': 13.45,
            'delivery_availability': 'unavailable',
            'stock_count': 0,
            'stock_type': 'on_supplier',
            'sold_count': 3,
            'status': 'published'
        },
        {
            'sku': 'ou23ou23ou',
            'seller_id': 'seller_c',
            'list_price': 74.56,
            'price': 53.45,
            'delivery_availability': 'unavailable',
            'stock_count': 18,
            'stock_type': 'on_supplier',
            'sold_count': 2,
            'status': 'published'
        },
        {
            'sku': '723uwej2u3',
            'seller_id': 'casaamerica',
            'list_price': 44.56,
            'price': 33.45,
            'delivery_availability': 'unavailable',
            'stock_count': 15,
            'stock_type': 'on_supplier',
            'sold_count': 1,
            'status': 'published'
        },
    ]


@pytest.fixture
def expected_priced_product():
    return {
        'title': 'Caneca Xablau Branca',
        'sold_count': 80,
        'price': 123.45,
        'review_count': 2,
        'review_score': 4.3,
        'type': 'product',
        'created_at': '2008-05-10T08:20:44.900000',
        'updated_at': '2008-05-10T08:20:44.900000',
        'message_timestamp': 1502734827.997473,
        'release_date': '2014-11-04T00:00:00',
        'is_delivery_available': True,
        'attributes': [],
        'categories': [
            {
                'id': 'PF',
                'name': 'Perfumaria',
                'composite_name': 'PF|Perfumaria',
                'url': 'perfumaria/l/pf/',
                'subcategories': [
                    {
                        'id': 'PFPF',
                        'name': 'Perfumes Femininos',
                        'composite_name': 'PFPF|Perfumes Femininos',
                        'url': 'perfumes-femininos/perfumaria/s/pf/pfpf/',  # noqa
                    },
                    {
                        'id': 'PFPM',
                        'name': 'Perfumes Masculinos',
                        'composite_name': 'PFPM|Perfumes Masculinos',
                        'url': 'perfumes-masculinos/perfumaria/s/pf/pfpm/',  # noqa
                    }
                ]
            }
        ],
        'variations': [
            {
                'id': '723829300',
                'title': 'Caneca Xablau Branca - 250ml',
                'reference': 'CXB250ML',
                'is_delivery_available': True,
                'media': {
                    'videos': ['723829300'],
                    'audios': [
                        '/magazineluiza/audios/723829300/723829300.mp3'
                    ],
                    'podcasts': [
                        '/magazineluiza/podcasts/723829300/723829300.mp3'
                    ],
                    'images': [
                        '/{w}x{h}/caneca-xablau-branca-250ml-cxb250ml/magazineluiza/723829300/723829300.jpg',  # noqa
                        '/{w}x{h}/caneca-xablau-branca-250ml-cxb250ml/magazineluiza/723829300/723829300-A.jpg'  # noqa
                    ]
                },
                'sellers': [
                    {
                        'delivery_availability': 'nationwide',
                        'description': 'Magazine Luiza',
                        'id': 'magazineluiza',
                        'list_price': 234.56,
                        'price': 123.45,
                        'currency': 'BRL',
                        'sku': '723829300',
                        'status': 'published',
                        'sold_count': 10,
                        'stock_count': 1,
                        'stock_type': 'on_seller',
                        'sells_to_company': True,
                        'score': 1,
                        'order': 0,
                        'store_pickup_available': False,
                        'delivery_plus_1': False,
                        'delivery_plus_2': False,
                        'fulfillment': True,
                        'matching_uuid': None,
                        'extra_data': None,
                        'parent_matching_uuid': None,
                        'minimum_order_quantity': 5
                    }
                ],
                'categories': [
                    {
                        'id': 'PF',
                        'name': 'Perfumaria',
                        'composite_name': 'PF|Perfumaria',
                        'url': 'perfumaria/l/pf/',
                        'subcategories': [
                            {
                                'id': 'PFPF',
                                'name': 'Perfumes Femininos',
                                'composite_name': 'PFPF|Perfumes Femininos',  # noqa
                                'url': 'perfumes-femininos/perfumaria/s/pf/pfpf/',  # noqa
                            },
                            {
                                'id': 'PFPM',
                                'name': 'Perfumes Masculinos',
                                'composite_name': 'PFPM|Perfumes Masculinos',  # noqa
                                'url': 'perfumes-masculinos/perfumaria/s/pf/pfpm/',  # noqa
                            }
                        ]
                    }
                ],
                'dimensions': {
                    'width': 0.18,
                    'depth': 0.13,
                    'weight': 0.47,
                    'height': 0.44
                },
                'selections': {
                    '7985': ['12669'],
                    '0': ['10709', '10811', '12416', '8079']
                },
            },
            {
                'id': '8weuwe88we',
                'title': 'Caneca Xablau Branca - 350ml',
                'reference': 'CXB350ML',
                'is_delivery_available': True,
                'media': {
                    'videos': ['8weuwe88we'],
                    'audios': [
                        '/magazineluiza/audios/8weuwe88we/8weuwe88we.mp3'
                    ],
                    'podcasts': [
                        '/magazineluiza/podcasts/8weuwe88we/8weuwe88we.mp3'
                    ],
                    'images': [
                        '/{w}x{h}/caneca-xablau-branca-350ml-cxb350ml/magazineluiza/8weuwe88we/8weuwe88we.jpg',  # noqa
                        '/{w}x{h}/caneca-xablau-branca-350ml-cxb350ml/magazineluiza/8weuwe88we/8weuwe88we-A.jpg'  # noqa
                    ]
                },
                'sellers': [
                    {
                        'delivery_availability': 'nationwide',
                        'description': 'Magazine Luiza',
                        'id': 'magazineluiza',
                        'list_price': 234.56,
                        'price': 123.45,
                        'currency': 'BRL',
                        'sku': '8weuwe88we',
                        'status': 'published',
                        'sold_count': 10,
                        'stock_count': 82,
                        'stock_type': 'on_seller',
                        'sells_to_company': True,
                        'score': 1,
                        'order': 0,
                        'store_pickup_available': False,
                        'delivery_plus_1': False,
                        'delivery_plus_2': False,
                        'fulfillment': False,
                        'matching_uuid': 'a0069aee16d441cab4030cce086debbc',
                        'extra_data': [{'name': 'is_magalu_indica', 'value': 'true'}], # noqa
                        'parent_matching_uuid': '5c2275661d8f11ed861d0242ac120002' # noqa
                    }
                ],
                'categories': [
                    {
                        'id': 'PF',
                        'name': 'Perfumaria',
                        'composite_name': 'PF|Perfumaria',
                        'url': 'perfumaria/l/pf/',
                        'subcategories': [
                            {
                                'id': 'PFPF',
                                'name': 'Perfumes Femininos',
                                'composite_name': 'PFPF|Perfumes Femininos',  # noqa
                                'url': 'perfumes-femininos/perfumaria/s/pf/pfpf/',  # noqa
                            },
                            {
                                'id': 'PFPM',
                                'name': 'Perfumes Masculinos',
                                'composite_name': 'PFPM|Perfumes Masculinos',  # noqa
                                'url': 'perfumes-masculinos/perfumaria/s/pf/pfpm/',  # noqa
                            }
                        ]
                    }
                ],
                'dimensions': {
                    'width': 0.18,
                    'depth': 0.13,
                    'weight': 0.47,
                    'height': 0.44
                },
                'selections': {
                    '7985': ['12669'],
                    '0': ['10709', '10811', '12416', '8079']
                },
            },
            {
                'id': '623728900',
                'title': 'Caneca Xablau Branca - 200ml',
                'reference': 'CXB200ML',
                'is_delivery_available': True,
                'media': {
                    'videos': ['623728900'],
                    'audios': [
                        '/magazineluiza/audios/623728900/623728900.mp3'
                    ],
                    'podcasts': [
                        '/magazineluiza/podcasts/623728900/623728900.mp3'
                    ],
                    'images': [
                        '/{w}x{h}/caneca-xablau-branca-200ml-cxb200ml/magazineluiza/623728900/623728900.jpg',  # noqa
                        '/{w}x{h}/caneca-xablau-branca-200ml-cxb200ml/magazineluiza/623728900/623728900-A.jpg'  # noqa
                    ]
                },
                'sellers': [
                    {
                        'delivery_availability': 'nationwide',
                        'delivery_plus_1': False,
                        'delivery_plus_2': False,
                        'description': 'Seu Zeh',
                        'id': 'seuzeh',
                        'list_price': 134.56,
                        'price': 23.45,
                        'currency': 'BRL',
                        'sku': '819283iqw',
                        'status': 'published',
                        'sold_count': 10,
                        'stock_count': 31,
                        'stock_type': 'on_seller',
                        'sells_to_company': True,
                        'score': 0,
                        'order': 0,
                        'store_pickup_available': False,
                        'fulfillment': False,
                        'matching_uuid': '57f5031ad56949ac92bff1873b3f5b4a',
                        'extra_data': None,
                        'parent_matching_uuid': '5c2275661d8f11ed861d0242ac120002' # noqa

                    },
                    {
                        'delivery_availability': 'nationwide',
                        'description': 'Magazine Luiza',
                        'id': 'magazineluiza',
                        'list_price': 434.56,
                        'price': 323.45,
                        'currency': 'BRL',
                        'sku': '623728900',
                        'status': 'published',
                        'sold_count': 10,
                        'stock_count': 0,
                        'stock_type': 'on_seller',
                        'sells_to_company': True,
                        'score': 1,
                        'order': 1,
                        'store_pickup_available': False,
                        'delivery_plus_1': False,
                        'delivery_plus_2': False,
                        'fulfillment': True,
                        'matching_uuid': 'a0069aee16d441cab4030cce086debbc',
                        'extra_data': [{'name': 'is_magalu_indica', 'value': 'true'}],  # noqa
                        'parent_matching_uuid': '5c2275661d8f11ed861d0242ac120002', # noqa
                        'minimum_order_quantity': 10
                    }
                ],
                'categories': [
                    {
                        'id': 'PF',
                        'name': 'Perfumaria',
                        'composite_name': 'PF|Perfumaria',
                        'url': 'perfumaria/l/pf/',
                        'subcategories': [
                            {
                                'id': 'PFPF',
                                'name': 'Perfumes Femininos',
                                'composite_name': 'PFPF|Perfumes Femininos',  # noqa
                                'url': 'perfumes-femininos/perfumaria/s/pf/pfpf/',  # noqa
                            },
                            {
                                'id': 'PFPM',
                                'name': 'Perfumes Masculinos',
                                'composite_name': 'PFPM|Perfumes Masculinos',  # noqa
                                'url': 'perfumes-masculinos/perfumaria/s/pf/pfpm/',  # noqa
                            }
                        ]
                    }
                ],
                'dimensions': {
                    'width': 0.18,
                    'depth': 0.13,
                    'weight': 0.47,
                    'height': 0.44
                },
                'selections': {
                    '7985': ['12669'],
                    '0': ['10709', '10811', '12416', '8079']
                },
            },
            {
                'id': '82323jjjj3',
                'title': 'Caneca Xablau Branca - 450ml',
                'reference': 'CXB450ML',
                'is_delivery_available': True,
                'media': {
                    'videos': ['82323jjjj3'],
                    'audios': [
                        '/seller-a/audios/82323jjjj3/82323jjjj3.mp3'
                    ],
                    'podcasts': [
                        '/seller-a/podcasts/82323jjjj3/82323jjjj3.mp3'
                    ],
                    'images': [
                        '/{w}x{h}/caneca-xablau-branca-450ml-cxb450ml/seller-a/82323jjjj3/82323jjjj3.jpg',  # noqa
                        '/{w}x{h}/caneca-xablau-branca-450ml-cxb450ml/seller-a/82323jjjj3/82323jjjj3-A.jpg'  # noqa
                    ]
                },
                'sellers': [
                    {
                        'delivery_availability': 'nationwide',
                        'description': 'Seller A',
                        'id': 'seller_a',
                        'list_price': 64.56,
                        'price': 33.45,
                        'currency': 'BRL',
                        'sku': '82323jjjj3',
                        'status': 'published',
                        'sold_count': 10,
                        'stock_count': 3,
                        'stock_type': 'on_supplier',
                        'sells_to_company': True,
                        'score': 0,
                        'order': 0,
                        'store_pickup_available': False,
                        'delivery_plus_1': False,
                        'delivery_plus_2': False,
                        'matching_uuid': 'af6f8d9cb9a64bcd8023e21c5a797b85',
                        'extra_data': [{'name': 'is_magalu_indica', 'value': 'true'}],  # noqa
                        'parent_matching_uuid': '5c2275661d8f11ed861d0242ac120002' # noqa

                    },
                    {
                        'delivery_availability': 'nationwide',
                        'description': 'Seller C',
                        'id': 'seller_c',
                        'list_price': 74.56,
                        'price': 53.45,
                        'currency': 'BRL',
                        'sku': 'ou23ou23ou',
                        'status': 'published',
                        'sold_count': 10,
                        'stock_count': 18,
                        'stock_type': 'on_supplier',
                        'sells_to_company': True,
                        'score': 0,
                        'order': 1,
                        'store_pickup_available': False,
                        'delivery_plus_1': False,
                        'delivery_plus_2': False,
                        'fulfillment': False,
                        'matching_uuid': 'af6f8d9cb9a64bcd8023e21c5a797b85',
                        'extra_data': [{'name': 'is_magalu_indica', 'value': 'true'}],  # noqa
                        'parent_matching_uuid': '5c2275661d8f11ed861d0242ac120002' # noqa

                    },
                    {
                        'delivery_availability': 'unavailable',
                        'description': 'Seller B',
                        'id': 'seller_b',
                        'list_price': 14.56,
                        'price': 13.45,
                        'currency': 'BRL',
                        'sku': '098asdwe28',
                        'status': 'published',
                        'sold_count': 10,
                        'stock_count': 0,
                        'stock_type': 'on_supplier',
                        'sells_to_company': True,
                        'score': 0,
                        'order': 2,
                        'store_pickup_available': False,
                        'delivery_plus_1': False,
                        'delivery_plus_2': False,
                        'matching_uuid': None,
                        'extra_data': None,
                        'parent_matching_uuid': None
                    }
                ],
                'categories': [
                    {
                        'id': 'PF',
                        'name': 'Perfumaria',
                        'composite_name': 'PF|Perfumaria',
                        'url': 'perfumaria/l/pf/',
                        'subcategories': [
                            {
                                'id': 'PFPF',
                                'name': 'Perfumes Femininos',
                                'composite_name': 'PFPF|Perfumes Femininos',  # noqa
                                'url': 'perfumes-femininos/perfumaria/s/pf/pfpf/',  # noqa
                            },
                            {
                                'id': 'PFPM',
                                'name': 'Perfumes Masculinos',
                                'composite_name': 'PFPM|Perfumes Masculinos',  # noqa
                                'url': 'perfumes-masculinos/perfumaria/s/pf/pfpm/',  # noqa
                            }
                        ]
                    }
                ],
                'dimensions': {
                    'width': 0.18,
                    'depth': 0.13,
                    'weight': 0.47,
                    'height': 0.44
                },
                'selections': {
                    '7985': ['12669'],
                    '0': ['10709', '10811', '12416', '8079']
                },
            },
            {
                'id': '723uwej2u3',
                'title': 'Caneca Xablau Branca - 150ml',
                'reference': 'CXB150ML',
                'is_delivery_available': False,
                'media': {
                    'videos': ['723uwej2u3'],
                    'audios': [
                        '/casaamerica/audios/723uwej2u3/723uwej2u3.mp3'
                    ],
                    'podcasts': [
                        '/casaamerica/podcasts/723uwej2u3/723uwej2u3.mp3'
                    ],
                    'images': [
                        '/{w}x{h}/caneca-xablau-branca-150ml-cxb150ml/casaamerica/723uwej2u3/723uwej2u3.jpg',  # noqa
                        '/{w}x{h}/caneca-xablau-branca-150ml-cxb150ml/casaamerica/723uwej2u3/723uwej2u3-A.jpg'  # noqa
                    ]
                },
                'sellers': [
                    {
                        'delivery_availability': 'nationwide',
                        'description': 'Casa America',
                        'id': 'casaamerica',
                        'list_price': 44.56,
                        'price': 33.45,
                        'currency': 'BRL',
                        'sku': '723uwej2u3',
                        'status': 'published',
                        'sold_count': 10,
                        'stock_count': 0,
                        'stock_type': 'on_supplier',
                        'sells_to_company': True,
                        'score': 0,
                        'order': 0,
                        'store_pickup_available': False,
                        'delivery_plus_1': False,
                        'delivery_plus_2': False,
                        'matching_uuid': None,
                        'extra_data': None,
                        'parent_matching_uuid': None
                    }
                ],
                'categories': [
                    {
                        'id': 'PF',
                        'name': 'Perfumaria',
                        'composite_name': 'PF|Perfumaria',
                        'url': 'perfumaria/l/pf/',
                        'subcategories': [
                            {
                                'id': 'PFPF',
                                'name': 'Perfumes Femininos',
                                'composite_name': 'PFPF|Perfumes Femininos',  # noqa
                                'url': 'perfumes-femininos/perfumaria/s/pf/pfpf/',  # noqa
                            },
                            {
                                'id': 'PFPM',
                                'name': 'Perfumes Masculinos',
                                'composite_name': 'PFPM|Perfumes Masculinos',  # noqa
                                'url': 'perfumes-masculinos/perfumaria/s/pf/pfpm/',  # noqa
                            }
                        ]
                    }
                ],
                'dimensions': {
                    'width': 0.18,
                    'depth': 0.13,
                    'weight': 0.47,
                    'height': 0.44
                },
                'selections': {
                    '7985': ['12669'],
                    '0': ['10709', '10811', '12416', '8079']
                },
            }
        ]
    }


@pytest.fixture
def expected_extracted_skus():
    return [
        (
            '723829300',
            'magazineluiza',
        ),
        (
            '8weuwe88we',
            'magazineluiza',
        ),
        (
            '623728900',
            'magazineluiza',
        ),
        (
            '819283iqw',
            'seuzeh',
        ),
        (
            '82323jjjj3',
            'seller_a',
        ),
        (
            '098asdwe28',
            'seller_b',
        ),
        (
            'ou23ou23ou',
            'seller_c',
        ),
        (
            '723uwej2u3',
            'casaamerica',
        )
    ]
