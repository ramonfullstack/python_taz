from unittest.mock import patch

import pytest

from taz.core.matching.common.enriched_products import EnrichedProductSamples
from taz.core.matching.common.samples import ProductSamples
from taz.core.merge.category import CategoryMerger


class TestCategoryMerge:

    @pytest.fixture
    def merger(self):
        return CategoryMerger()

    @pytest.fixture
    def mock_mount_data(self):
        return patch.object(CategoryMerger, '_mount_data')

    def test_when_receive_enriched_product_empty_then_return_default_categories( # noqa
        self,
        merger,
        mongo_database
    ):
        product = ProductSamples.magazineluiza_sku_217130800()
        categories = product['categories']

        result, _, _ = merger.merge(
            product['sku'],
            product['seller_id'],
            categories,
            None
        )

        assert result == categories

    @pytest.mark.parametrize('enriched_payload', [
        EnrichedProductSamples.shoploko_sku_74471(),
        EnrichedProductSamples.lt2shop_sku_0000998113(),
        EnrichedProductSamples.magazineluiza_hector_230382400()
    ])
    def test_when_receive_enriched_product_payload_then_should_format_data_and_return_categories( # noqa
        self,
        merger,
        mongo_database,
        enriched_payload
    ):
        product = ProductSamples.magazineluiza_sku_217130800()
        product['categories'][0]['id'] = 'RC'
        product['categories'][0]['subcategories'] = ['RCNM']

        result, _, _ = merger.merge(
            sku=product['sku'],
            seller_id=product['seller_id'],
            categories=product['categories'],
            enriched_products=[enriched_payload]
        )

        assert result[0]['id'] != product['categories'][0]['id']
        assert result[0]['subcategories'] != product['categories'][0]['subcategories'] # noqa

    def test_duplicated_categories(
        self,
        merger,
        mongo_database
    ):
        product = ProductSamples.magazineluiza_sku_217130800()
        sku = product['sku']
        seller_id = product['seller_id']

        enriched_product = EnrichedProductSamples.shoploko_sku_74471()
        enriched_product.update({'sku': sku, 'seller_id': seller_id})

        mongo_database.enriched_products.save(enriched_product)

        assert len(product['categories'][0]['subcategories']) == 2

        categories = [{
            'id': 'EP',
            'subcategories': [
                {'id': 'ELCO', 'name': 'Test'},
                {'id': 'ELCO', 'name': 'Fulano'},
                {'id': 'ELCO'},
                {'id': 'ELCO'},
                {'id': 'ELCO'},
                {'id': 'ELCO'},
                {'id': 'ELCO'},
            ]
        }]

        payload, _, _ = merger.merge(
            sku,
            seller_id,
            categories,
            [enriched_product]
        )

        assert len(payload[0]['subcategories']) == 1
        assert payload[0]['subcategories'] == [{'id': 'FREL'}]
