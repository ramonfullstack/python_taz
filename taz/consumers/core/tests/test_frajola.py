from unittest import mock

import pytest
import requests

from taz.consumers.core.frajola import FrajolaRequest
from taz.helpers.test_utils import mock_response


class TestFrajolaRequest:

    @pytest.fixture
    def client(self):
        return FrajolaRequest()

    @pytest.fixture
    def frajola_dict(self):
        return {
            'category_id': 'TM',
            'subcategory_id': 'TMTM',
            'title': 'titulo do produto',
            'reference': 'referencia do produto',
            'brand': 'Temp',
            'active': True
        }

    @pytest.fixture
    def product_id(self):
        return '1515489'

    @pytest.fixture
    def mock_get_return_value(self, product_id, frajola_dict):
        payload = frajola_dict
        payload['code'] = product_id

        return mock_response(json_data=payload)

    def test_should_post_product(
        self,
        client,
        product_id,
        frajola_dict,
        patch_requests_put
    ):
        with patch_requests_put as mock:
            client.put(product_id, frajola_dict)

        assert mock.called

    def test_should_post_returns_exceptions(
        self,
        client,
        product_id,
        frajola_dict,
        patch_requests_put
    ):
        with patch_requests_put as mock:
            mock.side_effect = Exception('Internal Error')
            with pytest.raises(Exception) as e:
                client.put('12345678', frajola_dict)

        assert mock.called
        assert e

    def test_should_get_product(
        self,
        client,
        product_id,
        patch_requests_get,
        mock_get_return_value,
        frajola_dict
    ):
        with patch_requests_get as mock_get:
            mock_get.return_value = mock_get_return_value
            response = client.get(product_id)

        assert mock_get.called
        assert response['code'] == frajola_dict['code']

    @mock.patch('requests.get')
    def test_should_get_returns_not_found(
        self,
        mock_get,
        client,
        product_id
    ):
        mock_resp = requests.models.Response()
        mock_resp.status_code = 404
        mock_get.return_value = mock_resp

        response = client.get(product_id)

        assert not response
        assert mock_get.called
