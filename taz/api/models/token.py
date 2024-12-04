import random
import string
import uuid

from mongoengine import Document, StringField, UUIDField
from simple_settings import settings


class TokenModel(Document):
    _id = UUIDField('id')
    owner = StringField(max_length=50, required=True)
    token = StringField(max_length=30, required=True, unique=True)

    meta = {'collection': 'tokens'}

    def save(self, *args, **kwargs):
        if not self._id:
            self._id = str(uuid.uuid4())

        return super(TokenModel, self).save(*args, **kwargs)

    @classmethod
    def generate(cls, owner, token=None):
        return TokenModel(
            owner=owner, token=token or cls.create_token()
        ).save()

    @classmethod
    def create_token(cls):
        return ''.join(
            [
                random.choice(string.ascii_letters + string.digits)
                for _ in range(settings.TOKEN_LENGTH)
            ]
        )
