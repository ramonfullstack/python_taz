from typing import Dict, Generator
from unittest.mock import Mock

import pytest

from taz.consumers.core.exceptions import NotFound
from taz.consumers.metadata_input.scopes.smartcontent import Scope


class TestSmartContentScope:

    @pytest.fixture
    def scope(self) -> Scope:
        return Scope()

    def test_smartcontent_scope_return_payload(
        self,
        scope: Scope,
        smartcontent_identified: str,
        smartcontent_payload: Dict,
        patch_requests_get: Mock
    ):
        with patch_requests_get as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'data': smartcontent_payload
            }
            mock_get.return_value = mock_response
            payload = scope.process(smartcontent_identified)

        assert payload == smartcontent_payload

    def test_smartcontent_scope_raise_not_found(
        self,
        scope: Scope,
        patch_requests_get: Mock,
        caplog: Generator
    ):
        with pytest.raises(NotFound):
            with patch_requests_get as mock_get:
                mock_response = Mock()
                mock_response.status_code = 404
                mock_get.return_value = mock_response
                scope.process('12345')

    def test_smartcontent_scope_raise_for_status(
        self,
        scope: Scope,
        smartcontent_identified: str,
        patch_requests_get: Mock
    ):
        with pytest.raises(Exception):
            with patch_requests_get as mock_get:
                mock_response = Mock()
                mock_response.status_code = 500
                mock_response.raise_for_status.side_effect = Exception
                mock_get.return_value = mock_response
                scope.process(smartcontent_identified)
