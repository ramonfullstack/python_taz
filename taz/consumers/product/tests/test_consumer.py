import copy
from datetime import datetime
from typing import Dict
from unittest.mock import ANY, patch
from uuid import uuid4

import pytest
from simple_settings import settings
from simple_settings.utils import settings_stub

from taz import constants
from taz.constants import (
    AUTO_BUYBOX_STRATEGY,
    CREATE_ACTION,
    DELETE_ACTION,
    MAGAZINE_LUIZA_SELLER_DESCRIPTION,
    MAGAZINE_LUIZA_SELLER_ID,
    PRODUCT_ALREADY_DISABLED_CODE,
    PRODUCT_ALREADY_DISABLED_MESSAGE,
    PRODUCT_ERROR_CODE,
    PRODUCT_ERROR_MESSAGE,
    PRODUCT_ORIGIN,
    PRODUCT_SKIP_PROCESS,
    PRODUCT_SUCCESS_CODE,
    PRODUCT_SUCCESS_MESSAGE,
    PRODUCT_UNFINISHED_PROCESS_CODE,
    PRODUCT_UNFINISHED_PROCESS_MESSAGE,
    REBUILD_ORIGIN,
    SINGLE_SELLER_STRATEGY,
    UPDATE_ACTION
)
from taz.consumers.core.exceptions import NavigationIdNotFound
from taz.consumers.product.consumer import ProductRecordProcessor
from taz.consumers.product.helpers import ProductHelpers
from taz.core.matching.common.samples import ProductSamples
from taz.helpers.json import json_dumps, json_loads


