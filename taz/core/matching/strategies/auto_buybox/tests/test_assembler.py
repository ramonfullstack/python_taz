import pytest

from taz import constants
from taz.constants import (
    META_TYPE_PRODUCT_AVERAGE_RATING,
    META_TYPE_PRODUCT_TOTAL_REVIEW_COUNT
)
from taz.core.matching.common.samples import ProductSamples
from taz.core.matching.strategies.auto_buybox.assembler import ProductAssembler
from taz.core.matching.strategies.auto_buybox.matcher import ProductMatcher
from taz.core.matching.strategies.tests.helpers import store_media


class TestProductAssembler:

    @pytest.fixture
    def assembler(self):
        return ProductAssembler(constants.AUTO_BUYBOX_STRATEGY)

    @pytest.fixture
    def matcher(self):
        return ProductMatcher()

    @pytest.fixture
    def review_data(self, mongo_database):
        for product_id in [
            '723uwej2u3',
            'ou23ou23ou',
            '0123456',
            '82323jjjj3',
            '819283iqw',
            '623728900',
            '8weuwe88we',
            '723829300'
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

    @pytest.fixture
    def matched_ml_variations(
        self,
        assembler,
        mongo_database,
        matcher,
        assembler_matched_ml_variations
    ):
        return matcher.match_variations(
            ProductSamples.unmatched_ml_variation_with_parent()
        )

    @pytest.fixture
    def matched_mktplace_variations(
        self, assembler,
        mongo_database, matcher
    ):
        variations_to_store = [
            ProductSamples.variation_without_parent_reference(),
            ProductSamples.variation_a_with_parent(),
            ProductSamples.seller_a_variation_with_parent(),
            ProductSamples.seller_b_variation_with_parent(),
            ProductSamples.seller_c_variation_with_parent(),
        ]

        for variation in variations_to_store:
            mongo_database.raw_products.insert_one(variation)
            mongo_database.items_ids.insert_one({
                'id': variation['navigation_id']
            })
            store_media(mongo_database, variation)

        unified_variation = matcher.match_variations(
            ProductSamples.seller_c_variation_with_parent()
        )
        return unified_variation

    @pytest.fixture
    def matched_variations_without_reviews(
        self,
        assembler,
        mongo_database,
        matcher
    ):
        variations_to_store = [
            ProductSamples.variation_without_parent_reference(),
            ProductSamples.variation_a_with_parent(),
            ProductSamples.ml_parent_variation(),
            ProductSamples.ml_variation_a_with_parent(),
            ProductSamples.seller_a_variation_with_parent(),
            ProductSamples.seller_b_variation_with_parent(),
            ProductSamples.seller_c_variation_with_parent(),
            ProductSamples.unmatched_ml_variation_with_parent(),
        ]

        for variation in variations_to_store:
            variation.pop('review_score', {})
            variation.pop('review_count', {})

            mongo_database.raw_products.insert_one(variation)

            mongo_database.items_ids.insert_one({
                'id': variation['navigation_id']
            })
            store_media(mongo_database, variation)

        return matcher.match_variations(
            ProductSamples.unmatched_ml_variation_with_parent()
        )

    @pytest.fixture
    def expected_product(self):
        return {
            'id': '7238293',
            'review_count': 32,
            'review_score': 2.5,
            'url': 'caneca-xablau-branca-250ml-cxb250ml/p/7238293/ud/udca/',
            'title': 'Caneca Xablau Branca - 250ml',
            'description': 'Caneca xablau branca belezinha',
            'reference': 'CXB250ML',
            'brand': '+Canecas Xablau',
            'canonical_ids': ['098asdwe28', '623728900', '723829300', '723uwej2u3', '819283iqw', '82323jjjj3', '8weuwe88we', 'ou23ou23ou'],  # noqa
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
                        },
                        {
                            'id': 'seuzeh',
                            'description': 'Seu Zeh',
                            'sku': '819283iqw',
                            'sells_to_company': False,
                            'sold_count': 82
                        }
                    ],
                    'attributes': [
                        {
                            'name': 'capacity',
                            'value': '200ml'
                        }
                    ]
                },
                {
                    'id': '82323jjjj3',
                    'ean': '3123123999999',
                    'title': 'Caneca Xablau Branca - 450ml',
                    'description': 'Caneca xablau batuta',
                    'reference': 'CXB450ML',
                    'dimensions': {
                        'width': 0.18,
                        'depth': 0.13,
                        'weight': 0.47,
                        'height': 0.44
                    },
                    'factsheet': {
                        'seller_id': 'seller_a',
                        'seller_sku': '82323jjjj3',
                    },
                    'sellers': [
                        {
                            'id': 'seller_a',
                            'description': 'Seller A',
                            'sku': '82323jjjj3',
                            'sells_to_company': False,
                            'sold_count': 14,
                            'matching_uuid': 'a0069aee16d441cab4030cce086debbc', # noqa
                            'extra_data': [{'name': 'is_magalu_indica', 'value': 'true'}] # noqa
                        },
                        {
                            'id': 'seller_b',
                            'description': 'Seller B GMBH',
                            'sku': '098asdwe28',
                            'sells_to_company': False,
                            'sold_count': 14,
                            'matching_uuid': 'a0069aee16d441cab4030cce086debbc', # noqa
                            'extra_data': [{'name': 'is_magalu_indica', 'value': 'true'}] # noqa
                        },
                        {
                            'id': 'seller_c',
                            'description': 'Seller C Ltda',
                            'sku': 'ou23ou23ou',
                            'sells_to_company': False,
                            'sold_count': 14
                        }
                    ],
                    'attributes': [{
                        'name': 'capacity',
                        'value': '450ml'
                    }]
                },
                {
                    'id': '723uwej2u3',
                    'ean': '8888887775120',
                    'title': 'Caneca Xablau Branca - 150ml',
                    'description': 'Caneca lero opa xa blau yo',
                    'reference': 'CXB150ML',
                    'dimensions': {
                        'width': 0.18,
                        'depth': 0.13,
                        'weight': 0.47,
                        'height': 0.44
                    },
                    'factsheet': {
                        'seller_id': 'casaamerica',
                        'seller_sku': '723uwej2u3',
                    },
                    'sellers': [
                        {
                            'id': 'casaamerica',
                            'description': 'Casa America',
                            'sku': '723uwej2u3',
                            'sells_to_company': False,
                            'sold_count': 53
                        }
                    ],
                    'attributes': [
                        {
                            'name': 'capacity',
                            'value': '150ml'
                        }
                    ]
                }
            ],
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
                        {'id': 'UDCG'},
                        {'id': 'UDCG'}
                    ]
                },
                {
                    'id': 'PR',
                    'subcategories': [
                        {'id': 'PRCA'}
                    ]
                }
            ]
        }

    def test_assemble(
        self,
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
            len(assembled_product['canonical_ids']) ==
            len(expected_product['canonical_ids'])
        )

        for attr_name, attr_value in expected_product.items():
            if isinstance(attr_value, list):
                expected_attribute = [
                    v for v in expected_product[attr_name]
                    if not isinstance(v, dict)
                ]
                product_attribute = [
                    v for v in attr_value
                    if not isinstance(v, dict)
                ]
                assert sorted(product_attribute) == sorted(expected_attribute)
            elif (
                not isinstance(attr_value, dict) and
                attr_name not in excluded_attributes
            ):
                assert assembled_product[attr_name] == attr_value

        assembled_variations = assembled_product['variations']
        expected_variations = expected_product['variations']

        for expected_variation in expected_variations:
            assembled_variation = assembled_variations[
                expected_variations.index(expected_variation)
            ]

            expected_sellers = expected_variation['sellers']
            assembled_sellers = assembled_variation['sellers']

            assert expected_sellers == assembled_sellers

    def test_always_generate_same_id(
        self, assembler, mongo_database,
        matched_mktplace_variations
    ):
        assembled_product, _ = assembler.assemble(
            matched_mktplace_variations
        )

        assert assembled_product is not None

        for _ in range(5):
            assembler.assemble(matched_mktplace_variations)

        ids = list(mongo_database.items_ids.find({
            'id': assembled_product['id']
        }))
        assert len(ids) == 1

        correlations = list(mongo_database.id_correlations.find({
            'product_id': assembled_product['id']
        }))
        assert len(correlations) == 5

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

    def test_unify_correlations_from_products_with_buybox_should_clean_unified(  # noqa
        self,
        assembler,
        mongo_database,
        matched_ml_variations
    ):
        ids = ['0123456', '9876543']

        for product_id in ids:
            for value in matched_ml_variations.values():
                for variation in value:
                    mongo_database.id_correlations.insert_one({
                        'product_id': product_id,
                        'variation_id': variation['sku'],
                        'sku': variation['sku'],
                        'seller_id': variation['seller_id'],
                    })

        for product_id in ids:
            mongo_database.unified_objects.insert_one({
                'id': product_id,
                'type': 'product'
            })

        assembled_product, _ = assembler.assemble(
            matched_ml_variations
        )
        assert assembled_product is not None

        total_unified = mongo_database.unified_objects.count_documents({
            'id': {'$in': ids}
        })
        assert total_unified == 0

    def test_canonicals_must_not_contain_invalid_values(
        self, assembler, mongo_database,
        matched_mktplace_variations
    ):
        for k in matched_mktplace_variations.values():
            mongo_database.id_correlations.insert_one({
                'product_id': None,
                'variation_id': None,
                'seller_id': k[0]['seller_id'],
                'sku': k[0]['sku']
            })

        assembled_product, _ = assembler.assemble(matched_mktplace_variations)

        assert assembled_product is not None

        assert len(assembled_product['canonical_ids']) > 1

        for canonical_id in assembled_product['canonical_ids']:
            assert canonical_id is not None

    def test_should_consider_customer_behavior_collection_review_values(
            self, assembler, review_data, matched_ml_variations
    ):
        source_ids = []
        for variations in matched_ml_variations.values():
            for variation in variations:
                source_ids += [
                    (
                        variation['sku'],
                        variation['seller_id'],
                        variation['parent_sku']
                    )
                ]

        elected_id, _ = assembler.find_product_id(source_ids)

        product = assembler._build_product(elected_id, matched_ml_variations)

        for variation in product['variations']:
            assert variation[META_TYPE_PRODUCT_AVERAGE_RATING]
            assert variation[META_TYPE_PRODUCT_TOTAL_REVIEW_COUNT]

        assert product['review_count'] == 32
        assert product['review_score'] == 2.5

    def test_should_use_raw_product_values_when_missing_on_customer_behaviors(
            self, assembler, matched_ml_variations, review_data
    ):
        source_ids = []
        for variations in matched_ml_variations.values():
            for variation in variations:
                source_ids += [
                    (
                        variation['sku'],
                        variation['seller_id'],
                        variation['parent_sku']
                    )
                ]

        elected_id, _ = assembler.find_product_id(source_ids)

        product = assembler._build_product(elected_id, matched_ml_variations)

        for variation in product['variations']:
            assert variation[META_TYPE_PRODUCT_AVERAGE_RATING]
            assert variation[META_TYPE_PRODUCT_TOTAL_REVIEW_COUNT]

        assert product['review_count'] == 32
        assert product['review_score'] == 2.5

    def test_should_use_raw_product_when_missing_1_key_on_customer_behaviors(
            self, assembler, matched_ml_variations, review_data
    ):
        source_ids = []
        for variations in matched_ml_variations.values():
            for variation in variations:
                source_ids += [
                    (
                        variation['sku'],
                        variation['seller_id'],
                        variation['parent_sku']
                    )
                ]

        elected_id, _ = assembler.find_product_id(source_ids)

        product = assembler._build_product(elected_id, matched_ml_variations)

        for variation in product['variations']:
            assert variation[META_TYPE_PRODUCT_AVERAGE_RATING]
            assert variation[META_TYPE_PRODUCT_TOTAL_REVIEW_COUNT]

        assert product['review_count'] == 32
        assert product['review_score'] == 2.5

    def test_should_send_zeroed_review_values_when_no_data(
        self,
        assembler,
        matched_variations_without_reviews
    ):
        source_ids = []
        for variations in matched_variations_without_reviews.values():
            for variation in variations:
                source_ids += [
                    (
                        variation['sku'],
                        variation['seller_id'],
                        variation['parent_sku']
                    )
                ]

        elected_id, _ = assembler.find_product_id(source_ids)

        product = assembler._build_product(
            elected_id,
            matched_variations_without_reviews
        )

        assert product['review_count'] == 0
        assert product['review_score'] == 0
