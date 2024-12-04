import pytest

from taz.core.matching.common.enriched_products import EnrichedProductSamples
from taz.core.matching.common.samples import ProductSamples
from taz.core.merge.scopes.datasheet import DatasheetScope


class TestDatasheetScope:

    @pytest.fixture
    def product(self):
        return ProductSamples.magazineluiza_sku_0233847()

    @pytest.fixture
    def enriched_product(self):
        return EnrichedProductSamples.magazineluiza_sku_0233847_datasheet()

    @pytest.fixture
    def scope(self, product, enriched_product):
        return DatasheetScope(product, enriched_product)

    @pytest.fixture
    def mock_expected_result_enrichment(self):
        return {
            'description': 'O que era inimaginável agora é real. Fritar comidas sem óleo.',  # noqa
            'attributes': [{'type': 'voltage', 'value': '220 volts'}]
        }

    def test_when_get_result_of_enrichment_then_return_attributes_and_description(  # noqa
        self,
        scope,
        mock_expected_result_enrichment
    ):
        assert scope.get_result() == mock_expected_result_enrichment

    def test_when_apply_enrichement_in_raw_products_then_updated_only_enabled_fields(  # noqa
        self,
        scope,
        product,
        mock_expected_result_enrichment
    ):
        scope.apply()

        product.update(mock_expected_result_enrichment)
        assert scope.raw_product == product
