import importlib
from collections import OrderedDict
from unittest.mock import patch
from uuid import uuid4

import pytest
from pymongo import MongoClient
from simple_settings import settings

from taz.constants import (
    AUTO_BUYBOX_STRATEGY,
    CREATE_ACTION,
    DELETE_ACTION,
    OMNILOGIC_STRATEGY
)
from taz.consumers.core.exceptions import UndefinedStrategyException
from taz.consumers.matching.processor import MatchingProcessor
from taz.core.matching.common.enriched_products import EnrichedProductSamples
from taz.core.matching.common.samples import ProductSamples


class TestMatchingProcessor:

    @pytest.fixture
    def processor(self):
        return MatchingProcessor(
            strategy=importlib.import_module(
                settings.STRATEGIES[AUTO_BUYBOX_STRATEGY]
            ),
            exclusive_strategy=False
        )

    def _store_variation_media(self, database, variation):
        database.medias.insert_many([
            {
                'seller_id': variation['seller_id'],
                'sku': variation['sku'],
                'videos': [
                    'https://x.xx.xxx/v/{}'.format(
                        variation['sku']
                    )
                ]
            },
            {
                'seller_id': variation['seller_id'],
                'sku': variation['sku'],
                'audios': [
                    'a/{}.mp3'.format(variation['sku'])
                ]
            },
            {
                'seller_id': variation['seller_id'],
                'sku': variation['sku'],
                'podcasts': [
                    'p/{}.mp3'.format(variation['sku'])
                ],
            },
            {
                'seller_id': variation['seller_id'],
                'sku': variation['sku'],
                'images': [
                    '{}x{}/x-{}.jpg'.format(1, 1, variation['sku']),
                    '{}x{}/x-{}-A.jpg'.format(1, 1, variation['sku'])
                ]
            }
        ])

    @pytest.fixture
    def single_variation_delete_match(self, database, processor):
        variations_to_store = [
            ProductSamples.variation_without_parent_reference(),
            ProductSamples.variation_a_with_parent(),
        ]
        for v in variations_to_store:
            database.raw_products.insert_one(v)
            self._store_variation_media(database, v)

        variation = ProductSamples.unmatched_ml_variation_with_parent()
        database.raw_products.insert_one(variation)

        processor.process_message({
            'sku': variation['sku'],
            'action': CREATE_ACTION,
            'seller_id': variation['seller_id']
        })

        correlation = database.id_correlations.find_one(
            {
                'sku': variation['sku'],
                'seller_id': variation['seller_id'],
            },
            {
                '_id': 0, 'product_id': 1
            }
        )

        return {
            'variation': variation,
            'product_id': correlation['product_id']
        }

    @pytest.fixture
    def whole_product_delete_match(self, database, processor):
        variation = ProductSamples.unmatched_ml_variation_with_parent()
        database.raw_products.insert_one(variation)

        processor.process_message({
            'sku': variation['sku'],
            'action': CREATE_ACTION,
            'seller_id': variation['seller_id']
        })

        correlation = database.id_correlations.find_one({
            'sku': variation['sku'],
            'seller_id': variation['seller_id'],
        })

        variation['disable_on_matching'] = True
        del variation['_id']
        database.raw_products.update_one({}, {'$set': variation})

        return {
            'sku': variation['sku'],
            'seller_id': variation['seller_id'],
            'product_id': correlation['product_id']
        }

    @pytest.fixture
    def database(self):
        client = MongoClient('127.0.0.1', 27017)
        return client.taz_tests

    def test_undefined_strategy_raises_error(self):
        with pytest.raises(UndefinedStrategyException):
            processor = MatchingProcessor()
            processor.assembler.assemble()

    @pytest.mark.parametrize(
        'variations_to_store,variation_to_match,expected_title,'
        'sellers_expected,variations_expected,'
        'product_correlations_expected,sku_correlations_expected', [
            (
                [],
                ProductSamples.unmatched_ml_variation_with_parent(),
                'Caneca Xablau Branca - 350ml',
                1,
                1,
                1,
                1,
            ),
            (
                [
                    ProductSamples.variation_without_parent_reference(),
                ],
                ProductSamples.variation_a_with_parent(),
                'Caneca Xablau Branca - 350ml',
                2,
                2,
                2,
                2,
            ),
            (
                [
                    ProductSamples.variation_without_parent_reference(),
                    ProductSamples.variation_a_with_parent(),
                ],
                ProductSamples.unmatched_ml_variation_with_parent(),
                'Caneca Xablau Branca - 350ml',
                3,
                3,
                3,
                3,
            ),
            (
                [
                    ProductSamples.variation_without_parent_reference(),
                    ProductSamples.variation_a_with_parent(),
                    ProductSamples.ml_parent_variation(),
                    ProductSamples.ml_variation_a_with_parent(),
                ],
                ProductSamples.unmatched_ml_variation_with_parent(),
                'Caneca Xablau Branca - 250ml',
                5,
                4,
                5,
                5,
            ),
            (
                [
                    ProductSamples.variation_without_parent_reference(),
                    ProductSamples.variation_a_with_parent(),
                    ProductSamples.ml_parent_variation(),
                    ProductSamples.ml_variation_a_with_parent(),
                    ProductSamples.seller_a_variation_with_parent(),
                    ProductSamples.seller_b_variation_with_parent(),
                ],
                ProductSamples.unmatched_ml_variation_with_parent(),
                'Caneca Xablau Branca - 250ml',
                7,
                5,
                7,
                7,
            ),
            (
                [
                    ProductSamples.matching_product_variation_a_110(
                        seller_id='mesbla',
                        seller_description='Mesbla SA',
                        ean='7898216299330',
                        parent_sku='2029230',
                        sku='202923100',
                    ),
                ],
                ProductSamples.matching_product_variation_a_220(
                    seller_id='mesbla',
                    seller_description='Mesbla SA',
                    ean='7898216299331',
                    parent_sku='2029230',
                    sku='202923101',
                ),
                'Ventilador de Mesa e Parede Mondial NV-15-6P 6 Pás',
                2,
                2,
                2,
                2,
            ),
            (
                [
                    ProductSamples.matching_seller_different_product_parent_skus_matching_a(),  # noqa
                    ProductSamples.matching_seller_different_product_parent_skus_matching_b(),  # noqa
                ],
                ProductSamples.matching_seller_different_product_parent_skus_matching_c(),  # noqa
                'Spray de envelopamento liquido Preto Fosco 400ML Multilaser - AU420',  # noqa
                1,
                1,
                1,
                3,
            ),
            (
                [
                    ProductSamples.ml_product_without_attributes(),
                ],
                ProductSamples.seller_product_with_attributes(),
                "Fone de Ouvido Multilaser Headphone Bluetooth Micro SD Radio com Microfone Hands - PH095",  # noqa
                1,
                1,
                1,
                2
            ),
            (
                [
                    ProductSamples.stamaco_sku_85(),
                    ProductSamples.stamaco_sku_86()
                ],
                ProductSamples.stamaco_sku_88(),
                "Disco de Serra Vdea Serramax",  # noqa
                1,
                1,
                1,
                3
            ),
        ]
    )
    def test_process_message_and_stores_unified(
        self,
        processor,
        database,
        variations_to_store,
        variation_to_match,
        expected_title,
        sellers_expected,
        variations_expected,
        product_correlations_expected,
        sku_correlations_expected
    ):
        """
        This is the "main" test for matching processor, since it
        asserts the main logic and parametrizes different product
        combinations and measures their outputs.
        Over the first iteration we force a bug when one or more
        correlations for the whole operation is expected.
        """
        variations = variations_to_store + [variation_to_match]

        for v in variations:
            database.raw_products.insert_one(v)
            if sku_correlations_expected > 1:
                database.id_correlations.insert_one({
                    'seller_id': v['seller_id'],
                    'variation_id': uuid4().hex,
                    'product_id': uuid4().hex,
                    'old_variation_ids': [],
                    'old_product_ids': [],
                    'sku': v['sku']
                })
            status, _ = processor.process_message({
                'sku': v['sku'],
                'action': CREATE_ACTION,
                'seller_id': v['seller_id']
            })
            assert status is not None

        sku_correlations = list(database.id_correlations.find({
            '$or': [
                {'sku': v['sku'], 'seller_id': v['seller_id']}
                for v in variations
            ]
        }))

        assert sku_correlations is not None
        assert len(sku_correlations) == sku_correlations_expected

        assert database.id_correlations.count_documents(
            {'product_id': sku_correlations[0]['product_id']}
        ) == product_correlations_expected

        for correlation in sku_correlations:
            product_id = correlation['product_id']

            result = database.unified_objects.find_one({'id': product_id})

            assert result is not None

            total_variations = len(result['variations'])
            assert total_variations == variations_expected

            total_sellers = 0
            for variation in result['variations']:
                total_sellers += len(variation['sellers'])

            assert 'seller_id' not in result
            assert 'seller_sku' not in result

            assert total_sellers == sellers_expected

    def test_process_message_deleting_single_variation(
        self,
        processor,
        database,
        single_variation_delete_match
    ):
        variation = single_variation_delete_match['variation']
        unified_product = database.unified_objects.find_one({
            'id': single_variation_delete_match['product_id'],
            'type': 'product',
        }, {'_id': 0})
        assert len(unified_product['variations']) == 3

        variation['disable_on_matching'] = True
        del variation['_id']
        database.raw_products.update_one(
            {},
            {'$set': variation}
        )

        processor.process_message({
            'sku': variation['sku'],
            'action': DELETE_ACTION,
            'seller_id': variation['seller_id']
        })

        unified_product = database.unified_objects.find_one({
            'id': single_variation_delete_match['product_id'],
            'type': 'product',
        })

        assert isinstance(unified_product, dict)
        assert len(unified_product['variations']) == 2

        total_sellers = 0
        for variation in unified_product['variations']:
            total_sellers += len(variation['sellers'])

        assert total_sellers == 2

    def test_process_message_deleting_whole_product(
        self,
        processor,
        database,
        whole_product_delete_match
    ):
        processor.process_message({
            'sku': whole_product_delete_match['sku'],
            'action': DELETE_ACTION,
            'seller_id': whole_product_delete_match['seller_id']
        })

        unified_product = database.unified_objects.find_one({
            'id': whole_product_delete_match['product_id'],
            'type': 'product',
        })

        assert isinstance(unified_product, dict)
        assert len(unified_product['variations']) == 0

    def test_two_products_with_attributes_and_one_product_without_attribute(
        self,
        database,
        processor
    ):
        products = [
            ProductSamples.matching_product_with_attributes_a(),
            ProductSamples.matching_product_with_attributes_b(),
            ProductSamples.matching_product_without_attributes_a()
        ]

        for product in products:
            database.raw_products.insert_one(product)
            status, _ = processor.process_message({
                'sku': product['sku'],
                'action': CREATE_ACTION,
                'seller_id': product['seller_id']
            })
            assert status is not None

        unified_objects = database.unified_objects.find()

        for unified_object in unified_objects:
            attributes = unified_object.get('attributes')

            if len(unified_object['variations']) == 2:
                assert len(attributes['color']['values']) == 2

            if len(unified_object['variations']) == 1:
                assert len(attributes) == 0

    def test_repeating_process_matching_returns_always_the_same_id(
        self,
        database,
        processor
    ):
        product = ProductSamples.matching_product_with_attributes_a()
        database.raw_products.insert_one(product)

        variation_id = None

        for _ in range(2):
            status, _ = processor.process_message({
                'sku': product['sku'],
                'action': CREATE_ACTION,
                'seller_id': product['seller_id']
            })
            assert status is not None

            unified_objects = list(database.unified_objects.find())
            assert len(unified_objects) == 1

            current_variation_id = unified_objects[0]['variations'][0]['id']

            if variation_id:
                assert variation_id == current_variation_id
            else:
                variation_id = current_variation_id

    def test_match_dismatch_rematch(self, database, processor):
        product_a = ProductSamples.matching_product_a()
        product_b = ProductSamples.matching_product_b()
        product_c = ProductSamples.matching_product_c()

        product_a['ean'] = '1'
        product_b['ean'] = '2'
        product_c['ean'] = '3'
        total_unified_objects = self._match(
            database,
            processor,
            product_a,
            product_b,
            product_c
        )
        assert total_unified_objects == 3

        product_a['ean'] = '0034264428874'
        product_b['ean'] = '0034264428874'
        product_c['ean'] = '0034264428874'
        total_unified_objects = self._match(
            database, processor,
            product_a, product_b, product_c
        )
        assert total_unified_objects == 2

        product_a['ean'] = '1'
        product_b['ean'] = '2'
        product_c['ean'] = '3'
        total_unified_objects = self._match(
            database, processor,
            product_a, product_b, product_c
        )
        assert total_unified_objects == 3

        product_a = ProductSamples.matching_product_a()
        product_b = ProductSamples.matching_product_b()
        product_c = ProductSamples.matching_product_c()

        total_unified_objects = self._match(
            database, processor,
            product_a, product_b, product_c
        )
        assert total_unified_objects == 2

    def _match(self, database, processor, product_a, product_b, product_c):
        products = [product_a, product_b, product_c]
        for product in products:
            database.raw_products.update_one({
                'sku': product['sku'],
                'seller_id': product['seller_id'],
            }, {'$set': product}, upsert=True)

        for product in products:
            processor.process_message({
                'sku': product['sku'],
                'action': CREATE_ACTION,
                'seller_id': product['seller_id']
            })
            assert database.id_correlations.count_documents(
                {'product_id': None}
            ) == 0
            assert database.id_correlations.count_documents(
                {'variation_id': None}
            ) == 0

        assert database.id_correlations.count_documents({}) == 3
        return database.unified_objects.count_documents({})

    def test_process_message_and_stores_unified_without_matching_variations(
        self,
        processor,
        database,
        caplog
    ):
        variation = ProductSamples.stamaco_sku_85()
        database.raw_products.insert_one(variation)

        with patch.object(
            processor.strategy.matcher.ProductMatcher,
            'match_variations',
            return_value=OrderedDict()
        ):
            status, _ = processor.process_message({
                'sku': variation['sku'],
                'action': CREATE_ACTION,
                'seller_id': variation['seller_id']
            })

        assert status is not None
        assert (
            'Removing product sku:85 seller:stamaco '
            'from matching queue, because couldn\'t '
            'finish the assemble'
        ) in caplog.text

    def test_process_message_should_update_id_correlations_of_deactivate_book(  # noqa
        self,
        database
    ):
        processor = MatchingProcessor(
            strategy=importlib.import_module(
                settings.STRATEGIES[OMNILOGIC_STRATEGY]
            ),
            exclusive_strategy=False
        )

        variations = [
            ProductSamples.magazineluiza_sku_222764000(),
            ProductSamples.meulivromegastore_sku_166271()
        ]

        variation_to_match = variations[0]

        enriched_variations = [
            EnrichedProductSamples.magazineluiza_sku_222764000(),
            EnrichedProductSamples.meulivromegastore_sku_166271()
        ]

        database.enriched_products.insert_many(enriched_variations)

        for variation in variations:
            for enriched in enriched_variations:
                if (
                    variation['sku'] == enriched['sku'] and
                    variation['seller_id'] == enriched['seller_id']
                ):
                    variation['matching_strategy'] = OMNILOGIC_STRATEGY
                    variation['product_hash'] = enriched['product_hash']
                    break

        database.raw_products.insert_many(variations)

        status, _ = processor.process_message({
            'sku': variation_to_match['sku'],
            'action': CREATE_ACTION,
            'seller_id': variation_to_match['seller_id']
        })

        assert status is not None

        sku_correlations = list(database.id_correlations.find({
            '$or': [
                {'sku': v['sku'], 'seller_id': v['seller_id']}
                for v in variations
            ]
        }))

        assert len(sku_correlations) == 2
        for correlation_info in sku_correlations:
            assert (
                correlation_info['product_id'] ==
                variations[0]['navigation_id']
            )

        last_variation = variations[1]

        last_variation['disable_on_matching'] = True
        criteria = {
            'sku': last_variation['sku'],
            'seller_id': last_variation['seller_id']
        }

        database.raw_products.update_one(criteria, {'$set': last_variation})

        status, _ = processor.process_message({
            'action': DELETE_ACTION,
            **criteria
        })

        sku_correlations = list(database.id_correlations.find({
            '$or': [
                {'sku': v['sku'], 'seller_id': v['seller_id']}
                for v in variations
            ]
        }))

        assert len(sku_correlations) == 2
        for correlation_info in sku_correlations:
            assert (
                correlation_info['product_id'] ==
                variations[0]['navigation_id']
            )

        new_variation = ProductSamples.authenticlivros_sku_1073972()
        new_enriched_variation = EnrichedProductSamples.authenticlivros_sku_1073972()  # noqa

        new_variation['product_hash'] = new_enriched_variation['product_hash']
        database.raw_products.insert_one(new_variation)
        database.enriched_products.insert_one(new_enriched_variation)

        status, _ = processor.process_message({
            'sku': new_variation['sku'],
            'action': CREATE_ACTION,
            'seller_id': new_variation['seller_id']
        })

        all_variations = variations + [new_variation]

        sku_correlations = list(database.id_correlations.find({
            '$or': [
                {'sku': v['sku'], 'seller_id': v['seller_id']}
                for v in all_variations
            ]
        }))

        assert sku_correlations is not None

        assert len(sku_correlations) == 3
        for correlation_info in sku_correlations:
            assert (
                correlation_info['product_id'] ==
                variations[0]['navigation_id']
            )