class TestProductProcessor:

    @pytest.fixture
    def processor(self) -> ProductRecordProcessor:
        return ProductRecordProcessor('product')

    @pytest.fixture
    def patch_catalog_notification(self, processor) -> patch:
        return patch.object(processor, '__catalog_notification')

    @pytest.fixture
    def patch_update(self, processor) -> patch:
        return patch.object(processor, '_update')

    @pytest.fixture
    def patch_create(self, processor) -> patch:
        return patch.object(processor, '_create')

    @pytest.fixture
    def patch_delete(self, processor) -> patch:
        return patch.object(processor, '_delete')

    @pytest.fixture
    def patch_raw_products(self, processor) -> patch:
        return patch.object(processor, 'raw_products')

    @pytest.fixture
    def patch_save_original_product_bucket(self, processor) -> patch:
        return patch.object(processor, '_save_original_product_bucket')

    @pytest.fixture
    def patch_normalize_product_payload(self, processor) -> patch:
        return patch.object(processor, 'normalize_product_payload')

    @pytest.fixture
    def patch_format_payload_product(self) -> patch:
        return patch.object(ProductHelpers, 'format_payload_product')

    @pytest.fixture
    def mock_task_id(self) -> str:
        return '186e1006ae3541128b6055b99bab7ca1'

    @pytest.fixture
    def mock_product_hash(self) -> str:
        return '46d4a88f-9c38-4f80-a18e-8a7afd3e801e'

    @pytest.fixture
    def mock_patolino_notification_payload(self, product: Dict):
        return {
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'code': PRODUCT_SUCCESS_CODE,
            'message': PRODUCT_SUCCESS_MESSAGE,
            'payload': {
                'navigation_id': product['navigation_id'],
                'action': CREATE_ACTION
            },
            'action': UPDATE_ACTION,
            'last_updated_at': ANY
        }

    @pytest.fixture
    def mock_notification_payload(self, product: Dict):
        return {
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'navigation_id': product['navigation_id'],
            'tracking_id': None
        }

    def test_when_create_product_then_should_process_with_success(
        self,
        processor,
        mongo_database,
        seller_info,
        mock_task_id,
        patch_patolino_product_post,
        patch_bucket_upload_data,
        patch_notification,
        product,
        mock_patolino_notification_payload,
        mock_notification_payload,
        caplog
    ):
        seller_info['id'] = product['seller_id']
        mongo_database.sellers.insert_one(seller_info)

        with patch_bucket_upload_data as mock_bucket:
            with patch_patolino_product_post as mock_patolino:
                with patch_notification as mock_notification:
                    processor.create(product)

        product_save_db = list(mongo_database.raw_products.find(
            {'sku': product['sku'], 'seller_id': product['seller_id']},
            {'_id': 0, 'navigation_id': 1}
        ))

        assert len(product_save_db) == 1
        mock_bucket.assert_called_once()
        mock_patolino.assert_called_once_with(
            mock_patolino_notification_payload,
            {
                'seller_id': product['seller_id'],
                'code': PRODUCT_SUCCESS_CODE,
                'has_tracking': 'false'
            }
        )

        mock_notification.assert_called_once_with(
            data=mock_notification_payload,
            scope='product',
            action=CREATE_ACTION,
            origin=PRODUCT_ORIGIN
        )

        assert (
            'Successfully created item sku:{sku} seller_id:{seller_id} '
            'navigation_id:{navigation_id}'.format(
                sku=product['sku'],
                seller_id=product['seller_id'],
                navigation_id=product_save_db[0]['navigation_id']
            ) in caplog.text
        )

    def test_when_create_magazineluiza_product_then_navigation_id_and_sku_should_be_equal( # noqa
        self,
        processor,
        mongo_database,
        seller_info,
        mock_task_id,
        patch_patolino_product_post,
        patch_bucket_upload_data,
        patch_notification,
        product
    ):
        seller_info['id'] = product['seller_id']
        mongo_database.sellers.insert_one(seller_info)

        with patch_bucket_upload_data:
            with patch_patolino_product_post as mock_patolino:
                with patch_notification as mock_notification:
                    processor.create(product)

        saved_product = mongo_database.raw_products.find_one(
            {'sku': product['sku'], 'seller_id': product['seller_id']},
            {'_id': 0, 'navigation_id': 1}
        )

        mock_patolino.assert_called_once()
        mock_notification.assert_called_once()
        assert saved_product['navigation_id'] == product['sku']

    def test_when_update_product_then_should_process_with_success(
        self,
        processor,
        mongo_database,
        seller_info,
        mock_task_id,
        patch_patolino_product_post,
        patch_bucket_upload_data,
        patch_notification,
        product,
        mock_patolino_notification_payload,
        mock_notification_payload,
        caplog
    ):
        seller_info['id'] = product['seller_id']
        mongo_database.sellers.insert_one(seller_info)
        mongo_database.raw_products.insert_one(copy.copy(product))

        product['title'] = 'update title'

        with patch_bucket_upload_data as mock_bucket:
            with patch_patolino_product_post as mock_patolino:
                with patch_notification as mock_notification:
                    processor.update(product)

        product_save_db = list(mongo_database.raw_products.find(
            {'sku': product['sku'], 'seller_id': product['seller_id']},
            {'_id': 0, 'navigation_id': 1, 'title': 1}
        ))

        assert len(product_save_db) == 1
        assert product_save_db[0]['title'] == 'update title'
        mock_bucket.assert_called_once()

        mock_patolino_notification_payload['payload']['action'] = UPDATE_ACTION
        mock_patolino.assert_called_once_with(
            mock_patolino_notification_payload,
            {
                'seller_id': product['seller_id'],
                'code': PRODUCT_SUCCESS_CODE,
                'has_tracking': 'false'
            }
        )

        mock_notification.assert_called_once_with(
            data=mock_notification_payload,
            scope='product',
            action=UPDATE_ACTION,
            origin=PRODUCT_ORIGIN
        )

        assert (
            'Successfully updated item sku:{sku} seller:{seller_id} '
            'navigation_id:{navigation_id}'.format(
                sku=product['sku'],
                seller_id=product['seller_id'],
                navigation_id=product['navigation_id']
            ) in caplog.text
        )

    def test_when_update_product_with_rebuild_origin_then_should_only_notify_and_skip_save_process( # noqa
        self,
        processor,
        mongo_database,
        seller_info,
        mock_task_id,
        patch_patolino_product_post,
        patch_bucket_upload_data,
        patch_notification,
        product: Dict,
        mock_notification_payload: Dict
    ):
        seller_info['id'] = product['seller_id']
        mongo_database.sellers.insert_one(seller_info)
        mongo_database.raw_products.insert_one(copy.copy(product))

        payload = {
            'action': CREATE_ACTION,
            'origin': REBUILD_ORIGIN,
            **product
        }

        with patch_bucket_upload_data:
            with patch_patolino_product_post as mock_patolino:
                with patch_notification as mock_notification:
                    processor.update(payload)

        mock_patolino.assert_not_called()
        mock_notification.assert_called_once_with(
            data=mock_notification_payload,
            scope='product',
            action=UPDATE_ACTION,
            origin=PRODUCT_ORIGIN
        )

    def test_when_update_product_without_navigation_id_then_raise_exception(
        self,
        processor,
        mongo_database,
        seller_info,
        mock_task_id,
        patch_patolino_product_post,
        patch_bucket_upload_data,
        patch_notification,
        product,
        mock_patolino_notification_payload
    ):
        seller_info['id'] = product['seller_id']
        mongo_database.sellers.insert_one(seller_info)

        del product['navigation_id']
        product['disable_on_matching'] = False
        mongo_database.raw_products.insert_one(product)

        with patch_patolino_product_post as mock_patolino:
            with pytest.raises(NavigationIdNotFound):
                processor.update(product)

        mock_patolino_notification_payload['code'] = PRODUCT_ERROR_CODE
        mock_patolino_notification_payload['message'] = PRODUCT_ERROR_MESSAGE
        mock_patolino_notification_payload['payload'] = {
            'action': UPDATE_ACTION,
            'navigation_id': None
        }

        mock_patolino.assert_called_once_with(
            mock_patolino_notification_payload,
            {
                'seller_id': product['seller_id'],
                'code': PRODUCT_ERROR_CODE,
                'has_tracking': 'false'
            }
        )

    def test_when_update_product_then_should_save_log_how_many_documents_are_updated( # noqa
        self,
        processor,
        mongo_database,
        product,
        patch_patolino_product_post,
        caplog
    ):
        sku = product['sku']
        seller_id = product['seller_id']

        product_1 = copy.copy(product)

        product_2 = ProductSamples.matching_product_b()
        product_2['sku'] = sku
        product_2['seller_id'] = seller_id

        mongo_database.raw_products.insert_many([
            product_1,
            product_2
        ])

        with patch_patolino_product_post as mock_patolino:
            processor._save_raw_product(product, UPDATE_ACTION)

        mock_patolino.assert_called_once()
        assert (
            f'Updated 2 documents in raw_products '
            f'for sku:{sku} seller_id:{seller_id}'
        ) in caplog.text

    @pytest.mark.parametrize('strategy', [
        AUTO_BUYBOX_STRATEGY,
        SINGLE_SELLER_STRATEGY
    ])
    def test_when_update_product_then_should_keep_strategy(
        self,
        mongo_database,
        processor,
        strategy,
        patch_bucket_upload_data,
        patch_patolino_product_post,
        patch_notification,
        seller_info
    ):
        product = ProductSamples.seller_a_variation_with_parent()

        seller_info['id'] = product['seller_id']
        mongo_database.sellers.insert_one(seller_info)
        mongo_database.raw_products.insert_one(product)

        product['matching_strategy'] = strategy
        with patch_bucket_upload_data:
            with patch_patolino_product_post as mock_patolino:
                with patch_notification as mock_notification:
                    processor.update(product)

        mock_patolino.assert_called_once()
        mock_notification.assert_called_once()

        raw_product = mongo_database.raw_products.find_one(
            {'sku': product['sku'], 'seller_id': product['seller_id']},
            {'_id': 0, 'matching_strategy': 1}
        )

        assert raw_product['matching_strategy'] == strategy

    @pytest.mark.parametrize('strategy', [
        AUTO_BUYBOX_STRATEGY,
        SINGLE_SELLER_STRATEGY
    ])
    def test_when_update_product_then_keeps_strategy_and_updates_selections(
        self,
        mongo_database,
        processor,
        strategy,
        patch_patolino_product_post,
        patch_bucket_upload_data,
        patch_notification,
        seller_info
    ):
        selections = {'0': ['1234', '5678']}

        product = ProductSamples.seller_a_variation_with_parent()
        product.update({
            'seller_id': constants.MAGAZINE_LUIZA_SELLER_ID,
            'sku': '123456789',
            'selections': selections,
            'matching_strategy': strategy
        })

        mongo_database.raw_products.insert_one(product)

        with patch_bucket_upload_data:
            with patch_patolino_product_post as mock_patolino:
                with patch_notification as mock_notification:
                    processor.update(product)

        mock_patolino.assert_called_once()
        mock_notification.assert_called_once()

        raw_product = mongo_database.raw_products.find_one(
            {'sku': product['sku'], 'seller_id': product['seller_id']},
            {'_id': 0, 'matching_strategy': 1, 'selections': 1}
        )

        assert raw_product['selections'] == selections
        assert raw_product['matching_strategy'] == strategy

    def test_when_delete_product_then_should_process_with_success(
        self,
        processor,
        mongo_database,
        seller_info,
        mock_task_id,
        patch_patolino_product_post,
        patch_bucket_upload_data,
        patch_bucket_get_data,
        patch_notification,
        mock_patolino_notification_payload,
        mock_notification_payload,
        caplog
    ):
        product = ProductSamples.seller_a_variation_with_parent()
        sku = product['sku']
        seller_id = product['seller_id']

        seller_info['id'] = seller_id
        mongo_database.sellers.insert_one(seller_info)
        mongo_database.raw_products.insert_one(product)

        with patch_bucket_get_data as mock_bucket_get:
            mock_bucket_get.return_value = product
            with patch_bucket_upload_data as mock_bucket_upload:
                with patch_patolino_product_post as mock_patolino:
                    with patch_notification as mock_notification:
                        processor.delete({'sku': sku, 'seller_id': seller_id})

        store_product = mongo_database.raw_products.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0, 'disable_on_matching': 1}
        )

        assert store_product['disable_on_matching'] is True
        mock_bucket_upload.assert_called_once()

        mock_patolino_notification_payload.update({
            'sku': sku,
            'seller_id': seller_id,
            'payload': {
                'action': DELETE_ACTION,
                'navigation_id': product['navigation_id']
            }
        })
        mock_patolino.assert_called_once_with(
            mock_patolino_notification_payload,
            {
                'seller_id': product['seller_id'],
                'code': PRODUCT_SUCCESS_CODE,
                'has_tracking': 'false'
            }
        )

        mock_notification.assert_called_once_with(
            data={
                'sku': sku,
                'seller_id': seller_id,
                'navigation_id': product['navigation_id'],
                'tracking_id': None
            },
            scope='product',
            action=DELETE_ACTION,
            origin=PRODUCT_ORIGIN
        )

        assert (
            'Successfully disabled item sku:{sku} '
            'seller_id:{seller_id} from raw_products'.format(
                sku=sku,
                seller_id=seller_id
            )
        )

    def test_when_delete_product_and_not_found_then_should_notify_patolino(
        self,
        processor,
        mongo_database,
        seller_info,
        mock_task_id,
        patch_patolino_product_post,
        patch_notification,
        mock_patolino_notification_payload
    ):
        product = ProductSamples.seller_a_variation_with_parent()
        sku = product['sku']
        seller_id = product['seller_id']

        seller_info['id'] = product['seller_id']
        mongo_database.sellers.insert_one(seller_info)

        with patch_patolino_product_post as mock_patolino:
            with patch_notification as mock_notification:
                result = processor.delete({'sku': sku, 'seller_id': seller_id})

        assert not result
        mock_notification.assert_not_called()

        mock_patolino_notification_payload.update({
            'sku': sku,
            'seller_id': seller_id,
            'code': PRODUCT_UNFINISHED_PROCESS_CODE,
            'message': PRODUCT_UNFINISHED_PROCESS_MESSAGE.format(
                sku=sku,
                seller_id=seller_id,
                reason='Product not found.'
            ),
            'payload': {
                'navigation_id': None,
                'action': DELETE_ACTION
            }
        })
        mock_patolino.assert_called_once_with(
            mock_patolino_notification_payload,
            {
                'seller_id': product['seller_id'],
                'code': PRODUCT_UNFINISHED_PROCESS_CODE,
                'has_tracking': 'false'
            }
        )

    def test_when_delete_product_with_magazineluiza_seller_and_product_is_active_then_should_call_update_method( # noqa
        self,
        processor,
        mongo_database,
        seller_info,
        patch_patolino_product_post,
        patch_notification,
        patch_update,
        caplog,
        product
    ):
        seller_info['id'] = product['seller_id']
        mongo_database.sellers.insert_one(seller_info)
        mongo_database.raw_products.insert_one(product)

        with patch_patolino_product_post as mock_patolino:
            with patch_notification as mock_notification:
                with patch_update as mock_update_method:
                    result = processor.delete({
                        'sku': product['sku'],
                        'seller_id': product['seller_id'],
                        'active': True
                    })

        assert not result
        mock_update_method.assert_called_once()
        mock_patolino.assert_not_called()
        mock_notification.assert_not_called()

        assert (
            'Ignoring product delete from sku:{sku} '
            'seller_id:{seller_id} because it is active'.format(
                sku=product['sku'],
                seller_id=product['seller_id']
            )
        )

    def test_delete_when_product_magazineluiza_and_is_not_active_then_should_process_delete_with_success( # noqa
        self,
        processor,
        mongo_database,
        seller_info,
        product,
        patch_save_original_product_bucket,
        patch_patolino_product_post,
        patch_notification,
        mock_patolino_notification_payload
    ):
        product['active'] = False
        product['disable_on_matching'] = False
        mongo_database.raw_products.insert_one(product)

        with patch_save_original_product_bucket:
            with patch_patolino_product_post as mock_patolino:
                with patch_notification as mock_notification:
                    processor.delete(product)

        mock_patolino_notification_payload['payload']['action'] = DELETE_ACTION
        mock_patolino.assert_called_once_with(
            mock_patolino_notification_payload,
            {
                'seller_id': product['seller_id'],
                'code': PRODUCT_SUCCESS_CODE,
                'has_tracking': 'false'
            }
        )

        mock_notification.assert_called_once_with(
            data={
                'sku': product['sku'],
                'seller_id': product['seller_id'],
                'navigation_id': product['navigation_id'],
                'tracking_id': None
            },
            scope='product',
            action=DELETE_ACTION,
            origin=PRODUCT_ORIGIN
        )

        saved_product = mongo_database.raw_products.find_one(
            {
                'sku': product['sku'],
                'seller_id': product['seller_id']
            },
            {
                '_id': 0,
                'disable_on_matching': 1
            }
        )

        assert saved_product['disable_on_matching']

    def test_delete_when_product_already_disabled_then_should_notification_patolino_and_skip_process( # noqa
        self,
        processor,
        mongo_database,
        seller_info,
        patch_patolino_product_post,
        patch_notification,
        patch_save_original_product_bucket,
        product,
        mock_patolino_notification_payload,
        caplog
    ):
        product['disable_on_matching'] = True
        product['active'] = False
        mongo_database.raw_products.insert_one(product)

        with patch_save_original_product_bucket:
            with patch_patolino_product_post as mock_patolino:
                result = processor.delete(product)

        assert not result
        mock_patolino_notification_payload.update({
            'code': PRODUCT_ALREADY_DISABLED_CODE,
            'message': PRODUCT_ALREADY_DISABLED_MESSAGE,
            'payload': {
                'navigation_id': product['navigation_id'],
                'action': DELETE_ACTION
            }
        })

        mock_patolino.assert_called_once_with(
            mock_patolino_notification_payload,
            {
                'seller_id': product['seller_id'],
                'code': PRODUCT_ALREADY_DISABLED_CODE,
                'has_tracking': 'false'
            }
        )

        assert (
            'Product sku:{sku} seller_id:{seller_id} already disabled '
            'on catalog, send event notification to Patolino'.format(
                sku=product['sku'],
                seller_id=product['seller_id']
            ) in caplog.text
        )

    def test_delete_product_should_save_original_product_in_bucket_and_save_raw_product_data_in_mongo( # noqa
        self,
        processor,
        mongo_database,
        seller_info,
        patch_patolino_product_post,
        patch_notification,
        patch_bucket_get_data,
        patch_bucket_upload_data,
        product
    ):
        product['disable_on_matching'] = False
        product['active'] = False
        product_storage = ProductSamples.magazineluiza_sku_193389600_from_storage() # noqa
        mongo_database.raw_products.insert_one(product)

        with patch_bucket_get_data as mock_bucket_get:
            mock_bucket_get.return_value = product_storage
            with patch_bucket_upload_data as mock_bucket_upload:
                with patch_patolino_product_post as mock_patolino:
                    with patch_notification as mock_notification:
                        processor.delete(product)

        product_storage['disable_on_matching'] = True
        product_storage['tracking_id'] = product.get('tracking_id')

        mock_notification.assert_called_once()
        mock_patolino.assert_called_once()
        mock_bucket_upload.assert_called_once_with(
            sku=product['sku'],
            seller_id=product['seller_id'],
            payload=json_dumps(product_storage, ensure_ascii=False)
        )

        saved_product = mongo_database.raw_products.find_one(
            {
                'sku': product['sku'],
                'seller_id': product['seller_id']
            },
            {
                '_id': 0, 'disable_on_matching': 1
            }
        )

        assert saved_product['disable_on_matching']

    @pytest.mark.parametrize(
        'processor_method', [
            CREATE_ACTION,
            UPDATE_ACTION
        ]
    )
    def test_when_save_product_throw_exception_then_should_notify_error_and_raise_exception( # noqa
        self,
        processor,
        mongo_database,
        seller_info,
        patch_patolino_product_post,
        patch_bucket_upload_data,
        patch_notification,
        patch_raw_products,
        processor_method,
        product,
        mock_patolino_notification_payload
    ):
        seller_info['id'] = product['seller_id']
        mongo_database.sellers.insert_one(seller_info)
        raw_products_find = None

        if processor_method == UPDATE_ACTION:
            mongo_database.raw_products.insert_one(copy.copy(product))
            raw_products_find = product

        with patch_bucket_upload_data as mock_bucket:
            with patch_patolino_product_post as mock_patolino:
                with patch_notification as mock_notification:
                    with patch_raw_products as mock_raw_products:
                        mock_raw_products.find_one.return_value = (
                            raw_products_find
                        )
                        mock_raw_products.update_many.side_effect = Exception
                        with pytest.raises(Exception):
                            getattr(processor, processor_method)(product)

        mock_patolino_notification_payload['code'] = PRODUCT_ERROR_CODE
        mock_patolino_notification_payload['message'] = PRODUCT_ERROR_MESSAGE
        mock_patolino_notification_payload['payload']['action'] = (
            processor_method
        )
        mock_patolino.assert_called_once_with(
            mock_patolino_notification_payload,
            {
                'seller_id': product['seller_id'],
                'code': PRODUCT_ERROR_CODE,
                'has_tracking': 'false'
            }
        )
        mock_bucket.assert_called_once()
        mock_notification.assert_not_called()

    def test_when_seller_is_magazine_luiza_then_should_return_default_payload(
        self,
        processor,
        product
    ):

        result = processor.get_seller_info(product, CREATE_ACTION)

        assert result == {
            'is_active': True,
            'sells_to_company': True,
            'name': MAGAZINE_LUIZA_SELLER_DESCRIPTION
        }

    def test_when_seller_is_different_magazine_luiza_then_should_get_data_from_seller_collection( # noqa
        self,
        processor,
        product,
        seller_info,
        mongo_database
    ):
        product['seller_id'] = 'luizalabs'
        seller_info['id'] = product['seller_id']
        mongo_database.sellers.insert_one(seller_info)

        result = processor.get_seller_info(product, CREATE_ACTION)
        assert result == {
            'is_active': seller_info['is_active'],
            'name': seller_info['name'],
            'sells_to_company': seller_info['sells_to_company']
        }

    def test_when_seller_info_not_found_then_should_notify_patolino_and_skip_process( # noqa
        self,
        processor,
        product,
        seller_info,
        mongo_database,
        patch_patolino_product_post,
        mock_patolino_notification_payload
    ):
        product['seller_id'] = 'luizalabs'
        with patch_patolino_product_post as mock_patolino:
            result = processor.get_seller_info(product, CREATE_ACTION)

        assert not result

        mock_patolino_notification_payload['code'] = PRODUCT_ERROR_CODE
        mock_patolino_notification_payload['message'] = PRODUCT_ERROR_MESSAGE
        mock_patolino_notification_payload['seller_id'] = product['seller_id']
        mock_patolino.assert_called_once_with(
            mock_patolino_notification_payload,
            {
                'seller_id': product['seller_id'],
                'code': PRODUCT_ERROR_CODE,
                'has_tracking': 'false'
            }
        )

    @pytest.mark.parametrize('processor_method', [
        CREATE_ACTION,
        UPDATE_ACTION
    ])
    def test_process_product_should_call_normalized_and_format_product_payload(
        self,
        processor,
        processor_method,
        mongo_database,
        product,
        patch_bucket_upload_data,
        patch_patolino_product_post,
        patch_notification,
        patch_normalize_product_payload,
        patch_format_payload_product
    ):
        if processor_method != CREATE_ACTION:
            mongo_database.raw_products.insert_one(product)

        with patch_bucket_upload_data:
            with patch_normalize_product_payload as mock_normalized_payload:
                with patch_format_payload_product as mock_format_payload:
                    with patch_patolino_product_post as mock_patolino:
                        with patch_notification as mock_notification:
                            getattr(processor, processor_method)(product)

        mock_format_payload.assert_called_once()
        mock_normalized_payload.assert_called_once()
        mock_patolino.assert_called_once()
        mock_notification.assert_called_once()

    def test_when_create_product_with_bundles_then_should_process_with_success(
        self,
        processor,
        product,
        mongo_database,
        patch_bucket_upload_data,
        patch_patolino_product_post,
        patch_notification
    ):
        del product['gift_product']

        with patch_bucket_upload_data:
            with patch_patolino_product_post as mock_patolino:
                with patch_notification as mock_notification:
                    processor.create(product)

        saved_product = mongo_database.raw_products.find_one(
            {'sku': product['sku'], 'seller_id': product['seller_id']},
            {'_id': 0, 'bundles': 1, 'gift_product': 1}
        )
        mock_patolino.assert_called_once()
        mock_notification.assert_called_once()

        assert saved_product['bundles'] == product['bundles']
        assert 'gift_product' not in saved_product

    def test_when_create_product_with_gift_product_then_should_process_with_success( # noqa
        self,
        processor,
        product,
        mongo_database,
        patch_bucket_upload_data,
        patch_patolino_product_post,
        patch_notification
    ):
        del product['bundles']

        with patch_bucket_upload_data:
            with patch_patolino_product_post as mock_patolino:
                with patch_notification as mock_notification:
                    processor.create(product)

        saved_product = mongo_database.raw_products.find_one(
            {'sku': product['sku'], 'seller_id': product['seller_id']},
            {'_id': 0, 'bundles': 1, 'gift_product': 1}
        )

        mock_patolino.assert_called_once()
        mock_notification.assert_called_once()
        assert saved_product['gift_product'] == product['gift_product']
        assert 'bundles' not in saved_product


    def test_when_product_has_gift_product_and_receive_event_to_remove_then_should_update_with_success( # noqa
        self,
        processor,
        product,
        mongo_database,
        patch_bucket_upload_data,
        patch_patolino_product_post,
        patch_notification,
        seller_info
    ):
        del product['bundles']

        with patch_bucket_upload_data, patch_patolino_product_post:
            with patch_notification:
                processor.create(product)

        saved_product = mongo_database.raw_products.find_one(
            {'sku': product['sku'], 'seller_id': product['seller_id']},
            {'_id': 0, 'gift_product': 1}
        )

        assert saved_product['gift_product'] == product['gift_product']

        del product['gift_product']
        with patch_bucket_upload_data, patch_patolino_product_post:
            with patch_notification:
                processor.update(product)

        saved_product = mongo_database.raw_products.find_one(
            {'sku': product['sku'], 'seller_id': product['seller_id']},
            {'_id': 0, 'bundles': 1, 'gift_product': 1}
        )

        assert 'gift_product' not in saved_product

    @pytest.mark.parametrize('processor_method', [
        CREATE_ACTION,
        UPDATE_ACTION
    ])
    def test_when_product_inactive_then_should_be_reactive_product_with_success( # noqa
        self,
        processor,
        mongo_database,
        patch_patolino_product_post,
        patch_save_original_product_bucket,
        patch_notification,
        seller_info,
        processor_method
    ):
        product = ProductSamples.seller_a_variation_with_parent()
        seller_info['id'] = product['seller_id']
        mongo_database.sellers.insert_one(seller_info)

        with patch_save_original_product_bucket:
            with patch_patolino_product_post, patch_notification:
                processor.create(product)
                processor.delete(product)

                saved_product = mongo_database.raw_products.find_one(
                    {'sku': product['sku'], 'seller_id': product['seller_id']},
                    {'_id': 0, 'disable_on_matching': 1}
                )

                assert saved_product['disable_on_matching'] is True

                getattr(processor, processor_method)(product)

                saved_product = mongo_database.raw_products.find_one(
                    {'sku': product['sku'], 'seller_id': product['seller_id']},
                    {'_id': 0, 'disable_on_matching': 1}
                )
                assert saved_product['disable_on_matching'] is False

    @pytest.mark.parametrize('processor_method', [
        CREATE_ACTION,
        UPDATE_ACTION
    ])
    def test_when_process_product_then_should_save_original_product_bucket_and_normalized_on_database(  # noqa
        self,
        processor,
        processor_method,
        mongo_database,
        seller_info,
        patch_patolino_product_post,
        patch_bucket_upload_data,
        patch_notification
    ):
        original = '<p style=\"text-align: center;\"><strong><span style=\"color:#FF0000;\"><span style=\"font-size: 24px;\"><span style=\"font-family: arial,helvetica,sans-serif;\">FILTRO DE AR CONDICIONADO AKX35157 WEGA</span></span></span></strong></p><div data-canvas-width=\"375.1015499999999\" style=\"left: 120px; top: 393.252px; font-size: 15px; font-family: sans-serif; transform: scaleX(0.992332);\"><p><strong><span style=\"font-size:16px;\">-</span></strong> <u><strong><span style=\"font-size:16px;\">Sobre a marca</span></strong></u><strong><span style=\"font-size:16px;\"> :</span></strong></p><p style=\"text-align: justify;\"><span style=\"line-height:22px;\"> A Wega imprime qualidade à sua marca utilizando-se do que há de mais moderno mundialmente em tecnologias, processos e matérias-primas no desenvolvimento de seus produtos.</span></p><p style=\"text-align: justify;\"><span style=\"line-height:22px;\"> Os produtos Wega seguem rigorosamente todas as especificações das montadoras de veículos nacionais e importados, o que garante a performance ideal exigidas em cada projeto de motor.</span></p><p><span style=\"font-size:16px;\"><strong>- </strong><u><strong><span style=\"line-height:22px;\">Porque deve-se trocá-lo regularmente?</span></strong></u></span></p><p><span style=\"font-size:16px;\"><span style=\"line-height:22px;\"> A troca regular do Filtro de Ar de Cabine garante um ambiente saudável aos ocupantes do veículo, pois evita a invasão de contaminantes como: poeiras, ácaros e outros micro-organismos nocivos que atacam as vias respiratórias do ser humano.</span></span></p></div><p><span style=\"font-size:16px;\"><strong><span style=\"font-family: arial,helvetica,sans-serif;\"><span style=\"line-height: 30px;\">- </span></span></strong><u><strong><span style=\"font-family: arial,helvetica,sans-serif;\"><span style=\"line-height: 30px;\">Aplicação</span></span></strong></u><strong><span style=\"font-family: arial,helvetica,sans-serif;\"><span style=\"line-height: 30px;\"> :</span></span><strong><span style=\"font-size:16px;\"> </span></strong></strong><span style=\"font-family:arial,helvetica,sans-serif;\"><span style=\"color: rgb(61, 61, 61);\">206 1.0 16V - (Quiksilver / Thecno / Soleil) - Gasolina - Mecânico // 207 1.4 8V Flex - (Blue Lion / Quiksilver Passion / X-Line / XR) - Álcool / Gasolina - Automático / Mecânico // Hoggar 1.4 Flex 16V - (X-Line / XR) - Álcool / Gasolina - Mecânico</span></span></span></p><table cellpadding=\"1\" cellspacing=\"1\" class=\"dado-tecnico\" style=\"margin: 0px; padding: 0px; border: 1px solid rgb(204, 204, 204); font-variant-numeric: inherit; font-stretch: inherit; line-height: inherit; font-family: Arial, Helvetica, sans-serif; vertical-align: baseline; border-collapse: collapse; border-spacing: 0px; width: 402px; color: rgb(68, 68, 68);\"><thead style=\"margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline;\"><tr style=\"margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline;\"><th style=\"margin: 0px; padding: 4px; border-top: 0px; border-right: 0px; border-left: 0px; border-image: initial; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline; background: rgb(227, 0, 27); color: rgb(255, 255, 255); border-bottom: 1px solid rgb(255, 255, 255) !important;\">Concorrente</th><th style=\"margin: 0px; padding: 4px; border-top: 0px; border-right: 0px; border-left: 0px; border-image: initial; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline; background: rgb(227, 0, 27); color: rgb(255, 255, 255); border-bottom: 1px solid rgb(255, 255, 255) !important;\">Código</th></tr></thead><tbody style=\"margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline;\"><tr style=\"margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline;\"><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">Bosch</td><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">0986BF0533</td></tr><tr style=\"margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline;\"><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">CES</td><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">CES1901</td></tr><tr style=\"margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline;\"><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">Corteco</td><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">51029F</td></tr><tr style=\"margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline;\"><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">Filtros Brasil</td><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">FB601</td></tr><tr style=\"margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline;\"><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">Filtros Mil</td><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">FC1901</td></tr><tr style=\"margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline;\"><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">Filtros Mil</td><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">FC1901C</td></tr><tr style=\"margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline;\"><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">Fram</td><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">CF9071</td></tr><tr style=\"margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline;\"><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">Hengst</td><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">E971LI</td></tr><tr style=\"margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline;\"><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">Idelmax</td><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">MX1019</td></tr><tr style=\"margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline;\"><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">Inpeca</td><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">SAC5013</td></tr><tr style=\"margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline;\"><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">Japanparts</td><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">FAAPE01</td></tr><tr style=\"margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline;\"><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">Mahle</td><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">LA57</td></tr><tr style=\"margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline;\"><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">Mann</td><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">CU29110</td></tr><tr style=\"margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline;\"><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">Mann</td><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">CU3448</td></tr><tr style=\"margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline;\"><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">Micron Air</td><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">MP057</td></tr><tr style=\"margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline;\"><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">Peugeot</td><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">6447AZ</td></tr><tr style=\"margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline;\"><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">Peugeot</td><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">6447TF</td></tr><tr style=\"margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline;\"><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">Purflux</td><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">AH140</td></tr><tr style=\"margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline;\"><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">Schuck</td><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">SK430</td></tr><tr style=\"margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline;\"><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">Seineca</td><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">SEI4800</td></tr><tr style=\"margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline;\"><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">Tecfil</td><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">ACP800</td></tr><tr style=\"margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline;\"><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">Vox</td><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">FAC2029</td></tr><tr style=\"margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline;\"><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">Vox</td><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">FAC800</td></tr><tr style=\"margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: inherit; font-stretch: inherit; font-size: inherit; line-height: inherit; font-family: inherit; vertical-align: baseline;\"><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">Wurth</td><td style=\"margin: 0px; padding: 8px; font-style: inherit; font-variant: inherit; font-stretch: inherit; font-size: 11px; line-height: inherit; font-family: Verdana, Geneva, sans-serif; vertical-align: baseline; color: rgb(0, 0, 0); width: auto; border: 1px solid rgb(204, 204, 204) !important;\">0764074</td></tr></tbody></table><hr/><p><span style=\"font-size:16px;\"><strong><img alt=\"\" src=\"https://images.tcdn.com.br/img/editor/up/478291/22395_1.jpg\" style=\"float: left; width: 405px; height: 405px;\"/></strong><strong><span style=\"font-family: arial,helvetica,sans-serif;\">- </span></strong><span style=\"font-family: arial,helvetica,sans-serif;\"><span style=\"line-height: 30px;\"><strong>Marca:</strong> WEGA</span></span></span></p><p style=\"margin-left: 40px;\"><span style=\"font-size:16px;\"><span style=\"font-family: arial,helvetica,sans-serif;\"><span style=\"line-height: 30px;\"><strong>- Modelo : </strong>AKX35157</span></span></span></p><p style=\"margin-left: 40px;\"><span style=\"font-size:16px;\"><span style=\"font-family: arial,helvetica,sans-serif;\"><span style=\"line-height: 30px;\"><strong>- Tipo de Filtro :</strong> Filtro Ar Cabine</span></span></span></p><p><span style=\"font-size:16px;\"><span style=\"font-family: arial,helvetica,sans-serif;\"><span style=\"line-height: 30px;\"><strong>- Conteúdo da embalagem :</strong> 1 Unidade</span></span></span></p><p><span style=\"font-size:16px;\"><strong>- Elemento Filtrante: </strong>Non Woven</span></p><p><span style=\"font-size:16px;\"><span style=\"font-family: arial,helvetica,sans-serif;\"><span style=\"line-height: 30px;\"><strong><strong>-</strong> Formato : </strong>Trapezoidal</span></span></span></p><p><span style=\"font-size:16px;\"><span style=\"font-family: arial,helvetica,sans-serif;\"><span style=\"line-height: 30px;\"><strong>- Comprimento : </strong>346 mm</span></span></span></p><p><span style=\"font-size:16px;\"><span style=\"font-family: arial,helvetica,sans-serif;\"><span style=\"line-height: 30px;\"><strong>- Altura : </strong>30 mm </span></span></span></p><p><span style=\"font-size:16px;\"><span style=\"font-family: arial,helvetica,sans-serif;\"><span style=\"line-height: 30px;\"><strong>- Largura : </strong>173 mm </span></span></span></p><p><span style=\"font-size:16px;\"><strong>- Cor : </strong>Branco</span></p><p><span style=\"font-size:16px;\"><strong>- Estrutura de Reforço: </strong>Plástico</span></p><p><span style=\"font-size:16px;\"><strong><span style=\"line-height:18px;\">Garantia de 90 Dias contra defeitos de fabricação . </span></strong></span></p><p><strong><img alt=\"\" src=\"https://images.tcdn.com.br/img/editor/up/478291/373039_2012030847.gif\" style=\"width: 25px; height: 25px;\"/> ATENÇÃO : Antes de efetuar a compra, nos comunique através do suporte o ano e modelo do seu veículo para que possamos enviar o filtro correto.</strong></p><p><span style=\"font-size:16px;\"><span style=\"line-height:18px;\">A Martinense de pneus recomenda a instalação por um profissional qualificado, e sugerimos seguir a especificações manual do veículo/Equipamento, se ausentando de qualquer dano causado por instalação inadequada e mau uso do produto</span>.</span></p><p> </p><hr/><p> </p>' # noqa
        expected = '<p><strong><span><span><span>FILTRO DE AR CONDICIONADO AKX35157 WEGA</span></span></span></strong></p><p><strong><span>-</span></strong> <strong><span>Sobre a marca</span></strong><strong><span> :</span></strong></p><p><span> A Wega imprime qualidade à sua marca utilizando-se do que há de mais moderno mundialmente em tecnologias, processos e matérias-primas no desenvolvimento de seus produtos.</span></p><p><span> Os produtos Wega seguem rigorosamente todas as especificações das montadoras de veículos nacionais e importados, o que garante a performance ideal exigidas em cada projeto de motor.</span></p><p><span><strong>- </strong><strong><span>Porque deve-se trocá-lo regularmente?</span></strong></span></p><p><span><span> A troca regular do Filtro de Ar de Cabine garante um ambiente saudável aos ocupantes do veículo, pois evita a invasão de contaminantes como: poeiras, ácaros e outros micro-organismos nocivos que atacam as vias respiratórias do ser humano.</span></span></p><p><span><strong><span><span>- </span></span></strong><strong><span><span>Aplicação</span></span></strong><strong><span><span> :</span></span> </strong><span><span>206 1.0 16V - (Quiksilver / Thecno / Soleil) - Gasolina - Mecânico // 207 1.4 8V Flex - (Blue Lion / Quiksilver Passion / X-Line / XR) - Álcool / Gasolina - Automático / Mecânico // Hoggar 1.4 Flex 16V - (X-Line / XR) - Álcool / Gasolina - Mecânico</span></span></span></p><p><span><strong><span>- </span></strong><span><span><strong>Marca:</strong> WEGA</span></span></span></p><p><span><span><span><strong>- Modelo : </strong>AKX35157</span></span></span></p><p><span><span><span><strong>- Tipo de Filtro :</strong> Filtro Ar Cabine</span></span></span></p><p><span><span><span><strong>- Conteúdo da embalagem :</strong> 1 Unidade</span></span></span></p><p><span><strong>- Elemento Filtrante: </strong>Non Woven</span></p><p><span><span><span><strong><strong>-</strong> Formato : </strong>Trapezoidal</span></span></span></p><p><span><span><span><strong>- Comprimento : </strong>346 mm</span></span></span></p><p><span><span><span><strong>- Altura : </strong>30 mm </span></span></span></p><p><span><span><span><strong>- Largura : </strong>173 mm </span></span></span></p><p><span><strong>- Cor : </strong>Branco</span></p><p><span><strong>- Estrutura de Reforço: </strong>Plástico</span></p><p><span><strong><span>Garantia de 90 Dias contra defeitos de fabricação . </span></strong></span></p><p><strong> ATENÇÃO : Antes de efetuar a compra, nos comunique através do suporte o ano e modelo do seu veículo para que possamos enviar o filtro correto.</strong></p><p><span><span>A Martinense de pneus recomenda a instalação por um profissional qualificado, e sugerimos seguir a especificações manual do veículo/Equipamento, se ausentando de qualquer dano causado por instalação inadequada e mau uso do produto</span>.</span></p> '  # noqa

        product = ProductSamples.magazineluiza_sku_217148200()
        product['description'] = original
        seller_info['id'] = product['seller_id']

        mongo_database.sellers.insert_one(seller_info)

        if processor_method != CREATE_ACTION:
            mongo_database.raw_products.insert_one(product)

        with patch_bucket_upload_data as mock_upload_storage:
            with patch_patolino_product_post as mock_patolino:
                with patch_notification as mock_notification:
                    getattr(processor, processor_method)(product)

        saved_product = mongo_database.raw_products.find_one(
            {
                'sku': product['sku'], 'seller_id': product['seller_id']
            },
            {
                '_id': 0, 'description': 1
            }
        )

        assert saved_product['description'] == expected
        mock_patolino.assert_called_once()
        mock_notification.assert_called_once()

        payload = json_loads(mock_upload_storage.call_args[1]['payload'])
        assert payload['description'] == original

    @pytest.mark.parametrize(
        'title', [
            'Arte de ligar o f*da-se',
            'Arte de ligar o fod@-se',
            '100% Whey Protein',
            'Capinha de celular a prova d\'água'
        ]
    )
    def test_when_normalize_product_with_special_characters_allowed_then_should_keep_value( # noqa
        self,
        processor,
        product,
        title
    ):
        product['title'] = title
        processor.normalize_product_payload(product)
        assert product['title'] == title

    def test_when_update_product_with_product_hash_then_should_save_with_success( # noqa
        self,
        processor,
        mongo_database,
        product,
        patch_patolino_product_post,
        patch_bucket_upload_data,
        patch_notification,
        seller_info,
        mock_product_hash
    ):
        product['product_hash'] = mock_product_hash
        seller_info['id'] = product['seller_id']
        mongo_database.sellers.insert_one(seller_info)
        mongo_database.raw_products.insert_one(product)

        with patch_bucket_upload_data:
            with patch_patolino_product_post as mock_patolino:
                with patch_notification as mock_notification:
                    processor.update(product)

        saved_product = mongo_database.raw_products.find_one(
            {
                'sku': product['sku'], 'seller_id': product['seller_id']
            },
            {
                '_id': 0, 'product_hash': 1
            }
        )

        mock_patolino.assert_called_once()
        mock_notification.assert_called_once()
        assert saved_product['product_hash'] == mock_product_hash

    @pytest.mark.parametrize(
        'processor_method',
        [
            CREATE_ACTION,
            UPDATE_ACTION,
            DELETE_ACTION
        ]
    )
    def test_consumer_product_should_send_tracking_id(
        self,
        processor,
        mongo_database,
        processor_method,
        patch_save_original_product_bucket,
        patch_patolino_product_post,
        patch_bucket_upload_data,
        patch_notification,
        seller_info,
        product
    ):
        product['seller_id'] = 'luizalabs'
        product['disable_on_matching'] = False
        seller_info['id'] = product['seller_id']
        mongo_database.sellers.insert_one(seller_info)

        if processor_method != CREATE_ACTION:
            mongo_database.raw_products.insert_one(product)

        tracking_id = str(uuid4())
        product['tracking_id'] = tracking_id

        with patch_save_original_product_bucket:
            with patch_notification, patch_bucket_upload_data:
                with patch_patolino_product_post as mock_patolino:
                    getattr(processor, processor_method)(product)

        assert mock_patolino.call_args[0][0]['tracking_id'] == tracking_id

    def test_when_create_product_with_seller_containing_name_then_include_seller_name_in_seller_description( # noqa
        self,
        processor,
        mongo_database,
        patch_notification,
        patch_patolino_product_post,
        patch_bucket_upload_data,
        seller_info
    ):
        product = ProductSamples.madeiramadeira_sku_173212()
        product['seller_description'] = product['seller_id']

        seller_name = 'Madeira Madeira'
        seller_info.update({'id': product['seller_id'], 'name': seller_name})
        mongo_database.sellers.insert_one(seller_info)

        with patch_bucket_upload_data:
            with patch_patolino_product_post as mock_patolino:
                with patch_notification as mock_notification:
                    processor.create(product)

        saved_product = mongo_database.raw_products.find_one()
        assert saved_product['seller_description'] == seller_name

        mock_notification.assert_called_once()
        mock_patolino.assert_called_once()

    @pytest.mark.parametrize('method', [
        CREATE_ACTION,
        UPDATE_ACTION
    ])
    def test_when_product_payload_has_ean_value_with_whitespace_then_should_remove_whitespace_and_valid_ean_with_success( # noqa
        self,
        processor,
        product,
        seller_info,
        mongo_database,
        patch_bucket_upload_data,
        patch_patolino_product_post,
        patch_notification,
        method
    ):
        product['ean'] = ' 7892946  3259 71 '
        product['md5'] = ''
        seller_info.update({'id': product['seller_id']})
        mongo_database.sellers.insert_one(seller_info)

        if method == UPDATE_ACTION:
            mongo_database.raw_products.insert_one(copy.copy(product))

        with patch_bucket_upload_data, patch_patolino_product_post:
            with patch_notification:
                getattr(processor, method)(product)

        saved_product = mongo_database.raw_products.find_one(
            {'sku': product['sku'], 'seller_id': product['seller_id']},
            {'_id': 0, 'ean': 1}
        )
        assert saved_product['ean'] == '7892946325971'

    @pytest.mark.parametrize(
        'input_payload,expected_payload', [
            (
                [
                    {
                        'value': ';;<span>Parallel Flow</br> <p>',
                        'type': 'model'
                    },
                    {
                        'value': ';;<strong>Alumínio Brasado</br> <li>',
                        'type': 'material'
                    },
                    {
                        'value': ';;<ul>Gerais: Altura (h): 450mm x Comprimento (l): 950mm x Largura (b): 60mm;Colméia: Altura (h): 315mm x Comprimento (l): 830mm x Largura (b): 20mm</br>', # noqa
                        'type': 'dimensions'
                    }
                ],
                [
                    {
                        'value': ';;Parallel Flow',
                        'type': 'model'
                    },
                    {
                        'value': ';;Alumínio Brasado',
                        'type': 'material'
                    },
                    {
                        'value': ';;Gerais: Altura (h): 450mm x Comprimento (l): 950mm x Largura (b): 60mm;Colméia: Altura (h): 315mm x Comprimento (l): 830mm x Largura (b): 20mm', # noqa
                        'type': 'dimensions'
                    }
                ]
            ),
            (
                [
                    {
                        'value': ';;<span>Parallel Flow</br> <p>',
                        'type': 'model'
                    },
                    {
                        'value': ';;<strong>Alumínio Brasado</br> <li>',
                        'type': 'material'
                    },
                    {
                        'value': ';;<ul>Gerais: Altura (h): 450mm x Comprimento (l): 950mm x Largura (b): 60mm;Colméia: Altura (h): 315mm x Comprimento (l): 830mm x Largura (b): 20mm</br>', # noqa
                        'type': 'dimensions'
                    }
                ],
                [
                    {
                        'value': ';;Parallel Flow',
                        'type': 'model'
                    },
                    {
                        'value': ';;Alumínio Brasado',
                        'type': 'material'
                    },
                    {
                        'value': ';;Gerais: Altura (h): 450mm x Comprimento (l): 950mm x Largura (b): 60mm;Colméia: Altura (h): 315mm x Comprimento (l): 830mm x Largura (b): 20mm', # noqa
                        'type': 'dimensions'
                    }
                ]
            ),
            (
                [
                    {
                        'value': 'AmAreLo Claro',
                        'type': 'color'
                    }
                ],
                [
                    {
                        'value': 'AmAreLo Claro',
                        'type': 'color'
                    },
                ]
            ),
            (
                [
                    {
                        'value': 'Verde Claro',
                        'type': 'color'
                    }
                ],
                [
                    {
                        'value': 'Verde Claro',
                        'type': 'color'
                    }
                ]
            )
        ]
    )
    def test_when_create_product_with_attributes_with_tag_html_then_should_clean_and_process_with_success( # noqa
        self,
        processor,
        product,
        input_payload,
        expected_payload
    ):
        product['attributes'] = input_payload
        processor.clean_html_from_product(product)
        assert product['attributes'] == expected_payload

    @pytest.mark.parametrize('seller_id,action', [
        (MAGAZINE_LUIZA_SELLER_ID, CREATE_ACTION),
        (MAGAZINE_LUIZA_SELLER_ID, UPDATE_ACTION),
        ('fake', CREATE_ACTION)
    ])
    def test_when_update_product_then_save_categorization(
        self,
        mongo_database,
        processor,
        product,
        patch_notification_sender_send,
        seller_id,
        action,
        mock_category_rc_payload
    ):
        product['seller_id'] = seller_id
        mongo_database.raw_products.insert_one(product)

        product.update(mock_category_rc_payload)

        with patch_notification_sender_send:
            processor._save_raw_product(product, action)

        product_updated = mongo_database.raw_products.find_one(
            {},
            {'_id': 0, 'categories': 1, 'main_category': 1}
        )

        assert {
            'categories': product_updated['categories'],
            'main_category': product_updated['main_category']
        } == mock_category_rc_payload

    def test_when_update_product_then_discard_categorization(
        self,
        mongo_database,
        processor,
        product,
        patch_notification_sender_send,
        mock_category_rc_payload
    ):
        product['seller_id'] = 'fake'
        mongo_database.raw_products.insert_one(product)

        product.update(mock_category_rc_payload)

        with patch_notification_sender_send:
            processor._save_raw_product(product, constants.UPDATE_ACTION)

        product_updated = mongo_database.raw_products.find_one(
            {},
            {'_id': 0, 'categories': 1, 'main_category': 1}
        )
        assert {
            'categories': product_updated['categories'],
            'main_category': product_updated['main_category']
        } != mock_category_rc_payload

    def test_when_update_product_with_same_values_then_should_skip_process(
        self,
        processor,
        mongo_database,
        caplog,
        patch_patolino_product_post,
        patch_bucket_upload_data,
        patch_notification,
        seller_info,
        product
    ):
        product_original = copy.copy(product)
        sku = product['sku']
        seller_id = product['seller_id']

        seller_info['id'] = product['seller_id']
        mongo_database.sellers.insert_one(seller_info)

        with patch_bucket_upload_data, patch_patolino_product_post:
            with patch_notification:
                processor.create(product)

        assert mongo_database.raw_products.count_documents(
            {'sku': sku, 'seller_id': seller_id}
        ) > 0

        with patch_bucket_upload_data:
            with patch_patolino_product_post as mock_patolino:
                with patch_notification as mock_notification:
                    processor.update(product_original)

        mock_notification.assert_not_called()
        assert (
            f'Skip product update for sku:{sku} '
            f'seller_id:{seller_id}' in caplog.text
        )

        mock_patolino.assert_called_once_with(
            {
                'sku': sku,
                'seller_id': seller_id,
                'code': PRODUCT_UNFINISHED_PROCESS_CODE,
                'message': PRODUCT_UNFINISHED_PROCESS_MESSAGE.format(
                    sku=sku,
                    seller_id=seller_id,
                    reason=PRODUCT_SKIP_PROCESS
                ),
                'payload': {
                    'navigation_id': product['navigation_id'],
                    'action': UPDATE_ACTION
                },
                'action': UPDATE_ACTION,
                'last_updated_at': ANY
            },
            {
                'seller_id': seller_id,
                'code': PRODUCT_UNFINISHED_PROCESS_CODE,
                'has_tracking': 'false'
            }
        )

    def test_when_update_product_with_different_data_then_should_process(
        self,
        processor,
        mongo_database,
        caplog,
        patch_patolino_product_post,
        patch_bucket_upload_data,
        patch_notification,
        seller_info,
        product
    ):
        product_original = copy.copy(product)
        sku = product_original['sku']

        seller_info['id'] = product['seller_id']
        mongo_database.sellers.insert_one(seller_info)

        with patch_bucket_upload_data, patch_patolino_product_post:
            with patch_notification:
                processor.create(product)

        created_product = mongo_database.raw_products.find_one(
            {'sku': product['sku'], 'seller_id': product['seller_id']},
            {'_id': 0, 'title': 1, 'md5': 1}
        )

        assert created_product['title'] == product_original['title']

        product_original['title'] = 'New title'

        with patch_bucket_upload_data:
            with patch_patolino_product_post as mock_patolino:
                with patch_notification as mock_notification:
                    processor.update(product_original)

        mock_patolino.assert_called_once()
        mock_notification.assert_called_once()

        updated_product = mongo_database.raw_products.find_one(
            {'sku': product['sku'], 'seller_id': product['seller_id']},
            {'_id': 0, 'title': 1, 'md5': 1}
        )

        assert updated_product['title'] == product_original['title']
        assert created_product['md5'] != updated_product['md5']
        assert f'Skip product update for sku:{sku}' not in caplog.text

    @settings_stub(SKIP_MD5_VALIDATION=True)
    def test_when_skip_validation_md5_is_enabled_then_should_ignore_skip_process( # noqa
        self,
        processor,
        mongo_database,
        caplog,
        patch_bucket_upload_data,
        patch_patolino_product_post,
        patch_notification,
        seller_info,
        product
    ):
        product_original = copy.copy(product)
        sku = product_original['sku']

        seller_info['id'] = product['seller_id']
        mongo_database.sellers.insert_one(seller_info)

        with patch_bucket_upload_data, patch_patolino_product_post:
            with patch_notification:
                processor.create(product)

        created_product = mongo_database.raw_products.find_one(
            {'sku': product['sku'], 'seller_id': product['seller_id']},
            {'_id': 0, 'title': 1}
        )

        assert created_product['title'] == product_original['title']

        product_original['title'] = 'New title'

        with patch_bucket_upload_data:
            with patch_patolino_product_post as mock_patolino:
                with patch_notification as mock_notification:
                    processor.update(product_original)

        mock_patolino.assert_called_once()
        mock_notification.assert_called_once()

        updated_product = mongo_database.raw_products.find_one(
            {'sku': product['sku'], 'seller_id': product['seller_id']},
            {'_id': 0, 'title': 1}
        )

        assert updated_product['title'] == product_original['title']
        assert f'Skip product update for sku:{sku}' not in caplog.text

    @pytest.mark.parametrize(
        'word_title_forbidden,'
        'title_forbidden,'
        'title_clean,'
        'word_description_forbidden,'
        'description_forbidden,'
        'description_clean,'
        'method', [
            (
                'v.e.l.c.r.o',
                'v.e.l.c.r.o fixação De Pedais - PRETO',
                'tiras autocolantes fixação De Pedais - PRETO',
                'velcron',
                'produto muito utilizado, Velcron para fixação de baterias, receptores',  # noqa
                'produto muito utilizado, tiras autocolantes para fixação de baterias, receptores',  # noqa
                'update'
            ),
            (
                'velcro',
                'Velcro com material',
                'tiras autocolantes com material',
                'velkro',
                'Fecho de Contato de Velkro em ambas as partes (não necessita cola)',  # noqa
                'Fecho de Contato de tiras autocolantes em ambas as partes (não necessita cola)',  # noqa
                'create'
            ),
            (
                'couro (sintetico)',
                'Jaqueta de Couro (sintético) Biker Com Bolsos Com Zíper Preto',  # noqa
                'Jaqueta de material sintético Biker Com Bolsos Com Zíper Preto',  # noqa
                'korino',
                'Procurando por uma jaqueta Korino resistente e estilosa para enfrentar as intempéries do dia a dia?', # noqa
                'Procurando por uma jaqueta material sintético resistente e estilosa para enfrentar as intempéries do dia a dia?', # noqa
                'update'
            ),
            (
                'couro fake',
                'Jaqueta Biker Com Bolsos Com Zíper Preto couro fake',
                'Jaqueta Biker Com Bolsos Com Zíper Preto material sintético',
                'semi coro',
                'A escolha perfeita para você! Confeccionada em semi coro, essa jaqueta é capaz de suportar ventos fortes e chuvas', # noqa
                'A escolha perfeita para você! Confeccionada em material sintético, essa jaqueta é capaz de suportar ventos fortes e chuvas', # noqa
                'create'
            ),
            (
                'crossfit',
                'Crossfit em casa com o novo...',
                'exercício funcional em casa com o novo...',
                'crosfit',
                'Aparelho de Crosfit para utilizar..',
                'Aparelho de exercício funcional para utilizar..',
                'update'
            ),
            (
                'criado mudo',
                'criado mudo ITÁLIA 2 Gavetas com Pés Retro - PRETO',
                'mesa de cabeceira ITÁLIA 2 Gavetas com Pés Retro - PRETO',
                'criados-mudo',
                'Novo criados-mudo 2 gavetas para utilizar..',
                'Novo mesa de cabeceira 2 gavetas para utilizar..',
                'update'
            ),
            (
                'criados -mudo',
                'criados -mudo novo 2 gavetas',
                'mesa de cabeceira novo 2 gavetas',
                'criados mudo',
                'criados mudo lançamento janeiro...',
                'mesa de cabeceira lançamento janeiro...',
                'create'
            )
        ]
    )
    def test_when_product_has_forbidden_term_then_should_replace_and_process_with_success(  # noqa
        self,
        processor,
        mongo_database,
        product,
        patch_bucket_upload_data,
        patch_patolino_product_post,
        patch_notification,
        word_title_forbidden,
        patch_datetime,
        title_forbidden,
        title_clean,
        word_description_forbidden,
        description_forbidden,
        description_clean,
        method
    ):
        product['title'] = title_forbidden
        product['description'] = description_forbidden

        if method == UPDATE_ACTION:
            mongo_database.raw_products.insert_one(product)

        mock_current_datetime = datetime(2023, 1, 1, 0, 0, 0)

        with patch_bucket_upload_data:
            with patch_patolino_product_post as mock_patolino:
                with patch_notification as mock_notification:
                    with patch_datetime as mock_datetime:
                        mock_datetime.now.return_value = mock_current_datetime
                        getattr(processor, method)(product)

        mock_patolino.assert_called_once()
        mock_notification.assert_called_once()

        product_process = mongo_database.raw_products.find_one(
            {'sku': product['sku'], 'seller_id': product['seller_id']},
            {'_id': 0, 'title': 1, 'description': 1, 'navigation_id': 1}
        )
        assert product_process['title'] == title_clean
        assert product_process['description'] == description_clean

        forbidden_terms = mongo_database.forbidden_terms.find_one(
            {'sku': product['sku'], 'seller_id': product['seller_id']},
            {'_id': 0}
        )

        title_expected = {
            'term': word_title_forbidden,
            'replace': settings.FORBIDDEN_TERMS.get(
                word_title_forbidden
            ),
            'field': 'title',
            'scope': 'product',
            'replaced_at': mock_current_datetime.isoformat()
        }

        description_expected = {
            'term': word_description_forbidden,
            'replace': settings.FORBIDDEN_TERMS.get(
                word_description_forbidden
            ),
            'field': 'description',
            'scope': 'product',
            'replaced_at': mock_current_datetime.isoformat()
        }

        count = 0
        for record in forbidden_terms['forbidden_terms']:
            if title_expected == record or description_expected == record:
                count += 1

        assert count == 2
        assert forbidden_terms['sku'] == product['sku']
        assert forbidden_terms['seller_id'] == product['seller_id']
        assert forbidden_terms['navigation_id'] == product_process['navigation_id'] # noqa

    @pytest.mark.parametrize('ean', [('0197529019726')])
    def test_when_normalize_identifiers_with_valid_ean_then_return_ean(
        self,
        processor,
        ean
    ):
        assert processor._normalize_identifiers(
            decoded_product={'ean': ean},
            stored_product={}
        ) == {'ean': ean}

    @pytest.mark.parametrize('isbn', [('9788582604663')])
    def test_when_normalize_identifiers_with_valid_isbn_then_return_ean_and_isbn(  # noqa
        self,
        processor,
        isbn
    ):
        assert processor._normalize_identifiers(
            decoded_product={'ean': isbn},
            stored_product={}
        ) == {'ean': isbn, 'isbn': isbn}

    def test_when_normalize_identifiers_without_ean_then_not_include_isbn(
        self,
        processor
    ):
        assert processor._normalize_identifiers(
            decoded_product={'ean': ''},
            stored_product={}
        ) == {'ean': ''}

    def test_when_normalize_identifiers_without_ean_but_stored_isbn_then_include_empty_isbn(  # noqa
        self,
        processor
    ):
        assert processor._normalize_identifiers(
            decoded_product={'ean': ''},
            stored_product={'ean': '9788582604663', 'isbn': '9788582604663'}
        ) == {'ean': '', 'isbn': ''}

    @pytest.mark.parametrize('isbn', [('9788582604663')])
    def test_when_normalize_product_payload_including_isbn_then_include_ean_and_isbn(  # noqa
        self,
        processor,
        product,
        isbn
    ):
        product.update({'ean': isbn})
        processor.normalize_product_payload(product, {})
        assert product['ean'] == isbn
        assert product['isbn'] == isbn

    def test_when_normalize_product_payload_removing_ean_then_clean_ean_and_isbn(  # noqa
        self,
        product,
        processor
    ):
        stored_product = copy.deepcopy(product)
        stored_product.update({
            'ean': '9788582604663',
            'isbn': '9788582604663'
        })
        product.update({'ean': ''})
        processor.normalize_product_payload(
            product,
            stored_product
        )
        assert product['ean'] == ''
        assert product['isbn'] == ''

    @pytest.mark.parametrize(
        'action', [
            'create',
            'update',
            'delete'
        ]
    )
    def test_process_message_can_get_method(
        self,
        action,
        processor,
        product,
        patch_create,
        patch_update,
        patch_delete
    ):
        patchs = {
            'create': patch_create,
            'update': patch_update,
            'delete': patch_delete
        }
        with patchs[action] as patch_method:
            processor.process_message({
                'action': action,
                'data': product
            })
            patch_method.assert_called_once()
