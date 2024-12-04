from typing import Dict, Generator
from unittest.mock import Mock

import pytest

from taz.consumers.core.exceptions import NotFound
from taz.consumers.metadata_input.scopes.metabooks import Scope


class TestMetabooksScope:

    @pytest.fixture
    def scope(self) -> Scope:
        return Scope()

    def test_metabooks_scope_return_payload(
        self,
        scope: Scope,
        metabooks_identified: str,
        metabooks_payload: Dict,
        patch_requests_get: Mock
    ):
        with patch_requests_get as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = metabooks_payload
            mock_get.return_value = mock_response

            payload = scope.process(metabooks_identified)

        assert payload
        assert payload == metabooks_payload

    def test_metabooks_scope_raise_not_found(
        self,
        scope: Scope,
        patch_requests_get: Mock,
        caplog: Generator
    ):
        with patch_requests_get as mock_get:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_get.return_value = mock_response
            with pytest.raises(NotFound):
                scope.process('12345')

    def test_metabooks_scope_raise_for_status(
        self,
        scope: Scope,
        metabooks_identified: str,
        patch_requests_get: Mock
    ):
        with patch_requests_get as mock_get:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_response.raise_for_status.side_effect = Exception
            mock_get.return_value = mock_response
            with pytest.raises(Exception):
                scope.process(metabooks_identified)
