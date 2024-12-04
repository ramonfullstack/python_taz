import pytest

from taz.core.matching.common.samples import ProductSamples
from taz.core.matching.strategies.auto_buybox.matcher import ProductMatcher
from taz.core.matching.strategies.tests.helpers import generate_medias


class TestProductMatcher:

    @pytest.fixture
    def matcher(self):
        return ProductMatcher()

    @pytest.fixture
    def trusted_variation_ean_list(self):
        trusted_variations = [
            ProductSamples.variation_a(),
            ProductSamples.variation_a_with_parent(),
            ProductSamples.seller_a_variation_with_parent()
        ]
        return [variation['ean'] for variation in trusted_variations]

    @pytest.fixture
    def same_attribute_variation(self, matcher, database):
        variations_to_store = [
            ProductSamples.ml_matching_product_variation_a_110(),
            ProductSamples.ml_matching_product_variation_a_220(),
            ProductSamples.ml_matching_product_variation_b_110(),
            ProductSamples.ml_matching_product_variation_b_220(),
            ProductSamples.ml_matching_product_variation_c_110(),
            ProductSamples.ml_matching_product_variation_c_220(),
        ]

        for variation in variations_to_store:
            database.raw_products.save(variation)
            database.medias.insert_many(generate_medias(variation))

        return ProductSamples.ml_matching_product_variation_c_220()

    @pytest.mark.parametrize(
        'list_variations,total_variations,total_sellers', [
            (
                [
                    ProductSamples.variation_a_match_main(),
                    ProductSamples.variation_b_match_a(),
                    ProductSamples.variation_c_match_d(),
                    ProductSamples.variation_d_match_b(),
                ],
                2,
                4
            ),
            (
                [ProductSamples.variation_a()],
                1,
                1
            ),
            (
                [
                    ProductSamples.variation_a(),
                    ProductSamples.variation_b()
                ],
                1,
                2
            ),
            (
                [
                    ProductSamples.variation_a(),
                    ProductSamples.disabled_variation(),
                    ProductSamples.variation_b()
                ],
                1,
                2
            ),
            (
                [
                    ProductSamples.variation_a(),
                    ProductSamples.variation_b(),
                    ProductSamples.unmatched_ml_variation(),
                    ProductSamples.disabled_variation()
                ],
                1,
                3
            ),
            (
                [
                    ProductSamples.matching_same_seller_without_attributes_b(),
                    ProductSamples.matching_same_seller_without_attributes_a(),
                    ProductSamples.matching_same_seller_without_attributes_c()
                ],
                1,
                1
            ),
            (
                [
                    ProductSamples.ml_similar_product_a(),
                    ProductSamples.seller_similar_product_a(),
                    ProductSamples.ml_similar_product_b()
                ],
                2,
                3
            ),
            (
                [
                    ProductSamples.seller_similar_product_a(),
                    ProductSamples.ml_similar_product_a(),
                    ProductSamples.ml_similar_product_b()
                ],
                2,
                3
            ),
            (
                [
                    ProductSamples.seller_product_with_attributes(),
                    ProductSamples.ml_product_without_attributes()
                ],
                1,
                1
            ),
            (
                [
                    ProductSamples.whirlpool_1339(),
                    ProductSamples.whirlpool_1338(),
                    ProductSamples.casaamerica_2015463(),
                    ProductSamples.casaamerica_2015515(),
                    ProductSamples.magazineluiza_088894700()
                ],
                3,
                5
            ),
        ]
    )
    def test_should_try_match_between_all_possible_variations(
        self, matcher, database,
        list_variations, total_variations, total_sellers
    ):
        for variation_to_match in list_variations:
            variations_to_store = list_variations.copy()
            variations_to_store.remove(variation_to_match)
            for p in variations_to_store + [variation_to_match]:
                database.raw_products.save(p)

            similar = matcher.match_variations(variation_to_match)
            assert len(similar) == total_variations

            non_unique_sellers_total = 0
            for group in similar.values():
                non_unique_sellers_total += len(group)
            assert non_unique_sellers_total == total_sellers

    @pytest.mark.parametrize(
        'variations_to_store,variation_to_match,total_variations,total_sellers', [  # noqa
            (
                [],
                ProductSamples.variation_a(),
                1,
                1
            ),
            (
                [ProductSamples.variation_a()],
                ProductSamples.variation_b(),
                1,
                2
            ),
            (
                [
                    ProductSamples.variation_a(),
                    ProductSamples.variation_b()
                ],
                ProductSamples.disabled_variation(),
                1,
                2
            ),
            (
                [
                    ProductSamples.variation_a(),
                    ProductSamples.variation_b(),
                    ProductSamples.disabled_variation(),
                ],
                ProductSamples.unmatched_ml_variation(),
                1,
                3
            ),
            (
                [
                    ProductSamples.matching_same_seller_without_attributes_b(),
                    ProductSamples.matching_same_seller_without_attributes_c()
                ],
                ProductSamples.matching_same_seller_without_attributes_a(),
                1,
                1
            ),
            (
                [
                    ProductSamples.ml_similar_product_a(),
                    ProductSamples.ml_similar_product_b()
                ],
                ProductSamples.seller_similar_product_a(),
                2,
                3
            ),
            (
                [
                    ProductSamples.seller_similar_product_a(),
                    ProductSamples.ml_similar_product_b()
                ],
                ProductSamples.ml_similar_product_a(),
                2,
                3
            ),
            (
                [
                    ProductSamples.seller_product_with_attributes(),
                ],
                ProductSamples.ml_product_without_attributes(),
                1,
                1
            ),
            (
                [
                    ProductSamples.casaamerica_sku_2019285(),
                    ProductSamples.cookeletroraro_sku_2002109(),
                    ProductSamples.magazineluiza_sku_216534900(),
                ],
                ProductSamples.whirlpool_sku_2003610(),
                1,
                2
            ),
            (
                [
                    ProductSamples.whirlpool_1339(),
                    ProductSamples.whirlpool_1338(),
                    ProductSamples.casaamerica_2015463(),
                    ProductSamples.casaamerica_2015515(),
                ],
                ProductSamples.magazineluiza_088894700(),
                3,
                5
            ),
        ]
    )
    def test_match_many_variations(
        self, matcher, database,
        variations_to_store, variation_to_match,
        total_variations, total_sellers
    ):
        for p in variations_to_store + [variation_to_match]:
            database.raw_products.save(p)

        similar = matcher.match_variations(variation_to_match)
        assert len(similar) == total_variations

        non_unique_sellers_total = 0
        for group in similar.values():
            non_unique_sellers_total += len(group)
        assert non_unique_sellers_total == total_sellers

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

    def test_match_variations(
        self,
        matcher,
        matched_variation,
    ):
        grouped_variations = matcher.match_variations(
            matched_variation,
        )
        assert len(grouped_variations) == 5

        keys = list(grouped_variations.keys())
        assert len(grouped_variations[keys[0]]) == 1
        assert len(grouped_variations[keys[1]]) == 1
        assert len(grouped_variations[keys[2]]) == 2
        assert len(grouped_variations[keys[3]]) == 3
        assert len(grouped_variations[keys[4]]) == 2

    def test_same_attributes_with_different_parents_arent_grouped(
        self,
        matcher,
        same_attribute_variation
    ):
        grouped_variations = matcher.match_variations(
            same_attribute_variation
        )
        assert len(grouped_variations) == 2

        for values in grouped_variations.values():
            assert len(values) == 1

    def test_same_product_different_sellers_matches_variations_groups_sellers(
        self,
        matcher,
        same_product_different_sellers
    ):
        grouped_variations = matcher.match_variations(
            same_product_different_sellers
        )
        assert len(grouped_variations) == 2

        for values in grouped_variations.values():
            assert len(values) == 2

    def test_magoo_matching_bug(self, matcher, matching_magoo_product):
        grouped_variations = matcher.match_variations(
            matching_magoo_product
        )
        assert len(grouped_variations) == 1

        for values in grouped_variations.values():
            assert len(values) == 2

    @pytest.mark.parametrize('variation', [
        ProductSamples.matching_product_without_attributes_a(),
        ProductSamples.variation_without_ean_and_attributes(),
        ProductSamples.disabled_variation()
    ])
    def test_return_false_to_variation_without_attribute_and_ean_not_in_trustable_list(  # noqa
        self, matcher, variation, trusted_variation_ean_list
    ):
        assert matcher._variation_is_trustable(
            variation, trusted_variation_ean_list
        ) is False

    @pytest.mark.parametrize('variation', [
        ProductSamples.variation_without_ean_but_with_attributes(),
        ProductSamples.variation_without_attributes_but_with_ean_trustable()
    ])
    def test_return_true_to_variation_with_attribute_or_ean_in_trustable_list(
        self, matcher, variation, trusted_variation_ean_list
    ):
        assert matcher._variation_is_trustable(
            variation, trusted_variation_ean_list
        ) is True

    @pytest.mark.parametrize(
        'variations_approved_to_match,'
        'possible_relatives,'
        'trusted_variation_ean_list', [
            (
                [
                    ProductSamples.seller_similar_product_a(),
                    ProductSamples.ml_similar_product_a()
                ],
                [ProductSamples.ml_similar_product_b()],
                {'0040094922475'}
            )
        ]
    )
    def test_approve_valid_variation_previously_rejected_to_similar_relatives(
        self, matcher,
        variations_approved_to_match,
        possible_relatives,
        trusted_variation_ean_list
    ):
        similar_variations = matcher._retry_match_variations_each_other(
            variations_approved_to_match,
            possible_relatives,
            trusted_variation_ean_list
        )
        assert len(similar_variations) == 3

    @pytest.mark.parametrize(
        'variations_approved_to_match,'
        'possible_relatives,'
        'trusted_variation_ean_list', [
            (
                [
                    ProductSamples.matching_same_seller_without_attributes_b(),
                ],
                [
                    ProductSamples.matching_same_seller_without_attributes_a(),
                    ProductSamples.matching_same_seller_without_attributes_c()
                ],
                {'3348900782556'}
            )
        ]
    )
    def test_reject_invalid_variation_previously_rejected_to_similar_relatives(
        self, matcher,
        variations_approved_to_match,
        possible_relatives,
        trusted_variation_ean_list
    ):
        similar_variations = matcher._retry_match_variations_each_other(
            variations_approved_to_match,
            possible_relatives,
            trusted_variation_ean_list
        )
        assert len(similar_variations) == 1
