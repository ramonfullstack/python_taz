import pytest

from taz import constants
from taz.core.matching.common.samples import ProductSamples
from taz.core.merge.scopes.api_luiza_express_delivery import (
    ApiLuizaExpressDelivery
)


class TestApiLuizaExpressDeliveryScope:

    @pytest.fixture
    def product(self):
        return ProductSamples.magazineluiza_sku_193389100()

    @pytest.fixture
    def scope(self, product):
        return ApiLuizaExpressDelivery(product)

    def test_scope_returns_delivery_plus_1(
        self,
        scope,
        product,
        mongo_database
    ):
        mongo_database.enriched_products.save({
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'delivery_days': 1,
            'source': constants.SOURCE_API_LUIZA_EXPRESS_DELIVERY
        })

        scope.apply()

        assert scope.raw_product['delivery_plus_1'] is True
        assert scope.raw_product['delivery_plus_2'] is False

    def test_scope_returns_delivery_plus_2(
        self,
        scope,
        product,
        mongo_database
    ):
        mongo_database.enriched_products.save({
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'delivery_days': 2,
            'source': constants.SOURCE_API_LUIZA_EXPRESS_DELIVERY
        })

        scope.apply()

        assert scope.raw_product['delivery_plus_2'] is False
        assert scope.raw_product['delivery_plus_1'] is True

    def test_scope_returns_nothing(
        self,
        scope,
        product,
        mongo_database
    ):
        mongo_database.enriched_products.save({
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'delivery_days': 4,
            'source': constants.SOURCE_API_LUIZA_EXPRESS_DELIVERY
        })

        scope.apply()

        assert 'delivery_plus_2' not in scope.raw_product
        assert 'delivery_plus_1' not in scope.raw_product

    def test_scope_returns_not_found(self, scope, product, logger_stream):
        scope.apply()

        log = logger_stream.getvalue()
        assert 'Enriched product not found from' in log
