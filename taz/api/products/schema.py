from marshmallow import Schema, fields, validate
from marshmallow.exceptions import ValidationError
from marshmallow.fields import Boolean, Integer, List, String
from simple_settings import settings


class ListProductsSchema(Schema):
    matching_uuid = String(allow_none=True)
    navigation_id = String(allow_none=True)
    identifier_type = String(allow_none=True)
    identifier_value = String(allow_none=True)
    disable_on_matching = Boolean(allow_none=True)
    fields = List(String)
    _limit = Integer(allow_none=True)
    _offset = Integer(allow_none=True)

    def validate(self, message):
        self._validate_query_string(message)
        self._validate_identifier_type(message['identifier_type'])

    @staticmethod
    def _validate_identifier_type(identifier_type):
        if identifier_type and identifier_type not in ['ean', 'isbn']:
            raise ValidationError(
                'Type of identifier invalid:{}'.format(
                    identifier_type
                )
            )

    @staticmethod
    def _validate_query_string(message):
        if not ((
            message.get('identifier_type') and
            message.get('identifier_value')
        ) or message.get('matching_uuid') or message.get('navigation_id')):
            raise ValidationError('Request without a valid query string')


class ExtraDataField(Schema):
    name = String(required=True)
    value = fields.String(validate=validate.Length(max=50))


class ProductExtraDataSchema(Schema):
    seller_id = String(required=True)
    sku = String(required=True)
    extra_data = fields.List(
        fields.Nested(ExtraDataField),
        required=True,
        validate=validate.Length(max=settings.KEY_LIMIT_ON_EXTRA_DATA)
    )
