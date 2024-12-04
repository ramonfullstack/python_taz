from unittest.mock import patch

import pytest

from taz.consumers.core.maas_product import MaasProductHTTPClient
from taz.consumers.rebuild.scopes.maas_product_reprocess import (
    MaasProductReprocess
)


class TestMaasProductReprocess:

    @pytest.fixture
    def scope(self):
        return MaasProductReprocess()

    @pytest.fixture
    def patch_post_maas_product_reprocess(self):
        return patch.object(MaasProductHTTPClient, 'reprocess')

    def test_when_reprocess_then_return_success(
        self,
        scope: MaasProductReprocess,
        mock_maas_product_reprocess_payload: dict,
        patch_post_maas_product_reprocess: patch,
        caplog: patch
    ):
        with patch_post_maas_product_reprocess as mock_patch_maas_product_reprocess:  # noqa
            mock_patch_maas_product_reprocess.return_value = True
            scope.rebuild('update', mock_maas_product_reprocess_payload)

        assert mock_patch_maas_product_reprocess.called
        assert 'success:True' in caplog.text

    def test_when_reprocess_then_return_failed(
        self,
        scope: MaasProductReprocess,
        mock_maas_product_reprocess_payload: dict,
        patch_post_maas_product_reprocess: patch,
        caplog: patch
    ):
        with patch_post_maas_product_reprocess as mock_patch_maas_product_reprocess:  # noqa
            mock_patch_maas_product_reprocess.return_value = False
            scope.rebuild('update', mock_maas_product_reprocess_payload)

        assert mock_patch_maas_product_reprocess.called
        assert 'success:False' in caplog.text

    @pytest.mark.parametrize('field', [('seller_id'), ('sku'), ('source')])
    def test_when_reprocess_with_invalid_payload_then_return_failed(
        self,
        scope: MaasProductReprocess,
        mock_maas_product_reprocess_payload: dict,
        patch_post_maas_product_reprocess: patch,
        caplog: patch,
        field: str
    ):
        mock_maas_product_reprocess_payload.pop(field, None)
        with patch_post_maas_product_reprocess as mock_patch_maas_product_reprocess:  # noqa
            mock_patch_maas_product_reprocess.return_value = False
            scope.rebuild('update', mock_maas_product_reprocess_payload)

        assert not mock_patch_maas_product_reprocess.called
        assert 'Invalid data' in caplog.text
