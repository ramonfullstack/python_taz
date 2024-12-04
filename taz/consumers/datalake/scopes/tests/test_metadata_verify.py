from typing import Dict
from unittest.mock import patch

import pytest
from pymongo.database import Database
from simple_settings import settings

from taz.constants import (
    MAGAZINE_LUIZA_SELLER_ID,
    META_TYPE_PRODUCT_AVERAGE_RATING,
    META_TYPE_PRODUCT_TOTAL_REVIEW_COUNT
)
from taz.consumers.datalake.scopes.metadata_verify import (
    Scope as MetadataVerifyScope
)
from taz.core.matching.common.samples import ProductSamples


class TestMetadataVerify:

    @pytest.fixture
    def product(self):
        return ProductSamples.magazineluiza_sku_193389600()

    @pytest.fixture
    def product_with_bundles(self):
        return ProductSamples.magazineluiza_sku_2090111_bundle()

    @pytest.fixture
    def save_product_with_bundles(
        self,
        product_with_bundles: Dict,
        mongo_database: Database
    ):
        mongo_database.raw_products.insert_one(product_with_bundles)

    @pytest.fixture
    def customer_behaviors(
        self,
        product: Dict
    ):
        return [
            {
                'product_id': product['navigation_id'],
                'type': META_TYPE_PRODUCT_TOTAL_REVIEW_COUNT,
                'value': 658
            },
            {
                'product_id': product['navigation_id'],
                'type': META_TYPE_PRODUCT_AVERAGE_RATING,
                'value': 4.730769230769231
            }
        ]

    @pytest.fixture
    def save_customer_behaviors(
        self,
        mongo_database: Database,
        customer_behaviors: Dict
    ):
        for customer_behavior in customer_behaviors:
            mongo_database.customer_behaviors.insert_one(customer_behavior)

    @pytest.fixture
    def save_product(
        self,
        product: Dict,
        mongo_database: Database
    ):
        mongo_database.raw_products.insert_one(product)

    @pytest.fixture
    def product_scope(self,):
        return MetadataVerifyScope(
            sku='193389600',
            seller_id=MAGAZINE_LUIZA_SELLER_ID
        )

    @pytest.fixture
    def product_with_bundles_scope(
        self,
        mongo_database,
        save_product_with_bundles,
        price,
        category,
        sub_category
    ):
        price['sku'] = '209011100'
        mongo_database.prices.insert_one(price)

        category['id'] = 'BB'
        mongo_database.categories.insert_one(category)

        sub_category['id'] = 'BBBU'
        sub_category['parent_id'] = 'BBBU'
        mongo_database.categories.insert_one(sub_category)

        return MetadataVerifyScope(
            sku='209011100',
            seller_id=MAGAZINE_LUIZA_SELLER_ID
        )

    @pytest.fixture
    def product_inactive_scope(
        self,
        save_product_inactive,
        save_price,
        save_category,
        save_sub_category,
        save_customer_behaviors
    ):
        return MetadataVerifyScope(
            sku='193389600',
            seller_id=MAGAZINE_LUIZA_SELLER_ID
        )

    @pytest.fixture
    def product_without_scope(
        self,
        save_product_inactive,
        save_price,
        save_category,
        save_sub_category,
        save_customer_behaviors
    ):
        return MetadataVerifyScope(
            sku='193389600',
            seller_id=MAGAZINE_LUIZA_SELLER_ID
        )

    @pytest.fixture
    def product_stock_scope(
        self,
        save_product,
        save_price,
        save_category,
        save_sub_category,
        save_customer_behaviors
    ):
        return MetadataVerifyScope(
            sku='193389600',
            seller_id=MAGAZINE_LUIZA_SELLER_ID
        )

    @pytest.fixture
    def product_without_price_scope(
        self,
        save_product,
        save_category,
        save_sub_category,
        save_customer_behaviors
    ):
        return MetadataVerifyScope(
            sku='193389600',
            seller_id=MAGAZINE_LUIZA_SELLER_ID
        )

    @pytest.fixture
    def product_without_category(
        self,
        save_product,
        save_price,
        save_customer_behaviors
    ):
        return MetadataVerifyScope(
            sku='193389600',
            seller_id=MAGAZINE_LUIZA_SELLER_ID
        )

    @pytest.fixture
    def product_without_customer_behaviors(
        self,
        save_product,
        save_category,
        save_price
    ):
        return MetadataVerifyScope(
            sku='193389600',
            seller_id=MAGAZINE_LUIZA_SELLER_ID
        )

    @pytest.fixture
    def product_category_scope(self, save_product, save_price):
        return MetadataVerifyScope(
            sku='193389600',
            seller_id=MAGAZINE_LUIZA_SELLER_ID
        )

    @pytest.fixture
    def get_fallback_category_mock(self):
        return patch.object(MetadataVerifyScope, '_get_fallback_category')

    def test_get_data_scope_product_should_return_product(
        self,
        product_scope,
        product,
        mongo_database,
        mock_matching_uuid,
        save_price,
        save_category,
        save_sub_category,
        save_customer_behaviors,
        sub_category,
        sub_category_other,
        category
    ):
        product['matching_uuid'] = mock_matching_uuid
        mongo_database.raw_products.insert_one(product)

        scope_product = product_scope.get_data()

        sub_category.pop('_id', None)
        category.pop('_id', None)
        sub_category_other.pop('_id', None)

        assert scope_product == {
            'title': 'Smart TV LED 55” Samsung 55K5300',
            'dimensions': {
                'height': 0.86,
                'weight': 21.2,
                'depth': 0.17,
                'width': 1.33
            },
            'navigation_id': '193389600',
            'parent_sku': '1933891',
            'attributes': [
                {
                    'value': "55'",
                    'type': 'inch'
                }
            ],
            'review_score': 0,
            'type': 'product',
            'ean': '7892509088329',
            'sells_to_company': True,
            'matching_strategy': 'SINGLE_SELLER',
            'seller_id': 'magazineluiza',
            'main_category': {
                'subcategory': {
                    'id': 'ELIT'
                },
                'id': 'ET'
            },
            'review_count': 0,
            'brand': 'samsung',
            'main_variation': True,
            'sold_count': 85,
            'disable_on_matching': False,
            'seller_description': 'Magazine Luiza',
            'updated_at': '2017-07-10T10:55:35.170000',
            'created_at': '2016-08-10T07:38:30.803000',
            'categories': [
                {
                    **category,
                    'subcategories': [
                        sub_category,
                        sub_category_other
                    ]
                }
            ],
            'sku': '193389600',
            'grade': 10,
            'description': 'Com a Tv Samsung 55K5300 você vai ter Design inovador que combina modernidade com funcionalidade. Com áudio frontal, você experimenta muito mais clareza no som para aproveitar muito mais seus programas favoritos. Navegue no novo menu e acesse seus aplicativos e canais favoritos com poucos cliques, inclusive os conteúdos do seu smartphone podem ser acessados na TV e sem a utilização de fios. Com acesso ao conteúdo smart você ganha muito mais opções na hora de escolher o que assistir e se divertir, são mais de 400 aplicativos disponíveis, de redes sociais, a cursos à distância.\n\nDesign Inovador: Auto Falantes frontais. Design inovador que combina modernidade com funcionalidade.\nCom áudio frontal, você experimenta muito mais clareza no som para aproveitar muito mais seus\nprogramas favoritos.\n\nConteúdo Smart: Centenas de aplicativos e serviços de entretenimento. Além disso, você encontra a mais completa oferta de serviços de vídeo on demand e Games, sem precisar de um videogame. \n\nPossui processador Quad Core. Sua Smart TV mais rápida e fácil de navegar. Melhor performance com aplicativos mais rápidos e controles mais precisos.\n', # noqa
            'reference': 'Conversor Digital 2 HDMI 1 USB',
            'active': True,
            'stock': True,
            'product_average_rating': 4.730769230769231,
            'product_total_review_count': 658,
            'scope_name': 'product',
            'extra_data': None,
            'fulfillment': None,
            'matching_uuid': mock_matching_uuid,
            'parent_matching_uuid': None
        }

    def test_get_data_should_return_product_with_bundles(
        self,
        product_with_bundles_scope
    ):
        product_result = product_with_bundles_scope.get_data()

        assert sorted(
            product_result['bundles'],
            key=lambda product: product['sku']
        ) == [
            {
                'sku': '176608400',
                'seller_id': MAGAZINE_LUIZA_SELLER_ID,
                'price': '179.00',
                'quantity': 1
            },
            {
                'sku': '201746100',
                'seller_id': MAGAZINE_LUIZA_SELLER_ID,
                'price': '95.00',
                'quantity': 1
            }
        ]

    def test_get_data_should_return_float_zeros_review_rating(
        self,
        product_without_customer_behaviors,
        get_fallback_category_mock
    ):
        with get_fallback_category_mock:
            product_result = product_without_customer_behaviors.get_data()
            assert product_result['product_average_rating'] == 0.0

    def test_get_data_should_return_product_inactive(
        self,
        product_inactive_scope,
        save_product,
        save_price,
        save_category
    ):
        product_result = product_inactive_scope.get_data()
        assert product_result['active'] is False

    def test_get_data_should_return_product_without_stock(
        self,
        product_without_price_scope
    ):
        product_result = product_without_price_scope.get_data()
        assert product_result['stock'] == 0

    def test_get_data_should_return_without_categories(
        self,
        product_category_scope,
        categories_expected
    ):
        product_result = product_category_scope.get_data()
        assert product_result['categories'] == categories_expected

    def test_get_data_with_unknown_subcategory_should_return_default_values(
        self,
        mongo_database,
        save_price,
        save_product,
        product,
        logger_stream
    ):
        categories = [
            {
                'id': 'ET',
                'active': True
            },
            {
                'id': 'RC',
                'description': 'Recem Chegados',
                'slug': 'recem-chegados',
                'parent_id': 'ML',
                'active': True
            }, {
                'id': 'RCNM',
                'description': 'No Magalu',
                'slug': 'no-magalu',
                'parent_id': 'RC',
                'active': True
            }
        ]

        for c in categories:
            mongo_database.categories.insert_one(c)

        product_scope = MetadataVerifyScope(
            sku=product['sku'],
            seller_id=product['seller_id']
        )

        product_result = product_scope.get_data()

        msg = 'Product with sku:{sku}, seller_id:{seller_id} and category:{category_id} not found subcategories in categories collection'.format( # noqa
            sku=product['sku'],
            seller_id=product['seller_id'],
            category_id=product['categories'][0]['id']
        )

        assert msg in logger_stream.getvalue()
        assert product_result['categories'][0]['id'] == settings.FALLBACK_MISSING_CATEGORY  # noqa
        assert product_result['categories'][0]['subcategories'][0]['id'] == settings.FALLBACK_MISSING_SUBCATEGORY  # noqa

    def test_get_data_with_product_without_subcategories_should_return_default_values(  # noqa
        self,
        mongo_database,
        save_price,
        product,
        logger_stream
    ):

        product['categories'] = [{
            'description': 'Armarinhos',
            'id': 'AM'
        }]

        mongo_database.raw_products.insert_one(product)

        categories = [{
            'id': 'RC',
            'description': 'Recem Chegados',
            'slug': 'recem-chegados',
            'parent_id': 'ML',
            'active': True
        }, {
            'id': 'RCNM',
            'description': 'No Magalu',
            'slug': 'no-magalu',
            'parent_id': 'RC',
            'active': True
        }]

        for c in categories:
            mongo_database.categories.insert_one(c)

        product_result = MetadataVerifyScope(
            sku=product['sku'],
            seller_id=product['seller_id']
        ).get_data()

        msg = 'Product with sku:{sku} seller_id:{seller_id} and category:{category_id} without subcategories'.format( # noqa
            sku=product['sku'],
            seller_id=product['seller_id'],
            category_id=product['categories'][0]['id']
        )

        assert msg in logger_stream.getvalue()
        assert product_result['categories'][0]['id'] == settings.FALLBACK_MISSING_CATEGORY  # noqa
        assert product_result['categories'][0]['subcategories'][0]['id'] == settings.FALLBACK_MISSING_SUBCATEGORY  # noqa

    def test_get_data_with_extra_data_should_return_payload_included_extra_data(  # noqa
        self,
        mongo_database,
        product_scope,
        product,
        mock_extra_data
    ):
        extra_data = mock_extra_data['extra_data']
        product.update({'extra_data': extra_data})

        mongo_database.raw_products.save(product)
        product_result = product_scope.get_data()

        assert product_result['extra_data'] == extra_data

    @pytest.mark.parametrize('payload', [
        {'parent_matching_uuid': '27006db39089436fb52c5c00c8464034'},
        {}
    ])
    def test_get_data_product_should_return_payload_with_parent_matching_uuid(
        self,
        mongo_database,
        product_scope,
        product,
        payload
    ):
        product.update(payload)
        mongo_database.raw_products.save(product)

        product_result = product_scope.get_data()

        assert product_result['parent_matching_uuid'] == payload.get(
            'parent_matching_uuid'
        )

    def test_get_data_should_return_payload_with_ordered_subcategories(
        self,
        mongo_database,
    ):

        category = {
            'id': 'ED',
            'description': 'Eletrodomésticos',
            'slug': 'eletrodomesticos',
            'parent_id': 'ML',
            'url': 'eletrodomesticos/l/ed/',
            'active': True
        }

        subcategories = [{
            'id': 'FEAG',
            'description': 'Forno de embutir a gás',
            'slug': 'forno-de-embutir-a-gas',
            'parent_id': 'ED',
            'url': 'forno-de-embutir-a-gas/eletrodomesticos/s/ed/feag/',
            'active': True
        }, {
            'id': 'FORN',
            'description': 'Fornos e Peças',
            'slug': 'fornos-e-pecas',
            'parent_id': 'ED',
            'url': 'fornos-e-pecas/eletrodomesticos/s/ed/forn/',
            'active': True
        }, {
            'id': 'EFRE',
            'description': 'Forno Embutir',
            'slug': 'forno-embutir',
            'parent_id': 'ED',
            'url': 'forno-embutir/eletrodomesticos/s/ed/efre/',
            'active': True
        }]

        for c in [category, *subcategories]:
            mongo_database.categories.insert_one(c)

        mongo_database.raw_products.insert_one(
            ProductSamples.magazineluiza_sku_216534900()
        )

        product_result = MetadataVerifyScope(
            sku='216534900',
            seller_id=MAGAZINE_LUIZA_SELLER_ID
        ).get_data()

        for sub in subcategories:
            sub.pop('_id', None)

        category.pop('_id', None)
        assert product_result['categories'] == [
            {
                **category,
                'subcategories': [
                    subcategories[2],
                    subcategories[0],
                    subcategories[1]
                ]
            }
        ]
