import json
from unittest.mock import patch

import pytest
import requests
from simple_settings import settings

from taz.constants import SOURCE_RECLASSIFICATION_PRICE_RULE
from taz.consumers.core.taz import TazRequest


class TestTazRequest:

    @pytest.fixture
    def client(self):
        return TazRequest()

    @pytest.fixture
    def patch_requests_delete(self):
        return patch.object(requests, 'delete')

    @pytest.fixture
    def patch_requests_post(self):
        return patch.object(requests, 'post')

    def test_should_return_not_found(
        self,
        client,
        patch_requests_delete
    ):
        with patch_requests_delete as mock_requests_delete:
            mock_resp = requests.models.Response()
            mock_resp.status_code = 404
            mock_requests_delete.return_value = mock_resp

            response = client.delete_enriched_product(
                seller_id='luizalabs',
                sku='xpto01',
                source=SOURCE_RECLASSIFICATION_PRICE_RULE
            )

        assert not response
        assert mock_requests_delete.called

    def test_should_request_returns_exceptions(
        self,
        client,
        patch_requests_post
    ):
        with patch_requests_post as mock:
            mock.side_effect = Exception('Internal Error')
            with pytest.raises(Exception) as err:
                client.post_notification(
                    SOURCE_RECLASSIFICATION_PRICE_RULE,
                    {},
                )

        assert mock.called
        assert err

    def test_should_delete_enriced_product(
        self,
        client,
        patch_requests_delete
    ):

        seller_id = 'luizalabs'
        sku = 'xpto01'
        source = SOURCE_RECLASSIFICATION_PRICE_RULE

        with patch_requests_delete as mock_requests_delete:
            client.delete_enriched_product(
                seller_id=seller_id,
                sku=sku,
                source=source
            )

        mock_requests_delete.assert_called_once_with(
            f'{settings.APIS["taz"]["url"]}/enriched_product' +
            f'/sku/{sku}/seller/{seller_id}/source/{source}',
            headers={
                'Content-type': 'application/json',
                'Authorization': None
            },
            timeout=5,
        )

        assert mock_requests_delete.called

    def test_should_post_notification(
        self,
        client,
        patch_requests_post
    ):
        source = SOURCE_RECLASSIFICATION_PRICE_RULE
        payload = {
            'sku': 'xpto01',
            'seller_id': 'luizalabs',
            'navigation_id': '123',
            'source': source
        }

        with patch_requests_post as mock_requests_post:
            client.post_notification(
                source=source,
                payload=payload
            )

        mock_requests_post.assert_called_once_with(
            f'{settings.APIS["taz"]["url"]}/notification/{source}',
            headers={
                'Content-type': 'application/json',
                'Authorization': None
            },
            timeout=5,
            data=json.dumps(payload),
        )

        assert mock_requests_post.called
