import pytest

from taz.consumers.product_exporter.scopes.helpers import (
    CacheCategories,
    ScopeHelper
)


class TestScopeHelper:

    @pytest.fixture
    def helper(self):
        return ScopeHelper()

    def teardown_method(self):
        cache = CacheCategories()
        cache.categories.clear()

    def test_scope_helper_get_categories_detail(
        self,
        helper,
        product_dict,
        categories_dicts
    ):
        categories = [
            {
                'subcategories': [
                    {'id': 'LAVA'},
                    {'id': 'ED'}
                ],
                'id': 'ED'
            }
        ]
        result = helper.get_categories_detail(categories)

        assert result == [{
            'subcategories': [
                {
                    'id': 'LAVA',
                    'url': 'maquina-de-lavar/eletrodomesticos/s/ed/lava/',
                    'name': 'Máquina de Lavar'
                },
                {
                    'id': 'ED',
                    'url': 'eletrodomesticos/l/ed/',
                    'name': 'Eletrodomésticos'
                }
            ],
            'id': 'ED',
            'url': 'eletrodomesticos/l/ed/',
            'name': 'Eletrodomésticos'
        }]

    def test_when_category_id_and_subcategory_id_are_equal_then_should_process_with_success( # noqa
        self,
        helper,
        categories_dicts
    ):
        categories = [{'subcategories': [{'id': 'ED'}], 'id': 'ED'}]
        result = helper.get_categories_detail(categories)

        assert result == [{
            'subcategories': [{
                'id': 'ED',
                'url': 'eletrodomesticos/l/ed/',
                'name': 'Eletrodomésticos'
            }],
            'id': 'ED',
            'url': 'eletrodomesticos/l/ed/',
            'name': 'Eletrodomésticos'
        }]

    def test_scope_helper_get_categories_detail_should_return_source(
        self,
        helper,
        product_dict
    ):
        categories = [{'subcategories': [{'id': 'LAVA'}], 'id': 'ED'}]
        result = helper.get_categories_detail(categories)

        assert result == categories

    def test_scope_helper_get_seller_name(self, helper, product_dict):
        result = helper.get_seller_name(product_dict['seller_id'])
        assert result == 'magazineluiza'

    def test_when_matching_successful_then_return_offer_id(
        self,
        helper,
        id_correlations_products_dict,
        raw_products_dict,
        unified_objects_dict
    ):
        offer_id_info = helper.get_offer_id_and_id_correlations(
            seller_id='zattini', sku='E86-2541-006-02'
        )
        offer_id = offer_id_info.get('offer_id')
        id_correlations = offer_id_info.get('id_correlations')

        unified_objects_dict['canonical_ids'].sort()
        assert offer_id == unified_objects_dict['id']
        assert len(id_correlations) == 6
        assert all([a == b for a, b in zip(id_correlations, unified_objects_dict['canonical_ids'])])  # noqa

    def test_collection_id_correlations_none_should_return_none(
        self,
        helper
    ):
        assert helper.get_offer_id_and_id_correlations(
            seller_id='zattini', sku='E86-2541-006-02'
        ) == {}

    def test_collection_unified_objects_none_should_return_none(
        self,
        helper,
        id_correlations_products_dict
    ):
        assert helper.get_offer_id_and_id_correlations(
            seller_id='zattini', sku='E86-2541-006-02'
        ) == {}

    def test_scope_helper_get_medias(
        self,
        helper,
        store_media,
        product_dict
    ):

        result = helper.get_medias(
            product_dict['seller_id'],
            product_dict['sku']
        )
        del result['_id']

        assert result == {
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
            ],
            'seller_id': 'magazineluiza',
            'sku': '213445900'
        }

    def test_scope_helper_get_medias_should_return_none(
        self,
        helper,
        product_dict
    ):
        result = helper.get_medias(
            product_dict['seller_id'],
            product_dict['sku']
        )

        assert not result

    def test_scope_helper_get_enriched_products(
        self,
        helper,
        enriched_product,
        product_dict,
        mongo_database
    ):
        mongo_database.enriched_products.save(enriched_product)
        del enriched_product['_id']

        result = helper.get_enriched_products(
            product_dict['seller_id'],
            product_dict['sku'],
        )

        assert result == [enriched_product]

    def test_scope_helper_get_enriched_products_should_return_empty(
        self,
        helper,
        product_dict
    ):
        result = helper.get_enriched_products(
            product_dict['seller_id'],
            product_dict['sku']
        )

        assert result == []

    @pytest.fixture
    def product_json(self):
        return {"navigation_id": "foo", "user": "bugsbunny"}

    @pytest.fixture
    def save_unpublished_products(self, mongo_database, product_json):
        mongo_database.unpublished_products.insert_one(product_json)

    def test_create_unavailable_product_payload_should_return_payload(
        self,
        helper,
        save_unpublished_products
    ):
        payload = helper.create_unavailable_product_payload(
            navigation_id='foo'
        )
        assert payload == {
            'availability': 'out of stock',
            'stock_count': 0,
            'active': False
        }

    def test_create_unavailable_product_payload_should_return_empty_dict(
        self,
        helper
    ):
        assert helper.create_unavailable_product_payload(
            navigation_id=None
        ) == {}
