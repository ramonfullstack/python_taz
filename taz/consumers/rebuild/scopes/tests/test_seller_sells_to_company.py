import pytest
from simple_settings.utils import settings_stub

from taz.consumers.rebuild.scopes.seller_sells_to_company import (
    RebuildSellerSellsToCompany
)
from taz.core.matching.common.samples import ProductSamples


class TestRebuildSellerSellsToCompany:

    @pytest.fixture
    def rebuild(self):
        return RebuildSellerSellsToCompany()

    @pytest.fixture
    def products(self):
        products = []

        for index in range(10):
            product = dict(ProductSamples.madeiramadeira_openapi_sku_302110())
            product['sku'] = index
            product['sells_to_company'] = True
            products.append(product)

        return products

    @pytest.fixture
    def seller_info(self, products):
        return {
            'id': products[0]['seller_id'],
            'sells_to_company': False
        }

    @pytest.fixture
    def save_products(self, mongo_database, products):
        mongo_database.raw_products.insert_many(products)

    @settings_stub(LIMIT_REBUILD_SELLER_PRODUCTS=5)
    def test_should_update_products_when_sells_to_company_has_changed_respecting_limit(  # noqa
        self,
        rebuild,
        mongo_database,
        save_products,
        products,
        seller_info,
        patch_publish_manager,
        logger_stream
    ):
        products_sorted = sorted(products, key=lambda x: x['sku'])

        for product in products:
            assert product['sells_to_company']

        with patch_publish_manager as mock_pubsub:
            rebuild.rebuild('update', seller_info)

        result = mongo_database.raw_products.find(
            {'seller_id': products[0]['seller_id'], 'sells_to_company': False},
            {'_id': 0, 'sku': 1}
        ).sort('sku', 1)

        products = list(result)

        log = logger_stream.getvalue()

        assert len(products) == 5

        for index in range(5):
            assert products[index]['sku'] == products_sorted[index]['sku']

        assert mock_pubsub.call_count == 6
        assert (
            'Starting sells_to_company rebuild for '
            'seller_id:madeiramadeira-openapi'
        ) in log
