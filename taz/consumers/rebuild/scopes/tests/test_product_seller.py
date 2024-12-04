from unittest.mock import patch

import pytest

from taz.consumers.rebuild.scopes.seller import RebuildProductSeller


class TestRebuildProductSeller:

    @pytest.fixture
    def patch_kinesis(self):
        return patch('taz.pollers.core.brokers.stream.KinesisBroker')

    @pytest.fixture
    def rebuild_product(self, patch_kinesis, mock_kinesis):
        with patch_kinesis as mock:
            mock.return_value = mock_kinesis
            return RebuildProductSeller()

    def test_rebuild_products_by_seller_id(
        self,
        rebuild_product,
        patch_pubsub_client,
        populated_products,
    ):
        with patch_pubsub_client as mock_pubsub:
            ret = rebuild_product.rebuild(
                'update',
                {'seller_id': 'magazineluiza'}
            )

            assert mock_pubsub.call_count == 3
            assert ret is True

    def test_invalid_seller_in_data(
        self, rebuild_product, mock_kinesis, populated_products, logger_stream
    ):
        rebuild_product.rebuild('update', {'seller_id': ''})

        assert (
            "{'seller_id': ['Length must be between 1 and 50.']}" in
            logger_stream.getvalue()
        )

        assert not mock_kinesis.put_many.called
        assert not mock_kinesis.shutdown.called
