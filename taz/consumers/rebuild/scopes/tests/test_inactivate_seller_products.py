from datetime import datetime

import pytest
from simple_settings.utils import settings_stub

from taz import constants
from taz.consumers.rebuild.scopes.inactivate_seller_products import (
    RebuildInactivateSellerProducts
)
from taz.core.matching.common.samples import ProductSamples


class TestRebuildInactivateSellerProducts:

    @pytest.fixture
    def rebuild(self):
        return RebuildInactivateSellerProducts()

    @pytest.fixture
    def products(self):
        products = []

        for index in range(10):
            product = dict(ProductSamples.madeiramadeira_openapi_sku_302110())
            product['sku'] = index
            products.append(product)

        return products

    @pytest.fixture
    def save_products(self, mongo_database, products):
        mongo_database.raw_products.insert_many(products)

    @settings_stub(LIMIT_REBUILD_SELLER_PRODUCTS=5)
    def test_should_inactivate_seller_products_with_success(
        self,
        rebuild,
        mongo_database,
        save_products,
        products,
        patch_patolino_product_post,
        patch_publish_manager
    ):
        products_sorted = sorted(products, key=lambda x: x['sku'])

        for product in products:
            assert not product['disable_on_matching']

        data = {
            'seller_id': products[0]['seller_id']
        }

        with patch_patolino_product_post as mock_patolino:
            with patch_publish_manager as mock_pubsub:
                rebuild.rebuild('update', data)

        result = mongo_database.raw_products.find(
            {
                'seller_id': products[0]['seller_id'],
                'disable_on_matching': True,
                'md5': ''
            },
            {'sku': 1, 'md5': 1}
        ).sort('sku', 1)

        products = list(result)

        assert len(products) == 5

        for index in range(5):
            assert products[index]['sku'] == products_sorted[index]['sku']

        assert not mock_patolino.call_count == 5
        assert mock_pubsub.call_count == 6

    @settings_stub(LIMIT_REBUILD_SELLER_PRODUCTS=2)
    def test_inactivate_seller_with_offset_should_process_only_remaining_products( # noqa
            self,
            rebuild,
            mongo_database,
            save_products,
            products,
            patch_pubsub_client,
            patch_patolino_product_post,
            patch_publish_manager
    ):
        products_sorted = sorted(products, key=lambda x: x['sku'])

        for product in products:
            assert not product['disable_on_matching']

        data = {
            'seller_id': products[0]['seller_id'],
            'sku': products_sorted[6]['sku']
        }

        with patch_patolino_product_post as mock_patolino:
            with patch_publish_manager as mock_pubsub:
                rebuild.rebuild('update', data)

        result = mongo_database.raw_products.find(
            {
                'seller_id': products[0]['seller_id'],
                'disable_on_matching': True,
                'md5': ''
            },
            {'sku': 1, 'md5': 1}
        ).sort('sku', 1)

        products = list(result)

        assert len(products) == 2
        assert products[0]['sku'] == products_sorted[7]['sku']
        assert products[1]['sku'] == products_sorted[8]['sku']
        assert not mock_patolino.call_count == 2
        assert mock_pubsub.call_count == 3

    @settings_stub(LIMIT_REBUILD_SELLER_PRODUCTS=2)
    def test_inactivate_seller_finish_pagination_process(
            self,
            rebuild,
            products,
            patch_pubsub_client,
            patch_patolino_product_post,
            patch_sqs_manager_put,
            logger_stream
    ):
        products_sorted = sorted(products, key=lambda x: x['sku'])
        seller_id = products[0]['seller_id']
        data = {
            'seller_id': seller_id,
            'sku': products_sorted[-1]['sku']
        }

        with patch_patolino_product_post as mock_patolino:
            with patch_sqs_manager_put as mock_sqs:
                with patch_pubsub_client as mock_pubsub:
                    rebuild.rebuild('update', data)

        assert 'Finish inactivate seller products rebuild for seller_id:{}'.format(seller_id) in logger_stream.getvalue()  # noqa
        assert not mock_patolino.called
        assert not mock_pubsub.called
        assert not mock_sqs.called

    @settings_stub(LIMIT_REBUILD_SELLER_PRODUCTS=2)
    def test_inactivate_seller_without_active_products(
            self,
            rebuild,
            products,
            patch_pubsub_client,
            patch_patolino_product_post,
            patch_sqs_manager_put,
            logger_stream
    ):
        data = {
            'seller_id': products[0]['seller_id'],
        }

        with patch_patolino_product_post as mock_patolino:
            with patch_sqs_manager_put as mock_sqs:
                with patch_pubsub_client as mock_pubsub:
                    rebuild.rebuild('update', data)

        assert 'Rebuild inactive products found no active products' in logger_stream.getvalue()  # noqa
        assert not mock_patolino.called
        assert not mock_pubsub.called
        assert not mock_sqs.called

    def test_should_abort_when_no_active_products_are_found(
        self,
        rebuild,
        mongo_database,
        save_products,
        caplog,
        patch_pubsub_client
    ):

        data = {'seller_id': 'foo'}

        with patch_pubsub_client as mock_pubsub:
            rebuild.rebuild('update', data)

        assert not mock_pubsub.called

        log = caplog.records[0].getMessage()
        assert log == (
            'Starting inactivate seller products rebuild with '
            'request:{\'seller_id\': \'foo\'}'
        )

    def test_should_abort_when_seller_is_in_unblockable_list(
        self,
        rebuild,
        mongo_database,
        save_products,
        caplog,
        patch_pubsub_client
    ):
        data = {'seller_id': constants.MAGAZINE_LUIZA_SELLER_ID}

        with patch_pubsub_client as mock_pubsub:
            rebuild.rebuild('update', data)

        assert not mock_pubsub.called

        log = caplog.records[1].getMessage()
        assert log == (
            'Rebuild inactive products cant inactive '
            'seller:magazineluiza products'
        )

    @settings_stub(LIMIT_REBUILD_SELLER_PRODUCTS=1)
    def test_should_inactivate_seller_products_notify_patolino(
        self,
        rebuild,
        mongo_database,
        save_products,
        products,
        patch_pubsub_client,
        patch_sqs_manager_put,
        patch_patolino_product_post,
        patch_datetime
    ):
        products_sorted = sorted(products, key=lambda x: x['sku'])
        for product in products:
            assert not product['disable_on_matching']

        data = {
            'seller_id': products[0]['seller_id'],
            'inactive_reason': 'Inactive Reason'
        }

        current_datetime = datetime(2022, 1, 24, 0, 0, 0)
        with patch_patolino_product_post as mock_patolino:
            with patch_pubsub_client:
                with patch_sqs_manager_put:
                    with patch_datetime as mock_datetime:
                        mock_datetime.utcnow.return_value = current_datetime
                        rebuild.rebuild('update', data)

        assert mock_patolino.called

        assert mock_patolino.call_args[0][0] == {
            'sku': products_sorted[0]['sku'],
            'seller_id': products_sorted[0]['seller_id'],
            'code': constants.MAAS_PRODUCT_INACTIVATION_SELLER_SUCCESS_CODE,
            'message': data['inactive_reason'],
            'payload': {
                'sku': products_sorted[0]['sku'],
                'seller_id': products_sorted[0]['seller_id'],
                'navigation_id': products_sorted[0]['navigation_id']
            },
            'action': 'update',
            'last_updated_at': '2022-01-24T00:00:00'
        }
