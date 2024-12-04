import pytest
from mongoengine.errors import NotUniqueError

from taz.api.models.token import TokenModel


class TestTokenModel:

    def test_should_raise_not_unique_error_for_duplicated_token(self):
        token = TokenModel.generate(owner='Chuck Norris')

        with pytest.raises(NotUniqueError) as e:
            TokenModel(owner='Darth Vader', token=token.token).save()

        assert e.typename == 'NotUniqueError'

    def test_create_a_specific_token(self):
        token_str = TokenModel().create_token()
        TokenModel.generate(owner='Chuck Norris', token=token_str)

        token = TokenModel.objects.get(token=token_str)
        assert token.token == token_str
