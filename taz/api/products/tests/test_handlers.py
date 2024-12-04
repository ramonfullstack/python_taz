import datetime
import json
from unittest.mock import ANY, PropertyMock, call, patch
from uuid import UUID

import pytest
from simple_settings import settings

from taz import constants
from taz.api.common.exceptions import NotFound
from taz.api.prices.models import PriceModel
from taz.api.products.handlers import (
    CustomProductAttributes,
    ProductUnpublishHandler
)
from taz.api.products.models import (
    CustomProductAttributesModel,
    RawProductModel,
    UnpublishProductModel
)
from taz.constants import CREATE_ACTION, DELETE_ACTION
from taz.consumers.datalake.publish_datalake_context import KafkaTetrix
from taz.core.matching.common.samples import ProductSamples


class TestListProductHandler:

    @pytest.fixture
    def mock_url(self):
        return '/product/list'

    @pytest.mark.parametrize(
        'query_string,expected_data', [
            ('', 3),
            ('seller=seller_a', 1)
        ]
    )
    def test_list_products(
        self,
        client,
        query_string,
        expected_data,
        save_raw_products,
        mock_url
    ):
        response = client.get(
            mock_url, query_string=query_string
        )
        assert len(response.json['data']) == expected_data

    def test_list_products_with_filter_and_without_results(
        self, client, mock_url
    ):
        response = client.get(mock_url, query_string='seller=seller_a')
        assert len(response.json['data']) == 0

    def test_list_products_without_results(self, client, mock_url):
        response = client.get(mock_url)
        assert len(response.json['data']) == 0


class TestProductHandler:

    @pytest.fixture
    def mock_url(self):
        return '/product/seller/{}/sku/{}'

    def test_get_product(
        self, client, save_raw_products, save_prices,
        save_medias, mock_url
    ):
        product = ProductSamples.seller_a_variation_with_parent()

        response = client.get(
            mock_url.format(
                product['seller_id'], product['sku']
            )
        )

        assert response.json['data']['seller_id'] == product['seller_id']
        assert response.json['data']['sku'] == product['sku']
        assert response.json['data']['price']['list_price'] == '234.56'
        assert len(response.json['data']['media']['images']) == 1

    def test_get_product_returns_product_not_found(self, client, mock_url):
        product = ProductSamples.seller_a_variation_with_parent()

        response = client.get(
            mock_url.format(
                product['seller_id'], product['sku']
            )
        )

        assert response.status_code == 404


class TestProductNavigationIdHandler:

    @pytest.fixture
    def mock_url(self):
        return '/product/seller/{}/sku/{}'

    def test_get_product_navigation_id(
        self, client, save_raw_products, save_prices,
        save_medias, mock_url
    ):
        product = ProductSamples.seller_a_variation_with_parent()

        response = client.get(
            '/product/navigation/{}'.format(product['navigation_id'])
        )

        assert response.json['data']['seller_id'] == product['seller_id']
        assert response.json['data']['sku'] == product['sku']
        assert response.json['data']['price']['list_price'] == '234.56'
        assert len(response.json['data']['media']['images']) == 1

    def test_get_product_navigation_id_returns_product_not_found(
        self, client, mock_url
    ):
        product = ProductSamples.seller_a_variation_with_parent()

        response = client.get(
            mock_url.format(
                product['seller_id'], product['sku']
            )
        )

        assert response.status_code == 404

    def test_get_product_returns_media_empty(
        self, client, save_raw_products, save_prices, mock_url
    ):
        product = ProductSamples.seller_a_variation_with_parent()

        response = client.get(
            mock_url.format(
                product['seller_id'], product['sku']
            )
        )

        assert response.status_code == 200
        assert response.json['data']['media'] == {}


class TestProductStatHandler:

    @pytest.fixture
    def seller_id(self):
        return 'magazineluiza'

    @pytest.fixture
    def product_dict(self):
        return ProductSamples.seller_a_variation_with_parent()

    @pytest.fixture
    def price_dict(self, product_dict):
        return {
            'sku': product_dict['sku'],
            'seller_id': product_dict['seller_id'],
            'list_price': '234.56',
            'price': '123.45',
            'delivery_availability': 'nationwide',
            'stock_count': 321,
            'stock_type': 'on_seller'
        }

    def test_get_product_stats_returns_success(
        self,
        client,
        product_dict,
        price_dict
    ):
        RawProductModel(**product_dict).save()
        PriceModel(**price_dict).save()

        response = client.get(
            '/product/variation/{}/count'.format(product_dict['seller_id'])
        )

        expected_result = {
            'unavailable_variations': 0,
            'total_active_variations': 1,
            'available_variations': 1,
            'total_variations': 1
        }

        assert response.status_code == 200
        assert response.json['data'] == expected_result

    def test_get_product_stats_without_prices_returns_success(
        self,
        client,
        product_dict,
        price_dict
    ):
        RawProductModel(**product_dict).save()

        price_dict['stock_count'] = 0
        PriceModel(**price_dict).save()

        response = client.get(
            '/product/variation/{}/count'.format(product_dict['seller_id'])
        )

        expected_result = {
            'unavailable_variations': 1,
            'total_active_variations': 1,
            'available_variations': 0,
            'total_variations': 1
        }

        assert response.status_code == 200
        assert response.json['data'] == expected_result

    def test_get_product_stats_seller_does_not_exists_returns_not_found(
        self,
        client,
        product_dict
    ):
        response = client.get(
            '/product/{}/count'.format(product_dict['seller_id'])
        )
        assert response.status_code == 404


