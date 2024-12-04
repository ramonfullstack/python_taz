import collections

import pytest

from taz.api.common.exceptions import MethodNotAllowed
from taz.api.middlewares.authorization_owner import AuthOwner


class TestAuthorizationOwner:

    @pytest.fixture
    def mock_request(self):
        Mock_request = collections.namedtuple('Mock_request', ['token_owner'])
        return Mock_request(token_owner='TazApi')

    def test_authorization_should_allow(self, mock_request):
        @AuthOwner(['TazApi'])
        def to_be_allowed(handler_object, request, *args, **kwargs):
            assert handler_object is self
            assert request.token_owner == 'TazApi'
            return 'allowed'

        assert to_be_allowed(self, mock_request) == 'allowed'

    def test_authorization_should_not_allow(self, mock_request):
        @AuthOwner(['another_owner'])
        def to_be_not_allowed(handler_object, request, *args, **kwargs):
            pass

        with pytest.raises(MethodNotAllowed) as error:
            to_be_not_allowed(self, mock_request)

        assert error.value.code == 405
