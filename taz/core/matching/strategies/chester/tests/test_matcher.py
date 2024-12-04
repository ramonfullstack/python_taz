import pytest

from taz.constants import CHESTER_STRATEGY
from taz.core.matching.common.samples import ProductSamples
from taz.core.matching.strategies.chester.assembler import ProductAssembler
from taz.core.matching.strategies.chester.matcher import ProductMatcher


class TestProductMatcherChester:

    @pytest.fixture
    def matcher(self):
        return ProductMatcher()

    @pytest.fixture
    def assembler(self):
        return ProductAssembler(CHESTER_STRATEGY)

    def test_matcher_chester_with_success(
        self,
        mongo_database,
        variations,
        matcher,
        mock_matching_uuid
    ):
        for variation in variations:
            variation['matching_strategy'] = CHESTER_STRATEGY
            variation['matching_uuid'] = mock_matching_uuid

        mongo_database.raw_products.insert_many(variations)

        response = matcher.match_variations(variations[0])
        assert len(response) == 1

    def test_assembler_chester_strategy_with_success(
        self,
        mongo_database,
        variations,
        mock_matching_uuid,
        assembler,
        matcher
    ):
        for variation in variations:
            variation['matching_strategy'] = CHESTER_STRATEGY
            variation['matching_uuid'] = mock_matching_uuid
            mongo_database.raw_products.insert_one(variation)

        match_variations = matcher.match_variations(variations[0])
        response = assembler.assemble(match_variations)
        assert len(response) == 2

    def test_matcher_chester_strategy_product_not_found(
        self,
        mongo_database,
        matcher,
        variations,
        caplog
    ):
        response = matcher.match_variations(variations[0])
        sku = variations[0]['sku']
        seller_id = variations[0]['seller_id']

        assert len(response) == 0
        assert (
            f'Product with sku:{sku} and seller_id:{seller_id} '
            'not found in raw products' in caplog.text
        )

    def test_matcher_chester_strategy_with_variation_without_matching_uuid(
        self,
        mongo_database,
        assembler,
        variations,
        matcher
    ):
        variations[0]['matching_strategy'] = CHESTER_STRATEGY
        mongo_database.raw_products.insert_one(variations[0])

        response = matcher.match_variations(variations[0])
        assert len(response) == 1

    def test_assembler_chester_strategy_with_variation_without_matching_uuid(
        self,
        mongo_database,
        assembler,
        variations,
        matcher
    ):
        variations[0]['matching_strategy'] = CHESTER_STRATEGY
        mongo_database.raw_products.insert_one(variations[0])

        match_variations = matcher.match_variations(variations[0])
        assert len(match_variations) == 1

        assembled_product, _ = assembler.assemble(match_variations)
        assert len(assembled_product['variations']) == 1

    def test_chester_strategy_gather_self_and_similar_variations(
        self,
        mongo_database,
        matcher,
        variations,
        mock_matching_uuid
    ):
        for variation in variations:
            variation['matching_uuid'] = mock_matching_uuid
            variation['matching_strategy'] = CHESTER_STRATEGY

        mongo_database.raw_products.insert_many(variations)
        response = matcher._gather_self_and_similar_variations(variations[0])

        assert len(response) == 10

    def test_assembler_chester_strategy_with_books(
        self,
        mongo_database,
        assembler,
        matcher,
        mock_matching_uuid
    ):
        products = [
            ProductSamples.livrariaflorence2_sku_9788543105757(),
            ProductSamples.livrariasebocapricho_sku_23036521(),
            ProductSamples.magazineluiza_sku_221841200(),
            ProductSamples.livrariaflorence2_sku_9788543105758(),
            ProductSamples.saraiva_sku_10260263()
        ]

        for product in products:
            product['matching_uuid'] = mock_matching_uuid
            product['matching_strategy'] = CHESTER_STRATEGY

        mongo_database.raw_products.insert_many(products)

        match_variations = matcher.match_variations(products[0])
        assembled_product, _ = assembler.assemble(match_variations)

        assembled_variations = assembled_product['variations']
        assert len(assembled_variations) == 1
        assert len(assembled_variations[0]['sellers']) == 4

    def test_assembler_chester_strategy_books_with_attributes(
        self,
        mongo_database,
        assembler,
        matcher,
        mock_matching_uuid
    ):
        products = [
            ProductSamples.book7_sku_9788506082645(),
            ProductSamples.cliquebooks_sku_543242_1(),
            ProductSamples.magazineluiza_sku_222786900()
        ]

        for product in products:
            product['matching_uuid'] = mock_matching_uuid
            product['matching_strategy'] = CHESTER_STRATEGY

        mongo_database.raw_products.insert_many(products)

        match_variations = matcher.match_variations(products[0])
        assembled_product, _ = assembler.assemble(match_variations)

        assemble_variations = assembled_product['variations']
        assert len(assemble_variations) == 1
        assert len(assemble_variations[0]['sellers']) == 2

    def test_duplicated_attributes_chester_strategy_remove_9482200926(
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

    def test_duplicated_attributes_chester_strategy_published_all_skus(
        self,
        matcher,
        variations_without_attributes_duplicated
    ):
        skus_published = [
            v['sku']
            for v in variations_without_attributes_duplicated
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

    def test_without_attributes_chester_strategy_published_all_skus(
        self,
        matcher,
        variations_with_attributes_duplicated
    ):
        skus_published = [
            v['sku']
            for v in variations_with_attributes_duplicated
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

    def test_different_brands_and_attributes_omnilogic_return_one_per_group(
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