class TestProductUnpublishHandler:

    @pytest.fixture
    def mock_url(self):
        return '/product/variation/unpublish'

    @pytest.fixture
    def patch_send_product(self):
        return patch.object(ProductUnpublishHandler, '_send_product')

    @pytest.fixture
    def patch_generate_uuid(self):
        return patch.object(
            UUID,
            'hex',
            new_callable=PropertyMock(
                return_value='6528c758-090d-4f59-a5b1-8ad09e4dd6a0'
            )
        )

    @pytest.fixture
    def patch_kafka(self):
        return patch.object(KafkaTetrix, 'publish')

    def test_when_product_not_found_then_should_save_product_unpublish_collection_and_process_with_success( # noqa
        self,
        client,
        mock_url,
        product_json,
        patch_send_product,
        patch_publish_manager,
        patch_kafka,
        patch_datetime
    ):
        with patch_publish_manager as mock_publish_pubsub:
            with patch_kafka as mock_kafka:
                mock_current_datetime = datetime.datetime(2023, 1, 1, 0, 0, 0)
                with patch_datetime as mock_datetime:
                    mock_datetime.utcnow.return_value = mock_current_datetime
                    ProductUnpublishHandler.scope = 'fake_scope'
                    with patch_send_product:
                        response = client.post(
                            mock_url,
                            body=json.dumps(product_json)
                        )

        assert response.status_code == 200
        mock_publish_pubsub.assert_called_once_with(
            content={
                'data': {
                    'navigation_id': product_json['navigation_id'],
                    'user': product_json['user'],
                    'updated_at': '2023-01-01T00:00:00',
                    'created_at': '2023-01-01T00:00:00',
                    'action': CREATE_ACTION
                },
                'schema': 'fake_scope'
            },
            topic_name='fake',
            project_id='maga-homolog'
        )

        mock_kafka.assert_called_once_with(
            {
                'navigation_id': product_json['navigation_id'],
                'user': product_json['user'],
                'updated_at': '2023-01-01T00:00:00',
                'created_at': '2023-01-01T00:00:00',
                'action': CREATE_ACTION
            },
            {'topic_name': 'fake', 'enabled': True}
        )

        assert UnpublishProductModel.get(
            navigation_id=product_json.get('navigation_id')
        )

    def test_should_unpublish_product_even_when_not_found_in_raw_products(
        self,
        client,
        mock_url,
        product_json,
        patch_kafka,
        caplog
    ):
        with patch_kafka:
            response = client.post(
                mock_url, body=json.dumps(product_json)
            )

        assert response.status_code == 200
        assert UnpublishProductModel.get(
            navigation_id=product_json.get('navigation_id')
        )
        assert 'Product {} not found in raw products.'.format(
            product_json['navigation_id']
        ) in caplog.text

    def test_should_delete_product_from_collection(
        self,
        client,
        mock_url,
        product_json,
        patch_send_product,
        patch_publish_manager,
        patch_kafka,
        patch_datetime,
        save_unpublished_products
    ):
        with patch_publish_manager as mock_publish_pubsub:
            with patch_kafka as mock_kafka:
                mock_current_datetime = datetime.datetime(2023, 1, 1, 0, 0, 0)
                with patch_datetime as mock_datetime:
                    mock_datetime.utcnow.return_value = mock_current_datetime
                    ProductUnpublishHandler.scope = 'fake_scope'
                    with patch_send_product:
                        response = client.delete(
                            mock_url,
                            body=json.dumps(product_json)
                        )

        navigation_id = product_json['navigation_id']
        assert response.status_code == 200

        mock_publish_pubsub.assert_called_once_with(
            content={
                'data': {
                    'navigation_id': navigation_id,
                    'user': product_json['user'],
                    'action': DELETE_ACTION
                },
                'schema': 'fake_scope'
            },
            topic_name='fake',
            project_id='maga-homolog'
        )

        mock_kafka.assert_called_once_with(
            {
                'navigation_id': product_json['navigation_id'],
                'user': product_json['user'],
                'action': DELETE_ACTION
            },
            {'topic_name': 'fake', 'enabled': True}
        )

        with pytest.raises(NotFound):
            UnpublishProductModel.get(
                navigation_id=product_json.get('navigation_id')
            )

    def test_should_delete_multiple_same_navigation_id_products(
        self,
        client,
        mock_url,
        product_json,
        patch_send_product,
        patch_publish_manager,
        patch_kafka
    ):
        UnpublishProductModel(**product_json).save()
        UnpublishProductModel(**product_json).save()

        with patch_publish_manager as mock_publish_pubsub:
            with patch_kafka as mock_kafka:
                ProductUnpublishHandler.scope = 'fake_scope'
                with patch_send_product:
                    response = client.delete(
                        mock_url,
                        body=json.dumps(product_json)
                    )

        assert response.status_code == 200
        assert mock_publish_pubsub.call_count == 2
        assert mock_kafka.call_count == 2

        with pytest.raises(NotFound):
            UnpublishProductModel.get(
                navigation_id=product_json.get('navigation_id')
            )

    def test_delete_should_raise_bad_request_missing_navigation_id(
        self,
        client,
        mock_url,
        product_json,
        patch_send_product
    ):
        UnpublishProductModel(**product_json).save()
        with patch_send_product:
            response = client.delete(
                mock_url, body=json.dumps({})
            )

        assert response.status_code == 400

    def test_delete_should_delete_if_navigation_id_more_than_7_digits(
        self,
        client,
        mock_url,
        product_json,
        patch_send_product,
        patch_publish_manager,
        patch_kafka
    ):
        product_json['navigation_id'] = '0123456790'
        UnpublishProductModel(**product_json).save()

        with patch_publish_manager, patch_kafka:
            ProductUnpublishHandler.scope = 'fake_scope'
            with patch_send_product:
                response = client.delete(
                    mock_url,
                    body=json.dumps(product_json)
                )

        assert response.status_code == 200

        with pytest.raises(NotFound):
            UnpublishProductModel.get(
                navigation_id=product_json.get('navigation_id')
            )

    def test_delete_should_delete_invalid_product_raise_not_found(
        self,
        client,
        mock_url,
        product_json,
        patch_send_product,
        patch_kafka
    ):
        with patch_send_product, patch_kafka:
            response = client.delete(
                mock_url, body=json.dumps(product_json)
            )

        assert response.status_code == 404

        with pytest.raises(NotFound):
            UnpublishProductModel.get(
                navigation_id=product_json.get('navigation_id')
            )

    def test_delete_should_notify_product_writer_with_update(
        self,
        client,
        mock_url,
        product_json,
        save_raw_products,
        patch_sqs_manager_put,
        patch_publish_manager,
        patch_kafka
    ):
        product_json['navigation_id'] = '82323jjjj3'
        UnpublishProductModel(**product_json).save()

        with patch_publish_manager as mock_pubsub:
            ProductUnpublishHandler.scope = 'fake_scope'
            response = client.delete(
                mock_url,
                body=json.dumps(product_json)
            )

        assert response.status_code == 200

        with pytest.raises(NotFound):
            UnpublishProductModel.get(
                navigation_id=product_json.get('navigation_id')
            )

        assert mock_pubsub.call_count == 2
        assert mock_pubsub.call_args[1]['content']['sku'] == '82323jjjj3'
        assert mock_pubsub.call_args[1]['content']['seller_id'] == 'seller_a'
        assert mock_pubsub.call_args[1]['content']['action'] == 'update'
        assert mock_pubsub.call_args[1]['content']['force'] is True

    def test_should_get_unpublished_product_list(
        self,
        client,
        mock_url,
        product_json,
        patch_send_product,
        patch_kafka
    ):
        with patch_send_product, patch_kafka:
            client.post(
                mock_url, body=json.dumps(product_json)
            )

        response = client.get(mock_url)

        assert response.status_code == 200
        assert (
            json.loads(response.text).get('products')[0].get(
                'navigation_id'
            ) == product_json.get('navigation_id')
        )

    def test_should_get_unpublished_product_list_with_navigation_id(
        self,
        client,
        mock_url,
        product_json,
        patch_kafka,
        patch_send_product
    ):
        with patch_send_product, patch_kafka:
            client.post(
                mock_url, body=json.dumps(product_json)
            )

        response = client.get(
            mock_url,
            query_string='navigation_id={}'.format(
                product_json['navigation_id']
            )
        )

        assert response.status_code == 200
        assert (
            json.loads(response.text).get('products')[0].get(
                'navigation_id'
            ) == product_json.get('navigation_id')
        )

    def test_should_get_empty_product_list(
        self,
        client,
        product_json,
        mock_url
    ):
        response = client.get(mock_url)

        assert response.status_code == 200
        assert json.loads(response.text).get('products') == []

    def test_should_get_empty_product_list_with_nonexistent_navigation_id(
        self,
        client,
        mock_url,
        product_json,
        patch_send_product,
        patch_kafka
    ):
        with patch_send_product, patch_kafka:
            client.post(
                mock_url, body=json.dumps(product_json)
            )

        response = client.get(
            mock_url,
            query_string='navigation_id=xablau'
        )

        assert response.status_code == 200
        assert json.loads(response.text).get('products') == []

    def test_should_send_product_to_product_writer_numeric(
        self,
        client,
        mock_url,
        save_raw_products,
        patch_publish_manager,
        patch_kafka,
        patch_sqs_manager_put
    ):
        product_json = {
            'navigation_id': '82323jjjj3',
            'user': 'xablau'
        }

        expected_criteria = {
            'sku': '82323jjjj3',
            'seller_id': 'seller_a',
            'action': 'update',
            'task_id': ANY,
            'force': True
        }
        with patch_publish_manager as mock_publish_pubsub:
            with patch_kafka as mock_kafka:
                ProductUnpublishHandler.scope = 'fake_scope'
                client.post(
                    mock_url,
                    body=json.dumps(product_json)
                )

        assert mock_publish_pubsub.call_count == 2
        assert mock_kafka.call_count == 1
        publised_content = mock_publish_pubsub.call_args_list[0][1]['content']

        for field, data in expected_criteria.items():
            assert publised_content[field] == data

    def test_should_send_product_to_product_writer_alphanumeric(
        self,
        client,
        mock_url,
        save_raw_products,
        patch_publish_manager,
        patch_kafka,
        patch_sqs_manager_put
    ):
        product_json = {
            'navigation_id': '82323jjjj3',
            'user': 'xablau'
        }

        expected_criteria = {
            'sku': product_json['navigation_id'],
            'seller_id': 'seller_a',
            'action': 'update',
            'task_id': ANY,
            'force': True
        }

        with patch_publish_manager as mock_publish_pubsub:
            with patch_kafka as mock_kafka:
                ProductUnpublishHandler.scope = 'fake_scope'
                client.post(
                    mock_url,
                    body=json.dumps(product_json)
                )

        assert mock_publish_pubsub.call_count == 2
        assert mock_kafka.call_count == 1

        publised_content = mock_publish_pubsub.call_args_list[0][1]['content']
        assert publised_content == expected_criteria

    @pytest.mark.parametrize('navigation_id', [
        '123123000',
        '1231230'
    ])
    def test_post_send_product_with_navigation_with_7_and_9_digits_then_should_find_values(  # noqa
        self,
        client,
        mock_url,
        product_json,
        patch_publish_manager,
        patch_kafka,
        patch_sqs_manager_put,
        mongo_database,
        navigation_id,
        patch_generate_uuid
    ):
        product = ProductSamples.magazineluiza_sku_0233847()
        product['navigation_id'] = navigation_id
        mongo_database.raw_products.save(product)

        with patch_publish_manager as mock_pubsub:
            with patch_kafka as mock_kafka:
                with patch_generate_uuid:
                    ProductUnpublishHandler.scope = 'fake_scope'
                    client.post(
                        mock_url,
                        body=json.dumps(product_json)
                    )

        assert mock_pubsub.call_count == 2
        assert mock_kafka.call_count == 1

        publised_content = mock_pubsub.call_args_list[0][1]['content']
        assert publised_content == {
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'action': 'update',
            'task_id': '6528c758-090d-4f59-a5b1-8ad09e4dd6a0',
            'force': True
        }


