import pytest

from taz.core.matching.common.samples import ProductSamples
from taz.core.matching.strategies.single_seller.matcher import ProductMatcher


class TestProductMatcher:

    @pytest.fixture
    def matcher(self):
        return ProductMatcher()

    @pytest.mark.parametrize(
        'variations_to_store,variation_to_match,expected_composition', [  # noqa
            (
                [],
                ProductSamples.variation_a(),
                [(1, 1)],
            ),
            (
                [ProductSamples.variation_a()],
                ProductSamples.variation_b(),
                [(1, 1)],
            ),
            (
                [
                    ProductSamples.variation_a(),
                    ProductSamples.variation_b(),
                    ProductSamples.disabled_variation(),
                ],
                ProductSamples.unmatched_ml_variation(),
                [(1, 1)],
            ),
            (
                [
                    ProductSamples.matching_same_seller_without_attributes_b(),
                    ProductSamples.matching_same_seller_without_attributes_c()
                ],
                ProductSamples.matching_same_seller_without_attributes_a(),
                [(1, 1)]
            )
        ]
    )
    def test_match_many_variations(
        self,
        matcher,
        database,
        variations_to_store,
        variation_to_match,
        expected_composition
    ):
        for p in variations_to_store + [variation_to_match]:
            database.raw_products.save(p)

        similar = matcher.match_variations(variation_to_match)

        for total_variations, total_sellers in expected_composition:
            assert len(similar) == total_variations
            for group in similar.values():
                assert len(group) == total_sellers

    def test_match_variations(
        self,
        matcher,
        matched_variation,
    ):
        grouped_variations = matcher.match_variations(
            matched_variation,
        )
        assert len(grouped_variations) == 3

        keys = list(grouped_variations.keys())
        assert len(grouped_variations[keys[0]]) == 1
        assert len(grouped_variations[keys[1]]) == 1
        assert len(grouped_variations[keys[2]]) == 1

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
            assert len(values) == 1

    def test_magoo_matching_bug(self, matcher, matching_magoo_product):
        grouped_variations = matcher.match_variations(
            matching_magoo_product
        )
        assert len(grouped_variations) == 1

        for values in grouped_variations.values():
            assert len(values) == 1

    @pytest.mark.parametrize(
        'variation, quantity_expected', [
            (
                ProductSamples.pequenostravessos_sku_571743566(),
                2
            ),
            (
                ProductSamples.pequenostravessos_sku_571743563(),
                1
            ),
            (
                ProductSamples.pequenostravessos_sku_571743567(),
                2
            ),
        ]
    )
    def test_matching_same_parent_but_with_different_attributes(
        self,
        matcher,
        database,
        variation,
        quantity_expected
    ):
        variations = [
            ProductSamples.pequenostravessos_sku_571743566(),
            ProductSamples.pequenostravessos_sku_571743563(),
            ProductSamples.pequenostravessos_sku_571743567()
        ]

        for v in variations:
            database.raw_products.save(v)

        grouped_variations = matcher.match_variations(variation)
        assert len(grouped_variations) == quantity_expected

    def test_matching_variations_even_if_one_of_then_is_disable(
        self,
        matcher,
        database
    ):
        variations = [
            ProductSamples.variation_a(),
            ProductSamples.variation_b(),
        ]

        variation_to_match = ProductSamples.disabled_variation()

        for v in variations + [variation_to_match]:
            database.raw_products.save(v)

        similar = matcher.match_variations(variation_to_match)
        assert len(similar) == 1
        for group in similar.values():
            assert group[0]['seller_id'] == 'seller_c'

    def test_duplicated_attributes_single_seller_remove_9482200926(
        self,
        matcher,
        variations_with_attributes_duplicated
    ):
        grouped_variations = matcher._group_variations(
            variations_with_attributes_duplicated
        )
        grouped_variations = dict(grouped_variations)

        skus_published = [
            '14497878997', '9482200887', '9482200890', '9482200881',
            '9482200904', '9482200894', '9482200912', '9482200916',
            '9482200922'
        ]

        skus_results = [
            item['sku']
            for group in grouped_variations.values()
            for item in group
        ]

        assert '9482200926' not in skus_results
        assert len(skus_results) == len(skus_published)
        for item in skus_published:
            assert item in skus_results

    def test_duplicated_attributes_single_seller_published_all_skus(
        self,
        matcher,
        variations_without_attributes_duplicated
    ):
        skus_published = [
            '9482200926', '9482200887', '9482200890', '9482200881',
            '9482200904', '9482200894', '9482200912', '9482200916',
            '9482200922'
        ]

        grouped_variations = matcher._group_variations(
            variations_without_attributes_duplicated
        )
        grouped_variations = dict(grouped_variations)

        skus_results = [
            item['sku']
            for group in grouped_variations.values()
            for item in group
        ]

        assert len(skus_results) == len(skus_published)
        for item in skus_published:
            assert item in skus_results

    def test_without_attributes_single_seller_published_all_skus(
        self,
        matcher,
        variations_with_attributes_duplicated
    ):
        skus_published = [
            '14497878997', '9482200926', '9482200887', '9482200890',
            '9482200881', '9482200904', '9482200894', '9482200912',
            '9482200916', '9482200922'
        ]

        for variation in variations_with_attributes_duplicated:
            variation.update({'attributes': {}})

        grouped_variations = matcher._group_variations(
            variations_with_attributes_duplicated
        )
        grouped_variations = dict(grouped_variations)

        skus_results = [
            item['sku']
            for group in grouped_variations.values()
            for item in group
        ]

        assert len(skus_results) == len(skus_published)
        for item in skus_published:
            assert item in skus_results

    def test_differents_brands_and_attributes_single_seller_return_one_per_group( # noqa
        self,
        matcher,
        variations_without_attributes_duplicated
    ):
        skus_published = [
            v['sku']
            for v in variations_without_attributes_duplicated
        ]

        for variation in variations_without_attributes_duplicated:
            variation.update({'brand': variation['sku']})

        grouped_variations = matcher._group_variations(
            variations_without_attributes_duplicated
        )
        grouped_variations = dict(grouped_variations)

        skus_results = [
            item['sku']
            for group in grouped_variations.values()
            for item in group
        ]

        assert len(skus_results) == len(skus_published)
        for item in skus_published:
            assert item in skus_results

        for item in grouped_variations.values():
            assert len(item) == 1
