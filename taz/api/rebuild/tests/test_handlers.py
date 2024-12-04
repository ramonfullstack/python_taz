import json
from unittest.mock import ANY

import pytest
from simple_settings import settings
from simple_settings.utils import settings_stub

from taz.constants import SOURCE_METABOOKS
from taz.consumers.core.notification import Notification
from taz.helpers.json import json_loads

MOCK_URL = '/rebuild/catalog/notification'
DATALAKE_URL = '/rebuild/datalake'


class TestRebuildHandler:

    @pytest.fixture
    def seller_id(self):
        return 'seller_b'

    def test_post_rebuild_returns_success(
        self,
        client,
        seller_id,
        save_raw_products,
        patch_publish_manager
    ):
        payload = {'seller_id': seller_id}

        with patch_publish_manager as mock_pubsub:
            response = client.post(
                '/rebuild/notification',
                body=json.dumps(payload)
            )

        assert response.status_code == 200
        assert mock_pubsub.call_count == 1

    def test_post_rebuild_returns_bad_request(
        self,
        client,
        seller_id,
        save_raw_products,
        patch_sqs_manager_put,
        patch_pubsub_client
    ):

        empty_payload = {}

        with patch_pubsub_client, patch_sqs_manager_put:
            response = client.post(
                '/rebuild/notification',
                body=json.dumps(empty_payload)
            )

        assert response.status_code == 400


class TestRebuildProductHandler:

    @pytest.fixture
    def products(self):
        return [
            {'seller_id': 'magazineluiza', 'sku': '123456789'},
            {'seller_id': 'murcho', 'sku': '9876'}
        ]

    def test_post_rebuild_products_returns_success(
        self,
        client,
        products,
        patch_publish_manager
    ):
        with patch_publish_manager as mock_pubsub:
            response = client.post(
                '/rebuild/products',
                body=json.dumps(products)
            )

        assert response.status_code == 200
        assert mock_pubsub.call_count == 1

    def test_post_rebuild_products_returns_bad_request(
        self,
        client,
        patch_publish_manager
    ):

        products = []

        with patch_publish_manager:
            response = client.post(
                '/rebuild/products',
                body=json.dumps(products)
            )

        assert response.status_code == 400


