from unittest.mock import ANY
from uuid import uuid4

import pytest

from taz.constants import (
    MAGAZINE_LUIZA_SELLER_ID,
    SOURCE_DATASHEET,
    SOURCE_GENERIC_CONTENT,
    SOURCE_HECTOR,
    SOURCE_METABOOKS,
    SOURCE_OMNILOGIC,
    SOURCE_RECLASSIFICATION_PRICE_RULE,
    SOURCE_TAZ
)
from taz.consumers.product_exporter.scopes.product_features import Scope
from taz.core.matching.common.enriched_products import EnrichedProductSamples


class TestProductFeaturesScope:

    @pytest.fixture
    def sku(self):
        return '123456789'

    @pytest.fixture
    def seller_id(self):
        return 'test'

    @pytest.fixture
    def scope(self, sku, seller_id):
        return Scope(sku=sku, seller_id=seller_id)

    @pytest.fixture
    def categories(self):
        return [
            {
                'id': 'LI',
                'parent_id': 'ML',
                'description': 'Livros',
                'slug': 'livros',
                'url': 'livros/l/li/',
                'active': True
            },
            {
                'id': 'LIAJ',
                'parent_id': 'LI',
                'description': 'Livro de Autoajuda',
                'slug': 'livro-de-autoajuda',
                'url': 'livro-de-autoajuda/livros/s/li/liaj/',
                'active': True
            }
        ]

    @pytest.fixture
    def enriched_products(self, sku, seller_id):
        generic_content = EnrichedProductSamples.generic_content_sku_fd3e322aab() # noqa
        generic_content.update({'sku': sku, 'seller_id': seller_id})

        return [
            {
                'sku': sku,
                'seller_id': seller_id,
                'source': SOURCE_HECTOR,
                'classifications': [
                    {'product_type': 'Livro_hector'},
                ]
            },
            {
                'sku': sku,
                'seller_id': seller_id,
                'source': SOURCE_OMNILOGIC,
                'entity': 'Livro_omnilogic',
            },
            {
                'sku': sku,
                'seller_id': seller_id,
                'source': SOURCE_METABOOKS,
                'entity': 'Livro_metabooks',
            },
            {
                'sku': sku,
                'seller_id': seller_id,
                'source': SOURCE_DATASHEET,
                'entity': 'Livro_datasheet',
            },
            generic_content
        ]

    @pytest.fixture
    def raw_product(self, sku, seller_id):
        return {
            'sku': sku,
            'seller_id': seller_id,
            'navigation_id': uuid4(),
            'parent_matching_uuid': uuid4(),
            'matching_uuid': uuid4(),
            'categories': [{
                'id': 'LI',
                'subcategories': [{'id': 'LIAJ'}]
            }],
        }

    @pytest.fixture
    def expected_payload(self, sku, seller_id, raw_product):
        return {
            'sku': sku,
            'seller': seller_id,
            'navigation_id': raw_product.get('navigation_id'),
            'product_type': 'Livro_metabooks',
            'parent_matching_uuid': raw_product.get('parent_matching_uuid'),
            'categories': [
                {
                    'id': 'LI',
                    'name': 'Livros',
                    'url': ANY,
                    'subcategories': [
                        {
                            'id': 'LIAJ',
                            'name': 'Livro de Autoajuda',
                            'url': ANY
                        }
                    ]
                }
            ],
            'matching_uuid': raw_product.get('matching_uuid'),
            'metadata': [{
                'source': SOURCE_GENERIC_CONTENT,
                'name': 'code_anatel',
                'value': 'HHHHH-AA-FFFFF'
            }],
            'datasheet': True,
            'timestamp': ANY,
            'source': SOURCE_TAZ
        }

    def test_should_return_complete_payload_with_success(
        self,
        scope,
        raw_product,
        enriched_products,
        categories,
        mongo_database,
        expected_payload
    ):
        mongo_database.categories.insert_many(categories)
        mongo_database.enriched_products.insert_many(enriched_products)
        mongo_database.raw_products.insert(raw_product)

        payload = scope.get_data()

        assert payload == expected_payload

    def test_source_hector(
        self,
        scope,
        raw_product,
        enriched_products,
        categories,
        mongo_database,
        expected_payload
    ):
        enriched_products[1]['entity'] = None
        enriched_products[2]['entity'] = None
        enriched_products[3]['entity'] = None

        mongo_database.categories.insert_many(categories)
        mongo_database.enriched_products.insert_many(enriched_products)
        mongo_database.raw_products.insert(raw_product)

        expected_payload['product_type'] = 'Livro_hector'

        payload = scope.get_data()

        assert payload == expected_payload

    def test_get_data_without_fields_not_found(
        self,
        scope,
        raw_product,
        enriched_products,
        categories,
        mongo_database,
        expected_payload
    ):
        raw_product['product_type'] = None
        raw_product['matching_uuid'] = None
        raw_product['parent_matching_uuid'] = None
        del enriched_products[-1]

        for enriched_product in enriched_products:
            if enriched_product.get('entity'):
                enriched_product['entity'] = None
            else:
                enriched_product['classifications'][0]['product_type'] = None

        mongo_database.categories.insert_many(categories)
        mongo_database.enriched_products.insert_many(enriched_products)
        mongo_database.raw_products.insert(raw_product)

        del expected_payload['matching_uuid']
        del expected_payload['parent_matching_uuid']
        del expected_payload['product_type']
        del expected_payload['categories']

        expected_payload['metadata'] = []

        payload = scope.get_data()

        assert payload == expected_payload

    def test_ignore_process_when_product_not_found_in_raw_products(
        self,
        scope,
        caplog,
    ):
        payload = scope.get_data()

        assert not payload
        assert (
            f'Product with sku:{scope.sku} and seller_id:{scope.seller_id}'
            'not found in raw products'
        )

    def test_ignore_seller_magazine_luiza(self):
        scope = Scope(
            sku='123456789',
            seller_id=MAGAZINE_LUIZA_SELLER_ID
        )

        payload = scope.get_data()
        assert not payload

    def test_source_reclassification(
        self,
        scope,
        raw_product,
        enriched_products,
        categories,
        mongo_database
    ):

        enriched_products.append(
            {
                'sku': scope.sku,
                'seller_id': scope.seller_id,
                'source': SOURCE_RECLASSIFICATION_PRICE_RULE,
                'product_type': 'Livro_reclassification',
            }
        )

        mongo_database.categories.insert_many(categories)
        mongo_database.enriched_products.insert_many(enriched_products)
        mongo_database.raw_products.insert(raw_product)

        expected = {
            'sku': scope.sku,
            'seller': scope.seller_id,
            'navigation_id': raw_product.get('navigation_id'),
            'timestamp': ANY,
            'product_type': 'Livro_reclassification',
            'parent_matching_uuid': raw_product.get('parent_matching_uuid'),
            'categories': ANY,
            'matching_uuid': raw_product.get('matching_uuid'),
            'metadata': [
                {
                    'name': 'code_anatel',
                    'source': SOURCE_GENERIC_CONTENT,
                    'value': 'HHHHH-AA-FFFFF'
                }
            ],
            'datasheet': True,
            'source': SOURCE_TAZ
        }

        payload = scope.get_data()

        assert payload == expected
