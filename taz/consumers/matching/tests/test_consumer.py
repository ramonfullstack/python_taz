from unittest.mock import patch

import pytest
from simple_settings import settings
from simple_settings.utils import settings_stub

from taz.constants import (
    AUTO_BUYBOX_STRATEGY,
    CHESTER_STRATEGY,
    DELETE_ACTION,
    MAGAZINE_LUIZA_SELLER_ID,
    META_TYPE_PRODUCT_AVERAGE_RATING,
    META_TYPE_PRODUCT_TOTAL_REVIEW_COUNT,
    OMNILOGIC_STRATEGY,
    SINGLE_SELLER_STRATEGY,
    UPDATE_ACTION
)
from taz.consumers.matching.consumer import MatchingRecordProcessor
from taz.core.matching.common.enriched_products import EnrichedProductSamples
from taz.core.matching.common.samples import ProductSamples
from taz.core.merge.merger import Merger
from taz.helpers.json import json_loads
from taz.utils import normalize_voltage


class TestMatchingConsumer:
    @pytest.fixture
    def processor(self):
        return MatchingRecordProcessor(
            persist_changes=False,
            exclusive_strategy=False
        )

    @pytest.fixture
    def exclusive_processor(self):
        return MatchingRecordProcessor(
            persist_changes=True,
            exclusive_strategy=True
        )

    @pytest.fixture
    def message(self, mongo_database):
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
            mongo_database.raw_products.insert_one(variation)

        match_product = ProductSamples.unmatched_ml_variation_with_parent()

        return {
            'action': UPDATE_ACTION,
            'sku': match_product['sku'],
            'seller_id': match_product['seller_id'],
            'timestamp': 0.1,
            'task_id': '186e1006ae3541128b6055b99bab7ca1'
        }

    @pytest.fixture
    def review_data(self, mongo_database):
        for product_id in [
            '723829300',
            '8weuwe88we',
            '623728900',
            '819283iqw',
            '82323jjjj3',
            '0123456',
            'ou23ou23ou',
            '723uwej2u3'
        ]:
            mongo_database.customer_behaviors.insert_one(
                {
                    'product_id': product_id,
                    'type': META_TYPE_PRODUCT_AVERAGE_RATING,
                    'value': 2.5
                }
            )
            mongo_database.customer_behaviors.insert_one(
                {
                    'product_id': product_id,
                    'type': META_TYPE_PRODUCT_TOTAL_REVIEW_COUNT,
                    'value': 4
                }
            )

    @pytest.fixture
    def expected_product(self):
        return {
            'id': '723829300',
            'review_count': 32,
            'review_score': 2.5,
            'url': 'caneca-xablau-branca-250ml-cxb250ml/p/7238293/ud/udca/',
            'title': 'Caneca Xablau Branca - 250ml',
            'description': 'Caneca xablau branca belezinha',
            'reference': 'CXB250ML',
            'brand': '+Canecas Xablau',
            'canonical_ids': ['623728900', '723829300', '723uwej2u3', '82323jjjj3', '8weuwe88we'],  # noqa
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
                        'seller_id': MAGAZINE_LUIZA_SELLER_ID,
                        'seller_sku': '723829300',
                    },
                    'sellers': [
                        {
                            'id': MAGAZINE_LUIZA_SELLER_ID,
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
                        'seller_id': MAGAZINE_LUIZA_SELLER_ID,
                        'seller_sku': '8weuwe88we',
                    },
                    'sellers': [
                        {
                            'id': MAGAZINE_LUIZA_SELLER_ID,
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
                        'seller_id': MAGAZINE_LUIZA_SELLER_ID,
                        'seller_sku': '623728900',
                    },
                    'sellers': [
                        {
                            'id': MAGAZINE_LUIZA_SELLER_ID,
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
                            'extra_data': [{'name': 'is_magalu_indica', 'value': 'true'}], # noqa
                        },
                        {
                            'id': 'seller_b',
                            'description': 'Seller B GMBH',
                            'sku': '098asdwe28',
                            'sells_to_company': False,
                            'sold_count': 14,
                            'matching_uuid': 'a0069aee16d441cab4030cce086debbc', # noqa
                            'extra_data': [{'name': 'is_magalu_indica', 'value': 'true'}], # noqa
                        },
                        {
                            'id': 'seller_c',
                            'description': 'Seller C Ltda',
                            'sku': 'ou23ou23ou',
                            'sells_to_company': False,
                            'sold_count': 14
                        }
                    ],
                    'attributes': [
                        {
                            'name': 'capacity',
                            'value': '450ml'
                        }
                    ]
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
                },
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

    @pytest.fixture
    def foccus_nutricao_product_samples(self):
        return [
            ProductSamples.foccusnutricao_sku_4098_6290(),
            ProductSamples.foccusnutricao_sku_4098_6293(),
            ProductSamples.foccusnutricao_sku_4098_6295(),
            ProductSamples.foccusnutricao_sku_4098_6297(),
            ProductSamples.foccusnutricao_sku_4099_6303(),
            ProductSamples.foccusnutricao_sku_4100_6306(),
            ProductSamples.foccusnutricao_sku_4100_6314(),
            ProductSamples.foccusnutricao_sku_4101_6319(),
            ProductSamples.foccusnutricao_sku_4101_6321()
        ]

    @pytest.fixture
    def mock_default_message(self):
        return {
            'action': UPDATE_ACTION,
            'task_id': '186e1006ae3541128b6055b99bab7ca1',
            'timestamp': 0.1
        }

    def update_variation(
        self,
        mongo_database,
        variation,
        enriched_products
    ):
        for enriched in enriched_products:
            if (
                variation['sku'] == enriched['sku'] and
                variation['seller_id'] == enriched['seller_id']
            ):
                variation['matching_strategy'] = OMNILOGIC_STRATEGY
                variation['product_hash'] = enriched['product_hash']
                mongo_database.raw_products.insert_one(variation)
                break

    def process_message(
        self,
        variation,
        mongo_database,
        processor,
        patch_pubsub_client,
        matching_strategy=None,
        categories=None
    ):
        if matching_strategy:
            variation['matching_strategy'] = matching_strategy

        if categories:
            variation['categories'] = categories

        mongo_database.raw_products.insert_one(variation)

        message = {
            'action': UPDATE_ACTION,
            'sku': variation['sku'],
            'seller_id': variation['seller_id'],
            'task_id': '186e1006ae3541128b6055b99bab7ca1',
            'timestamp': 0.1
        }

        processor.persist_changes = True

        with patch_pubsub_client as mock_pubsub:
            processor.process_message(message)

        assert mock_pubsub.called

    @settings_stub(DEFAULT_MATCHING_STRATEGY=AUTO_BUYBOX_STRATEGY)
    def test_consume_message_successfully_notifies_queue(
        self,
        processor,
        message,
        patch_pubsub_client
    ):
        processor.persist_changes = True

        with patch_pubsub_client as mock_pubsub:
            processor.process_message(message)

        assert mock_pubsub.called

        data = json_loads(mock_pubsub.call_args_list[0][1]['data'].decode())
        assert data['action'] == message['action']
        assert data['seller_id'] == message['seller_id']
        assert data['sku'] == message['sku']
        assert data['origin'] == 'matching'

    @settings_stub(DEFAULT_MATCHING_STRATEGY=AUTO_BUYBOX_STRATEGY)
    def test_consume_message_returns_matched_product(
        self,
        processor,
        message,
        expected_product,
        mongo_database,
        review_data
    ):
        consumed_product = processor.process_message(message)
        assert consumed_product is not None

        assert mongo_database.unified_objects.count_documents({}) == 0

        excluded_attributes = ('_id', 'id', 'url')

        assembled_main_category = consumed_product['categories'][0]
        assembled_subcategories = assembled_main_category['subcategories']
        assert len(assembled_subcategories) == 2

        assert len(consumed_product['canonical_ids']) == 8

        for attr_name, attr_value in expected_product.items():
            if attr_name in excluded_attributes:
                continue

            if isinstance(attr_value, list):
                expected_attribute = [
                    v for v in expected_product[attr_name]
                    if not isinstance(v, dict)
                ]
                consumed_attribute = [
                    v for v in attr_value
                    if not isinstance(v, dict)
                ]
                assert sorted(consumed_attribute) == sorted(expected_attribute)
            elif not isinstance(attr_value, dict):
                assert consumed_product[attr_name] == attr_value

        assembled_variations = consumed_product['variations']
        expected_variations = expected_product['variations']

        for expected_variation in expected_variations:
            assembled_variation = assembled_variations[
                expected_variations.index(expected_variation)
            ]

            expected_sellers = expected_variation['sellers']
            assembled_sellers = assembled_variation['sellers']

            assert assembled_variation['main_media']
            assert assembled_variation['factsheet']
            assert expected_sellers == assembled_sellers

    def test_processor_validate_wrong_message(
        self,
        processor,
        logger_stream,
        patch_pubsub_client
    ):
        with patch_pubsub_client as mock_pubsub:
            with patch.object(processor, 'process_message'):
                processor.run_as_thread({})

        assert not mock_pubsub.called
        assert (
            "'sku': ['Missing data for required field.']"
            in logger_stream.getvalue() and
            "'task_id': ['Missing data for required field.']"
            in logger_stream.getvalue()
        )

    def test_processor_returns_bundles(
        self,
        mongo_database,
        processor,
        patch_pubsub_client,
        mock_default_message
    ):
        product = ProductSamples.magazineluiza_sku_2090111_bundle()
        mongo_database.raw_products.insert_one(product)

        message = {
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            **mock_default_message
        }

        processor.persist_changes = True
        with patch_pubsub_client as mock_pubsub:
            processor.process_message(message)

        assert mongo_database.unified_objects.count_documents({}) == 1

        stored_product = mongo_database.unified_objects.find()[0]
        main_variation = stored_product['variations'][0]

        assert main_variation['bundles'] == product['bundles']
        assert mock_pubsub.called

    def test_processor_returns_gift_product(
        self,
        mongo_database,
        processor,
        patch_pubsub_client,
        mock_default_message
    ):
        product = ProductSamples.magazineluiza_sku_155108800_gift_product()
        mongo_database.raw_products.insert_one(product)

        message = {
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            **mock_default_message
        }

        processor.persist_changes = True
        with patch_pubsub_client as mock_pubsub:
            processor.process_message(message)

        assert mongo_database.unified_objects.count_documents({}) == 1

        stored_product = mongo_database.unified_objects.find()[0]
        main_variation = stored_product['variations'][0]

        assert main_variation['gift_product'] == product['gift_product']
        assert mock_pubsub.called

    def test_processor_product_returns_categories_and_selection_in_variation(
        self,
        mongo_database,
        processor,
        patch_pubsub_client,
        mock_default_message
    ):
        product = ProductSamples.magazineluiza_sku_155108800_gift_product()
        mongo_database.raw_products.insert_one(product)

        message = {
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            **mock_default_message
        }

        processor.persist_changes = True
        with patch_pubsub_client as mock_pubsub:
            processor.process_message(message)

        assert mongo_database.unified_objects.count_documents({}) == 1

        stored_product = mongo_database.unified_objects.find()[0]

        assert 'categories' in stored_product
        assert 'selections' in stored_product

        main_variation = stored_product['variations'][0]

        assert main_variation['categories'] == product['categories']
        assert main_variation['selections'] == product['selections']

        assert mock_pubsub.called

    @pytest.mark.parametrize('variations_to_store, variation_to_match, expected_variations, expected_sellers', [  # noqa
        (
            [
                ProductSamples.casaamerica_sku_2019285(),
                ProductSamples.cookeletroraro_sku_2002109(),
                ProductSamples.magazineluiza_sku_216534900(),
            ],
            ProductSamples.whirlpool_sku_2003610(),
            1,
            1
        ),
        (
            [
                ProductSamples.casaamerica_sku_2019285(),
                ProductSamples.cookeletroraro_sku_2002109(),
                ProductSamples.whirlpool_sku_2003610(),
            ],
            ProductSamples.magazineluiza_sku_216534900(),
            1,
            2
        ),
        (
            [
                ProductSamples.casaamerica_sku_2019285(
                    disable_on_matching=False,
                ),
                ProductSamples.cookeletroraro_sku_2002109(
                    disable_on_matching=False,
                ),
                ProductSamples.magazineluiza_sku_216534900(
                    disable_on_matching=False,
                ),
            ],
            ProductSamples.whirlpool_sku_2003610(
                disable_on_matching=False,
                matching_strategy='AUTO_BUYBOX'
            ),
            1,
            4
        ),
    ])
    def test_non_exclusive_matching_uses_any_strategy(
        self,
        mongo_database,
        processor,
        variations_to_store,
        variation_to_match,
        expected_variations,
        expected_sellers,
        patch_pubsub_client,
        mock_default_message
    ):
        for variation in variations_to_store + [variation_to_match]:
            mongo_database.raw_products.insert_one(variation)

        message = {
            'sku': variation_to_match['sku'],
            'seller_id': variation_to_match['seller_id'],
            **mock_default_message
        }

        processor.persist_changes = True

        with patch_pubsub_client as mock_pubsub:
            processor.process_message(message)

        assert mongo_database.id_correlations.count_documents(
            {}
        ) == expected_sellers

        stored_product = mongo_database.unified_objects.find()[0]

        assert len(stored_product['variations']) == expected_variations

        for variation in stored_product['variations']:
            assert len(variation['sellers']) == expected_sellers

        assert mock_pubsub.called

    @pytest.mark.parametrize('variations_to_store, variation_to_match, expected_variations, expected_sellers', [  # noqa
        (
            [
                ProductSamples.casaamerica_sku_2019285(),
                ProductSamples.cookeletroraro_sku_2002109(),
                ProductSamples.magazineluiza_sku_216534900(),
                ProductSamples.whirlpool_sku_2003610(),
            ],
            ProductSamples.whirlpool_sku_2003610(),
            1,
            1
        ),
        (
            [
                ProductSamples.casaamerica_sku_2019285(),
                ProductSamples.cookeletroraro_sku_2002109(),
                ProductSamples.whirlpool_sku_2003610(),
            ],
            ProductSamples.magazineluiza_sku_216534900(),
            1,
            1
        ),
        (
            [
                ProductSamples.casaamerica_sku_2019285(
                    disable_on_matching=False,
                ),
                ProductSamples.cookeletroraro_sku_2002109(
                    disable_on_matching=False,
                ),
                ProductSamples.magazineluiza_sku_216534900(
                    disable_on_matching=False,
                ),
            ],
            ProductSamples.whirlpool_sku_2003610(
                disable_on_matching=False,
            ),
            1,
            1
        ),
        (
            [
                ProductSamples.casaamerica_sku_2019285(
                    disable_on_matching=False,
                ),
                ProductSamples.cookeletroraro_sku_2002109(
                    disable_on_matching=False,
                ),
                ProductSamples.whirlpool_sku_2003610(
                    disable_on_matching=False,
                ),
            ],
            ProductSamples.magazineluiza_sku_216534900(
                disable_on_matching=False,
            ),
            1,
            3
        ),
        (
            [
                ProductSamples.casaamerica_sku_2019285(
                    disable_on_matching=False,
                ),
                ProductSamples.cookeletroraro_sku_2002109(
                    disable_on_matching=False,
                ),
                ProductSamples.magazineluiza_sku_216534900(
                    disable_on_matching=False,
                ),
            ],
            ProductSamples.whirlpool_sku_2003610(
                disable_on_matching=False,
                matching_strategy='AUTO_BUYBOX',
            ),
            1,
            4
        ),
    ])
    def test_exclusive_matching_uses_referred_strategy(
        self,
        mongo_database,
        exclusive_processor,
        variations_to_store,
        variation_to_match,
        expected_variations,
        expected_sellers,
        patch_pubsub_client,
        mock_default_message
    ):
        for variation in variations_to_store + [variation_to_match]:
            mongo_database.raw_products.insert_one(variation)

        message = {
            'sku': variation_to_match['sku'],
            'seller_id': variation_to_match['seller_id'],
            **mock_default_message
        }

        exclusive_processor.persist_changes = True

        with patch_pubsub_client as mock_pubsub:
            exclusive_processor.process_message(message)

        assert mongo_database.id_correlations.count_documents(
            {}
        ) == expected_sellers

        stored_product = mongo_database.unified_objects.find()[0]

        assert len(stored_product['variations']) == expected_variations

        for variation in stored_product['variations']:
            assert len(variation['sellers']) == expected_sellers

        assert mock_pubsub.called

    def test_processor_three_products_with_the_same_parents_but_two_with_attributes_returns_product_with_two_variations(  # noqa
        self,
        mongo_database,
        processor,
        patch_pubsub_client,
        mock_default_message
    ):
        variations = [
            ProductSamples.magazineluiza_sku_193389100(),
            ProductSamples.magazineluiza_sku_193389600(),
            ProductSamples.magazineluiza_sku_193389300()
        ]

        for variation in variations:
            mongo_database.raw_products.insert_one(variation)

        for variation in variations:
            message = {
                'sku': variation['sku'],
                'seller_id': variation['seller_id'],
                **mock_default_message
            }

            processor.persist_changes = True
            with patch_pubsub_client as mock_pubsub:
                processor.process_message(message)

            assert mock_pubsub.called

        assert mongo_database.unified_objects.count_documents({}) == 2

        variation = ProductSamples.magazineluiza_sku_193389100()
        unified_object = mongo_database.unified_objects.find_one(
            {'id': variation['navigation_id']}
        )

        assert len(unified_object['variations']) == 1

        variation = ProductSamples.magazineluiza_sku_193389600()
        unified_object = mongo_database.unified_objects.find_one(
            {'id': variation['navigation_id']}
        )

        assert len(unified_object['variations']) == 2

    def test_matching_same_parent_but_with_different_attributes_1(
        self,
        mongo_database,
        processor,
        patch_pubsub_client,
        mock_default_message
    ):
        variations = [
            ProductSamples.pequenostravessos_sku_571743566(),
            ProductSamples.pequenostravessos_sku_571743563(),
            ProductSamples.pequenostravessos_sku_571743567()
        ]

        for variation in variations:
            mongo_database.raw_products.insert_one(variation)

        for variation in variations:
            message = {
                'sku': variation['sku'],
                'seller_id': variation['seller_id'],
                **mock_default_message
            }

            processor.persist_changes = True
            with patch_pubsub_client as mock_pubsub:
                processor.process_message(message)

            assert mock_pubsub.called

        assert mongo_database.unified_objects.count_documents({}) == 2

    def test_matching_returns_main_media(
        self,
        mongo_database,
        processor,
        patch_pubsub_client,
        mock_default_message
    ):
        variations = [
            ProductSamples.pequenostravessos_sku_571743566(),
            ProductSamples.pequenostravessos_sku_571743567()
        ]

        for variation in variations:
            mongo_database.raw_products.insert_one(variation)

        for variation in variations:
            message = {
                'sku': variation['sku'],
                'seller_id': variation['seller_id'],
                **mock_default_message
            }

            processor.persist_changes = True
            with patch_pubsub_client as mock_pubsub:
                processor.process_message(message)

            assert mock_pubsub.called

        assert mongo_database.unified_objects.count_documents({}) == 1

        unified_object = mongo_database.unified_objects.find_one()
        for variation in unified_object['variations']:
            assert variation['main_media'] == variation['factsheet']

    def test_matching_same_parent_with_sku_without_attributes(
        self,
        mongo_database,
        processor,
        patch_pubsub_client,
        mock_default_message
    ):
        variations = [
            ProductSamples.magazineluiza_sku_088878800(),
            ProductSamples.whirlpool_sku_27(),
            ProductSamples.magazineluiza_sku_088878900(),
            ProductSamples.whirlpool_sku_257(),
            ProductSamples.surikato_sku_4182(),
        ]

        for variation in variations:
            variation['matching_strategy'] = AUTO_BUYBOX_STRATEGY
            mongo_database.raw_products.insert_one(variation)

        for variation in variations:
            message = {
                'sku': variation['sku'],
                'seller_id': variation['seller_id'],
                **mock_default_message
            }

            processor.persist_changes = True
            with patch_pubsub_client as mock_pubsub:
                processor.process_message(message)

            assert mock_pubsub.called

        assert mongo_database.unified_objects.count_documents({}) == 2

    def test_matching_correcting_unification_with_different_eans(
        self,
        mongo_database,
        processor,
        patch_pubsub_client,
        mock_default_message
    ):
        variations = [
            ProductSamples.magazineluiza_sku_200513500(),
            ProductSamples.whirlpool_sku_1157(),
            ProductSamples.magazineluiza_sku_200513600(),
            ProductSamples.whirlpool_sku_1048(),
            ProductSamples.cookeletroraro_sku_2001305(),
            ProductSamples.whirlpool_sku_1183(),
            ProductSamples.whirlpool_1339(),
            ProductSamples.whirlpool_1338(),
            ProductSamples.whirlpool_sku_1047(),
            ProductSamples.magazineluiza_sku_088894400(),
            ProductSamples.magazineluiza_sku_088894500(),
            ProductSamples.magazineluiza_sku_088894600(),
            ProductSamples.magazineluiza_sku_088894700(),
            ProductSamples.magazineluiza_sku_200513300(),
            ProductSamples.magazineluiza_sku_200513400()
        ]

        for variation in variations:
            variation['matching_strategy'] = AUTO_BUYBOX_STRATEGY
            mongo_database.raw_products.insert_one(variation)

        variation = ProductSamples.whirlpool_sku_1157()
        message = {
            'sku': variation['sku'],
            'seller_id': variation['seller_id'],
            **mock_default_message
        }

        processor.persist_changes = True
        with patch_pubsub_client as mock_pubsub:
            processor.process_message(message)

        assert mock_pubsub.called
        assert mongo_database.unified_objects.count_documents({}) == 1

        unified_object = mongo_database.unified_objects.find_one()
        assert len(unified_object['variations']) == 2

    def test_matching_correcting_unification_with_different_titles(
        self,
        mongo_database,
        processor,
        patch_pubsub_client,
        mock_default_message
    ):
        variations = [
            ProductSamples.magazineluiza_sku_011704201(),
            ProductSamples.whirlpool_sku_192(),
            ProductSamples.cookeletroraro_sku_2000160(),
            ProductSamples.magazineluiza_sku_011704400(),
            ProductSamples.cookeletroraro_sku_2000159(),
            ProductSamples.magazineluiza_sku_011704500(),
            ProductSamples.whirlpool_sku_335(),
            ProductSamples.magazineluiza_sku_011704301(),
            ProductSamples.cookeletroraro_sku_2000837(),
            ProductSamples.whirlpool_sku_334()
        ]

        for variation in variations:
            variation['matching_strategy'] = AUTO_BUYBOX_STRATEGY
            mongo_database.raw_products.insert_one(variation)

        variation = ProductSamples.whirlpool_sku_334()
        message = {
            'sku': variation['sku'],
            'seller_id': variation['seller_id'],
            **mock_default_message
        }

        processor.persist_changes = True
        with patch_pubsub_client as mock_pubsub:
            processor.process_message(message)

        assert mock_pubsub.called
        assert mongo_database.unified_objects.count_documents({}) == 1

        unified_object = mongo_database.unified_objects.find_one()
        assert len(unified_object['variations']) == 3

    def test_matching_ungrouping_products(
        self,
        mongo_database,
        processor,
        patch_pubsub_client,
        mock_default_message
    ):
        variations = [
            ProductSamples.magazineluiza_sku_193410900(),
            ProductSamples.magazineluiza_sku_193411000(),
            ProductSamples.magazineluiza_sku_193411100()
        ]

        mongo_database.raw_products.insert_many(variations)

        for variation in variations:
            message = {
                'sku': variation['sku'],
                'seller_id': variation['seller_id'],
                **mock_default_message
            }

            processor.persist_changes = True
            with patch_pubsub_client as mock_pubsub:
                processor.process_message(message)

            assert mock_pubsub.called

        assert mongo_database.unified_objects.count_documents({}) == 1
        assert mongo_database.id_correlations.count_documents({}) == 3

        for variation in variations:
            variation['parent_sku'] = variation['sku'][:7]
            if '_id' in variation:
                del variation['_id']
            mongo_database.raw_products.insert_one(variation)

        for variation in variations:
            message = {
                'action': UPDATE_ACTION,
                'sku': variation['sku'],
                'seller_id': variation['seller_id'],
                'task_id': '186e1006ae3541128b6055b99bab7ca1',
                'timestamp': 0.1
            }

            processor.persist_changes = True
            with patch_pubsub_client as mock_pubsub:
                processor.process_message(message)

            assert mock_pubsub.called

        assert mongo_database.unified_objects.count_documents({}) == 1
        assert mongo_database.id_correlations.count_documents({}) == 3

    def test_matching_same_parent_but_with_equals_attributes(
        self,
        mongo_database,
        processor,
        patch_pubsub_client
    ):
        variations = [
            ProductSamples.avalancheshop_sku_768(),
            ProductSamples.avalancheshop_sku_769(),
            ProductSamples.avalancheshop_sku_770(),
            ProductSamples.avalancheshop_sku_771()
        ]

        for variation in variations:
            self.process_message(
                variation=variation,
                mongo_database=mongo_database,
                processor=processor,
                patch_pubsub_client=patch_pubsub_client,
            )

        assert mongo_database.unified_objects.count_documents({}) == 4

    @pytest.mark.parametrize('matching_strategy', [
        AUTO_BUYBOX_STRATEGY,
        SINGLE_SELLER_STRATEGY
    ])
    def test_matching_with_same_parent_and_two_different_attributes(
        self,
        mongo_database,
        processor,
        matching_strategy,
        foccus_nutricao_product_samples,
        patch_pubsub_client,
        mock_default_message
    ):
        variations = foccus_nutricao_product_samples

        for variation in variations:
            variation['parent_sku'] = 4098
            variation['matching_strategy'] = matching_strategy
            mongo_database.raw_products.insert_one(variation)

            message = {
                'sku': variation['sku'],
                'seller_id': variation['seller_id'],
                **mock_default_message
            }

            processor.persist_changes = True
            with patch_pubsub_client as mock_pubsub:
                processor.process_message(message)

            assert mock_pubsub.called

        assert mongo_database.unified_objects.count_documents({}) == 1

    @pytest.mark.parametrize('matching_strategy', [
        AUTO_BUYBOX_STRATEGY,
        SINGLE_SELLER_STRATEGY
    ])
    def test_matching_with_two_different_attributes_one_variation_with_different_category(  # noqa
        self,
        mongo_database,
        processor,
        matching_strategy,
        foccus_nutricao_product_samples,
        patch_pubsub_client
    ):
        variations = foccus_nutricao_product_samples

        for variation in variations:
            self.process_message(
                variation=variation,
                matching_strategy=matching_strategy,
                mongo_database=mongo_database,
                processor=processor,
                patch_pubsub_client=patch_pubsub_client,
            )

        assert mongo_database.unified_objects.count_documents({}) == 4

    @pytest.mark.parametrize('matching_strategy', [
        AUTO_BUYBOX_STRATEGY,
        SINGLE_SELLER_STRATEGY
    ])
    def test_matching_with_two_different_attributes_and_same_categories(
        self,
        mongo_database,
        processor,
        matching_strategy,
        patch_pubsub_client
    ):
        product = ProductSamples.foccusnutricao_sku_4098_6290()
        categories = product['categories']

        variations = [
            product,
            ProductSamples.foccusnutricao_sku_4098_6293(),
            ProductSamples.foccusnutricao_sku_4098_6295(),
            ProductSamples.foccusnutricao_sku_4098_6297(),
            ProductSamples.foccusnutricao_sku_4099_6303(),
            ProductSamples.foccusnutricao_sku_4100_6306(),
            ProductSamples.foccusnutricao_sku_4100_6314(),
            ProductSamples.foccusnutricao_sku_4101_6319(),
            ProductSamples.foccusnutricao_sku_4101_6321()
        ]

        for variation in variations:
            self.process_message(
                variation=variation,
                matching_strategy=matching_strategy,
                mongo_database=mongo_database,
                processor=processor,
                patch_pubsub_client=patch_pubsub_client,
                categories=categories
            )

        assert mongo_database.unified_objects.count_documents({}) == 4

    @pytest.mark.parametrize('matching_strategy', [
        AUTO_BUYBOX_STRATEGY,
        SINGLE_SELLER_STRATEGY
    ])
    def test_matching_with_two_different_attributes_and_one_product_with_one_attribute(  # noqa
        self,
        mongo_database,
        processor,
        matching_strategy,
        patch_pubsub_client
    ):
        product = ProductSamples.foccusnutricao_sku_4098_6290()
        categories = product['categories']
        product['attributes'] = [product['attributes'][0]]

        variations = [
            product,
            ProductSamples.foccusnutricao_sku_4098_6293(),
            ProductSamples.foccusnutricao_sku_4098_6295(),
            ProductSamples.foccusnutricao_sku_4098_6297(),
            ProductSamples.foccusnutricao_sku_4099_6303(),
            ProductSamples.foccusnutricao_sku_4100_6306(),
            ProductSamples.foccusnutricao_sku_4100_6314(),
            ProductSamples.foccusnutricao_sku_4101_6319(),
            ProductSamples.foccusnutricao_sku_4101_6321()
        ]

        for variation in variations:
            self.process_message(
                variation=variation,
                matching_strategy=matching_strategy,
                mongo_database=mongo_database,
                processor=processor,
                patch_pubsub_client=patch_pubsub_client,
                categories=categories
            )

        assert mongo_database.unified_objects.count_documents({}) == 5

    def test_matching_correcting_unification_with_different_titles_and_normaliza_voltage(  # noqa
        self,
        mongo_database,
        processor,
        patch_pubsub_client,
        mock_default_message
    ):
        variations = [
            ProductSamples.magazineluiza_sku_011704201(),
            ProductSamples.whirlpool_sku_192(),
            ProductSamples.cookeletroraro_sku_2000160(),
            ProductSamples.magazineluiza_sku_011704400(),
            ProductSamples.cookeletroraro_sku_2000159(),
            ProductSamples.magazineluiza_sku_011704500(),
            ProductSamples.whirlpool_sku_335(),
            ProductSamples.magazineluiza_sku_011704301(),
            ProductSamples.cookeletroraro_sku_2000837(),
            ProductSamples.whirlpool_sku_334()
        ]

        for variation in variations:
            for attribute in variation['attributes']:
                attribute['value'] = normalize_voltage(attribute['value'])

            variation['matching_strategy'] = AUTO_BUYBOX_STRATEGY
            mongo_database.raw_products.insert_one(variation)

        variation = ProductSamples.whirlpool_sku_334()
        message = {
            'sku': variation['sku'],
            'seller_id': variation['seller_id'],
            **mock_default_message
        }

        processor.persist_changes = True
        with patch_pubsub_client as mock_pubsub:
            processor.process_message(message)

        assert mock_pubsub.called
        assert mongo_database.unified_objects.count_documents({}) == 1

        unified_object = mongo_database.unified_objects.find_one()
        assert len(unified_object['variations']) == 2
        matching_strategy = settings.STRATEGIES[AUTO_BUYBOX_STRATEGY]
        assert unified_object['matching_strategy'] == matching_strategy

    @pytest.mark.parametrize('matching_strategy', [
        AUTO_BUYBOX_STRATEGY,
        SINGLE_SELLER_STRATEGY
    ])
    def test_matching_with_one_size_attribute_one_variation_with_different_parents(  # noqa
        self,
        mongo_database,
        processor,
        matching_strategy,
        foccus_nutricao_product_samples,
        patch_pubsub_client,
        mock_default_message
    ):
        variations = foccus_nutricao_product_samples

        for variation in variations:
            variation['matching_strategy'] = matching_strategy

            attributes = []
            for attribute in variation['attributes']:
                if attribute['type'] != 'size':
                    continue

                attributes.append(attribute)

            variation['attributes'] = attributes
            mongo_database.raw_products.insert_one(variation)

            message = {
                'sku': variation['sku'],
                'seller_id': variation['seller_id'],
                **mock_default_message
            }

            processor.persist_changes = True
            with patch_pubsub_client as mock_pubsub:
                processor.process_message(message)

            assert mock_pubsub.called

        assert mongo_database.unified_objects.count_documents({}) == 4

    @pytest.mark.parametrize('matching_strategy', [
        AUTO_BUYBOX_STRATEGY,
        SINGLE_SELLER_STRATEGY
    ])
    def test_matching_with_one_color_attribute_one_variation_with_different_parents(  # noqa
        self,
        mongo_database,
        processor,
        matching_strategy,
        foccus_nutricao_product_samples,
        patch_pubsub_client
    ):
        variations = foccus_nutricao_product_samples

        for variation in variations:
            self.process_message(
                variation=variation,
                matching_strategy=matching_strategy,
                mongo_database=mongo_database,
                processor=processor,
                patch_pubsub_client=patch_pubsub_client,
            )

        assert mongo_database.unified_objects.count_documents({}) == 4

    @pytest.mark.parametrize('matching_strategy', [
        AUTO_BUYBOX_STRATEGY,
        SINGLE_SELLER_STRATEGY
    ])
    def test_matching_product_differents_attributes_and_same_title(  # noqa
        self,
        mongo_database,
        processor,
        matching_strategy,
        foccus_nutricao_product_samples,
        patch_pubsub_client
    ):
        variations = [
            ProductSamples.magazineluiza_sku_216218600(),
            ProductSamples.magazineluiza_sku_216218700()
        ]

        for variation in variations:
            self.process_message(
                variation=variation,
                matching_strategy=matching_strategy,
                mongo_database=mongo_database,
                processor=processor,
                patch_pubsub_client=patch_pubsub_client,
            )

        assert mongo_database.unified_objects.count_documents({}) == 2

    @pytest.mark.parametrize('matching_strategy', [
        AUTO_BUYBOX_STRATEGY,
        SINGLE_SELLER_STRATEGY
    ])
    def test_matching_different_products_with_same_titles_and_same_attributes(  # noqa
        self,
        mongo_database,
        processor,
        matching_strategy,
        patch_pubsub_client
    ):
        variations = [
            ProductSamples.magazineluiza_sku_215522200(),
            ProductSamples.magazineluiza_sku_215522700()
        ]

        for variation in variations:
            self.process_message(
                variation=variation,
                matching_strategy=matching_strategy,
                mongo_database=mongo_database,
                processor=processor,
                patch_pubsub_client=patch_pubsub_client,
            )

        assert mongo_database.unified_objects.count_documents({}) == 2

    @pytest.mark.parametrize('matching_strategy', [
        AUTO_BUYBOX_STRATEGY,
        SINGLE_SELLER_STRATEGY
    ])
    def test_matching_two_products_with_same_titles_seller_and_attributes(
        self,
        mongo_database,
        processor,
        matching_strategy,
        patch_pubsub_client
    ):
        variations = [
            ProductSamples.magazineluiza_sku_217130800(),
            ProductSamples.magazineluiza_sku_218374600(),
            ProductSamples.magazineluiza_sku_218374700(),
            ProductSamples.magazineluiza_sku_217130900()
        ]

        for variation in variations:
            self.process_message(
                variation=variation,
                matching_strategy=matching_strategy,
                mongo_database=mongo_database,
                processor=processor,
                patch_pubsub_client=patch_pubsub_client,
            )

        assert mongo_database.unified_objects.count_documents({}) == 2

        for unified_object in mongo_database.unified_objects.find():
            assert len(unified_object['variations']) == 2

    @pytest.mark.parametrize('matching_strategy, expected', [
        (AUTO_BUYBOX_STRATEGY, 1),
        (SINGLE_SELLER_STRATEGY, 1)
    ])
    def test_matching_two_products_with_same_titles_and_attributes_and_some_equal_sellers(  # noqa
        self,
        mongo_database,
        processor,
        matching_strategy,
        expected,
        patch_pubsub_client,
        mock_default_message
    ):
        variations = [
            ProductSamples.whirlpool_sku_1225(),
            ProductSamples.whirlpool_sku_1224(),
            ProductSamples.magazineluiza_sku_010554000(),
            ProductSamples.whirlpool_sku_1226(),
            ProductSamples.magazineluiza_sku_010554100(),
            ProductSamples.whirlpool_sku_1227()
        ]

        for variation in variations:
            variation['matching_strategy'] = matching_strategy
            mongo_database.raw_products.insert_one(variation)

        message = {
            'sku': variation['sku'],
            'seller_id': variation['seller_id'],
            **mock_default_message
        }

        processor.persist_changes = True
        with patch_pubsub_client as mock_pubsub:
            processor.process_message(message)

        assert mock_pubsub.called

        assert mongo_database.unified_objects.count_documents({}) == expected

    @pytest.mark.parametrize('matching_strategy, expected', [
        (SINGLE_SELLER_STRATEGY, 2),
        (AUTO_BUYBOX_STRATEGY, 2)
    ])
    def test_matching_products_with_console_attributes(
        self,
        mongo_database,
        processor,
        matching_strategy,
        expected,
        patch_pubsub_client
    ):
        variations = [
            ProductSamples.magazineluiza_sku_218849100(),
            ProductSamples.magazineluiza_sku_218849200(),
        ]

        for variation in variations:
            self.process_message(
                variation=variation,
                matching_strategy=matching_strategy,
                mongo_database=mongo_database,
                processor=processor,
                patch_pubsub_client=patch_pubsub_client,
            )

        assert mongo_database.unified_objects.count_documents({}) == expected

    @pytest.mark.parametrize('matching_strategy, expected', [
        (SINGLE_SELLER_STRATEGY, 3),
        (AUTO_BUYBOX_STRATEGY, 3)
    ])
    def test_matching_products_with_size_attributes(
        self,
        mongo_database,
        processor,
        matching_strategy,
        expected,
        patch_pubsub_client
    ):
        variations = [
            ProductSamples.magazineluiza_sku_218200700(),
            ProductSamples.magazineluiza_sku_218200800(),
            ProductSamples.magazineluiza_sku_218200900(),
        ]

        for variation in variations:
            self.process_message(
                variation=variation,
                matching_strategy=matching_strategy,
                mongo_database=mongo_database,
                processor=processor,
                patch_pubsub_client=patch_pubsub_client,
            )

        assert mongo_database.unified_objects.count_documents({}) == expected

    @pytest.mark.parametrize('matching_strategy, expected', [
        (SINGLE_SELLER_STRATEGY, 3),
        (AUTO_BUYBOX_STRATEGY, 3),
    ])
    def test_matching_products_with_capacity_attributes(
        self,
        mongo_database,
        processor,
        matching_strategy,
        expected,
        patch_pubsub_client
    ):
        variations = [
            ProductSamples.magazineluiza_sku_216868300(),
            ProductSamples.magazineluiza_sku_216868400(),
            ProductSamples.magazineluiza_sku_216868500(),
        ]

        for variation in variations:
            self.process_message(
                variation=variation,
                matching_strategy=matching_strategy,
                mongo_database=mongo_database,
                processor=processor,
                patch_pubsub_client=patch_pubsub_client,
            )

        assert mongo_database.unified_objects.count_documents({}) == expected

    @pytest.mark.parametrize('matching_strategy, expected', [
        (SINGLE_SELLER_STRATEGY, 2),
        (AUTO_BUYBOX_STRATEGY, 2)
    ])
    def test_matching_product_bigtires_sku_2027_20274(
        self,
        mongo_database,
        processor,
        matching_strategy,
        expected,
        patch_pubsub_client
    ):
        variations = [
            ProductSamples.bigtires_sku_20274(),
            ProductSamples.bigtires_sku_2027()
        ]

        for variation in variations:
            self.process_message(
                variation=variation,
                matching_strategy=matching_strategy,
                mongo_database=mongo_database,
                processor=processor,
                patch_pubsub_client=patch_pubsub_client,
            )

        assert mongo_database.unified_objects.count_documents({}) == expected

    @pytest.mark.parametrize(
        'matching_strategy, product_expected, variation_expected',
        [
            (SINGLE_SELLER_STRATEGY, 4, 1),
            (AUTO_BUYBOX_STRATEGY, 4, 1)
        ]
    )
    def test_matching_products_with_color_attributes(
        self,
        mongo_database,
        processor,
        matching_strategy,
        product_expected,
        variation_expected,
        patch_pubsub_client
    ):
        variations = [
            ProductSamples.magazineluiza_sku_217110800(),
            ProductSamples.magazineluiza_sku_217110900(),
            ProductSamples.magazineluiza_sku_217111000(),
            ProductSamples.magazineluiza_sku_218828600(),
        ]

        for variation in variations:
            self.process_message(
                variation=variation,
                matching_strategy=matching_strategy,
                mongo_database=mongo_database,
                processor=processor,
                patch_pubsub_client=patch_pubsub_client,
            )

        assert mongo_database.unified_objects.count_documents(
            {}
        ) == product_expected

        unified_object = mongo_database.unified_objects.find_one()
        assert len(unified_object['variations']) == variation_expected

    @pytest.mark.parametrize(
        'matching_strategy, product_expected, variation_expected',
        [
            (SINGLE_SELLER_STRATEGY, 2, 2),
            (AUTO_BUYBOX_STRATEGY, 2, 2)
        ]
    )
    def test_matching_products_with_color_and_voltage_attributes(
        self,
        mongo_database,
        processor,
        matching_strategy,
        product_expected,
        variation_expected,
        patch_pubsub_client
    ):
        variations = [
            ProductSamples.magazineluiza_sku_218178700(),
            ProductSamples.magazineluiza_sku_218178900(),
            ProductSamples.magazineluiza_sku_218178800(),
            ProductSamples.magazineluiza_sku_218179000()
        ]

        for variation in variations:
            self.process_message(
                variation=variation,
                matching_strategy=matching_strategy,
                mongo_database=mongo_database,
                processor=processor,
                patch_pubsub_client=patch_pubsub_client,
            )

        assert mongo_database.unified_objects.count_documents(
            {}
        ) == product_expected

        unified_object = mongo_database.unified_objects.find_one()
        assert len(unified_object['variations']) == variation_expected

    @pytest.mark.parametrize(
        'matching_strategy, product_expected, variation_expected',
        [
            (SINGLE_SELLER_STRATEGY, 3, 1),
            (AUTO_BUYBOX_STRATEGY, 3, 1)
        ]
    )
    def test_matching_products_with_same_title_and_without_attributes(
        self,
        mongo_database,
        processor,
        matching_strategy,
        product_expected,
        variation_expected,
        patch_pubsub_client
    ):
        variations = [
            ProductSamples.magazineluiza_sku_218557800(),
            ProductSamples.magazineluiza_sku_218557900(),
            ProductSamples.magazineluiza_sku_214945600()
        ]

        for variation in variations:
            self.process_message(
                variation=variation,
                matching_strategy=matching_strategy,
                mongo_database=mongo_database,
                processor=processor,
                patch_pubsub_client=patch_pubsub_client,
            )

        assert mongo_database.unified_objects.count_documents(
            {}
        ) == product_expected

        unified_object = mongo_database.unified_objects.find_one()
        assert len(unified_object['variations']) == variation_expected

    @pytest.mark.parametrize(
        'matching_strategy, product_expected, variation_expected',
        [
            (SINGLE_SELLER_STRATEGY, 1, 1),
            (AUTO_BUYBOX_STRATEGY, 1, 1)
        ]
    )
    def test_matching_one_product_disable_on_matching_during_the_flow(
        self,
        mongo_database,
        processor,
        matching_strategy,
        product_expected,
        variation_expected,
        patch_pubsub_client
    ):
        variations = [
            ProductSamples.efacil_sku_193574_46(),
            ProductSamples.efacil_sku_193574_123()
        ]

        for variation in variations:
            self.process_message(
                variation=variation,
                matching_strategy=matching_strategy,
                mongo_database=mongo_database,
                processor=processor,
                patch_pubsub_client=patch_pubsub_client,
            )

        variation = ProductSamples.efacil_sku_193574_46()

        criteria = {
            'sku': variation['sku'],
            'seller_id': variation['seller_id']
        }
        raw_product = mongo_database.raw_products.find_one(criteria)

        raw_product['disable_on_matching'] = True
        mongo_database.raw_products.update_one(criteria, {'$set': raw_product})

        message = {
            'action': DELETE_ACTION,
            'sku': variation['sku'],
            'seller_id': variation['seller_id'],
            'task_id': '186e1006ae3541128b6055b99bab7ca1',
            'timestamp': 0.1
        }

        processor.persist_changes = True
        with patch_pubsub_client as mock_pubsub:
            processor.process_message(message)

        assert mock_pubsub.called
        assert mongo_database.unified_objects.count_documents(
            {}
        ) == product_expected

        unified_object = mongo_database.unified_objects.find_one()
        assert len(unified_object['variations']) == variation_expected

    @pytest.mark.parametrize(
        'matching_strategy',
        [
            SINGLE_SELLER_STRATEGY,
            AUTO_BUYBOX_STRATEGY
        ]
    )
    def test_matching_products_same_parent_after_matching_different_parents(
        self,
        mongo_database,
        processor,
        matching_strategy,
        patch_pubsub_client,
        mock_default_message
    ):
        variations = [
            ProductSamples.lojamultilaser_sku_3771(),
            ProductSamples.lojamultilaser_sku_3770()
        ]

        for variation in variations:
            variation['parent_sku'] = '3767'
            variation['matching_strategy'] = matching_strategy
            mongo_database.raw_products.insert_one(variation)

            message = {
                'sku': variation['sku'],
                'seller_id': variation['seller_id'],
                **mock_default_message
            }

            processor.persist_changes = True
            with patch_pubsub_client as mock_pubsub:
                processor.process_message(message)

            assert mock_pubsub.called

        assert mongo_database.unified_objects.count_documents({}) == 1

        unified_object = mongo_database.unified_objects.find_one()
        assert len(unified_object['variations']) == 2

        raw_products = mongo_database.raw_products.find({}, {'_id': 0})
        for raw_product in raw_products:
            raw_product['parent_sku'] = raw_product['sku']
            mongo_database.raw_products.update_one({}, {'$set': raw_product})

            variation = raw_product
            message = {
                'action': UPDATE_ACTION,
                'sku': variation['sku'],
                'seller_id': variation['seller_id'],
                'task_id': '186e1006ae3541128b6055b99bab7ca1',
                'timestamp': 0.1
            }

            processor.persist_changes = True
            with patch_pubsub_client as mock_pubsub:
                processor.process_message(message)

            assert mock_pubsub.called

        assert mongo_database.unified_objects.count_documents({}) == 2

        unified_object = mongo_database.unified_objects.find_one()
        assert len(unified_object['variations']) == 1

    def test_matching_omnilogic_strategy(
        self,
        mongo_database,
        processor,
        patch_storage_manager_upload,
        patch_kinesis_put,
        patch_pubsub_client,
        mock_default_message
    ):
        enriched_products = [
            EnrichedProductSamples.shoploko_sku_74471(),
            EnrichedProductSamples.magazineluiza_sku_0233847(),
            EnrichedProductSamples.topbrinquedos_sku_2898(),
            EnrichedProductSamples.amplocomercial_sku_230(),
            EnrichedProductSamples.efacil_sku_200298(),
            EnrichedProductSamples.mainshop_sku_5643126(),
            EnrichedProductSamples.mainshop_sku_5643123(),
            EnrichedProductSamples.gynshop_sku_5643188(),
            EnrichedProductSamples.gynshop_sku_5643191(),
            EnrichedProductSamples.efacil_sku_185402(),
            EnrichedProductSamples.casa_e_video_sku_10359(),
            EnrichedProductSamples.topbrinquedos_sku_1964(),
            EnrichedProductSamples.amplocomercial_sku_232()
        ]

        mongo_database.enriched_products.insert_many(enriched_products)

        variations = [
            ProductSamples.shoploko_sku_74471(),
            ProductSamples.magazineluiza_sku_0233847(),
            ProductSamples.topbrinquedos_sku_2898(),
            ProductSamples.amplocomercial_sku_230(),
            ProductSamples.efacil_sku_200298(),
            ProductSamples.mainshop_sku_5643126(),
            ProductSamples.mainshop_sku_5643123(),
            ProductSamples.gynshop_sku_5643188(),
            ProductSamples.gynshop_sku_5643191(),
            ProductSamples.efacil_sku_185402(),
            ProductSamples.casa_e_video_sku_10359(),
            ProductSamples.topbrinquedos_sku_1964(),
            ProductSamples.amplocomercial_sku_232()
        ]

        for index, variation in enumerate(variations):
            variation['matching_strategy'] = OMNILOGIC_STRATEGY
            mongo_database.raw_products.insert_one(variation)

            with patch_storage_manager_upload:
                with patch_kinesis_put, patch_pubsub_client:
                    Merger(
                        raw_product=variation,
                        enriched_product=None,
                        action=UPDATE_ACTION
                    ).merge()

            message = {
                'sku': variation['sku'],
                'seller_id': variation['seller_id'],
                **mock_default_message
            }

            processor.persist_changes = True
            with patch_pubsub_client as mock_pubsub:
                with patch_kinesis_put:
                    processor.process_message(message)

            assert mock_pubsub.called

        variation = ProductSamples.amplocomercial_sku_232()
        criteria = {
            'sku': variation['sku'],
            'seller_id': variation['seller_id']
        }
        raw_product = mongo_database.raw_products.find_one(
            criteria, {'_id': 0}
        )

        raw_product['disable_on_matching'] = True
        mongo_database.raw_products.update_one(criteria, {'$set': raw_product})

        message = {
            'action': DELETE_ACTION,
            'sku': variation['sku'],
            'seller_id': variation['seller_id'],
            'task_id': '186e1006ae3541128b6055b99bab7ca1',
            'timestamp': 0.1
        }

        processor.persist_changes = True
        with patch_pubsub_client as mock_pubsub:
            with patch_kinesis_put:
                processor.process_message(message)

        assert mock_pubsub.called
        assert mongo_database.unified_objects.count_documents({}) == 1

        unified_object = mongo_database.unified_objects.find_one()
        assert len(unified_object['variations']) == 2
        assert len(unified_object['canonical_ids']) == 11
        assert len(unified_object['variations'][0]['sellers']) == 8
        assert len(unified_object['variations'][1]['sellers']) == 3

    def test_matching_omnilogic_strategy_without_enriched_products(
        self,
        mongo_database,
        processor,
        patch_kinesis_put,
        patch_pubsub_client,
        mock_default_message
    ):
        variations = [
            ProductSamples.shoploko_sku_74471(),
            ProductSamples.magazineluiza_sku_0233847(),
            ProductSamples.topbrinquedos_sku_2898(),
            ProductSamples.amplocomercial_sku_230(),
            ProductSamples.efacil_sku_200298(),
            ProductSamples.mainshop_sku_5643126(),
            ProductSamples.mainshop_sku_5643123(),
            ProductSamples.gynshop_sku_5643188(),
            ProductSamples.gynshop_sku_5643191(),
            ProductSamples.efacil_sku_185402(),
            ProductSamples.casa_e_video_sku_10359(),
            ProductSamples.topbrinquedos_sku_1964(),
            ProductSamples.amplocomercial_sku_232()
        ]

        for variation in variations:
            variation['matching_strategy'] = OMNILOGIC_STRATEGY
            mongo_database.raw_products.insert_one(variation)

            message = {
                'sku': variation['sku'],
                'seller_id': variation['seller_id'],
                **mock_default_message
            }

            processor.persist_changes = True
            with patch_pubsub_client as mock_pubsub:
                with patch_kinesis_put:
                    processor.process_message(message)

            assert mock_pubsub.called

        variation = ProductSamples.amplocomercial_sku_232()
        criteria = {
            'sku': variation['sku'],
            'seller_id': variation['seller_id']
        }
        raw_product = mongo_database.raw_products.find_one(
            criteria, {'_id': 0}
        )

        raw_product['disable_on_matching'] = True
        mongo_database.raw_products.update_one(criteria, {'$set': raw_product})

        message = {
            'action': DELETE_ACTION,
            'sku': variation['sku'],
            'seller_id': variation['seller_id'],
            'task_id': '186e1006ae3541128b6055b99bab7ca1',
            'timestamp': 0.1
        }

        processor.persist_changes = True
        with patch_pubsub_client as mock_pubsub:
            processor.process_message(message)

        assert mock_pubsub.called
        assert mongo_database.unified_objects.count_documents({}) == 11

        unified_object = mongo_database.unified_objects.find_one()
        assert len(unified_object['variations']) == 1

    def test_matching_omnilogic_strategy_with_product_hash_is_null(
        self,
        mongo_database,
        processor,
        patch_kinesis_put,
        patch_pubsub_client,
        mock_default_message
    ):
        enriched_products = [
            EnrichedProductSamples.lojasmel_openapi_45035(),
            EnrichedProductSamples.gazinshop_4470()
        ]

        for enriched_product in enriched_products:
            mongo_database.enriched_products.insert_one(enriched_product)

        variation = ProductSamples.lojasmel_openapi_45035()
        variation['matching_strategy'] = OMNILOGIC_STRATEGY
        mongo_database.raw_products.insert_one(variation)

        message = {
            'sku': variation['sku'],
            'seller_id': variation['seller_id'],
            **mock_default_message
        }

        processor.persist_changes = True
        with patch_pubsub_client as mock_pubsub:
            with patch_kinesis_put:
                processor.process_message(message)

        assert mock_pubsub.called

        assert mongo_database.unified_objects.count_documents({}) == 1

        unified_object = mongo_database.unified_objects.find_one()
        assert len(unified_object['variations']) == 1

    def test_matching_omnilogic_strategy_with_variations(
        self,
        mongo_database,
        processor,
        patch_kinesis_put,
        patch_pubsub_client,
        mock_default_message
    ):
        enriched_products = [
            EnrichedProductSamples.colormaq_sku_1408001_1(),
            EnrichedProductSamples.colormaq_sku_1408002()
        ]

        for enriched_product in enriched_products:
            mongo_database.enriched_products.insert_one(enriched_product)

        variations = [
            ProductSamples.colormaq_sku_1408001_1(),
            ProductSamples.colormaq_sku_1408002()
        ]

        for variation in variations:
            self.update_variation(mongo_database, variation, enriched_products)

            message = {
                'sku': variation['sku'],
                'seller_id': variation['seller_id'],
                **mock_default_message
            }

            processor.persist_changes = True
            with patch_pubsub_client as mock_pubsub:
                with patch_kinesis_put:
                    processor.process_message(message)

            assert mock_pubsub.called

        assert mongo_database.unified_objects.count_documents({}) == 1

        unified_object = mongo_database.unified_objects.find_one()
        assert len(unified_object['variations']) == 2

    def test_should_returns_store_pickup_available(
        self,
        mongo_database,
        processor,
        patch_kinesis_put,
        patch_pubsub_client,
        mock_default_message
    ):
        product = ProductSamples.magazineluiza_sku_0233847()
        product['store_pickup_available'] = True

        mongo_database.raw_products.insert_one(product)

        message = {
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            **mock_default_message
        }

        processor.persist_changes = True
        with patch_pubsub_client as mock_pubsub:
            with patch_kinesis_put:
                processor.process_message(message)

        assert mock_pubsub.called

        assert mongo_database.unified_objects.count_documents({}) == 1

        unified_object = mongo_database.unified_objects.find_one()
        seller = unified_object['variations'][0]['sellers'][0]
        assert seller['store_pickup_available'] is True

    def test_should_not_returns_store_pickup_available(
        self,
        mongo_database,
        processor,
        patch_kinesis_put,
        patch_pubsub_client,
        mock_default_message
    ):
        product = ProductSamples.magazineluiza_sku_0233847()

        mongo_database.raw_products.insert_one(product)

        message = {
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            **mock_default_message
        }

        processor.persist_changes = True
        with patch_pubsub_client as mock_pubsub:
            with patch_kinesis_put:
                processor.process_message(message)

        assert mock_pubsub.called

        assert mongo_database.unified_objects.count_documents({}) == 1

        unified_object = mongo_database.unified_objects.find_one()
        seller = unified_object['variations'][0]['sellers'][0]
        assert 'store_pickup_available' not in seller

    def test_should_returns_delivery_plus_1(
        self,
        mongo_database,
        processor,
        patch_kinesis_put,
        patch_pubsub_client,
        mock_default_message
    ):
        product = ProductSamples.magazineluiza_sku_0233847()
        product['delivery_plus_1'] = True

        mongo_database.raw_products.insert_one(product)

        message = {
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            **mock_default_message
        }

        processor.persist_changes = True
        with patch_pubsub_client as mock_pubsub:
            with patch_kinesis_put:
                processor.process_message(message)

        assert mock_pubsub.called

        assert mongo_database.unified_objects.count_documents({}) == 1

        unified_object = mongo_database.unified_objects.find_one()
        seller = unified_object['variations'][0]['sellers'][0]
        assert seller['delivery_plus_1'] is True
        assert 'delivery_plus_2' not in seller

    def test_should_returns_delivery_plus_2(
        self,
        mongo_database,
        processor,
        patch_kinesis_put,
        patch_pubsub_client,
        mock_default_message
    ):
        product = ProductSamples.magazineluiza_sku_0233847()
        product['delivery_plus_2'] = True

        mongo_database.raw_products.insert_one(product)

        message = {
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            **mock_default_message
        }

        processor.persist_changes = True
        with patch_pubsub_client as mock_pubsub:
            with patch_kinesis_put:
                processor.process_message(message)

        assert mock_pubsub.called

        assert mongo_database.unified_objects.count_documents({}) == 1

        unified_object = mongo_database.unified_objects.find_one()
        seller = unified_object['variations'][0]['sellers'][0]
        assert seller['delivery_plus_2'] is True
        assert 'delivery_plus_1' not in seller

    def test_matching_omnilogic_strategy_with_different_brands(
        self,
        mongo_database,
        processor,
        patch_kinesis_put,
        patch_pubsub_client,
        mock_default_message
    ):
        enriched_products = [
            EnrichedProductSamples.magazineluiza_sku_222764000(),
            EnrichedProductSamples.meulivromegastore_sku_166271()
        ]

        for enriched_product in enriched_products:
            mongo_database.enriched_products.insert_one(enriched_product)

        variations = [
            ProductSamples.magazineluiza_sku_222764000(),
            ProductSamples.meulivromegastore_sku_166271()
        ]

        for variation in variations:
            self.update_variation(mongo_database, variation, enriched_products)

            message = {
                'sku': variation['sku'],
                'seller_id': variation['seller_id'],
                **mock_default_message
            }

            processor.persist_changes = True
            with patch_pubsub_client as mock_pubsub:
                with patch_kinesis_put:
                    processor.process_message(message)

            assert mock_pubsub.called

        assert mongo_database.unified_objects.count_documents({}) == 1

        unified_object = mongo_database.unified_objects.find_one()
        assert len(unified_object['variations']) == 1
        assert len(unified_object['variations'][0]['sellers']) == 2

    def test_matching_omnilogic_strategy_with_duplicate_sellers(
        self,
        mongo_database,
        processor,
        patch_kinesis_put,
        patch_pubsub_client,
        mock_default_message
    ):
        enriched_products = [
            EnrichedProductSamples.livrariaflorence2_sku_9788543105757(),
            EnrichedProductSamples.livrariasebocapricho_sku_23036521(),
            EnrichedProductSamples.magazineluiza_sku_221841200(),
            EnrichedProductSamples.livrariaflorence2_sku_9788543105758(),
            EnrichedProductSamples.saraiva_sku_10260263()
        ]

        for enriched_product in enriched_products:
            mongo_database.enriched_products.insert_one(enriched_product)

        variations = [
            ProductSamples.livrariaflorence2_sku_9788543105757(),
            ProductSamples.livrariasebocapricho_sku_23036521(),
            ProductSamples.magazineluiza_sku_221841200(),
            ProductSamples.livrariaflorence2_sku_9788543105758(),
            ProductSamples.saraiva_sku_10260263()
        ]

        for variation in variations:
            self.update_variation(mongo_database, variation, enriched_products)

            message = {
                'sku': variation['sku'],
                'seller_id': variation['seller_id'],
                **mock_default_message
            }

            processor.persist_changes = True
            with patch_pubsub_client as mock_pubsub:
                with patch_kinesis_put:
                    processor.process_message(message)

            assert mock_pubsub.called

        assert mongo_database.unified_objects.count_documents({}) == 1

        unified_object = mongo_database.unified_objects.find_one()
        assert len(unified_object['variations']) == 1
        assert len(unified_object['variations'][0]['sellers']) == 4

    def test_matching_different_ean_using_single_seller_strategy(
        self,
        mongo_database,
        processor,
        patch_kinesis_put,
        patch_pubsub_client,
        mock_default_message
    ):
        variations = [
            ProductSamples.mundokids_sku_57(),
            ProductSamples.mundokids_sku_55(),
        ]

        for variation in variations:
            variation['matching_strategy'] = SINGLE_SELLER_STRATEGY
            variation['ean'] = '1234567890123'
            mongo_database.raw_products.insert_one(variation)

            message = {
                'sku': variation['sku'],
                'seller_id': variation['seller_id'],
                **mock_default_message
            }

            processor.persist_changes = True
            with patch_pubsub_client as mock_pubsub:
                with patch_kinesis_put:
                    processor.process_message(message)

            assert mock_pubsub.called

        assert mongo_database.unified_objects.count_documents({}) == 1

        unified_object = mongo_database.unified_objects.find_one()
        assert len(unified_object['variations']) == 2

    def test_matching_books_one_book_with_attributes(
        self,
        mongo_database,
        processor,
        patch_kinesis_put,
        patch_pubsub_client,
        mock_default_message
    ):
        enriched_products = [
            EnrichedProductSamples.cliquebooks_sku_543242_1(),
            EnrichedProductSamples.magazineluiza_sku_222786900(),
            EnrichedProductSamples.book7_sku_9788506082645(),
        ]
        mongo_database.enriched_products.insert_many(enriched_products)

        variations = [
            ProductSamples.cliquebooks_sku_543242_1(),
            ProductSamples.magazineluiza_sku_222786900(),
            ProductSamples.book7_sku_9788506082645(),
        ]

        for variation in variations:
            variation['matching_strategy'] = OMNILOGIC_STRATEGY
            mongo_database.raw_products.insert_one(variation)

            message = {
                'action': UPDATE_ACTION,
                'sku': variation['sku'],
                'seller_id': variation['seller_id'],
                **mock_default_message
            }

            processor.persist_changes = True
            with patch_pubsub_client as mock_pubsub:
                with patch_kinesis_put:
                    processor.process_message(message)

            assert mock_pubsub.called

        assert mongo_database.unified_objects.count_documents({}) == 2

        unified_object = mongo_database.unified_objects.find_one({
            'id': variations[0]['navigation_id']
        })
        assert len(unified_object['variations']) == 1
        assert len(unified_object['variations'][0]['sellers']) == 1

        unified_object = mongo_database.unified_objects.find_one({
            'id': variations[1]['navigation_id']
        })

        assert len(unified_object['variations']) == 1
        assert len(unified_object['variations'][0]['sellers']) == 2

    def test_matching_duplicated_magazineluiza(
        self,
        mongo_database,
        processor,
        patch_kinesis_put,
        patch_pubsub_client,
        mock_default_message
    ):
        enriched_products = [
            EnrichedProductSamples.magazineluiza_sku_225300068(),
            EnrichedProductSamples.magazineluiza_sku_225620500(),
            EnrichedProductSamples.livrariabaluarte_sku_7576847209()
        ]

        for enriched_product in enriched_products:
            mongo_database.enriched_products.insert_one(enriched_product)

        variations = [
            ProductSamples.magazineluiza_sku_225300068(),
            ProductSamples.magazineluiza_sku_225620500(),
            ProductSamples.livrariabaluarte_sku_7576847209()
        ]

        for variation in variations:
            self.update_variation(mongo_database, variation, enriched_products)

        message = {
            'sku': variation['sku'],
            'seller_id': variation['seller_id'],
            **mock_default_message
        }

        processor.persist_changes = True
        with patch_pubsub_client as mock_pubsub:
            with patch_kinesis_put:
                processor.process_message(message)

        assert mock_pubsub.called

        assert mongo_database.unified_objects.count_documents({}) == 1

        unified_object = mongo_database.unified_objects.find_one()
        assert len(unified_object['variations'][0]['sellers']) == 2

    def test_matching_should_return_main_media_highest_score(
        self,
        mongo_database,
        processor,
        patch_storage_manager_upload,
        patch_kinesis_put,
        patch_pubsub_client,
        mock_default_message
    ):
        enriched_products = [
            EnrichedProductSamples.shoploko_sku_74471(),
            EnrichedProductSamples.topbrinquedos_sku_2898()
        ]

        mongo_database.enriched_products.insert_many(enriched_products)

        variations = [
            ProductSamples.shoploko_sku_74471(),
            ProductSamples.topbrinquedos_sku_2898()
        ]

        scores = [
            {
                'sku': variations[0]['sku'],
                'seller_id': variations[0]['seller_id'],
                'final_score': 40,
                'active': True
            },
            {
                'sku': variations[1]['sku'],
                'seller_id': variations[1]['seller_id'],
                'final_score': 50,
                'active': True
            }
        ]

        mongo_database.scores.insert_many(scores)

        for variation in variations:
            self.update_variation(mongo_database, variation, enriched_products)

            message = {
                'sku': variation['sku'],
                'seller_id': variation['seller_id'],
                **mock_default_message
            }

            processor.persist_changes = True
            with patch_pubsub_client as mock_pubsub:
                with patch_kinesis_put:
                    processor.process_message(message)

            assert mock_pubsub.called

        unified_object = mongo_database.unified_objects.find_one()
        main_media = unified_object['variations'][0]['main_media']

        assert main_media['seller_sku'] == '2898'
        assert main_media['seller_id'] == 'topbrinquedos'

    def test_process_message_should_send_tracking_id(
        self,
        processor,
        patch_pubsub_client,
        patch_notification,
        mock_tracking_id
    ):
        with patch_pubsub_client:
            with patch_notification as mock_notify:
                processor._notify(
                    action=UPDATE_ACTION,
                    seller_id=MAGAZINE_LUIZA_SELLER_ID,
                    sku='123456789',
                    navigation_id='123',
                    tracking_id=mock_tracking_id
                )

        data = mock_notify.call_args.args[0]
        assert data['tracking_id'] == mock_tracking_id

    @pytest.mark.parametrize(
        'matching_strategy,product_strategy,expected_module', [
            (CHESTER_STRATEGY, OMNILOGIC_STRATEGY, 'chester'),
            (None, OMNILOGIC_STRATEGY, 'omnilogic'),
            (None, None, 'single_seller')
        ]
    )
    def test_get_strategy(
        self,
        matching_strategy,
        product_strategy,
        expected_module
    ):
        consumer = MatchingRecordProcessor(
            strategy=matching_strategy
        )
        module = consumer._get_strategy_for_item(product_strategy)

        assert expected_module in str(module)

    def test_dont_return_falsy_when_product_does_not_exists(
        self
    ):
        consumer = MatchingRecordProcessor(
            strategy=SINGLE_SELLER_STRATEGY
        )
        message = {
            'action': UPDATE_ACTION,
            'sku': 'sku',
            'seller_id': 'seller_id',
            'task_id': '186e1006ae3541128b6055b99bab7ca1',
            'timestamp': 0.1
        }
        assert bool(consumer.process_message(message=message)) is True
