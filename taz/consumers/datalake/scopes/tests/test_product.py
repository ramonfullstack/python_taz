from typing import Dict
from unittest.mock import patch

import pytest

from taz.consumers.datalake.scopes.product import Scope as ProductScope
from taz.core.matching.common.samples import ProductSamples


class TestProductScope:

    @pytest.fixture
    def product_from_storage(self):
        return ProductSamples.magazineluiza_sku_193389600_from_storage()

    def test_when_receive_event_then_should_process_with_success(
        self,
        patch_raw_products_storage_get_bucket_data: patch,
        product_from_storage: Dict
    ):
        with patch_raw_products_storage_get_bucket_data as mock_bucket:
            mock_bucket.return_value = product_from_storage
            product = ProductScope(
                sku=product_from_storage['sku'],
                seller_id=product_from_storage['seller_id']
            ).get_data()

            product.update({'scope_name': 'product_original'})
            assert product_from_storage == product