class TestProductCustomAttributes:

    @pytest.fixture
    def seller_id(self):
        return 'franca-games'

    @pytest.fixture
    def sku(self):
        return '10366'

    @pytest.fixture
    def custom_attributes(self, seller_id, sku):
        return {
            'short_title': 'PS4 - Shadow of the Colossus',
            'short_description': (
                'SHADOW OF THE COLOSSUS Recriado do zero'
            )
        }

    @pytest.fixture
    def save_custom_attributes(self, custom_attributes, seller_id, sku):
        payload = {
            'seller_id': seller_id,
            'sku': sku
        }

        payload.update(custom_attributes)

        CustomProductAttributesModel(**payload).save()

    @pytest.fixture
    def expected_criteria(self):
        return {
            'seller_id': 'franca-games',
            'sku': '10366',
            'action': 'update',
            'task_id': 'd77fba5b1b1148a692b86f1a4264c26f',
            'force': True
        }

    @pytest.fixture
    def mock_url(self):
        return '/product/custom-attributes/{}/{}'

    @pytest.fixture
    def patch_send_product(self):
        return patch.object(CustomProductAttributes, '_send_product')

    @pytest.fixture
    def patch_uuid(self):
        return patch.object(
            CustomProductAttributes,
            '_new_uuid',
            return_value='d77fba5b1b1148a692b86f1a4264c26f'
        )

    def test_should_send_notification_via_pubsub(
        self,
        client,
        custom_attributes,
        seller_id,
        sku,
        expected_criteria,
        mock_url,
        patch_publish_manager,
        patch_uuid
    ):
        with patch_uuid, patch_publish_manager as mock_pubsub:
            response = client.post(
                mock_url.format(seller_id, sku),
                body=json.dumps(custom_attributes)
            )

        assert response.status_code == 200
        assert mock_pubsub.call_args == call(
            content=expected_criteria,
            topic_name=settings.PUBSUB_PRODUCT_WRITER_TOPIC_NAME,
            project_id=settings.GOOGLE_PROJECT_ID,
        )

    def test_should_save_custom_attributes(
        self,
        client,
        custom_attributes,
        seller_id,
        sku,
        mock_url,
        patch_send_product
    ):
        with patch_send_product:
            response = client.post(
                mock_url.format(seller_id, sku),
                body=json.dumps(custom_attributes)
            )

        assert response.status_code == 200

        data_saved = CustomProductAttributesModel.objects(
            seller_id=seller_id, sku=sku
        ).first()

        assert data_saved['sku'] == sku
        assert data_saved['seller_id'] == seller_id
        assert data_saved['short_title'] == 'PS4 - Shadow of the Colossus'
        assert data_saved['short_description'] == (
            'SHADOW OF THE COLOSSUS Recriado do zero'
        )

    def test_should_update_custom_attributes(
        self,
        client,
        save_custom_attributes,
        custom_attributes,
        seller_id,
        sku,
        mock_url,
        patch_send_product
    ):
        custom_attributes['short_title'] = 'God of War'

        with patch_send_product:
            client.post(
                mock_url.format(seller_id, sku),
                body=json.dumps(custom_attributes)
            )

        data_saved = CustomProductAttributesModel.objects(
            seller_id=seller_id, sku=sku
        ).first()

        assert data_saved['short_title'] == 'God of War'

    def test_should_validate_short_title(
        self,
        client,
        custom_attributes,
        seller_id,
        sku,
        mock_url,
        patch_send_product
    ):
        custom_attributes['short_title'] = (
            'PS4 - Shadow of the Colossus asfasdffsdfsdfsdfsfsd'
        )
        with patch_send_product:
            response = client.post(
                mock_url.format(seller_id, sku),
                body=json.dumps(custom_attributes)
            )

        assert response.status_code == 400
        assert json.loads(response.text) == {
            'error': 400,
            'message': 'Validation Error',
            'detail': {
                'short_title': 'String value is too long'
            }
        }

    def test_should_validate_short_description(
        self,
        client,
        custom_attributes,
        seller_id,
        sku,
        mock_url,
        patch_send_product
    ):
        custom_attributes['short_description'] = (
            'SHADOW OF THE COLOSSUS Recriado do zero asfasdfdfsddsfsdfdsf'
        )

        with patch_send_product:
            response = client.post(
                mock_url.format(seller_id, sku),
                body=json.dumps(custom_attributes)
            )

        assert response.status_code == 400
        assert json.loads(response.text) == {
            'error': 400,
            'message': 'Validation Error',
            'detail': {
                'short_description': 'String value is too long'
            }
        }

    def test_should_not_duplicate_skus(
        self,
        client,
        custom_attributes,
        seller_id,
        sku,
        mock_url,
        patch_send_product
    ):
        for _ in range(0, 2):
            with patch_send_product:
                response = client.post(
                    mock_url.format(seller_id, sku),
                    body=json.dumps(custom_attributes)
                )
            assert response.status_code == 200

        records = CustomProductAttributesModel.objects(
            seller_id=seller_id, sku=sku
        ).count()

        assert records == 1

    def test_get_custom_attributes(
        self,
        client,
        save_custom_attributes,
        custom_attributes,
        seller_id,
        sku,
        mock_url
    ):
        response = client.get(
            mock_url.format(seller_id, sku),
            body=json.dumps(custom_attributes)
        )

        payload = {
            'seller_id': seller_id,
            'sku': sku
        }
        payload.update(custom_attributes)

        assert response.status_code == 200
        assert json.loads(response.text) == payload

    def test_get_404_if_custom_attributes_not_exists(
        self,
        client,
        custom_attributes
    ):
        response = client.get(
            '/product/custom-attributes/megamamute/000000',
            body=json.dumps(custom_attributes)
        )

        assert response.status_code == 404

    def test_should_delete_custom_attributes(
        self,
        client,
        save_custom_attributes,
        seller_id,
        sku,
        mock_url,
        patch_send_product
    ):
        with patch_send_product:
            response = client.delete(
                mock_url.format(seller_id, sku)
            )
        assert response.status_code == 200

        records = CustomProductAttributesModel.objects(
            seller_id=seller_id, sku=sku
        ).count()

        assert records == 0

    def test_should_return_404_on_delete_not_found_custom_attributes(
        self,
        client
    ):
        response = client.delete('/product/custom-attributes/megamamute/0000')
        assert response.status_code == 404


