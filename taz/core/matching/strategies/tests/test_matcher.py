import pytest

from taz.core.matching.common.samples import ProductSamples
from taz.core.matching.strategies.auto_buybox.matcher import (
    ProductMatcher as auto_buybox_matcher
)
from taz.core.matching.strategies.single_seller.matcher import (
    ProductMatcher as single_seller_matcher
)


class TestMatcher:

    @pytest.mark.parametrize('matcher', [
        (single_seller_matcher()),
        (auto_buybox_matcher())
    ])
    def test_sort_variations_by_default_seller_priority(
        self, matcher, variations_to_test
    ):
        sorted_variations = matcher._sort_by_default_seller_priority(
            variations_to_test
        )
        assert len(sorted_variations) == 3
        assert sorted_variations[0]['sku'] == '723829300'
        assert sorted_variations[1]['sku'] == '623728900'
        assert sorted_variations[2]['sku'] == '8weuwe88we'

    @pytest.mark.parametrize('matcher', [
        (single_seller_matcher()),
        (auto_buybox_matcher())
    ])
    def test_sort_variations_by_biggest_grade(
        self, matcher, variations_to_test
    ):
        sorted_variations = matcher._sort_by_biggest_grade(
            variations_to_test
        )
        assert len(sorted_variations) == 9
        assert sorted_variations[0]['sku'] == '8weuwe88we'
        assert sorted_variations[1]['sku'] == '623728900'
        assert sorted_variations[2]['sku'] == '723829300'
        assert sorted_variations[3]['sku'] == '82323jjjj3'
        assert sorted_variations[4]['sku'] == '098asdwe28'
        assert sorted_variations[5]['sku'] == 'ou23ou23ou'
        assert sorted_variations[6]['sku'] == '723uwej2u3'
        assert sorted_variations[7]['sku'] == '819283iqw'
        assert sorted_variations[8]['sku'] == '72384uoueg'

    @pytest.mark.parametrize('matcher, expected_sorted_variations', [
        (
            single_seller_matcher(),
            [
                ProductSamples.ml_variation_a_with_parent(),
                ProductSamples.unmatched_ml_variation_with_parent(),
                ProductSamples.ml_parent_variation(),
                ProductSamples.seller_a_variation_with_parent(),
                ProductSamples.seller_b_variation_with_parent(),
                ProductSamples.seller_c_variation_with_parent(),
                ProductSamples.variation_without_parent_reference(),
                ProductSamples.variation_a_with_parent(),
                ProductSamples.variation_without_ean(),
            ],
        ),
        (
            auto_buybox_matcher(),
            [
                ProductSamples.ml_variation_a_with_parent(),
                ProductSamples.unmatched_ml_variation_with_parent(),
                ProductSamples.ml_parent_variation(),
                ProductSamples.seller_a_variation_with_parent(),
                ProductSamples.seller_b_variation_with_parent(),
                ProductSamples.seller_c_variation_with_parent(),
                ProductSamples.variation_without_parent_reference(),
                ProductSamples.variation_a_with_parent(),
                ProductSamples.variation_without_ean(),
            ]
        )
    ])
    def test_sort_variations(
        self, matcher, variations_to_test, expected_sorted_variations
    ):
        sorted_variations = matcher.sort_variations(variations_to_test)
        sorted_keys = [s['sku'] for s in sorted_variations]
        expected_keys = [s['sku'] for s in expected_sorted_variations]
        assert sorted_keys == expected_keys

    @pytest.mark.parametrize('matcher', [
        (single_seller_matcher()),
        (auto_buybox_matcher())
    ])
    def test_same_parent_with_same_seller_groups_by_ean(
        self,
        matcher,
        same_parent_different_ean
    ):
        grouped_variations = matcher.match_variations(
            same_parent_different_ean
        )
        assert len(grouped_variations) == 2

        for values in grouped_variations.values():
            assert len(values) == 1

    @pytest.mark.parametrize('matcher', [
        (single_seller_matcher()),
        (auto_buybox_matcher())
    ])
    def test_same_parent_with_different_seller_doesnt_group(
        self,
        matcher,
        same_parent_different_sellers_variation
    ):
        grouped_variations = matcher.match_variations(
            same_parent_different_sellers_variation
        )
        assert len(grouped_variations) == 3

        for values in grouped_variations.values():
            assert len(values) == 1

    @pytest.mark.parametrize('matcher', [
        (single_seller_matcher()),
        (auto_buybox_matcher())
    ])
    def test_same_parent_with_same_seller_groups_only_by_variation(
        self,
        matcher,
        same_parent_variation
    ):
        grouped_variations = matcher.match_variations(
            same_parent_variation
        )
        assert len(grouped_variations) == 3

        for values in grouped_variations.values():
            assert len(values) == 1

    @pytest.mark.parametrize('matcher', [
        (single_seller_matcher()),
        (auto_buybox_matcher())
    ])
    def test_seller_matching_different_variations(
        self, matcher, matching_seller_different_variations
    ):
        grouped_variations = matcher.match_variations(
            matching_seller_different_variations
        )
        assert len(grouped_variations) == 2

        for values in grouped_variations.values():
            assert len(values) == 1

    @pytest.mark.parametrize('matcher, variation', [
        (single_seller_matcher(), ProductSamples.variation_a()),
        (single_seller_matcher(), ProductSamples.variation_b()),
        (single_seller_matcher(), ProductSamples.matching_magoo_product()),
        (auto_buybox_matcher(), ProductSamples.variation_a()),
        (auto_buybox_matcher(), ProductSamples.variation_b()),
        (auto_buybox_matcher(), ProductSamples.matching_magoo_product()),
    ])
    def test_seller_sorted_variation_multiple_attributes_bugfix(
        self, matcher, database, variation
    ):
        database.raw_products.save(variation)
        grouped_variations = matcher.match_variations(variation)
        assert grouped_variations is not None
