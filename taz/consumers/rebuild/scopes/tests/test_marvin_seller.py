import pytest
from simple_settings import settings
from simple_settings.utils import settings_stub

from taz.constants import MAGAZINE_LUIZA_SELLER_ID, UPDATE_ACTION
from taz.consumers.rebuild.scopes.marvin_seller import RebuildMarvinSeller
from taz.core.matching.common.samples import ProductSamples


class TestRebuildMarvinSeller:

    @pytest.fixture
    def rebuild(self):
        return RebuildMarvinSeller()

    @pytest.fixture
    def product(self):
        return ProductSamples.magazineluiza_sku_193389600()

    @pytest.fixture
    def products_pagination(self, mongo_database):
        return [
            ProductSamples.magazineluiza_sku_193389600(),
            ProductSamples.magazineluiza_sku_010554100(),
            ProductSamples.magazineluiza_sku_010554000(),
            ProductSamples.magazineluiza_sku_011704201(),
            ProductSamples.magazineluiza_sku_124383300()
        ]

    @pytest.fixture
    def save_products_pagination(
        self,
        mongo_database,
        products_pagination
    ):
        mongo_database.raw_products.insert_many(products_pagination)

    @pytest.fixture
    def mock_marvin_seller_topic(self):
        return 'projects/{}/topics/{}'.format(
            settings.MARVIN_NOTIFICATION['project_id'],
            settings.MARVIN_NOTIFICATION['topic_name']
        )

    def test_rebuild_empty_data(self, rebuild, patch_publish_manager):
        data = {}

        with patch_publish_manager as mock_pubsub:
            rebuild.rebuild(UPDATE_ACTION, data)

        assert mock_pubsub.call_count == 0

    def test_rebuild_returns_not_found(self, rebuild, patch_publish_manager):
        data = {'seller_id': MAGAZINE_LUIZA_SELLER_ID}

        with patch_publish_manager as mock_pubsub:
            rebuild.rebuild(UPDATE_ACTION, data)

        assert mock_pubsub.call_count == 0

    @settings_stub(LIMIT_MARVIN_SELLER_REBUILD=3)
    def test_rebuild_marvin_seller_success(
        self,
        rebuild,
        patch_pubsub_client,
        product,
        products_pagination,
        save_products_pagination,
        logger_stream,
        mock_marvin_seller_topic
    ):
        products_sorted = sorted(products_pagination, key=lambda x: x['sku'])

        data = {
            'seller_id': product['seller_id'],
            'min_sku': products_sorted[0]['sku'],
            'max_sku': products_sorted[-1]['sku']
        }

        with patch_pubsub_client as mock_pubsub:
            ret = rebuild.rebuild(UPDATE_ACTION, data)

        assert ret
        assert mock_pubsub.call_count == 5
        assert (
            'Starting marvin seller rebuild with action' in
            logger_stream.getvalue()
        )

    def test_rebuild_invalid_data(
        self,
        rebuild,
        patch_publish_manager,
        product,
        mongo_database,
        logger_stream
    ):
        mongo_database.raw_products.insert_one(product)
        data = 'invalid_data'

        with patch_publish_manager as mock_pubsub:
            rebuild.rebuild('update', data)

        assert mock_pubsub.call_count == 0

    def test_rebuild_invalid_action(
        self,
        rebuild,
        patch_publish_manager,
        product,
        mongo_database
    ):
        mongo_database.raw_products.insert_one(product)
        data = {'seller_id': product['seller_id']}

        with patch_publish_manager as mock_pubsub:
            rebuild.rebuild('invalid_action', data)

        assert mock_pubsub.call_count == 0
