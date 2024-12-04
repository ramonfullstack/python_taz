import pytest

from taz.core.matching.common.enriched_products import EnrichedProductSamples
from taz.core.matching.common.samples import ProductSamples
from taz.core.merge.scopes.metabooks import MetabooksScope


class TestMetabooksScope:

    @pytest.fixture
    def product(self):
        return ProductSamples.lt2shop_sku_0000998113()

    @pytest.fixture
    def enriched_product(self):
        return EnrichedProductSamples.lt2shop_sku_0000998113()

    @pytest.fixture
    def metabooks(self, product, enriched_product):
        return MetabooksScope(product, enriched_product)

    def test_normalize_title(self, metabooks, enriched_product):
        metabooks._normalize_title()

        expected_title = 'Livro - {}'.format(enriched_product['title'])

        assert metabooks.raw_product['title'] == expected_title
        assert metabooks.raw_product['offer_title'] == expected_title

    @pytest.mark.parametrize('publishers, expected', [
        (
            ['Bookman'],
            'Bookman',
        ),
        (
            ['Bookman', 'Murcho'],
            'Bookman, Murcho',
        ),
    ])
    def test_normalize_brand(
        self,
        metabooks,
        enriched_product,
        publishers,
        expected
    ):
        enriched_product['metadata']['Editora'] = publishers
        metabooks._normalize_brand()

        assert ', '.join(metabooks.raw_product['brand']) == expected