class TestRebuildCatalogNotification:

    @pytest.fixture
    def valid_product_notification(self):
        return [
            {
                'type': 'product',
                'seller_id': 'magazineluiza',
                'sku': '123456789',
                'navigation_id': 'xablau',
                'action': 'update'
            }
        ]

    @pytest.fixture
    def valid_checkout_price_notification(self):
        return [
            {
                'type': 'checkout_price',
                'seller_id': 'magazineluiza',
                'sku': '123456789',
                'navigation_id': 'xablau',
                'action': 'update'
            }
        ]

    def test_post_rebuild_catalog_notification_returns_bad_request(
        self, client
    ):
        empty_payload = {}

        response = client.post(
            MOCK_URL,
            body=json.dumps(empty_payload)
        )

        assert response.status_code == 400

    def test_missing_type_notification_returns_bad_request(
        self,
        client,
        valid_product_notification
    ):
        del valid_product_notification[0]['type']
        response = client.post(
            MOCK_URL,
            body=json.dumps(valid_product_notification)
        )

        assert response.status_code == 400

    def test_missing_sku_navigation_id_notification_returns_bad_request(
        self,
        client,
        valid_product_notification
    ):
        del valid_product_notification[0]['sku']
        del valid_product_notification[0]['navigation_id']

        response = client.post(
            MOCK_URL,
            body=json.dumps(valid_product_notification)
        )

        assert response.status_code == 400

    def test_missing_seller_navigation_id_notification_returns_bad_request(
        self,
        client,
        valid_product_notification
    ):
        del valid_product_notification[0]['seller_id']
        del valid_product_notification[0]['navigation_id']

        response = client.post(
            MOCK_URL,
            body=json.dumps(valid_product_notification)
        )

        assert response.status_code == 400

    def test_invalid_type_notification_returns_bad_request(
        self,
        client,
        valid_product_notification
    ):
        valid_product_notification[0]['type'] = 'xablau'
        response = client.post(
            MOCK_URL,
            body=json.dumps(valid_product_notification)
        )

        assert response.status_code == 400

    def test_invalid_action_notification_returns_bad_request(
        self,
        client,
        valid_product_notification
    ):
        valid_product_notification[0]['action'] = 'xablau'
        response = client.post(
            MOCK_URL,
            body=json.dumps(valid_product_notification)
        )

        assert response.status_code == 400

    def test_invalid_post_returns_bad_request(self, client):
        response = client.post(
            MOCK_URL,
            body=json.dumps({})
        )
        assert response.status_code == 400

    @settings_stub(CATALOG_NOTIFICATION_PUBSUB=[])
    def test_post_rebuild_products_returns_success(
        self,
        client,
        valid_product_notification,
        patch_pubsub_client,
        caplog
    ):
        with patch_pubsub_client as mock_pubsub:
            response = client.post(
                MOCK_URL,
                body=json.dumps(valid_product_notification)
            )
            assert response.status_code == 200
        assert mock_pubsub.call_count == 1

        data = json_loads(mock_pubsub.call_args_list[0][1]['data'].decode())

        assert data['task_id']
        del data['task_id']

        assert data == {
            'origin': 'rebuild',
            'type': 'product',
            'timestamp': 0,
            'sku': '123456789',
            'seller_id': 'magazineluiza',
            'navigation_id': 'xablau',
            'action': 'update'
        }

    @pytest.mark.parametrize('pubsub_type', [
        'checkout_price',
        None,
    ])
    def test_post_rebuild_products_pubsub_returns_success(
        self,
        client,
        valid_checkout_price_notification,
        patch_pubsub_client,
        caplog,
        pubsub_type
    ):
        with settings_stub(CATALOG_NOTIFICATION_PUBSUB=[pubsub_type]):
            with patch_pubsub_client as mock_pubsub:
                response = client.post(
                    MOCK_URL,
                    body=json.dumps(valid_checkout_price_notification)
                )
                assert response.status_code == 200

        if pubsub_type is not None:
            assert mock_pubsub.call_count == 1

            data = mock_pubsub.call_args[1]['data']
            subscription_id = mock_pubsub.call_args[1]['subscription_id']
            payload = json.loads(data.decode('utf-8'))

            assert payload['task_id']
            del payload['task_id']

            assert subscription_id == 'marvin-gateway-force-taz-sub'

            assert payload == {
                'origin': 'checkout_price',
                'type': 'checkout_price',
                'action': 'update',
                'timestamp': 0,
                'sku': '123456789',
                'seller_id': 'magazineluiza',
                'navigation_id': 'xablau'
            }

            topic_name = settings.MARVIN_NOTIFICATION['topic_name']
            assert f'Request rebuild for {topic_name}' in caplog.text
        else:
            data = json_loads(mock_pubsub.call_args_list[0][1]['data'])
            assert data['task_id']
            del data['task_id']

            assert data == {
                'origin': 'rebuild',
                'type': 'checkout_price',
                'timestamp': 0,
                'sku': '123456789',
                'seller_id': 'magazineluiza',
                'navigation_id': 'xablau',
                'action': 'update'
            }

            assert 'Request rebuild catalog SNS' in caplog.text

    @pytest.mark.parametrize('criteria, delete_fields', [
        ({'navigation_id': '82323jjjj3'}, ['seller_id', 'sku']),
        ({'seller_id': 'seller_a', 'sku': '82323jjjj3'}, ['navigation_id']),
    ])
    def test_post_rebuild_returns_success(
        self,
        client,
        valid_product_notification,
        save_raw_products,
        patch_pubsub_client,
        criteria,
        delete_fields
    ):
        for f in delete_fields:
            del valid_product_notification[0][f]

        valid_product_notification[0].update(criteria)

        with patch_pubsub_client as mock_pubsub:
            response = client.post(
                MOCK_URL,
                body=json.dumps(valid_product_notification)
            )
            assert response.status_code == 200
        assert mock_pubsub.call_count == 1

        data = json_loads(mock_pubsub.call_args_list[0][1]['data'])
        assert data['task_id']
        del data['task_id']

        assert data == {
            'origin': 'rebuild',
            'type': 'product',
            'timestamp': 0,
            'sku': '82323jjjj3',
            'seller_id': 'seller_a',
            'navigation_id': '82323jjjj3',
            'action': 'update'
        }

    def test_warning_of_invalid_navigation_id(
        self,
        client,
        valid_product_notification,
        save_raw_products,
        patch_pubsub_client,
        caplog,
        logger_stream
    ):
        del valid_product_notification[0]['sku']

        with patch_pubsub_client:
            response = client.post(
                MOCK_URL,
                body=json.dumps(valid_product_notification)
            )
            assert response.status_code == 200

        assert 'Notification not found with navigation_id' in logger_stream.getvalue()  # noqa

    def test_post_rebuild_with_invalid_sku_do_not_notificate(
        self,
        client,
        valid_product_notification,
        save_raw_products,
        patch_pubsub_client,
        caplog
    ):
        del valid_product_notification[0]['navigation_id']

        with patch_pubsub_client as mock_pubsub:
            response = client.post(
                MOCK_URL,
                body=json.dumps(valid_product_notification)
            )
            assert response.status_code == 200

        assert mock_pubsub.call_count == 0

        expected_message = (
            'Notification not found with sku:{sku} and seller_id:{seller_id}'
        )
        assert expected_message.format(
            sku=valid_product_notification[0]['sku'],
            seller_id=valid_product_notification[0]['seller_id']
        ) in caplog.text


