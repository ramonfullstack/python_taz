from unittest.mock import patch

import pytest
from simple_settings.utils import settings_stub

from taz.constants import (
    CREATE_ACTION,
    DELETE_ACTION,
    MAGAZINE_LUIZA_SELLER_ID,
    UPDATE_ACTION
)
from taz.consumers.complete_product import SCOPE
from taz.consumers.complete_product.consumer import (
    CompleteProductConsumer,
    CompleteProductProcessor
)
from taz.core.matching.common.samples import ProductSamples
from taz.core.storage.raw_products_storage import RawProductsStorage
from taz.helpers.json import json_dumps


class TestCompleteProduct:

    @pytest.fixture
    def processor(self):
        return CompleteProductProcessor(scope=SCOPE)

    @pytest.fixture
    def consumer(self):
        return CompleteProductConsumer()

    @pytest.fixture
    def mock_message(self):
        return {
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'sku': '213445900',
            'action': CREATE_ACTION
        }

    @pytest.fixture
    def patch_get_bucket_data(self):
        return patch.object(RawProductsStorage, 'get_bucket_data')

    @pytest.fixture
    def patch_get_product_data(self):
        return patch.object(CompleteProductProcessor, '_get_product_data')

    @pytest.fixture
    def patch_should_skip_process(self):
        return patch.object(CompleteProductProcessor, '_should_skip_process')

    @pytest.fixture
    def patch_notify_omnilogic(self):
        return patch.object(CompleteProductProcessor, '_notify_omnilogic')

    @pytest.fixture
    def product_dict(self):
        return ProductSamples.magazineluiza_sku_213445900()

    @pytest.fixture
    def save_price(self, mongo_database, product_dict):
        price = {
            'sku': product_dict['sku'],
            'seller_id': product_dict['seller_id'],
            'list_price': 234.56,
            'price': 123.45,
            'delivery_availability': 'nationwide',
            'stock_count': 321,
            'stock_type': 'on_seller',
            'checkout_price': 234.56,
        }

        mongo_database.prices.insert_one(price)

    @pytest.fixture
    def save_medias(self, mongo_database, product_dict):
        mongo_database.medias.insert_many([
            {
                'seller_id': product_dict['seller_id'],
                'sku': product_dict['sku'],
                'images': [
                    {
                        'url': 'http://img.magazineluiza.com.br/1500x1500/x-213445900.jpg',  # noqa
                        'hash': 'd4b4755b9ee658406f6e40f1d6e6129c'
                    },
                    {
                        'url': 'http://img.magazineluiza.com.br/1500x1500/x-213445900a.jpg',  # noqa
                        'hash': 'ce86964b8543828d1433cb1e029770e5'
                    },
                    '213445900.jpg',
                    '213445900-A.jpg',
                ]
            }
        ])

    def test_when_product_not_exists_then_should_save_log_and_ignore_message(
        self,
        processor,
        mock_message,
        patch_get_bucket_data,
        caplog
    ):
        with patch_get_bucket_data as mock_bucket:
            mock_bucket.return_value = None
            response = processor.process_message(mock_message)

        assert response
        assert (
            'Product not found in for sku:{} seller_id:{}'.format(
                mock_message['sku'],
                mock_message['seller_id']
            ) in caplog.text
        )

    @settings_stub(COMPLETE_PRODUCT_CATEGORY_SKIP=['LI'])
    def test_when_product_exists_and_category_allowed_then_should_return_product_from_bucket( # noqa
        self,
        processor,
        patch_get_bucket_data,
        product_dict,
        mock_message,
        mongo_database
    ):

        mongo_database.raw_products.insert_one(product_dict)
        sku = mock_message['sku']
        seller_id = mock_message['seller_id']

        expected = {
            'sku': '123',
            'seller_id': 'luizalabs'
        }

        with patch_get_bucket_data as mock_bucket:
            mock_bucket.return_value = expected
            product = processor._get_product_data(sku, seller_id)

        mock_bucket.assert_called_once_with(
            sku=sku, seller_id=seller_id
        )
        assert product == expected

    @settings_stub(COMPLETE_PRODUCT_CATEGORY_SKIP=['LI'])
    def test_when_product_exists_and_category_not_allowed_then_not_should_get_product_from_bucket( # noqa
        self,
        processor,
        patch_get_bucket_data,
        mock_message,
        mongo_database
    ):
        product = ProductSamples.magazineluiza_sku_213445900()
        product['categories'] = [{'id': 'LI'}]
        mongo_database.raw_products.insert_one(product)

        sku = product['sku']
        seller_id = product['seller_id']

        with patch_get_bucket_data as mock_bucket:
            result = processor._get_product_data(sku, seller_id)

        mock_bucket.assert_not_called()
        assert sku == result['sku']
        assert seller_id == result['seller_id']

    def test_when_processor_process_success_then_should_notify_omnilogic(
        self,
        processor,
        patch_requests_post,
        product_dict,
        caplog,
        mock_message,
        patch_should_skip_process,
        patch_get_product_data
    ):
        sku = mock_message['sku']
        seller_id = mock_message['seller_id']
        navigation_id = product_dict['navigation_id']

        with patch_should_skip_process as mock_skip_process:
            mock_skip_process.return_value = False
            with patch_get_product_data as mock_get_product:
                mock_get_product.return_value = product_dict
                with patch_requests_post as mock_post:
                    mock_post.return_value.status_code = 200
                    status = processor.process_message(mock_message)

        product = mock_post.call_args[1]['json']

        assert product['sku'] == sku
        assert product['seller_id'] == seller_id
        assert status
        assert (
            f'Message sent successfully for sku:{sku} seller_id:{seller_id} '
            f'navigation_id:{navigation_id} action:create'
        ) in caplog.text

    def test_when_processor_notify_omnilogic_and_return_error_then_should_return_false( # noqa
        self,
        processor,
        patch_requests_post,
        mock_message
    ):
        with pytest.raises(Exception):
            with patch_requests_post as mock_post:
                mock_post.return_value.status_code = 200
                mock_post.return_value.json = lambda: {
                    json_dumps("{'invalid'': 'value'}")
                }
                notification_success = processor._notify_omnilogic(
                    {
                        'sku': mock_message['sku'],
                        'seller_id': mock_message['seller_id']
                    }
                )

            assert not notification_success

    def test_when_processor_notify_omnilogic_and_return_status_500_then_should_return_false( # noqa
        self,
        processor,
        patch_requests_post,
        mock_message
    ):
        with patch_requests_post as mock_post:
            mock_post.return_value.status_code = 500
            notification_success = processor._notify_omnilogic({
                'sku': mock_message['sku'],
                'seller_id': mock_message['seller_id']
            })
            assert not notification_success

    def test_when_processor_receive_message_with_delete_action_should_process_success_with_action_update( # noqa
        self,
        processor,
        product_dict,
        patch_get_product_data,
        patch_should_skip_process,
        patch_notify_omnilogic,
        mock_message
    ):
        mock_message['action'] = DELETE_ACTION
        product_dict['disable_on_matching'] = True

        with patch_should_skip_process as mock_skip_process:
            mock_skip_process.return_value = False
            with patch_get_product_data as mock_get_product:
                mock_get_product.return_value = product_dict
                with patch_notify_omnilogic as mock_notify_ol:
                    status = processor.process_message(mock_message)

        payload_notify = mock_notify_ol.call_args[0][0]

        assert status
        assert not payload_notify['active']
        assert payload_notify['action'] == UPDATE_ACTION
        assert payload_notify['sku'] == mock_message['sku']
        assert payload_notify['seller_id'] == mock_message['seller_id']

    @pytest.mark.parametrize('ean, isbn, expected', [
        ('', '1234567890123', '1234567890123'),
        ('1234567890123', '', '1234567890123'),
        ('', '', ''),
    ])
    def test_create_payload_ean_and_isbn_priority(
        self,
        processor,
        product_dict,
        ean,
        isbn,
        expected
    ):

        product_dict['ean'] = ean
        product_dict['isbn'] = isbn

        payload = processor._create_payload(
            product=product_dict,
            price={},
            images=[],
            action=UPDATE_ACTION,
            path='path'
        )

        assert payload['ean'] == expected

    @pytest.mark.parametrize('field, value, expected', [
        ('product_hash', None, None),
        ('product_hash', 'fake_product_hash', 'fake_product_hash'),
        ('price', None, '0.00'),
        ('price', '5000', '5000'),
        ('list_price', None, '0.00'),
        ('list_price', '7000', '7000'),
        ('stock_count', None, 0),
        ('stock_count', 500, 500),
        ('dimensions', None, {}),
        ('dimensions', {'width': 1}, {'width': 1}),
        ('offer_title', 'fake_offer_title', 'fake_offer_title'),
        ('offer_title', None, 'Lavadora de Roupas Electrolux Addmix'),
        ('attributes', [{'type': 'color'}], [{'type': 'color'}]),
        ('attributes', None, []),
    ])
    def test_create_payload_without_specifics_fields(
        self,
        processor,
        product_dict,
        field,
        value,
        expected
    ):
        price = {}
        if field not in ['price', 'list_price', 'stock_count']:
            product_dict[field] = value
        else:
            price.update({field: value})

        payload = processor._create_payload(
            product=product_dict,
            price=price,
            images=[],
            action=CREATE_ACTION,
            path='fake_path'
        )

        assert payload[field] == expected

    def test_processor_send_message_to_queue_with_correct_medias_values(
        self,
        processor,
        product_dict,
        save_medias,
        mock_message,
        patch_should_skip_process,
        patch_get_product_data,
        patch_notify_omnilogic
    ):
        with patch_should_skip_process as mock_skip_process:
            mock_skip_process.return_value = False
            with patch_get_product_data as mock_get_product:
                mock_get_product.return_value = product_dict
                with patch_notify_omnilogic as mock_notify_ol:
                    status = processor.process_message(mock_message)

        payload_notify = mock_notify_ol.call_args[0][0]

        assert status
        assert payload_notify['medias'] == [
            'https://x.xx.xxx/{w}x{h}/lavadora-de-roupas-electrolux-addmix-13kg/magazineluiza/213445900/d4b4755b9ee658406f6e40f1d6e6129c.jpg',  # noqa
            'https://x.xx.xxx/{w}x{h}/lavadora-de-roupas-electrolux-addmix-13kg/magazineluiza/213445900/ce86964b8543828d1433cb1e029770e5.jpg',  # noqa
            'https://x.xx.xxx/{w}x{h}/lavadora-de-roupas-electrolux-addmix-13kg/magazineluiza/213445900/213445900.jpg',  # noqa
            'https://x.xx.xxx/{w}x{h}/lavadora-de-roupas-electrolux-addmix-13kg/magazineluiza/213445900/213445900-A.jpg'  # noqa
        ]

    def test_when_error_to_read_category_from_product_then_save_log_and_skip_process( # noqa
        self,
        processor,
        product_dict,
        caplog
    ):
        sku = product_dict['sku']
        seller_id = product_dict['seller_id']
        navigation_id = product_dict['navigation_id']

        result = processor._should_skip_process(
            sku=sku,
            seller_id=seller_id,
            navigation_id=navigation_id,
            category=[]
        )

        assert result
        assert (
            f'Skip process category not found for product sku:{sku} '
            f'seller_id:{seller_id} navigation_id:{navigation_id}'
        ) in caplog.text

    @pytest.mark.parametrize('value', [
        'RC',
        '*'
    ])
    def test_when_category_is_forbidden_to_notify_ol_then_save_log_and_skip_process( # noqa
        self,
        processor,
        product_dict,
        caplog,
        value
    ):
        sku = product_dict['sku']
        seller_id = product_dict['seller_id']
        navigation_id = product_dict['navigation_id']

        with settings_stub(CATEGORY_SKIP_EXTERNAL_OMNILOGIC=value):
            result = processor._should_skip_process(
                sku=sku,
                seller_id=seller_id,
                navigation_id=navigation_id,
                category=[{'id': 'RC'}]
            )

        assert result
        assert (
            f'Skip process for product sku:{sku} seller_id:{seller_id} '
            f'navigation_id:{navigation_id} category_id:RC'
        ) in caplog.text
