import pytest


@pytest.fixture
def product():
    return {
        'main_variation': True,
        'seller_id': 'magazineluiza',
        'seller_description': 'Magazine Luiza',
        'description': 'O console Xbox 360 está mais elegante.',
        'review_count': 0,
        'review_score': 0,
        'updated_at': '2015-07-19T00:26:56.280000',
        'created_at': '2014-03-28T06:54:47.160000',
        'price': 899.0,
        'ean': '0885370592634',
        'brand': 'Microsoft',
        'reference': 'Cartão Xbox Live 1 Mês - Microsoft',
        'variations': [{
            'type': 'voltage',
            'value': 'Bivolt'
        }],
        'title': 'Xbox 360 4GB com Controle sem Fio',
        'main_category': {
            'id': 'GA',
            'subcategory': {
                'id': 'GACO'
            }
        },
        'categories': [{
            'subcategories': [{
                'id': 'XBOX',
            }],
            'id': 'GA',
        }],
        'type': 'product',
        'dimensions': {
            'height': '0.29',
            'width': '0.18',
            'weight': '4.1',
            'depth': '0.31'
        },
        'sold_count': 0,
        'technical_price': 754.04,
        'sku': '043071200',
        'navigation_id': '043071200',
        'parent_sku': '0430712',
        'list_price': 899.0,
        'is_active': True,
        'bundles': {
            '176608400': {'price': '179.00', 'quantity': '1'},
            '201746100': {'price': '95.00', 'quantity': '1'}
        },
        'gift_product': '150658700'
    }


@pytest.fixture
def seller_info():
    return {
        'is_active': True,
        'sells_to_company': False,
        'name': 'Magalu'
    }