class TestProductEanHandler:

    @pytest.fixture
    def mock_url(self):
        return '/product/ean/{}'

    def test_get_products_not_default_seller(
        self,
        client,
        save_raw_products,
        save_medias,
        mock_url
    ):
        product = ProductSamples.seller_a_variation_with_parent()
        response = client.get(mock_url.format(product['ean']))

        assert len(response.json['data']) == 3

    def test_get_products_by_magazineluiza(
        self,
        client,
        save_medias,
        mock_url
    ):
        product = ProductSamples.seller_a_variation_with_parent()
        product['seller_id'] = constants.MAGAZINE_LUIZA_SELLER_ID

        raw_products = [
            product,
            ProductSamples.seller_b_variation_with_parent(),
            ProductSamples.seller_c_variation_with_parent()
        ]

        for product in raw_products:
            RawProductModel(**product).save()

        response = client.get(
            mock_url.format(product['ean'])
        )

        expected_payload = [
            {
                'title': 'Caneca Xablau Branca - 450ml - CXB450ML',
                'brand': '+Canecas Xablau',
                'description': 'Caneca xablau batuta',
                'dimensions': {
                    'width': 0.18,
                    'depth': 0.13,
                    'weight': 0.47,
                    'height': 0.44
                }, 'images': [], 'ean': '3123123999999',
                'attributes': [
                    {'type': 'capacity', 'value': '450ml'}
                ]
            }
        ]

        assert len(response.json['data']) == 1
        assert response.json['data'] == expected_payload

    def test_get_products_no_images(
        self,
        client,
        mock_url
    ):
        product = ProductSamples.seller_a_variation_with_parent()
        product['seller_id'] = constants.MAGAZINE_LUIZA_SELLER_ID

        RawProductModel(**product).save()

        response = client.get(
            mock_url.format(product['ean'])
        )

        assert response.json['data'][0]['images'] == []

    def test_get_products_returns_empty_list(
        self,
        client,
        mock_url
    ):
        product = ProductSamples.seller_a_variation_with_parent()

        response = client.get(
            mock_url.format(product['ean'])
        )

        assert response.status_code == 200
        assert response.json['data'] == []

    def test_get_products_without_attributes(
        self,
        client,
        mock_url,
        save_raw_products_without_attributes
    ):
        product = ProductSamples.seller_a_variation_with_parent()

        response = client.get(
            mock_url.format(product['ean'])
        )

        assert response.status_code == 200

        product_response = response.json

        assert product['ean'] == product_response['data'][0]['ean']

    def test_get_ean_with_thirteen_digits_by_default(
        self,
        client,
        mock_url,
        mongo_database
    ):
        product = ProductSamples.seller_a_variation_with_parent()
        product['ean'] = '0001234567890'
        mongo_database.raw_products.insert_one(product)

        response = client.get(mock_url.format('1234567890'))
        assert len(response.json['data']) == 1


