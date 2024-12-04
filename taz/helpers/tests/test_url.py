import pytest

from taz.helpers.url import generate_product_url, remove_url_param


class TestHelperUrl:

    @pytest.fixture
    def categories(self):
        return [{
            'id': 'UD',
            'subcategories': [
                {'id': 'UDCA'}, {'id': 'UDCG'}
            ]
        }]

    @pytest.fixture
    def variation(self):
        return {
            'sold_count': 14,
            'navigation_id': '82323jjjj3',
            'parent_sku': '82323jjjj3',
            'type': 'product',
            'description': 'Caneca xablau batuta',
            'seller_id': 'seller_a',
            'dimensions': {
                'weight': 0.47,
                'width': 0.18,
                'height': 0.44,
                'depth': 0.13
            },
            'title': 'Caneca Xablau Branca - 450ml',
            'brand': '+Canecas Xablau',
            'review_count': 9,
            'sku': '82323jjjj3',
            'sells_to_company': False,
            'seller_description': 'Seller A',
            'reference': 'CXB450ML',
            'categories': [{
                'id': 'UD',
                'subcategories': [{
                    'id': 'UDCA'
                }, {
                    'id': 'UDCG'
                }]
            }],
            'grade': 500,
            'main_variation': False,
            'review_score': 4.1,
            'updated_at': '2016-08-17T06:17:03.503000',
            'attributes': [{
                'label': 'Capacidade',
                'value': '450ml',
                'type': 'capacity'
            }],
            'ean': '3123123999999',
            'disable_on_matching': False,
            'created_at': '2016-08-17T06:17:03.503000'
        }

    @pytest.mark.parametrize('product_id,variation_inputs,expected_url', [
        (
            '2162346',
            {
                'title': 'Smartphone Motorola Moto G 4ª Geração Plus 32GB',
                'reference': 'Preto Dual Chip 4G Câm 16MP + Selfie 5MP Tela 5.5"',  # noqa
                'id': '2162346',
                'categories': [{'id': 'TE', 'subcategories': [{'id': 'MDVX'}]}]
            },
            'smartphone-motorola-moto-g-4a-geracao-plus-32gb-preto-dual-chip-4g-cam-16mp-selfie-5mp-tela-5-5/p/2162346/te/mdvx/'  # noqa
        ),
        (
            '123qweasd',
            {
                'title': 'Caneca Xablau',
                'id': '123qweasd',
                'categories': [{'id': 'UD', 'subcategories': [{'id': 'UDXD'}]}]
            },
            'caneca-xablau/p/123qweasd/ud/udxd/'
        ),
        (
            '123qweasd',
            {
                'title': 'Caneca Xablau',
                'id': '123qweasd',
                'categories': []
            },
            ''
        ),
        (
            '2162346',
            {
                'title': 'Smartphone Motorola Moto G 4ª Geração Plus 32GB',
                'reference': None,
                'id': '2162346',
                'categories': [{'id': 'TE', 'subcategories': [{'id': 'MDVX'}]}]
            },
            'smartphone-motorola-moto-g-4a-geracao-plus-32gb/p/2162346/te/mdvx/'  # noqa
        )
    ])
    def test_generate_product_url(
        self,
        product_id,
        variation_inputs,
        expected_url
    ):
        generated_url = generate_product_url(
            product_id,
            variation_inputs,
            variation_inputs['categories']
        )

        assert generated_url == expected_url

    def test_generate_product_url_without_subcategories(
        self
    ):
        expected_url = 'smartphone-motorola-moto-g-4a-geracao-plus-32gb/p/2162346/te/rcnm/' # noqa
        product_id = '2162346'
        variation_inputs = {
            'title': 'Smartphone Motorola Moto G 4ª Geração Plus 32GB',
            'reference': None,
            'id': '2162346',
            'categories': [{'id': 'TE'}]
        }
        generated_url = generate_product_url(
            product_id,
            variation_inputs,
            variation_inputs['categories']
        )

        assert generated_url == expected_url

    @pytest.mark.parametrize('url,param_name,output_url', [
        (
            'https://api.magalu/v1/cover/123?access_token=secret_token&filter=name', # noqa
            'access_token',
            'https://api.magalu/v1/cover/123?filter=name',
        ),
        (
            'https://api.magalu/v1/cover/123?access_token=secret_token',
            'access_token',
            'https://api.magalu/v1/cover/123',
        ),
        (
            'https://api.magalu/v1/cover/123',
            'access_token',
            'https://api.magalu/v1/cover/123'
        ),
        (
            'https://api.magalu/v1/cover/123/',
            'access_token',
            'https://api.magalu/v1/cover/123/'
        ),
        (
            'https://api.magalu/v1/cover/123?access_token=secret_token&filter=name', # noqa
            'filter',
            'https://api.magalu/v1/cover/123?access_token=secret_token',
        ),
        (
            'https://api.magalu/v1/cover/123?access_token=secret_token&filter=name&order=asc&color=blue', # noqa
            'filter',
            'https://api.magalu/v1/cover/123?access_token=secret_token&order=asc&color=blue', # noqa
        ),
    ])
    def test_remove_url_param(self, url, param_name, output_url):
        result = remove_url_param(url, param_name)
        assert result == output_url
