from unittest.mock import patch

import pytest

from taz import constants
from taz.consumers.core.notification_enrichment import NotificationEnrichment
from taz.consumers.rebuild.scopes.classify_product import (
    RebuildClassifyProduct
)
from taz.core.matching.common.samples import ProductSamples


class TestClassifyProduct:

    @pytest.fixture
    def product(self):
        return ProductSamples.magazineluiza_sku_193389600()

    @pytest.fixture
    def rebuild(self):
        return RebuildClassifyProduct()

    @pytest.fixture
    def patch_get_product_by_sku_and_seller_id(self):
        return patch.object(
            RebuildClassifyProduct,
            '_get_product_by_sku_and_seller_id'
        )

    @pytest.fixture
    def patch_notify_chester(self):
        return patch.object(NotificationEnrichment, 'notify')

    @pytest.fixture
    def mock_message_data(self, product):
        return {
            'navigation_id': product['navigation_id'],
            'seller_id': product['seller_id'],
            'sku': product['sku']
        }

    def test_when_product_found_then_send_message_with_successfully(
        self,
        rebuild,
        patch_get_product_by_sku_and_seller_id,
        product,
        mock_message_data,
        patch_notify_chester
    ):
        attributes = {
            'event_type': constants.EnrichmentEventType.CLASSIFY.value
        }
        with patch_notify_chester as mock_notify_chester:
            with patch_get_product_by_sku_and_seller_id as mock_get_product:
                mock_get_product.return_value = product

                assert rebuild.rebuild('update', mock_message_data)
                mock_notify_chester.assert_called_once_with(
                    product=product,
                    attributes=attributes
                )

    def test_when_product_not_found_then_not_send_message_with_successfully(
        self,
        rebuild,
        product,
        patch_get_product_by_sku_and_seller_id,
        mock_message_data,
        patch_notify_chester,
        caplog
    ):
        with patch_notify_chester as mock_notify_chester:
            with patch_get_product_by_sku_and_seller_id as mock_get_product:
                mock_get_product.return_value = None
                assert rebuild.rebuild('update', mock_message_data)
                assert not mock_notify_chester.called

                message = (
                    'Product with sku:{} seller_id:{} navigation_id:{} '
                    'not found in scope:{}'.format(
                        product['sku'],
                        product['seller_id'],
                        product['navigation_id'],
                        'classify_product'
                    )
                )

                assert message in caplog.text