class TestTrustedProductEanHandler:

    @pytest.fixture
    def mock_url(self):
        return '/trusted_product/ean/{}'

    def test_get_product_with_success_using_by_default_ean_with_thirteen_digits( # noqa
        self,
        client,
        mock_url,
        mongo_database
    ):
        product_magazineluiza = ProductSamples.ml_variation_a_with_parent()
        product_magazineluiza['ean'] = '0001234567890'
        mongo_database.raw_products.insert_one(product_magazineluiza)

        response = client.get(mock_url.format('1234567890'))
        assert len(response.json['data']) == 1

    def test_get_product_should_return_information_primarily_from_seller_magazineluiza(  # noqa
        self,
        client,
        mock_url
    ):
        same_ean = '0001234567890'

        product_any = ProductSamples.seller_a_variation_with_parent()
        product_kabum = ProductSamples.kabum_sku_102632()
        product_magazineluiza = ProductSamples.ml_variation_a_with_parent()

        raw_products = [product_any, product_kabum, product_magazineluiza]

        for product in raw_products:
            product.update({'ean': same_ean})
            RawProductModel(**product).save()

        response = client.get(
            mock_url.format(same_ean)
        )

        full_title = '{} - {}'.format(
            product_magazineluiza['title'],
            product_magazineluiza['reference']
        )

        assert len(response.json['data']) == 1
        assert response.json['data'][0]['title'] == full_title


    def test_get_product_should_return_information_primarily_from_trusted_sellers(  # noqa
        self,
        client,
        mock_url
    ):
        same_ean = '0001234567890'

        product_any = ProductSamples.seller_a_variation_with_parent()
        product_kabum = ProductSamples.kabum_sku_102632()

        raw_products = [product_any, product_kabum]

        for product in raw_products:
            product.update({'ean': same_ean})
            RawProductModel(**product).save()

        response = client.get(
            mock_url.format(same_ean)
        )

        assert len(response.json['data']) == 1
        assert response.json['data'][0]['title'] == product_kabum['title']


    def test_get_product_should_return_empty_list_if_there_is_no_info_from_trusted_sellers(  # noqa
        self,
        client,
        mock_url
    ):
        product_any = ProductSamples.seller_a_variation_with_parent()

        RawProductModel(**product_any).save()

        response = client.get(
            mock_url.format(product_any['ean'])
        )

        assert len(response.json['data']) == 0
        assert response.json['data'] == []

    def test_get_product_should_return_newer_product_if_there_is_info_from_more_than_one_trusted_seller(  # noqa
        self,
        client,
        mock_url
    ):
        same_ean = '0001234567890'

        product_any = ProductSamples.seller_a_variation_with_parent()
        product_newer = ProductSamples.kabum_sku_102632()
        product_older = ProductSamples.epocacosmeticos_sku_2546()

        raw_products = [product_any, product_newer, product_older]

        for product in raw_products:
            product.update({'ean': same_ean})
            RawProductModel(**product).save()

        response = client.get(
            mock_url.format(same_ean)
        )

        assert len(response.json['data']) == 1
        assert response.json['data'][0]['title'] == product_newer['title']  # noqa


