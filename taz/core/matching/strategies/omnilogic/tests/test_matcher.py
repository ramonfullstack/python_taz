import pytest

from taz import constants
from taz.constants import MAGAZINE_LUIZA_SELLER_ID, OMNILOGIC_STRATEGY
from taz.core.matching.common.enriched_products import EnrichedProductSamples
from taz.core.matching.common.samples import ProductSamples
from taz.core.matching.strategies.omnilogic.assembler import ProductAssembler
from taz.core.matching.strategies.omnilogic.matcher import ProductMatcher
from taz.core.merge.scopes.helpers import normalize_attributes


class TestProductMatcherOmnilogic:

    @pytest.fixture
    def matcher(self):
        return ProductMatcher()

    @pytest.fixture
    def assembler(self):
        return ProductAssembler(OMNILOGIC_STRATEGY)

    @pytest.fixture
    def save_raw_and_enriched_products(self, mongo_database):
        enriched_products = [
            EnrichedProductSamples.maniavirtual_sku_9022086_01(),
            EnrichedProductSamples.maniavirtual_sku_9022085_01(),
            EnrichedProductSamples.casa_e_video_sku_8186(),
            EnrichedProductSamples.magazineluiza_sku_217148200(),
            EnrichedProductSamples.madeiramadeira_openapi_sku_302110(),
            EnrichedProductSamples.madeiramadeira_openapi_sku_302117(),
            EnrichedProductSamples.magazineluiza_sku_217148100(),
            EnrichedProductSamples.havan_sku_2078836(),
            EnrichedProductSamples.havan_sku_2078835(),
            EnrichedProductSamples.mundoautomacao_sku_320_257(),
            EnrichedProductSamples.mundoautomacao_sku_320_258()
        ]

        mongo_database.enriched_products.insert_many(enriched_products)

        products = [
            ProductSamples.maniavirtual_sku_9022086_01(),
            ProductSamples.maniavirtual_sku_9022085_01(),
            ProductSamples.casa_e_video_sku_8186(),
            ProductSamples.magazineluiza_sku_217148200(),
            ProductSamples.madeiramadeira_openapi_sku_302110(),
            ProductSamples.madeiramadeira_openapi_sku_302117(),
            ProductSamples.magazineluiza_sku_217148100(),
            ProductSamples.havan_sku_2078836(),
            ProductSamples.havan_sku_2078835(),
            ProductSamples.mundoautomacao_sku_320_257(),
            ProductSamples.mundoautomacao_sku_320_258()
        ]

        for product in products:
            if product['seller_id'] == MAGAZINE_LUIZA_SELLER_ID:
                product['disable_on_matching'] = True

        mongo_database.raw_products.insert_many(products)

        return products[0]

    def test_matcher_omnilogic_strategy(
        self,
        mongo_database,
        variations,
        enriched_products,
        matcher,
        patch_kinesis_put,
        patch_pubsub_client
    ):
        mongo_database.enriched_products.insert_many(enriched_products)

        enriched = {
            '{}.{}'.format(
                enriched_product['sku'],
                enriched_product['seller_id']
            ): enriched_product
            for enriched_product in enriched_products
        }

        for variation in variations:
            sku = variation['sku']
            seller_id = variation['seller_id']

            e = enriched.get(f'{sku}.{seller_id}', {})
            m = e.get('metadata')

            metadata = {
                attribute_name: m.get(attribute_name)
                for attribute_name in e['sku_metadata']
            }

            variation['matching_strategy'] = constants.OMNILOGIC_STRATEGY
            variation['attributes'] = normalize_attributes(metadata)
            variation['product_hash'] = e['product_hash']

        mongo_database.raw_products.insert_many(variations)

        response = matcher.match_variations(variations[0])
        assert len(response) == 2

    def test_assembler_omnilogic_strategy(
        self,
        mongo_database,
        variations,
        enriched_products,
        assembler,
        matcher
    ):
        for variation in variations:
            for enriched in enriched_products:
                if (
                    variation['sku'] == enriched['sku'] and
                    variation['seller_id'] == enriched['seller_id']
                ):
                    variation['matching_strategy'] = OMNILOGIC_STRATEGY
                    variation['product_hash'] = enriched['product_hash']

        mongo_database.raw_products.insert_many(variations)
        mongo_database.enriched_products.insert_many(enriched_products)

        match_variations = matcher.match_variations(variations[0])
        response = assembler.assemble(match_variations)

        assert response[0]
        assert response[1] == []

    def test_matcher_omnilogic_strategy_with_product_hash_is_null(
        self,
        mongo_database,
        matcher,
        caplog
    ):
        variation = ProductSamples.lojasmel_openapi_45035()
        mongo_database.raw_products.insert_one(variation)

        mongo_database.enriched_products.insert_many([
            EnrichedProductSamples.lojasmel_openapi_45035(),
            EnrichedProductSamples.gazinshop_4470()
        ])

        assert mongo_database.enriched_products.count_documents(
            {'product_hash': None}
        ) == 2

        response = matcher.match_variations(variation)
        assert len(response) == 1
        assert (
            'Product hash not found for sku:{sku} and '
            'seller_id:{seller_id} with source:magalu'.format(
                sku=variation['sku'],
                seller_id=variation['seller_id']
            )
        ) in caplog.text

    def test_assembler_omnilogic_strategy_with_product_hash_is_null(
        self,
        mongo_database,
        assembler,
        matcher,
        caplog
    ):
        variation = ProductSamples.lojasmel_openapi_45035()
        mongo_database.raw_products.insert_one(variation)

        mongo_database.enriched_products.insert_many([
            EnrichedProductSamples.lojasmel_openapi_45035(),
            EnrichedProductSamples.gazinshop_4470()
        ])

        assert mongo_database.enriched_products.count_documents(
            {'product_hash': None}
        ) == 2

        match_variations = matcher.match_variations(variation)
        assert len(match_variations) == 1
        assert (
            'Product hash not found for sku:{sku} and '
            'seller_id:{seller_id} with source:magalu'.format(
                sku=variation['sku'],
                seller_id=variation['seller_id']
            )
        ) in caplog.text

        assembled_product, _ = assembler.assemble(match_variations)
        assert len(assembled_product['variations']) == 1

    def test_gather_self_and_similar_variations(
        self,
        matcher,
        save_raw_and_enriched_products
    ):
        response = matcher._gather_self_and_similar_variations(
            save_raw_and_enriched_products
        )

        assert len(response) == 11

    def test_assembler_omnilogic_strategy_with_ml_inactive(
        self,
        mongo_database,
        assembler,
        matcher,
        save_raw_and_enriched_products
    ):
        match_variations = matcher.match_variations(
            save_raw_and_enriched_products
        )

        assembled_product, _ = assembler.assemble(match_variations)
        assemble_variations = assembled_product['variations']

        assert len(assemble_variations) == 2

    def test_assembler_omnilogic_strategy_books(
        self,
        mongo_database,
        assembler,
        matcher
    ):
        mongo_database.enriched_products.insert_many([
            EnrichedProductSamples.livrariaflorence2_sku_9788543105757(),
            EnrichedProductSamples.livrariasebocapricho_sku_23036521(),
            EnrichedProductSamples.magazineluiza_sku_221841200(),
            EnrichedProductSamples.livrariaflorence2_sku_9788543105758(),
            EnrichedProductSamples.saraiva_sku_10260263()
        ])

        products = [
            ProductSamples.livrariaflorence2_sku_9788543105757(),
            ProductSamples.livrariasebocapricho_sku_23036521(),
            ProductSamples.magazineluiza_sku_221841200(),
            ProductSamples.livrariaflorence2_sku_9788543105758(),
            ProductSamples.saraiva_sku_10260263()
        ]

        mongo_database.raw_products.insert_many(products)

        match_variations = matcher.match_variations(products[0])
        assembled_product, _ = assembler.assemble(match_variations)
        assemble_variations = assembled_product['variations']

        assert len(assemble_variations) == 1

    def test_assembler_omnilogic_strategy_books_with_attributes(
        self,
        mongo_database,
        assembler,
        matcher
    ):
        mongo_database.enriched_products.insert_many([
            EnrichedProductSamples.cliquebooks_sku_543242_1(),
            EnrichedProductSamples.magazineluiza_sku_222786900(),
            EnrichedProductSamples.book7_sku_9788506082645()
        ])

        products = [
            ProductSamples.book7_sku_9788506082645(),
            ProductSamples.cliquebooks_sku_543242_1(),
            ProductSamples.magazineluiza_sku_222786900()
        ]

        mongo_database.raw_products.insert_many(products)

        match_variations = matcher.match_variations(products[0])
        assembled_product, _ = assembler.assemble(match_variations)
        assemble_variations = assembled_product['variations']

        assert len(assemble_variations) == 1

    def test_duplicated_attributes_omnilogic_remove_9482200926(
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

    def test_duplicated_attributes_omnilogic_published_all_skus(
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

    def test_without_attributes_omnilogic_published_all_skus(
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
