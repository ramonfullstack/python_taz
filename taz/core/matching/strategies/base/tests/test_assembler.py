from collections import OrderedDict
from unittest.mock import patch
from uuid import uuid4

import pytest
from simple_settings.utils import settings_stub

from taz.constants import (
    META_TYPE_PRODUCT_AVERAGE_RATING,
    META_TYPE_PRODUCT_TOTAL_REVIEW_COUNT
)
from taz.core.matching.common.samples import ProductSamples
from taz.core.matching.strategies.base.assembler import BaseAssembler


class TestProductAssembler:

    @pytest.fixture
    def assembler(self):
        return BaseAssembler('BASE_STRATEGY')

    @pytest.mark.parametrize('fulfillment,enabled_fulfillment,enabled_parent_matching', [ # noqa
        ([True, True, False, False, True], True, False),
        ([True, False, None, None, False], True, True),
        ([None, None, None, None, None], False, False)
    ])
    def test_assemble_returns_canonical_ids_and_info_from_variations_if_exists( # noqa
        self,
        assembler,
        mongo_database,
        fulfillment,
        enabled_fulfillment,
        enabled_parent_matching
    ):
        product = dict(ProductSamples.ml_matching_product_variation_a_110())
        product['seller_id'] = 'test'
        product['sku'] = '12345'
        product['matching_uuid'] = '7e36684b186c495197e139c9029e7af2'
        product['extra_data'] = [{'name': 'is_magalu_indica', 'value': 'true'}]

        variation_group_1 = [
            ProductSamples.seller_a_variation_with_parent(),
            ProductSamples.seller_b_variation_with_parent(),
            ProductSamples.seller_c_variation_with_parent()
        ]

        variation_group_2 = [
            ProductSamples.ml_matching_product_variation_a_110(),
            product
        ]

        variations_groups = variation_group_1 + variation_group_2
        matching_uuids = []
        extra_datas = []
        parent_matching_uuids = []

        for index, value in enumerate(variations_groups):
            if fulfillment[index] is not None:
                value['fulfillment'] = fulfillment[index]

            matching_uuids.append(value.get('matching_uuid'))
            extra_datas.append(value.get('extra_data'))
            parent_matching = None

            if enabled_parent_matching and value.get('matching_uuid'):
                parent_matching = '5c2275661d8f11ed861d0242ac120002'
                value['parent_matching_uuid'] = '5c2275661d8f11ed861d0242ac120002' # noqa

            parent_matching_uuids.append(parent_matching)

        for variation in variations_groups:
            mongo_database.raw_products.insert_one(variation)
            mongo_database.items_ids.insert_one({
                'id': variation['navigation_id']
            })

        variation_groups = OrderedDict()
        group_key_1 = uuid4().hex
        variation_groups[group_key_1] = variation_group_1

        canonical_ids_1 = []
        for x in variation_group_1:
            canonical_ids_1.append(x['navigation_id'])

        group_key_2 = uuid4().hex
        variation_groups[group_key_2] = variation_group_2

        canonical_ids_2 = []
        for y in variation_group_2:
            canonical_ids_2.append(y['navigation_id'])

        with settings_stub(
            ENABLE_FULFILLMENT=enabled_fulfillment,
            ENABLE_PARENT_MATCHING=enabled_parent_matching
        ):
            assembled_product, _ = assembler.assemble(variation_groups)

        variations = assembled_product['variations']
        assert variations[0]['canonical_ids'] == canonical_ids_1
        assert variations[1]['canonical_ids'] == canonical_ids_2

        unified_objects = list(mongo_database.unified_objects.find())

        count = 0
        for x, variation in enumerate(unified_objects[0]['variations']):
            for y, seller in enumerate(variation['sellers']):
                assert fulfillment[count] == seller.get('fulfillment') # noqa
                assert matching_uuids[count] == seller.get('matching_uuid') # noqa
                assert parent_matching_uuids[count] == seller.get('parent_matching_uuid') # noqa
                assert extra_datas[count] == seller.get('extra_data')
                count += 1

    @pytest.fixture
    def none_review_data(self, mongo_database):
        for product_id in [
            'ou23ou23ou',
            '0123456',
            '82323jjjj3'
        ]:
            mongo_database.customer_behaviors.insert_many([
                {
                    'product_id': product_id,
                    'type': META_TYPE_PRODUCT_AVERAGE_RATING,
                    'value': None
                },
                {
                    'product_id': product_id,
                    'type': META_TYPE_PRODUCT_TOTAL_REVIEW_COUNT,
                    'value': None
                }
            ])

    def test_build_product_review_none_values(
        self,
        assembler,
        mongo_database,
        none_review_data
    ):
        variations = [
            ProductSamples.seller_a_variation_with_parent(),
            ProductSamples.seller_b_variation_with_parent(),
            ProductSamples.seller_c_variation_with_parent(),
        ]

        mongo_database.raw_products.insert_many(variations)

        source_ids = [
            (
                variation['sku'],
                variation['seller_id'],
                variation['parent_sku']
            )
            for variation in variations
        ]

        variation_groups = OrderedDict({uuid4().hex: variations})
        elected_id, _ = assembler.find_product_id(source_ids)
        product = assembler._build_product(elected_id, variation_groups)

        assert product['review_count'] == 0
        assert product['review_score'] == 0

    @pytest.mark.parametrize('attributes, expected', [
        (
            [{'type': 'tom-de-pele', 'value': 'Pink'}],
            [{'type': 'tom-de-pele', 'value': 'Pink', 'label': 'Tom de pele'}]
        ),
        (
            [{'type': 'color', 'value': 'Pink'}],
            [{'type': 'color', 'value': 'Pink', 'label': 'Cor'}]
        ),
        (
            [{'type': None, 'value': 'Pink'}],
            [{'type': None, 'value': 'Pink'}]
        ),
        (
            [{'type': 'Color', 'value': 'Pink'}],
            [{'type': 'Color', 'value': 'Pink', 'label': 'Cor'}]
        ),
        (
            [{'type': 'Voltage', 'value': '110V'}],
            [{'type': 'Voltage', 'value': '110V', 'label': 'Voltagem'}]
        )
    ])
    def test_should_set_attribute_labels(
        self,
        assembler,
        attributes,
        expected
    ):
        assembler._set_attribute_labels(attributes)
        assert attributes == expected

    def test_assemble_with_empty_variations_return_false(
        self,
        assembler
    ):
        variation_groups = OrderedDict()
        assembled_product, _ = assembler.assemble(variation_groups)

        assert not assembled_product

    def test_disassemble_should_update_unified_object(
        self,
        assembler,
        mongo_database
    ):
        variations_to_store = [
            ProductSamples.seller_a_variation_with_parent(),
            ProductSamples.seller_b_variation_with_parent(),
            ProductSamples.seller_c_variation_with_parent(),
        ]

        for variation in variations_to_store:
            mongo_database.raw_products.insert_one(variation)
            mongo_database.items_ids.insert_one({
                'id': variation['navigation_id']
            })

        variation_groups = OrderedDict()
        group_key = uuid4().hex
        variation_groups[group_key] = variations_to_store

        unified_product, _ = assembler.assemble(variation_groups)

        assert len(unified_product['variations'][0]['sellers']) == 3

        unified_product = assembler.disassemble(variations_to_store[-1])

        assert len(unified_product['variations'][0]['sellers']) == 2
        assert not unified_product.get('_id')

    def test_disassemble_should_do_nothing_if_dont_find_unified_object(
        self,
        assembler,
        mongo_database
    ):
        variation = ProductSamples.seller_c_variation_with_parent()
        mongo_database.raw_products.insert_one(variation)

        unified_product = assembler.disassemble(variation)

        assert not unified_product

    def test_find_product_id_should_discard_old_unified_objects(
        self,
        assembler,
        mongo_database
    ):
        variations = [
            ProductSamples.seller_a_variation_with_parent(),
            ProductSamples.seller_b_variation_with_parent(),
            ProductSamples.seller_c_variation_with_parent(),
        ]

        for variation in variations:
            mongo_database.raw_products.insert_one(variation)
            mongo_database.unified_objects.insert_one({
                'id': variation['navigation_id']
            })
            mongo_database.id_correlations.insert_one({
                'sku': variation['sku'],
                'seller_id': variation['seller_id'],
                'product_id': variation['navigation_id'],
                'variation_id': variation['navigation_id']
            })

        source_ids = [
            (
                variation['sku'],
                variation['seller_id'],
                variation['parent_sku']
            )
            for variation in variations
        ]

        assert len(list(mongo_database.unified_objects.find())) == 3

        elected_id, _ = assembler.find_product_id(source_ids)

        assert len(list(mongo_database.unified_objects.find())) == 1

    @pytest.mark.parametrize('attributes', [
        (None),
        ([])
    ])
    def test_build_product_with_attributes_is_empty(
        self,
        assembler,
        mongo_database,
        attributes
    ):
        variation = ProductSamples.seller_a_variation_with_parent()
        variation['attributes'] = attributes
        mongo_database.raw_products.insert_one(variation)
        variation_groups = OrderedDict({uuid4().hex: [variation]})
        elected_id = assembler.get_product_id(variation_groups)
        product = assembler._build_product(elected_id, variation_groups)
        assert product['attributes'] == {}

    def test_build_product_without_attributes(
        self,
        assembler,
        mongo_database
    ):
        variation = ProductSamples.seller_a_variation_with_parent()
        del variation['attributes']
        mongo_database.raw_products.insert_one(variation)
        variation_groups = OrderedDict({uuid4().hex: [variation]})
        elected_id = assembler.get_product_id(variation_groups)
        product = assembler._build_product(elected_id, variation_groups)
        assert product['attributes'] == {}

    def test_when_product_1p_in_offer_then_return_1p_winning_matching(
        self,
        assembler
    ):
        winning_variation = ProductSamples.magazineluiza_sku_217148200()
        grouped_variations = [
            winning_variation,
            ProductSamples.casa_e_video_sku_8186(),
            ProductSamples.madeiramadeira_openapi_sku_302110()
        ]

        result = assembler._select_winning_variation(
            grouped_variations
        )
        assert result == {
            'seller_id': winning_variation['seller_id'],
            'seller_sku': winning_variation['sku']
        }

    def test_when_offer_without_product_1p_then_return_variation_with_highest_score_winning_matching(  # noqa
        self,
        assembler
    ):
        winning_variation = ProductSamples.casa_e_video_sku_8186()
        grouped_variations = [
            winning_variation,
            ProductSamples.madeiramadeira_openapi_sku_302110()
        ]
        with patch.object(
            BaseAssembler, '_get_highest_score'
        ) as mock_get_highest_score:
            mock_get_highest_score.return_value = {
                'sku': winning_variation['sku'],
                'seller_id': winning_variation['seller_id']
            }
            result = assembler._select_winning_variation(
                grouped_variations
            )

        assert result == {
            'seller_id': winning_variation['seller_id'],
            'seller_sku': winning_variation['sku']
        }

    def test_when_get_product_with_higgest_score_then_return_product_with_score_100(  # noqa
        self,
        assembler,
        mongo_database
    ):
        mock_scores = [
            {'seller_id': 'a', 'sku': 'a', 'final_score': 10, 'active': True},
            {'seller_id': 'b', 'sku': 'b', 'final_score': 20, 'active': True},
            {'seller_id': 'c', 'sku': 'c', 'final_score': 100, 'active': True}
        ]
        skus = [
            {'sku': v['sku'], 'seller_id': v['seller_id']}
            for v in mock_scores
        ]
        mongo_database.scores.insert_many(mock_scores)
        result = assembler._get_highest_score(skus)
        assert result['seller_id'] == 'c'

    def test_when_get_variation_category_subcategory_then_return_data(
        self,
        assembler
    ):
        subs = assembler._get_variation_category_and_subcategory(
            ProductSamples.authenticlivros_sku_1073972()
        )

        assert dict(subs) == {
            'LI': {
                'id': 'LI',
                'subcategories': [{'id': 'LLIT'}]
            }
        }

    def test_when_get_variation_category_subcategory_then_return_none(
        self,
        assembler
    ):
        product = ProductSamples.authenticlivros_sku_1073972()
        product['categories'] = []
        subs = assembler._get_variation_category_and_subcategory(
            product
        )

        assert not subs

    def test_when_mount_buybox_with_duplicate_offers_from_a_seller_then_return_one_variation( # noqa
        self,
        assembler,
        mongo_database
    ):
        variations = [
            ProductSamples.variation_a(),
            ProductSamples.variation_a_match_main(),
        ]
        variation_groups = OrderedDict({})
        variation_groups[uuid4().hex] = variations
        elected_id = variations[0]['navigation_id']

        mongo_database.raw_products.insert_many(variations)

        payload = assembler._build_product(elected_id, variation_groups)
        assert elected_id in payload['url']
        assert len(payload['variations']) == 1

    @pytest.mark.parametrize(
        'variations,expected',
        [
            (
                [
                    ProductSamples.disabled_variation(),
                    ProductSamples.variation_a(),
                    ProductSamples.variation_b(),
                ],
                ProductSamples.variation_a()
            ),
            (
                [
                    ProductSamples.variation_a(),
                ],
                ProductSamples.variation_a(),
            )
        ]
    )
    def test_when_mount_buybox_with_disabled_variation(
        self,
        assembler,
        mongo_database,
        variations,
        expected,
    ):
        variation_groups = OrderedDict({})
        variation_groups[uuid4().hex] = variations
        elected_id = expected['navigation_id']

        mongo_database.raw_products.insert_many(variations)

        payload = assembler._build_product(elected_id, variation_groups)

        assert elected_id in payload['url']
        assert len(payload['variations']) == 1

        winner = payload['variations'][0]
        assert winner['main_media']['seller_sku'] == expected['sku']
        assert winner['main_media']['seller_id'] == expected['seller_id']
        assert winner['factsheet']['seller_sku'] == expected['sku']
        assert winner['factsheet']['seller_id'] == expected['seller_id']
