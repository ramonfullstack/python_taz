import json
from unittest.mock import patch

import pytest

from taz.consumers.rebuild.consumer import RebuildProcessor
from taz.consumers.rebuild.scopes.catalog_notification import (
    RebuildCatalogNotification
)
from taz.consumers.rebuild.scopes.classify_product import (
    RebuildClassifyProduct
)
from taz.consumers.rebuild.scopes.complete_products import (
    RebuildCompleteProductBySeller,
    RebuildCompleteProductBySku
)
from taz.consumers.rebuild.scopes.marvin_seller import RebuildMarvinSeller
from taz.consumers.rebuild.scopes.marvin_seller_paginator import (
    RebuildMarvinSellerPaginator
)
from taz.consumers.rebuild.scopes.matching_product import (
    RebuildMatchingProduct
)
from taz.consumers.rebuild.scopes.product_score import (
    RebuildProductScoreBySeller,
    RebuildProductScoreBySku
)
from taz.consumers.rebuild.scopes.seller import RebuildProductSeller


class FakeMessage:
    _id = 1

    def __init__(self, data):
        self.data = json.dumps(data)
        self.message_id = str(FakeMessage._id)
        FakeMessage._id += 1


class TestRebuildConsumer:

    @pytest.fixture
    def consumer(self):
        return RebuildProcessor('rebuild')

    @pytest.fixture
    def patch_rebuild_seller(self):
        return patch.object(RebuildProductSeller, 'rebuild')

    @pytest.fixture
    def patch_rebuild_marvin_seller(self):
        return patch.object(RebuildMarvinSeller, 'rebuild')

    @pytest.fixture
    def patch_rebuild_catalog_notification(self):
        return patch.object(RebuildCatalogNotification, 'rebuild')

    @pytest.fixture
    def patch_rebuild_complete_product_seller(self):
        return patch.object(RebuildCompleteProductBySeller, 'rebuild')

    @pytest.fixture
    def patch_rebuild_complete_product_sku(self):
        return patch.object(RebuildCompleteProductBySku, 'rebuild')

    @pytest.fixture
    def patch_rebuild_score_product_by_seller(self):
        return patch.object(RebuildProductScoreBySeller, 'rebuild')

    @pytest.fixture
    def patch_rebuild_score_product_by_sku(self):
        return patch.object(RebuildProductScoreBySku, 'rebuild')

    @pytest.fixture
    def patch_rebuild_matching_by_sku(self):
        return patch.object(RebuildMatchingProduct, 'rebuild')

    @pytest.fixture
    def patch_rebuild_classify_by_sku(self):
        return patch.object(RebuildClassifyProduct, 'rebuild')

    @pytest.fixture
    def patch_rebuild_marvin_seller_panigator(self):
        return patch.object(RebuildMarvinSellerPaginator, 'rebuild')

    def test_rebuild_seller(self, consumer, patch_rebuild_seller):
        with patch_rebuild_seller as mock_rebuild:
            consumer.process_message(
                FakeMessage(data={
                    'scope': 'seller',
                    'action': 'update',
                    'data': {
                        'seller_id': 'magazineluiza'
                    }
                })
            )

        assert mock_rebuild.called

    def test_rebuild_marvin_seller(
        self, consumer, patch_rebuild_marvin_seller
    ):
        with patch_rebuild_marvin_seller as mock_rebuild:
            consumer.process_message(
                FakeMessage(
                    data={
                        'scope': 'marvin_seller',
                        'action': 'update',
                        'data': {
                            'seller_id': 'magazineluiza'
                        }
                    }
                )
            )

        assert mock_rebuild.called

    def test_rebuild_marvin_seller_invalid_status(
        self, consumer, patch_rebuild_marvin_seller
    ):
        with patch_rebuild_marvin_seller as mock_rebuild:
            msg = FakeMessage(
                data={
                    'scope': 'marvin_seller',
                    'action': 'invalid_status',
                    'data': {
                        'seller_id': 'magazineluiza'
                    }
                }
            )
            consumer.process_message(msg)

        assert mock_rebuild.called

    def test_rebuild_marvin_seller_paginator(
        self, consumer, patch_rebuild_marvin_seller_panigator
    ):
        with patch_rebuild_marvin_seller_panigator as mock_rebuild:
            msg = FakeMessage(
                data={
                    'scope': 'rebuild_marvin_seller_paginator',
                    'action': 'update',
                    'data': {
                        'seller_id': 'magazineluiza'
                    }
                }
            )
            consumer.process_message(msg)

        assert mock_rebuild.called

    def test_rebuild_catalog_notification(
        self,
        consumer,
        patch_rebuild_catalog_notification
    ):
        with patch_rebuild_catalog_notification as mock_rebuild:
            msg = FakeMessage(
                data={
                    'scope': 'catalog_notification',
                    'action': 'update',
                    'data': {
                        'seller_id': 'magazineluiza'
                    }
                }
            )
            consumer.process_message(msg)

        assert mock_rebuild.called

    def test_rebuild_complete_product_seller(
        self,
        consumer,
        patch_rebuild_complete_product_seller
    ):
        with patch_rebuild_complete_product_seller as mock_rebuild:
            msg = FakeMessage(
                data={
                    'scope': 'complete_products_by_seller',
                    'action': 'update',
                    'data': {
                        'seller_id': 'magazineluiza'
                    }
                }
            )
            consumer.process_message(msg)

        assert mock_rebuild.called

    def test_rebuild_complete_product_sku(
        self,
        consumer,
        patch_rebuild_complete_product_sku
    ):
        with patch_rebuild_complete_product_sku as mock_rebuild:
            msg = FakeMessage(
                data={
                    'scope': 'complete_products_by_sku',
                    'action': 'update',
                    'data': [
                        {'sku': '1234', 'seller_id': 'magazineluiza'},
                        {'sku': '4321', 'seller_id': 'murcho'}
                    ]
                }
            )
            consumer.process_message(msg)

        assert mock_rebuild.called

    def test_rebuild_score_product_seller(
        self,
        consumer,
        patch_rebuild_score_product_by_seller
    ):
        with patch_rebuild_score_product_by_seller as mock_rebuild:
            msg = FakeMessage(
                data={
                    'scope': 'product_score_by_seller',
                    'action': 'update',
                    'data': {
                        'seller_id': 'magazineluiza'
                    }
                }
            )
            consumer.process_message(msg)

        assert mock_rebuild.called

    def test_rebuild_score_product_sku(
        self,
        consumer,
        patch_rebuild_score_product_by_sku
    ):
        with patch_rebuild_score_product_by_sku as mock_rebuild:
            msg = FakeMessage(
                data={
                    'scope': 'product_score_by_sku',
                    'action': 'update',
                    'data': {
                        'seller_id': 'magazineluiza',
                        'sku': '012345678'
                    }
                }
            )
            consumer.process_message(msg)

        assert mock_rebuild.called

    def test_rebuild_matching_by_sku(
        self,
        consumer,
        patch_rebuild_matching_by_sku
    ):
        with patch_rebuild_matching_by_sku as mock_rebuild:
            msg = FakeMessage(
                data={
                    'scope': 'matching_by_sku',
                    'action': 'update',
                    'data': {
                        'seller_id': 'magazineluiza',
                        'sku': '012345678',
                        'navigation_id': '012345678'
                    }
                }
            )
            consumer.process_message(msg)

        assert mock_rebuild.called

    def test_rebuild_classify_by_sku(
        self,
        consumer,
        patch_rebuild_classify_by_sku
    ):
        with patch_rebuild_classify_by_sku as mock_rebuild:
            msg = FakeMessage(
                data={
                    'scope': 'classify_by_sku',
                    'action': 'update',
                    'data': {
                        'seller_id': 'magazineluiza',
                        'sku': '012345678',
                        'navigation_id': '012345678'
                    }
                }
            )
            consumer.process_message(msg)

        assert mock_rebuild.called
