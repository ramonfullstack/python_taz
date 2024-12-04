import base64
import json
from unittest.mock import patch

import pytest

from taz.api.common.utils import parse_base64_to_dict


class TestListSellerHandler:

    @pytest.fixture
    def mock_url(self):
        return '/seller/list'

    def test_list_sellers(
        self, client, save_raw_products, mock_url
    ):
        response = client.get(mock_url)
        assert len(response.json['data']) == 3

    def test_list_sellers_without_results(
        self, client, mock_url
    ):
        response = client.get(mock_url)
        assert len(response.json['data']) == 0


class TestSellerHandler:

    @pytest.fixture
    def mock_url(self):
        return '/seller/'

    def test_should_call_sqs_ipdv_marvin_seller_rebuild_when_seller_is_active(
        self,
        client,
        mock_url,
        seller_payload,
        patch_sqs_manager_put,
        create_seller,
        patch_publish_manager
    ):
        with patch_publish_manager as mock_pubsub_publish:
            response = client.post(
                mock_url,
                json=seller_payload
            )

        assert response.status_code == 200

        assert mock_pubsub_publish.call_count == 2
        assert mock_pubsub_publish.call_args_list[0][1].get("content") == {
            'scope': 'marvin_seller_ipdv',
            'action': 'update',
            'data': parse_base64_to_dict(seller_payload['message']['data']),
            'task_id': '7704ae9b6dbc8959562e41c624e624f4'
        }

    @pytest.mark.parametrize(
        'inactive_reason',
        [None, 'Inactive reason']
    )
    def test_should_call_sqs_rebuilds_when_seller_is_inactive(
        self,
        client,
        mock_url,
        inactive_seller_payload,
        inactive_reason,
        create_seller,
        patch_publish_manager
    ):
        expected_param = {
            'scope': 'inactivate_seller_products',
            'action': 'update',
            'data': {'seller_id': 'mlentregas'},
            'task_id': 'e296ffe69c4701745284db683538b5f1'
        }

        if inactive_reason:
            expected_param['data'].update(
                inactive_reason=inactive_reason
            )

            seller = parse_base64_to_dict(
                inactive_seller_payload['message']['data']
            )
            seller.update(inactive_reason=inactive_reason)

            inactive_seller_payload['message']['data'] = base64.b64encode(
                json.dumps(seller).encode('utf-8')
            ).decode('utf-8')

        with patch_publish_manager as mock_pubsub:
            response = client.post(
                mock_url,
                json=inactive_seller_payload
            )

            assert response.status_code == 200

            assert mock_pubsub.call_count == 3

            assert mock_pubsub.call_args_list[0][1].get("content") == {
                'scope': 'marvin_seller_ipdv',
                'action': 'update',
                'data': parse_base64_to_dict(
                    inactive_seller_payload['message']['data']
                ),
                'task_id': '7704ae9b6dbc8959562e41c624e624f4'
            }
            content = mock_pubsub.call_args_list[1][1].get("content")
            assert content == expected_param

    def test_should_raise_bad_request_when_no_payload(
        self,
        client,
        mock_url,
        seller_payload
    ):

        response = client.post(mock_url)

        assert response.status_code == 400

    def test_should_raise_bad_request_when_no_message_in_payload(
        self,
        client,
        mock_url,
        seller_payload
    ):

        del seller_payload['message']

        response = client.post(mock_url, json=seller_payload)

        assert response.status_code == 400

    def test_should_raise_bad_request_when_no_data_in_payload(
        self,
        client,
        mock_url,
        seller_payload
    ):

        del seller_payload['message']['data']

        response = client.post(mock_url, json=seller_payload)

        assert response.status_code == 400

    def test_should_raise_bad_request_when_message_is_invalid_base64(
        self,
        client,
        mock_url,
        seller_payload,
        caplog
    ):
        seller_payload['message']['data'] = 'base64-invalido'

        response = client.post(mock_url, json=seller_payload)

        assert (
            'Could not parse seller base64 payload to dict '
            'error:Incorrect padding payload:base64-invalido'
        ) in caplog.text

        assert response.status_code == 400

    def test_should_insert_seller_in_mongo_collection_sellers(
        self,
        client,
        mock_url,
        mongo_database,
        seller_payload,
        patch_sqs_manager_put,
        patch_pubsub_client
    ):
        with patch_sqs_manager_put:
            with patch_pubsub_client:
                response = client.post(
                    mock_url,
                    json=seller_payload
                )

        criteria = {'id': 'mlentregas'}
        db_data = mongo_database.sellers.find_one(criteria)

        assert response.status_code == 200
        assert db_data['id'] == 'mlentregas'

    def test_should_return_not_found_when_seller_not_exist(
        self,
        client,
        create_seller
    ):
        seller_id = 'fazendaoiosdagua'
        response = client.get('/seller/{}'.format(seller_id))

        assert response.status_code == 404

    def test_should_return_seller_info_when_seller_exist(
        self,
        client,
        create_seller,
        seller
    ):
        seller_id = 'mlentregas'
        response = client.get('/seller/{}'.format(seller_id))

        del seller['_id']
        del seller['api_signature_secret']

        assert response.status_code == 200
        assert response.json['data'] == seller

    def test_should_call_sqs_seller_rebuild_when_sells_to_company_has_changed(
        self,
        client,
        mock_url,
        create_seller,
        seller_sells_to_company_false_payload,
        patch_publish_manager,
    ):
        with patch_publish_manager as mock_pubsub:
            response = client.post(
                mock_url,
                json=seller_sells_to_company_false_payload
            )

        assert response.status_code == 200
        assert mock_pubsub.call_count == 3
        assert mock_pubsub.call_args_list[0][1]['content']['scope'] == 'marvin_seller_ipdv'  # noqa
        assert mock_pubsub.call_args_list[1][1]['content']['scope'] == 'seller_sells_to_company'  # noqa

    def test_should_not_call_sqs_seller_rebuild_when_sells_to_company_has_not_changed(  # noqa
        self,
        client,
        mock_url,
        create_seller,
        seller_payload,
        patch_publish_manager
    ):
        with patch_publish_manager as mock_pubsub:
            response = client.post(
                mock_url,
                json=seller_payload
            )

        assert response.status_code == 200
        assert mock_pubsub.call_count == 2
        assert mock_pubsub.call_args_list[0][1]['content']['scope'] == 'marvin_seller_ipdv'  # noqa

    @pytest.mark.parametrize('field', [
        ('legal_name'),
        ('name'),
        ('document_number'),
        ('address')
    ])
    def test_should_process_seller_without_field_then_not_publish_message_in_taz_sellers_topic( # noqa
        self,
        client,
        mock_url,
        seller_payload,
        patch_publish_manager,
        create_seller,
        field
    ):
        seller = parse_base64_to_dict(seller_payload['message']['data'])
        del seller[field]

        seller_payload['message']['data'] = base64.b64encode(
            json.dumps(seller).encode('utf-8')
        ).decode('utf-8')

        with patch_publish_manager as mock_pubsub:
            response = client.post(
                mock_url,
                json=seller_payload
            )

        assert response.status_code == 200
        assert mock_pubsub.call_count == 1

    def test_should_not_call_sqs_rebuilds_when_inactivate_flag_is_disabled(
        self,
        client,
        mock_url,
        inactive_seller_payload,
        patch_publish_manager,
        create_seller
    ):
        with patch('simple_settings.settings.INACTIVATE_SELLER_SKUS_FLOW_ENABLED', False): # noqa
            with patch_publish_manager as mock_pubsub:
                response = client.post(mock_url, json=inactive_seller_payload)

        assert response.status_code == 200
        assert mock_pubsub.call_count == 2

        assert mock_pubsub.call_args_list[0][1]['content'] == {
            'scope': 'marvin_seller_ipdv',
            'action': 'update',
            'data': parse_base64_to_dict(
                inactive_seller_payload['message']['data']
            ),
            'task_id': '7704ae9b6dbc8959562e41c624e624f4'
        }

    def test_should_call_sqs_rebuilds_when_inactivate_flag_is_enabled(
        self,
        client,
        mock_url,
        inactive_seller_payload,
        patch_publish_manager,
        create_seller
    ):
        with patch_publish_manager as mock_pubsub:
            response = client.post(
                mock_url,
                json=inactive_seller_payload
            )

        assert response.status_code == 200
        assert mock_pubsub.call_count == 3
        assert mock_pubsub.call_args_list[0][1]['content'] == {
            'scope': 'marvin_seller_ipdv',
            'action': 'update',
            'data': parse_base64_to_dict(
                inactive_seller_payload['message']['data']
            ),
            'task_id': '7704ae9b6dbc8959562e41c624e624f4'
        }
        assert mock_pubsub.call_args_list[1][1]['content'] == {
            'scope': 'inactivate_seller_products',
            'action': 'update',
            'data': {'seller_id': 'mlentregas'},
            'task_id': 'e296ffe69c4701745284db683538b5f1'
        }
