from unittest.mock import patch

import pytest

from taz.consumers.core.marvin import MarvinRequest
from taz.consumers.rebuild.scopes.marvin_seller_ipdv import (
    RebuildMarvinSellerIpdv
)


class TestRebuildMarvinSellerIpdv:

    @pytest.fixture
    def rebuild(self):
        return RebuildMarvinSellerIpdv()

    @pytest.fixture
    def mock_register_google(self):
        return patch.object(
            MarvinRequest,
            'post',
            return_value=True
        )

    def test_rebuild_should_success_with_ipdv_seller(
        self,
        rebuild,
        mock_register_google
    ):
        action = {'update'}

        data = {
            'integration_info': {
                'erp': 'Api',
                'platform': 'iPDV'
            },
            'seller_external_id': 'c93208429b214caa8270c9d4ae6f614c',
            'id': 'lojatop'
        }

        with mock_register_google as mock:
            response = rebuild._rebuild(action, data)

        assert mock.call_args[0][0]['seller_id'] == 'lojatop'
        assert mock.call_args[0][0]['account_name'] == 'ParceiroMagalu-lojatop'  # noqa
        assert mock.called
        assert response

    def test_rebuild_should_success_with_another_type_seller(
        self,
        rebuild,
        mock_register_google
    ):
        action = {'update'}

        data = {
            'integration_info': {
                'erp': 'Api',
                'platform': 'Teste'
            },
            'seller_external_id': 'c93208429b214caa8270c9d4ae6f614c',
            'id': 'lojatop'
        }

        with mock_register_google as mock:
            response = rebuild._rebuild(action, data)

        assert mock.call_args[0][0]['seller_id'] == 'lojatop'
        assert mock.call_args[0][0]['account_name'] == 'MC-lojatop'  # noqa
        assert mock.called
        assert response

    def test_rebuild_should_call_marvin_with_other_platform(
        self,
        rebuild,
        mock_register_google
    ):
        action = {'update'}

        data = {
            'integration_info': {
                'erp': 'Api',
                'platform': 'coop'
            },
            'seller_external_id': 'c93208429b214caa8270c9d4ae6f614c',
            'id': 'lojatop'
        }

        with mock_register_google as mock:
            response = rebuild._rebuild(action, data)

        assert mock.called
        assert response

    def test_rebuild_should_not_call_marvin_when_no_integration(
        self,
        rebuild,
        mock_register_google
    ):
        action = {}
        data = {}

        with mock_register_google as mock:
            response = rebuild._rebuild(action, data)

        assert not mock.called
        assert response

    def test_rebuild_should_not_plataform_ipdv(
        self,
        rebuild,
        mock_register_google
    ):
        action = {'update'}

        data = {
            'integration_info': None,
            'seller_external_id': 'c93208429b214caa8270c9d4ae6f614c',
            'id': 'lojatop'
        }

        with mock_register_google as mock:
            response = rebuild._rebuild(action, data)

        assert not mock.called
        assert response
