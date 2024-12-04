import copy

import pytest


@pytest.fixture
def raw_product_dict():
    return {
        'active': True,
        'brand': 'Tramontina',
        'categories': [{
            'id': 'UD',
            'subcategories': [{
                'id': 'PANL'
            }]
        }],
        'created_at': '2018-01-19T07:48:21.980000',
        'description': 'As dez peças do jogo de panelas compacto vermelho 20298/722 Turim, da Tramontina, vão fazer muito sucesso na sua cozinha. Feitas em alumínio, essas panelas possuem revestimento antiaderente Starflon T1, fazendo com que elas sejam muito mais simples de limpar e ainda ficam bonitas por mais tempo. E o melhor de tudo: podem ser usadas em fogão à gás, elétrico ou vitrocerâmico. É só escolher!\n\n\n\t\t\t',  # noqa
        'dimensions': {
            'depth': 0.4,
            'height': 0.25,
            'weight': 4.62,
            'width': 0.41
        },
        'ean': '7891112250536',
        'main_category': {
            'id': 'UD',
            'subcategory': {
                'id': 'PANL'
            }
        },
        'main_variation': False,
        'parent_sku': '1441299',
        'reference': 'de Alumínio Vermelho 10 Peças Turim 20298/722',
        'review_count': 0,
        'review_score': 0,
        'selections': {},
        'seller_description': 'Magazine Luiza',
        'seller_id': 'magazineluiza',
        'sku': '144129900',
        'sold_count': 0,
        'title': 'Jogo de Panelas Tramontina Antiaderente',
        'type': 'product',
        'updated_at': '2019-06-13T08:02:03.697000',
        'disable_on_matching': False,
        'offer_title': 'Jogo de Panelas Tramontina Antiaderente - de Alumínio Vermelho 10 Peças Turim 20298/722',  # noqa
        'grade': 1010,
        'navigation_id': '144129900',
        'matching_strategy': 'SINGLE_SELLER',
        'md5': '14840a616781d1eb399b33570041f698',
        'last_updated_at': '2019-06-13T11:07:48.178372',
        'sells_to_company': True
    }


@pytest.fixture
def product_json():
    return {
        'navigation_id': '123123000',
        'user': 'bugsbunny'
    }


@pytest.fixture
def save_unpublished_products(mongo_database, product_json):
    mongo_database.unpublished_products.insert_one(copy.copy(product_json))
