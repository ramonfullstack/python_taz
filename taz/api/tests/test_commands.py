from taz.api.commands import TokenCommand
from taz.api.models.token import TokenModel


class TestTokenCommand:

    def test_create_token_command(self):
        TokenCommand(owner='Test Murhco').create_token()

        assert TokenModel.objects.count() == 1

    def test_create_token_command_with_specific_token(self):
        TokenCommand(owner='Test Murhco', token='murcho').create_token()

        assert TokenModel.objects.count() == 1
