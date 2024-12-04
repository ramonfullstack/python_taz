import pytest

from taz.consumers.rebuild.scopes.catalog_notification import (
    RebuildCatalogNotification
)
from taz.core.matching.common.samples import ProductSamples


class TestRebuildCatalogNotification:

    @pytest.fixture
    def product(self):
        return ProductSamples.magazineluiza_sku_193389600()

    @pytest.fixture
    def rebuild(self):
        return RebuildCatalogNotification()

    def test_rebuild_complete_products_successfully(
        self,
        rebuild,
        patch_pubsub_client,
        mongo_database,
        product
    ):
        mongo_database.raw_products.insert_one(product)

        data = {'seller_id': product['seller_id']}

        with patch_pubsub_client as mock_pubsub:
            ret = rebuild.rebuild('update', data)

        assert mock_pubsub.call_count == 1
        assert ret is True