class TestProductVariationHandler:

    @pytest.mark.parametrize('expected_amount', [1, 2, 3])
    def test_get_product_variation(self, expected_amount, client):
        for item in range(expected_amount):
            product = ProductSamples.variation_a_with_parent()
            product['sku'] = '{sku}-{item}'.format(
                sku=product['sku'], item=str(item)
            )
            product['seller_id'] = constants.MAGAZINE_LUIZA_SELLER_ID
            RawProductModel(**product).save()

        response = client.get(
            '/product/parent_sku/{parent}/seller_id/{seller_id}'.format(
                parent=product['parent_sku'],
                seller_id=constants.MAGAZINE_LUIZA_SELLER_ID
            )
        )

        assert response.status_code == 200
        assert len(response.json['data']) == expected_amount

    def test_get_product_return_not_found_status(self, client):
        product = ProductSamples.variation_a_with_parent()
        RawProductModel(**product).save()

        response = client.get(
            '/product/parent_sku/{parent}/seller_id/{seller_id}'.format(
                parent='sku-does-not-exist',
                seller_id=constants.MAGAZINE_LUIZA_SELLER_ID
            )
        )

        assert response.status_code == 404


class TestRawProductBySkuSellerHandler:

    def test_get_with_sku_seller_id_should_return_content_from_storage(
        self,
        client,
        raw_product_dict,
        patch_storage_manager_get_json
    ):
        with patch_storage_manager_get_json as mock_get_json:
            mock_get_json.return_value = raw_product_dict
            response = client.get(
                '/product/raw/seller_id/{seller_id}/sku/{sku}'.format(
                    seller_id=raw_product_dict['seller_id'],
                    sku=raw_product_dict['sku']
                )
            )

        expected_file = '{}/{}.json'.format(
            raw_product_dict['seller_id'],
            raw_product_dict['sku']
        )
        assert mock_get_json.call_count == 1
        assert mock_get_json.call_args[0][0] == expected_file

        assert response.status_code == 200
        assert response.json['data'] == raw_product_dict

    def test_get_with_sku_seller_id_should_return_not_found_if_raise_error(
        self,
        client,
        patch_storage_manager_get_json
    ):
        with patch_storage_manager_get_json as mock_get_json:
            mock_get_json.side_effect = NotFound()
            response = client.get(
                '/product/raw/seller_id/{seller_id}/sku/{sku}'.format(
                    seller_id='does-not-exist',
                    sku='does-not-exist'
                )
            )

        assert mock_get_json.call_count == 1
        assert mock_get_json.call_args[0][0] == (
            'does-not-exist/does-not-exist.json'
        )

        assert response.status_code == 404


class TestRawProductByNavigationHandler:

    @pytest.fixture
    def mock_url(self):
        return '/product/raw/navigation_id/{navigation_id}'

    @pytest.fixture
    def mock_expected_file(self, raw_product_dict):
        return '{}/{}.json'.format(
            raw_product_dict['seller_id'],
            raw_product_dict['sku']
        )

    def test_get_with_navigation_id_should_return_content_from_storage(
        self,
        client,
        mock_url,
        raw_product_dict,
        mock_expected_file,
        patch_storage_manager_get_json
    ):
        RawProductModel(**raw_product_dict).save()

        with patch_storage_manager_get_json as mock_get_json:
            mock_get_json.return_value = raw_product_dict
            response = client.get(
                mock_url.format(
                    navigation_id=raw_product_dict['navigation_id']
                )
            )

        assert mock_get_json.call_count == 1
        assert mock_get_json.call_args[0][0] == mock_expected_file

        assert response.status_code == 200
        assert response.json['data'] == raw_product_dict

    def test_get_with_navigation_id_should_return_not_found_if_storage_raises(
        self,
        client,
        mock_url,
        patch_storage_manager_get_json,
        raw_product_dict,
        mock_expected_file
    ):
        RawProductModel(**raw_product_dict).save()

        with patch_storage_manager_get_json as mock_get_json:
            mock_get_json.side_effect = NotFound()
            response = client.get(
                mock_url.format(
                    navigation_id=raw_product_dict['navigation_id']
                )
            )

        assert mock_get_json.call_count == 1
        assert mock_get_json.call_args[0][0] == mock_expected_file
        assert response.status_code == 404

    def test_get_with_navigation_id_not_found_if_does_not_exist_in_collection(
        self,
        client,
        mock_url,
        patch_storage_manager_get_json,
        raw_product_dict
    ):
        with patch_storage_manager_get_json as mock_get_json:
            mock_get_json.return_value = raw_product_dict
            response = client.get(
                mock_url.format(
                    navigation_id=raw_product_dict['navigation_id']
                )
            )

        assert mock_get_json.call_count == 0

        assert response.status_code == 404