class TestRebuildMarvinSellerHandler:

    @pytest.fixture
    def data(self):
        return {'data': {'seller_id': 'magazineluiza'}, 'action': 'update'}

    def test_post_rebuild_products_returns_success(
        self,
        client,
        data,
        patch_publish_manager
    ):
        with patch_publish_manager as mock_pubsub:
            response = client.post(
                '/rebuild/marvin/seller',
                body=json.dumps(data)
            )

        assert response.status_code == 200
        assert mock_pubsub.call_count == 1

    def test_post_rebuild_products_returns_error_empty_payload(
        self,
        client,
        patch_publish_manager
    ):
        with patch_publish_manager as mock_pubsub:
            response = client.post(
                '/rebuild/marvin/seller',
                body=json.dumps({})
            )

        assert response.status_code == 400
        assert mock_pubsub.call_count == 0


class TestRebuildProductScoreHandler:

    @pytest.fixture
    def seller_id(self):
        return 'seller_b'

    @pytest.fixture
    def products(self):
        return [
            {'seller_id': 'magazineluiza', 'sku': '123456789'},
            {'seller_id': 'murcho', 'sku': '9876'}
        ]

    def test_post_rebuild_product_score_returns_success(
        self,
        client,
        seller_id,
        save_raw_products,
        patch_publish_manager
    ):
        payload = {'seller_id': seller_id}

        with patch_publish_manager as mock_pubsub:
            response = client.post(
                '/rebuild/score',
                body=json.dumps(payload)
            )

        assert response.status_code == 200
        assert mock_pubsub.call_count == 1

    def test_post_rebuild_score_sku_returns_bad_request_if_invalid_payload(
        self,
        client,
        products,
        patch_publish_manager
    ):
        with patch_publish_manager as mock_pubsub:
            response = client.post(
                '/rebuild/score',
                body=''
            )

        assert response.status_code == 400
        assert mock_pubsub.call_count == 0


class TestRebuildProductScoreBySkuHandler:

    @pytest.fixture
    def products(self):
        return [
            {'seller_id': 'magazineluiza', 'sku': '123456789'},
            {'seller_id': 'murcho', 'sku': '9876'}
        ]

    def test_post_rebuild_score_by_products_returns_success(
        self,
        client,
        products,
        patch_publish_manager
    ):
        with patch_publish_manager as mock_pubsub:
            response = client.post(
                '/rebuild/score/products',
                body=json.dumps(products)
            )

        assert response.status_code == 200
        assert mock_pubsub.call_count == 1

    def test_post_rebuild_score_sku_returns_bad_request_if_invalid_payload(
        self,
        client,
        products,
        patch_publish_manager
    ):
        with patch_publish_manager as mock_pubsub:
            response = client.post(
                '/rebuild/score/products',
                body=''
            )

        assert response.status_code == 400
        assert mock_pubsub.call_count == 0


