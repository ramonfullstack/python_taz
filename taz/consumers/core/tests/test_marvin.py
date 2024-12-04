import pytest

from taz.consumers.core.marvin import MarvinRequest


class TestMarvinRequest:

    @pytest.fixture
    def client(self):
        return MarvinRequest()

    @pytest.fixture
    def ipdv_seller_payload(self):
        return {
            'seller_id': 'lojatop',
            'account_name': 'ParceiroMagalu-lojatop'
        }

    def test_should_register_seller(
        self,
        client,
        ipdv_seller_payload,
        patch_requests_post
    ):
        with patch_requests_post as mock:
            response = client.post(ipdv_seller_payload)

            assert mock.called
            assert response