class TestListProductsHandler:

    @pytest.fixture
    def mock_url(self):
        return '/v1/products'

    @pytest.fixture
    def mock_identifier_type(self):
        return 'ean'

    @pytest.fixture
    def mock_identifier_value(self):
        return '3123123999999'

    @pytest.fixture
    def mock_matching_uuid_value(self):
        return 'a0069aee16d441cab4030cce086debbc'

    @pytest.fixture
    def save_medias(self, mongo_database):
        raw_products = [
            ProductSamples.seller_a_variation_with_parent(),
            ProductSamples.seller_c_variation_with_parent()
        ]

        for product in raw_products:
            media = {
                'images': [
                    'd2e14e48997a911745931e6a2991b2cf.jpg',
                    'd2e14e48997a911745931e6a299saass.jpg'
                ],
                'audios': [
                    'd2e14e48997a911745931e6a2991b2cf.wav'
                ],
                'videos': [
                    'd2e14e48997a911745931e6a2991b2cf.mp4'
                ],
                'podcasts': [
                    'd2e14e48997a911745931e6a2991b2cf.wav'
                ],
                'seller_id': product['seller_id'],
                'sku': product['sku']
            }

            mongo_database.medias.save(media)

    def test_when_get_products_with_identifier_in_query_string_then_return_list_of_products( # noqa
        self,
        mock_url,
        client,
        mock_identifier_type,
        mock_identifier_value,
        save_medias,
        save_raw_products,
        save_unpublished_products
    ):
        query_string = 'identifier.type={}&identifier.value={}'.format(
            mock_identifier_type,
            mock_identifier_value
        )
        response = client.get(mock_url, query_string=query_string)
        assert response.json['meta']['page']['count'] == 3
        assert len(response.json['results']) == 3

    def test_when_get_products_with_matching_uuid_in_query_string_then_return_list_of_products( # noqa
        self,
        mock_url,
        client,
        mock_matching_uuid_value,
        save_raw_products_with_inactive
    ):
        query_string = 'matching_uuid={}'.format(mock_matching_uuid_value)
        response = client.get(mock_url, query_string=query_string)

        assert response.json['meta']['page']['count'] == 3
        assert len(response.json['results']) == 3

    @pytest.mark.parametrize(
        'disable_on_matching,expected_count', [
            ('false', 2),
            ('true', 1)
        ]
    )
    def test_when_get_products_with_matching_uuid_and_disable_on_matching_in_query_string_then_return_list_of_products( # noqa
        self,
        mock_url,
        client,
        disable_on_matching,
        expected_count,
        mock_matching_uuid_value,
        save_raw_products_with_inactive
    ):
        query_string = (f'matching_uuid={mock_matching_uuid_value}'
                        f'&disable_on_matching={disable_on_matching}')
        response = client.get(mock_url, query_string=query_string)

        assert response.json['meta']['page']['count'] == expected_count
        assert len(response.json['results']) == expected_count

    def test_when_get_products_with_navigation_id_in_query_string_then_return_specific_product( # noqa
        self,
        mock_url,
        client,
        save_raw_products,
        save_medias
    ):
        response = client.get(
            mock_url,
            query_string='navigation_id=82323jjjj3'
        )
        assert response.json['meta']['page']['count'] == 1
        assert len(response.json['results']) == 1

    @pytest.mark.parametrize(
        'fields_filtered,result', [
            ('navigation_id', ['navigation_id']),
            ('sku,seller_id', ['sku', 'seller_id'])
        ]
    )
    def test_when_get_products_with_specifics_fields_then_return_list_of_products_filtered( # noqa
        self,
        mock_url,
        client,
        mock_identifier_type,
        mock_identifier_value,
        fields_filtered,
        result,
        save_raw_products,
        save_medias
    ):
        query_string = 'identifier.type={}&identifier.value={}&fields={}'.format( # noqa
            mock_identifier_type,
            mock_identifier_value,
            fields_filtered
        )
        response = client.get(mock_url, query_string=query_string)
        for product in response.json['results']:
            assert all(field in product.keys() for field in result)

    @pytest.mark.parametrize(
        'query_string', [
            'matching_uuid=a0069aee16d441cab4030cce086debbc',
            'identifier.type=ean&identifier.value=3123123999999'
        ]
    )
    def test_when_get_products_with_limit_and_offset_invalids_then_return_values_acceptable( # noqa
        self,
        mock_url,
        client,
        query_string
    ):
        query_string = '{}&_limit=100000&_offset=-1'.format(query_string)
        response = client.get(mock_url, query_string=query_string)

        assert response.json['meta']['page']['limit'] == 999
        assert response.json['meta']['page']['offset'] == 0

    @pytest.mark.parametrize('field', ['x'])
    def test_when_get_products_with_non_existent_field_then_return_list_of_products_with_null_field( # noqa
        self,
        mock_url,
        client,
        mock_identifier_type,
        mock_identifier_value,
        field,
        save_raw_products
    ):
        query_string = 'identifier.type={}&identifier.value={}&fields={}'.format( # noqa
            mock_identifier_type,
            mock_identifier_value,
            field
        )
        response = client.get(mock_url, query_string=query_string)
        for product in response.json['results']:
            assert field in product
            assert product[field] is None

    def test_when_get_products_without_fields_then_return_complete_payload_products( # noqa
        self,
        mock_url,
        client,
        mock_matching_uuid_value,
        save_raw_products
    ):
        query_string = 'matching_uuid={}'.format(mock_matching_uuid_value)
        response = client.get(mock_url, query_string=query_string)
        assert len(response.json['results']) == 2
        assert response.json['results'][0] == {
            **ProductSamples.seller_a_variation_with_parent(),
            'media': {}
        }
        assert response.json['results'][1] == {
            **ProductSamples.seller_b_variation_with_parent(),
            'media': {}
        }

    def test_when_get_products_then_return_complete_payload_with_medias(
        self,
        mock_url,
        client,
        mock_matching_uuid_value,
        save_medias,
        save_raw_products
    ):
        query_string = 'matching_uuid={}'.format(mock_matching_uuid_value)
        response = client.get(mock_url, query_string=query_string)

        assert response.json['meta']['page']['count'] == 2
        assert len(response.json['results']) == 2
        assert response.json['results'][1]['media'] == {}
        assert response.json['results'][0]['media'] == {
            'audios': ['/seller_a/audios/82323jjjj3/d2e14e48997a911745931e6a2991b2cf.wav'], # noqa
            'videos': ['d2e14e48997a911745931e6a2991b2cf.mp4'],
            'podcasts': ['/seller_a/podcasts/82323jjjj3/d2e14e48997a911745931e6a2991b2cf.wav'], # noqa
            'images': [
                'https://x.xx.xxx/600x400/caneca-xablau-branca-450ml-cxb450ml/seller_a/82323jjjj3/d2e14e48997a911745931e6a2991b2cf.jpg', # noqa
                'https://x.xx.xxx/600x400/caneca-xablau-branca-450ml-cxb450ml/seller_a/82323jjjj3/d2e14e48997a911745931e6a299saass.jpg'  # noqa
            ]
        }

    def test_when_get_products_without_medias_then_return_complete_payload_with_media_empty( # noqa
        self,
        mock_url,
        client,
        mock_identifier_type,
        mock_identifier_value,
        save_raw_products
    ):
        query_string = 'identifier.type={}&identifier.value={}'.format(
            mock_identifier_type,
            mock_identifier_value
        )
        response = client.get(mock_url, query_string=query_string)

        assert response.json['meta']['page']['count'] == 3
        assert len(response.json['results']) == 3

        for product in response.json['results']:
            assert product['media'] == {}

    def test_when_get_products_with_only_media_in_fields_then_return_media_with_success( # noqa
        self,
        mock_url,
        client,
        mock_matching_uuid_value,
        save_medias,
        save_raw_products
    ):
        query_string = 'matching_uuid={}&fields=media'.format(
            mock_matching_uuid_value
        )
        response = client.get(mock_url, query_string=query_string)

        assert response.json['meta']['page']['count'] == 2
        assert len(response.json['results']) == 2
        assert response.json['results'][1]['media'] == {}
        assert response.json['results'][0]['media'] == {
            'audios': ['/seller_a/audios/82323jjjj3/d2e14e48997a911745931e6a2991b2cf.wav'],  # noqa
            'videos': ['d2e14e48997a911745931e6a2991b2cf.mp4'],
            'podcasts': ['/seller_a/podcasts/82323jjjj3/d2e14e48997a911745931e6a2991b2cf.wav'],  # noqa
            'images': [
                'https://x.xx.xxx/600x400/caneca-xablau-branca-450ml-cxb450ml/seller_a/82323jjjj3/d2e14e48997a911745931e6a2991b2cf.jpg', # noqa
                'https://x.xx.xxx/600x400/caneca-xablau-branca-450ml-cxb450ml/seller_a/82323jjjj3/d2e14e48997a911745931e6a299saass.jpg'  # noqa
            ]
        }