class TestRebuildMetabooksHandler:

    def test_get_rebuild_products_returns_success(
        self,
        client,
        patch_publish_manager
    ):
        with patch_publish_manager as mock_pubsub:
            response = client.get(f'/rebuild/{SOURCE_METABOOKS}/777')

        assert response.status_code == 200
        mock_pubsub.assert_called_with(
            topic_name=settings.PUBSUB_METADATA_INPUT_TOPIC_NAME,
            project_id=settings.GOOGLE_PROJECT_ID,
            content={
                'source': SOURCE_METABOOKS,
                'identified': '777'
            }
        )

    def test_get_rebuild_products_returns_error_empty_payload(
        self,
        client,
        patch_publish_manager
    ):
        with patch_publish_manager as mock_pubsub:
            response = client.get('/rebuild/metabooks/')

        assert response.status_code == 404
        assert mock_pubsub.call_count == 0


class TestRebuildMatchingOmnilogicHandler:

    def test_get_rebuild_products_returns_success(
        self,
        client,
        patch_publish_manager
    ):
        payload = {'entity': 'Livro'}

        with patch_publish_manager as mock_pubsub:
            response = client.post(
                '/rebuild/matching/omnilogic',
                body=json.dumps(payload)
            )

        assert response.status_code == 200
        assert mock_pubsub.call_count == 1

    def test_get_rebuild_products_returns_error_empty_payload(
        self,
        client,
        patch_publish_manager
    ):
        with patch_publish_manager as mock_pubsub:
            response = client.post(
                '/rebuild/matching/omnilogic'
            )

        assert response.status_code == 400
        assert mock_pubsub.call_count == 0


class TestRebuildProductExporterHandler:

    @pytest.fixture
    def handler(self):
        from taz.api.rebuild.handlers import RebuildProductExporterHandler
        return RebuildProductExporterHandler()

    def test_should_post_rebuild_product_exporter(
        self,
        client,
        patch_pubsub_client
    ):
        payload = {
            'sku': '12345676879',
            'seller_id': 'murcho',
            'type': 'product'
        }

        with patch_pubsub_client as mock_pubsub:
            response = client.post(
                '/rebuild/product/exporter',
                body=json.dumps(payload)
            )

        assert response.status_code == 200
        assert mock_pubsub.call_count == 1
        assert json.loads(mock_pubsub.call_args_list[0][1]['data']) == {
            'sku': '12345676879',
            'seller_id': 'murcho',
            'type': 'product'
        }

    def test_should_post_without_type_rebuild_product_exporter(
        self,
        client,
        patch_sqs_manager_put,
        patch_pubsub_client
    ):
        payload = {
            'sku': '12345676879',
            'seller_id': 'murcho'
        }

        with patch_pubsub_client as mock_pubsub:
            response = client.post(
                '/rebuild/product/exporter',
                body=json.dumps(payload)
            )

        assert response.status_code == 200
        assert mock_pubsub.call_count == 1
        assert json.loads(mock_pubsub.call_args_list[0][1]['data']) == {
            'sku': '12345676879',
            'seller_id': 'murcho',
            'type': 'product'
        }

    def test_validation_error_for_invalid_payload_type(
        self,
        handler
    ):
        payload = {
            'sku': '12345676879',
            'seller_id': 'murcho',
            'type': 'invalid_type_mock'
        }

        from taz.api.common.exceptions import BadRequest
        with pytest.raises(BadRequest):
            handler._validate_payload(payload)

    def test_validation_error_for_required_fields(
        self,
        handler
    ):
        payload = {
            'sku': '12345676879',
            'type': 'invalid_type_mock'
        }

        from taz.api.common.exceptions import BadRequest
        with pytest.raises(BadRequest):
            handler._validate_payload(payload)


class TestRebuildMatchingProductHandler:

    def test_when_receive_payload_product_then_should_publish_sqs_notification(
        self,
        client,
        patch_publish_manager
    ):
        payload = {
            'sku': '1234567890',
            'seller_id': 'test',
        }

        with patch_publish_manager as mock_pubsub:
            response = client.post(
                '/rebuild/matching/product',
                body=json.dumps(payload)
            )

        assert response.status_code == 200
        assert mock_pubsub.call_count == 1
        assert mock_pubsub.call_args_list[0][1].get("content") == {
            'scope': 'matching_by_sku',
            'action': 'update',
            'data': {
                'sku': '1234567890',
                'seller_id': 'test'
            }
        }

    def test_when_payload_product_is_empty_then_return_bad_request(
        self,
        client,
        patch_publish_manager
    ):
        with patch_publish_manager as mock_pubsub:
            response = client.post('/rebuild/matching/product')

        assert response.status_code == 400
        assert mock_pubsub.call_count == 0


