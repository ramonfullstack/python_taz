import datetime
from uuid import uuid4

import pytest

from taz.constants import (
    META_TYPE_PRODUCT_AVERAGE_RATING,
    META_TYPE_PRODUCT_TOTAL_REVIEW_COUNT,
    SINGLE_SELLER_STRATEGY,
    UNPUBLISHED_CODE,
    UNPUBLISHED_MESSAGE
)
from taz.core.matching.common.samples import ProductSamples
from taz.core.matching.strategies.single_seller.assembler import (
    ProductAssembler
)
from taz.core.matching.strategies.single_seller.matcher import ProductMatcher
from taz.core.matching.strategies.tests.helpers import generate_medias
from taz.utils import convert_id_to_nine_digits


class TestProductAssembler:

    @pytest.fixture
    def assembler(self):
        return ProductAssembler(SINGLE_SELLER_STRATEGY)

    @pytest.fixture
    def matcher(self):
        return ProductMatcher()

    @pytest.fixture
    def matched_ml_variations(
        self,
        assembler,
        mongo_database,
        matcher,
        assembler_matched_ml_variations
    ):
        for variation in assembler_matched_ml_variations:
            for i in range(3):
                mongo_database.id_correlations.insert_one({
                    'seller_id': variation['seller_id'],
                    'variation_id': uuid4().hex,
                    'product_id': uuid4().hex,
                    'sku': variation['sku']
                })

        return matcher.match_variations(
            ProductSamples.unmatched_ml_variation_with_parent()
        )

    @pytest.fixture
    def matched_mktplace_variations(
        self,
        assembler,
        mongo_database,
        matcher,
        assembler_matched_ml_variations
    ):
        unified_variation = matcher.match_variations(
            ProductSamples.seller_c_variation_with_parent()
        )
        return unified_variation

    def _store_media(self, mongo_database, variation):
        mongo_database.medias.insert_many(generate_medias(variation))

    @pytest.fixture
    def expected_product(self):
        return {
            'id': '723829300',
            'review_count': 12,
            'review_score': 2.5,
            'url': 'caneca-xablau-branca-250ml-cxb250ml/p/7238293/ud/udca/',
            'title': 'Caneca Xablau Branca - 250ml',
            'description': 'Caneca xablau branca belezinha',
            'reference': 'CXB250ML',
            'brand': '+Canecas Xablau',
            'canonical_ids': ['623728900', '723829300', '8weuwe88we'],
            'variations': [
                {
                    'id': '723829300',
                    'ean': '3123123123930',
                    'title': 'Caneca Xablau Branca - 250ml',
                    'description': 'Caneca xablau branca belezinha',
                    'reference': 'CXB250ML',
                    'dimensions': {
                        'width': 0.18,
                        'depth': 0.13,
                        'weight': 0.47,
                        'height': 0.44
                    },
                    'factsheet': {
                        'seller_id': 'magazineluiza',
                        'seller_sku': '723829300',
                    },
                    'sellers': [
                        {
                            'id': 'magazineluiza',
                            'description': 'Magazine Luiza',
                            'sku': '723829300',
                            'sells_to_company': False,
                            'sold_count': 31
                        }
                    ],
                    'attributes': [
                        {
                            'name': 'capacity',
                            'value': '250ml'
                        }
                    ],
                    'categories': [
                        {
                            'id': 'UD',
                            'subcategories': [
                                {'id': 'UDCA'},
                            ]
                        }
                    ]
                },
                {
                    'id': '8weuwe88we',
                    'ean': '3123123123990',
                    'title': 'Caneca Xablau Branca - 350ml',
                    'description': 'Caneca xablau joinha',
                    'reference': 'CXB350ML',
                    'dimensions': {
                        'width': 0.18,
                        'depth': 0.13,
                        'weight': 0.47,
                        'height': 0.44
                    },
                    'factsheet': {
                        'seller_id': 'magazineluiza',
                        'seller_sku': '8weuwe88we',
                    },
                    'sellers': [
                        {
                            'id': 'magazineluiza',
                            'description': 'Magazine Luiza',
                            'sku': '8weuwe88we',
                            'sells_to_company': False,
                            'sold_count': 14
                        }
                    ],
                    'attributes': [
                        {
                            'name': 'capacity',
                            'value': '350ml'
                        }
                    ],
                    'categories': [
                        {
                            'id': 'UD',
                            'subcategories': [
                                {'id': 'UDCA'},
                                {'id': 'UDCG'},
                            ]
                        }
                    ]
                },
                {
                    'id': '623728900',
                    'ean': '3123123123120',
                    'title': 'Caneca Xablau Branca - 200ml',
                    'description': 'Canequinha branca lindeza total, xaplex xablau',  # noqa
                    'reference': 'CXB200ML',
                    'dimensions': {
                        'width': 0.18,
                        'depth': 0.13,
                        'weight': 0.47,
                        'height': 0.44
                    },
                    'factsheet': {
                        'seller_id': 'magazineluiza',
                        'seller_sku': '623728900',
                    },
                    'sellers': [
                        {
                            'id': 'magazineluiza',
                            'description': 'Magazine Luiza',
                            'sku': '623728900',
                            'sells_to_company': False,
                            'sold_count': 12
                        }
                    ],
                    'attributes': [
                        {
                            'name': 'capacity',
                            'value': '200ml'
                        }
                    ],
                    'categories': [
                        {
                            'id': 'UD',
                            'subcategories': [
                                {'id': 'UDCA'},
                            ]
                        }
                    ]
                },
            ],
            'type': 'product',
            'attributes': [
                {
                    'name': 'capacity',
                    'label': 'Capacidade',
                    'values': ['150ml', '200ml', '250ml', '350ml', '450ml']
                }
            ],
            'categories': [
                {
                    'id': 'UD',
                    'subcategories': [
                        {'id': 'UDCA'},
                        {'id': 'UDCG'},
                        {'id': 'UDCC'}
                    ]
                }
            ]
        }

    @pytest.fixture
    def review_data(self, mongo_database):
        for product_id in [
            '723829300',
            '623728900',
            '8weuwe88we',
            '723829300',
        ]:
            mongo_database.customer_behaviors.insert_many([
                {
                    'product_id': product_id,
                    'type': META_TYPE_PRODUCT_AVERAGE_RATING,
                    'value': 2.5
                },
                {
                    'product_id': product_id,
                    'type': META_TYPE_PRODUCT_TOTAL_REVIEW_COUNT,
                    'value': 4
                }
            ])

    def test_assemble_single_seller(
        self,
        mongo_database,
        assembler,
        matched_ml_variations,
        expected_product,
        review_data
    ):
        assembled_product, _ = assembler.assemble(
            matched_ml_variations
        )

        assert assembled_product is not None

        excluded_attributes = (
            'id', 'url', 'title',
            'reference', 'description'
        )

        assembled_main_category = assembled_product['categories'][0]
        assembled_subcategories = assembled_main_category['subcategories']
        assert len(assembled_subcategories) == 2

        assert (
            sorted(assembled_product['canonical_ids']) ==
            sorted(expected_product['canonical_ids'])
        )

        for attr_name, attr_value in expected_product.items():
            if isinstance(attr_value, list):
                assert (
                    sorted(assembled_product) == sorted(expected_product)
                )
            elif (
                not isinstance(attr_value, dict) and
                attr_name not in excluded_attributes
            ):
                assert assembled_product[attr_name] == attr_value

        assembled_variations = assembled_product['variations']
        expected_variations = expected_product['variations']

        for expected_variation in expected_variations:
            assert len(expected_variation['sellers']) == 1

            assembled_variation = assembled_variations[
                expected_variations.index(expected_variation)
            ]

            expected_sellers = expected_variation['sellers']
            assembled_sellers = assembled_variation['sellers']

            assert expected_sellers == assembled_sellers
            assert assembled_variation['categories'] == expected_variation['categories']  # noqa

    def test_always_generate_same_id(
        self,
        assembler,
        mongo_database,
        matched_mktplace_variations
    ):
        assembled_product, _ = assembler.assemble(
            matched_mktplace_variations
        )

        for _ in range(5):
            assembler.assemble(matched_mktplace_variations)

        assert mongo_database.items_ids.count_documents({
            'id': assembled_product['id']
        }) == 1

        assert mongo_database.id_correlations.count_documents({
            'product_id': assembled_product['id']
        }) == 1

    def test_assemble_returns_categories_not_found(
        self, assembler, matched_ml_variations, expected_product
    ):
        for value in matched_ml_variations.values():
            for variation in value:
                variation['categories'] = []

        assembled_product, _ = assembler.assemble(
            matched_ml_variations
        )

        assert not assembled_product

    def _rematch_disabled_variations(
        self,
        variations,
        mongo_database,
        matcher
    ):
        for variation in variations:
            mongo_database.raw_products.update_one(
                {
                    'seller_id': variation['seller_id'],
                    'sku': variation['sku']
                },
                {'$set': {'disable_on_matching': True}}
            )

        return matcher.match_variations(
            ProductSamples.unmatched_ml_variation_with_parent()
        )

    def test_assemble_with_all_products_disable_on_matching(
        self,
        assembler,
        expected_product,
        assembler_matched_ml_variations,
        mongo_database,
        matcher
    ):
        matched_ml_variations = self._rematch_disabled_variations(
            assembler_matched_ml_variations,
            mongo_database,
            matcher
        )

        assembled_product, _ = assembler.assemble(
            matched_ml_variations
        )

        assert not assembled_product

    def test_assemble_should_remove_old_unified_object(
        self,
        assembler,
        expected_product,
        assembler_matched_ml_variations,
        matched_ml_variations,
        mongo_database,
        matcher
    ):
        assembled_product, _ = assembler.assemble(
            matched_ml_variations
        )

        unified_objects = list(mongo_database.unified_objects.find())

        assert assembled_product
        assert unified_objects

        matched_ml_variations = self._rematch_disabled_variations(
            assembler_matched_ml_variations,
            mongo_database,
            matcher
        )

        assembled_product, _ = assembler.assemble(
            matched_ml_variations
        )

        unified_objects = list(mongo_database.unified_objects.find())

        assert not assembled_product
        assert not unified_objects

    def test_assemble_with_all_products_unpublished_should_not_assemble(
        self,
        mongo_database,
        assembler,
        matched_ml_variations,
        assembler_matched_ml_variations,
        expected_product,
        patch_patolino_product_post
    ):
        for variation in assembler_matched_ml_variations:
            payload = {
                'navigation_id': convert_id_to_nine_digits(
                    variation.get('navigation_id')
                ),
                'user': 'xablau',
                'updated_at': datetime.datetime.now(),
                'created_at': datetime.datetime.now()
            }

            mongo_database.unpublished_products.insert_one(payload)

        with patch_patolino_product_post as mock_patolino:
            assembled_product, _ = assembler.assemble(
                matched_ml_variations
            )

        assert mock_patolino.called
        assert not assembled_product

    def test_assemble_with_one_products_unpublished_should_assemble(
        self,
        mongo_database,
        assembler,
        matched_ml_variations,
        expected_product,
        patch_patolino_product_post
    ):
        with patch_patolino_product_post as mock_patolino:
            assembled_product, _ = assembler.assemble(
                matched_ml_variations
            )

        assert not mock_patolino.called
        assert assembled_product

        expected_canonical_ids = ['623728900', '723829300', '8weuwe88we']
        assert assembled_product['canonical_ids'] == expected_canonical_ids
        assert [v['id'] for v in assembled_product['variations']] == [
            '723829300', '8weuwe88we', '623728900'
        ]

        payload = {
            'navigation_id': convert_id_to_nine_digits(
                "623728900"
            ),
            'user': 'xablau',
            'updated_at': datetime.datetime.strptime(
                '2021-06-09T133414',
                '%Y-%m-%dT%H%M%S'
            ),
            'created_at': datetime.datetime.strptime(
                '2021-06-09T133414',
                '%Y-%m-%dT%H%M%S'
            )
        }

        mongo_database.unpublished_products.insert_one(payload)

        with patch_patolino_product_post as mock_patolino:
            assembled_product, _ = assembler.assemble(
                matched_ml_variations
            )

        assert mock_patolino.called

        patolino_payload = mock_patolino.call_args[0][0]
        assert patolino_payload['sku'] == '623728900'
        assert patolino_payload['seller_id'] == 'magazineluiza'
        assert patolino_payload['code'] == UNPUBLISHED_CODE
        assert patolino_payload['message'] == UNPUBLISHED_MESSAGE
        assert patolino_payload['payload'] == {
            'navigation_id': '623728900',
            'user': 'xablau',
            'updated_at': '2021-06-09T133414',
            'created_at': '2021-06-09T133414'
        }

        assert assembled_product
        assert assembled_product['canonical_ids'] == expected_canonical_ids
        assert [v['id'] for v in assembled_product['variations']] == [
            '723829300', '8weuwe88we'
        ]
