import pytest

from taz.consumers.rebuild.scopes.complete_products import (
    RebuildCompleteProductBySeller,
    RebuildCompleteProductBySku
)
from taz.core.matching.common.samples import ProductSamples


class TestRebuildCompleteProductBySeller:

    @pytest.fixture
    def rebuild(self):
        return RebuildCompleteProductBySeller()

    @pytest.fixture
    def product(self):
        return ProductSamples.magazineluiza_sku_193389600()

    def test_rebuild_returns_not_found(self, rebuild, patch_publish_manager):
        data = {'seller_id': 'magazineluiza'}

        with patch_publish_manager as mock_pubsub:
            rebuild.rebuild('update', data)

        assert mock_pubsub.call_count == 0

    def test_rebuild_success(
        self,
        rebuild,
        patch_publish_manager,
        product,
        mongo_database
    ):
        mongo_database.raw_products.save(product)

        data = {'seller_id': product['seller_id']}

        with patch_publish_manager as mock_pubsub:
            ret = rebuild.rebuild('update', data)

        assert mock_pubsub.call_count == 1
        assert ret is True


class TestRebuildCompleteProductBySku:

    @pytest.fixture
    def rebuild(self):
        return RebuildCompleteProductBySku()

    def test_rebuild_success(self, rebuild, patch_publish_manager):
        data = [
            {'sku': '1234', 'seller_id': 'magazineluiza'},
            {'sku': '4321', 'seller_id': 'murcho'}
        ]

        with patch_publish_manager as mock_pubsub:
            ret = rebuild.rebuild('update', data)

        assert mock_pubsub.call_count == 2
        assert ret is True