class TestRebuildClassifyProductHandler:

    def test_when_receive_payload_product_then_should_publish_sqs_notification(
            self,
            client,
            patch_publish_manager,
    ):
        payload = {
            'sku': '1234567890',
            'seller_id': 'test',
        }

        with patch_publish_manager as mock_pubsub:
            response = client.post(
                '/rebuild/classify/product',
                body=json.dumps(payload)
            )

        assert response.status_code == 200
        assert mock_pubsub.call_count == 1
        assert mock_pubsub.call_args_list[0][1].get("content") == {
            'scope': 'classify_by_sku',
            'action': 'update',
            'data': {
                'sku': '1234567890',
                'seller_id': 'test'
            }
        }

    def test_when_payload_product_is_empty_then_return_bad_request(
            self,
            client,
            patch_publish_manager
    ):
        with patch_publish_manager as mock_pubsub:
            response = client.post('/rebuild/classify/product')

        assert response.status_code == 400
        assert mock_pubsub.call_count == 0


class TestRebuildDatalakeHandler:

    @pytest.fixture
    def mock_payload(self):
        return {
            'seller_id': 'magazineluiza',
            'sku': '010513600',
            'navigation_id': '0105136',
            'type': 'product',
            'action': 'update',
            'source': 'magalu'
        }

    @pytest.fixture
    def url(self):
        return '/rebuild/datalake'

    @pytest.fixture
    def handler(self):
        from taz.api.rebuild.handlers import RebuildDatalakeHandler
        return RebuildDatalakeHandler()

    def test_when_validate_payload_then_return_none(
        self,
        mock_payload,
        handler
    ):
        assert handler._validate_payload(mock_payload) is None

    @pytest.mark.parametrize('field', [
        'action',
        'seller_id',
        'sku',
        'navigation_id',
        'type'
    ])
    def test_when_validate_payload_then_raise_bad_request(
        self,
        mock_payload,
        handler,
        field
    ):
        mock_payload.pop(field)
        from taz.api.common.exceptions import BadRequest
        with pytest.raises(BadRequest):
            handler._validate_payload(mock_payload)

    def test_when_post_rebuild_datalake_then_return_success(
        self,
        client,
        patch_publish_manager,
        mock_payload,
        url
    ):
        with patch_publish_manager as mock_pubsub:
            response = client.post(
                DATALAKE_URL,
                body=json.dumps(mock_payload)
            )

        assert response.status_code == 200
        assert mock_pubsub.call_count == 1

    def test_when_post_rebuild_datalake_then_raise_bad_request(
        self,
        client,
        patch_publish_manager,
        url
    ):

        with patch_publish_manager as mock_pubsub:
            response = client.post(DATALAKE_URL)

        assert response.status_code == 400
        assert mock_pubsub.call_count == 0

    def test_when_post_rebuild_datalake_with_source_then_return_success(
            self,
            client,
            patch_publish_manager,
            mock_payload,
            url
    ):
        with patch_publish_manager as mock_pubsub:
            response = client.post(
                DATALAKE_URL,
                json=mock_payload
            )

        formated_payload = Notification.format_payload(
            sku=mock_payload['sku'],
            seller_id=mock_payload['seller_id'],
            navigation_id=mock_payload['navigation_id'],
            action=mock_payload['action'],
            scope=mock_payload['type'],
            source=mock_payload.get('source'),
            origin='rebuild',
        )

        formated_payload['task_id'] = ANY

        assert formated_payload['source'] == mock_payload['source']

        mock_pubsub.assert_called_with(
            topic_name='taz-datalake',
            project_id='maga-homolog',
            content=formated_payload,

        )

        assert response.status_code == 200
        assert mock_pubsub.call_count == 1

    def test_validate_invalid_source(
        self,
        mock_payload,
        client,
        url,
        caplog
    ):
        mock_payload['source'] = 'invalid_source'

        response = client.post(
            url,
            body=json.dumps(mock_payload)
        )

        assert response.status_code == 400
        assert 'Invalid source type:invalid_source' in caplog.text