class TestProductExtraDataHandler:

    @pytest.fixture
    def mock_url(self):
        return '/product/extra_data'

    @pytest.fixture
    def save_product(self, mongo_database, raw_product_dict):
        mongo_database.raw_products.insert_one(raw_product_dict)


    def test_when_product_exists_then_should_update_with_extra_data_field_with_success( # noqa
        self,
        client,
        mock_url,
        mock_extra_data,
        raw_product_dict,
        save_product,
        patch_publish_manager,
        mongo_database
    ):
        sku = raw_product_dict['sku']
        seller_id = raw_product_dict['seller_id']

        mock_extra_data['sku'] = sku
        mock_extra_data['seller_id'] = seller_id

        assert raw_product_dict.get('fulfillment') is None

        with patch_publish_manager as mock_pubsub:
            response = client.post(
                mock_url,
                body=json.dumps(mock_extra_data)
            )

        assert response.status_code == 200

        product = mongo_database.raw_products.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'extra_data': 1, 'fulfillment': 1, '_id': 0}
        )

        assert mock_extra_data['extra_data'] == product['extra_data']
        assert product['fulfillment']
        assert mock_pubsub.called

    def test_when_product_has_fulfillment_and_receive_fulfillment_false_then_should_update_info_with_success( # noqa
        self,
        client,
        mock_url,
        mock_extra_data,
        raw_product_dict,
        patch_publish_manager,
        mongo_database
    ):
        sku = raw_product_dict['sku']
        seller_id = raw_product_dict['seller_id']

        raw_product_dict['fulfillment'] = True
        mongo_database.raw_products.insert_one(raw_product_dict)

        mock_extra_data['sku'] = sku
        mock_extra_data['seller_id'] = seller_id
        mock_extra_data['extra_data'] = [
            {
                'name': 'fulfillment',
                'value': 'false'
            }
        ]

        with patch_publish_manager as mock_pubsub:
            response = client.post(
                mock_url,
                body=json.dumps(mock_extra_data)
            )

        assert response.status_code == 200

        product = mongo_database.raw_products.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'extra_data': 1, 'fulfillment': 1, '_id': 0}
        )

        assert mock_extra_data['extra_data'] == product['extra_data']
        assert not product['fulfillment']
        assert mock_pubsub.called

    def test_when_extra_data_payload_without_required_field_then_should_return_bad_request( # noqa
        self,
        client,
        mock_url,
        mock_extra_data,
        patch_publish_manager
    ):
        del mock_extra_data['extra_data']
        with patch_publish_manager as mock_pubsub:
            response = client.post(
                mock_url,
                body=json.dumps(mock_extra_data)
            )

        assert response.status_code == 400
        assert json.loads(response.content) == {
            'error_message': "Invalid payload: {'extra_data': ['Missing data for required field.']}" # noqa
        }

        assert not mock_pubsub.called

    def test_when_product_not_exists_yet_then_should_return_not_found(
        self,
        client,
        mock_url,
        mock_extra_data,
        patch_publish_manager
    ):
        with patch_publish_manager as mock_pubsub:
            response = client.post(
                mock_url,
                body=json.dumps(mock_extra_data)
            )

        assert response.status_code == 404
        assert json.loads(response.content) == {
            'message': 'Product not exists'
        }
        assert not mock_pubsub.called
