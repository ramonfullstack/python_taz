from unittest import mock

import pytest

from taz.crontabs.express_delivery_scrapper.http_client import HttpClient
from taz.helpers.test_utils import mock_response


class TestHttpClient:

    @pytest.fixture
    def http_client(self):
        return HttpClient()

    @mock.patch('requests.post')
    def test_should_delivery_request(
        self,
        mock_get,
        http_client,
        mock_deliveries
    ):
        mock_get.return_value = mock_response(json_data=mock_deliveries)

        response = http_client.post('220907400', 1099, '02136000')

        assert response['records'][0]['deliveries'][0]['modals'][0] == {
            'branch': {
                'departurePoint': 'cd',
                'id': 204,
                'inventory': 300,
                'inventoryOrigin': 300
            },
            'expressDelivery': True,
            'id': 1,
            'inventoryType': {
                'id': 1,
                'name': 'Physical'
            },
            'modality': {
                'abbreviation': 'SE',
                'id': 1,
                'integrationCode': 'SE',
                'name': 'courrier',
                'skipIntegration': False
            },
            'name': 'Convencional',
            'shippingRates': {
                'customerCost': '13.90',
                'operatingCost': '19.23'
            },
            'shippingTime': {
                'businessDays': 1
            },
            'type': 'conventional',
            'zipcodeRestriction': False
        }

    @mock.patch('requests.get')
    def test_should_delivery_request_returns_error(
        self,
        mock_get,
        http_client
    ):
        mock_get.return_value = mock_response(
            status=500,
            raise_for_status=Exception()
        )

        with pytest.raises(Exception) as e:
            http_client.post()

        assert e

    def test_should_delivery_request_returns_not_found(
        self,
        http_client
    ):
        with pytest.raises(Exception) as e:
            http_client.post('111111', 1099, '02136000')

        assert e.value.response.status_code == 404