class TestRebuildMediaHandler:

    mock_path = '/rebuild/medias'

    def test_post_media_rebuild_success(
        self,
        client,
        patch_publish_manager,
        caplog
    ):
        with patch_publish_manager as mock_pubsub:
            body = json.dumps({
                'seller_id': 'magazineluiza',
                'sku': '123456789',
            })
            response = client.post(self.mock_path, body=body)
            assert response.status_code == 200

        assert mock_pubsub.call_count == 1
        assert mock_pubsub.call_args_list[0][1].get("content") == {
            'scope': 'media_rebuild',
            'action': 'update',
            'data': {
                'seller_id': 'magazineluiza',
                'sku': '123456789',
            }
        }
        assert 'Request rebuild media with payload:' in caplog.text

    @pytest.mark.parametrize(
        'seller_id,sku', [
            ('', '123456789'),
            ('magazineluiza', ''),
            ('', ''),
        ])
    def test_post_media_rebuild_without_seller_or_sku(
        self,
        client,
        patch_publish_manager,
        seller_id,
        sku,
    ):
        with patch_publish_manager as mock_pubsub:
            body = json.dumps({
                'seller_id': seller_id,
                'sku': sku,
            })
            response = client.post(self.mock_path, body=body)
            assert response.status_code == 400

        assert mock_pubsub.call_count == 0

    def test_mount_media_with_from_bucket_is_true(
        self,
        client,
        patch_publish_manager,
        caplog
    ):
        body = json.dumps({
            'seller_id': 'magazineluiza',
            'sku': '123456789',
            'from_bucket': 'true'
        })
        with patch_publish_manager as mock_pubsub:
            response = client.post(self.mock_path, body=body)
            assert response.status_code == 200

        assert mock_pubsub.call_count == 1
        assert mock_pubsub.call_args_list[0][1].get("content") == {
            'scope': 'media_rebuild',
            'action': 'update',
            'data': {
                'seller_id': 'magazineluiza',
                'sku': '123456789',
                'from_bucket': 'true'
            }
        }
        assert 'Request rebuild media with payload:' in caplog.text

    def test_mount_media_with_from_bucket_is_true_and_invalid_seller_id(
        self,
        client,
        patch_publish_manager
    ):
        body = json.dumps({
            'seller_id': 'test',
            'sku': '123456789',
            'from_bucket': 'true'
        })
        with patch_publish_manager as mock_pubsub:
            response = client.post(self.mock_path, body=body)
            assert response.status_code == 400
            assert mock_pubsub.call_count == 0


class TestRebuildPriceRulesHandler:

    @pytest.fixture
    def mock_payload(self):
        return {
            'seller_id': 'magazineluiza',
            'sku': '010513600',
            'navigation_id': '0105136',
        }

    @pytest.fixture
    def handler(self):
        from taz.api.rebuild.handlers import RebuildPriceRulesHandler
        return RebuildPriceRulesHandler()

    def test_when_validate_payload_then_return_none(
        self,
        mock_payload,
        handler
    ):
        assert handler._validate_payload(mock_payload) is None

    @pytest.mark.parametrize('field', [
        'seller_id',
        'sku',
        'navigation_id',
    ])
    def test_when_validate_payload_then_raise_bad_request(
        self,
        mock_payload,
        handler,
        field
    ):
        mock_payload.pop(field)
        from taz.api.common.exceptions import BadRequest
        with pytest.raises(BadRequest):
            handler._validate_payload(mock_payload)

    def test_when_post_rebuild_price_rules_then_return_success(
        self,
        client,
        patch_publish_manager,
        mock_payload
    ):
        with patch_publish_manager as mock_pubsub:
            response = client.post(
                '/rebuild/price_rules',
                body=json.dumps(mock_payload)
            )

        assert response.status_code == 200
        assert mock_pubsub.call_count == 1

    def test_when_post_rebuild_price_rules_then_raise_bad_request(
        self,
        client,
        patch_publish_manager
    ):

        with patch_publish_manager as mock_pubsub:
            response = client.post('/rebuild/price_rules')

        assert response.status_code == 400
        assert mock_pubsub.call_count == 0
