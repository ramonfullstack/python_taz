from enum import Enum

from marshmallow import Schema, ValidationError, fields, validate, validates
from simple_settings import settings

FIELDS_ENABLED_INPUT = (
    '_id',
    'product_type',
    'operation',
    'price',
    'to',
    'user'
)


class ClassificationsRulesStatus(Enum):
    created: str = 'created'
    updated: str = 'updated'
    deleted: str = 'deleted'
    applied: str = 'applied'


class ClassificationsRulesOperation(Enum):
    MENOR_IGUAL: str = 'MENOR_IGUAL'
    MAIOR_IGUAL: str = 'MAIOR_IGUAL'


class ClassificationsRulesTo(Schema):
    product_type = fields.String(required=True)
    category_id = fields.String(required=True)
    subcategory_ids = fields.List(
        fields.String(),
        required=True,
        validate=[validate.Length(min=1)]
    )


class ClassificationsRules(Schema):
    _id = fields.UUID(data_key='id')
    product_type = fields.String(required=True)
    operation = fields.Enum(
        enum=ClassificationsRulesOperation,
        required=True,
        by_value=True
    )
    price = fields.Float(required=True)
    to = fields.Nested(ClassificationsRulesTo, required=True)
    active = fields.Bool(required=True)
    user = fields.String(required=True)
    status = fields.Enum(
        enum=ClassificationsRulesStatus,
        required=True,
        by_value=True
    )
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=False)

    @validates('product_type')
    def validate_is_book(self, product_type: str):
        if product_type in settings.BLOCKED_PRODUCT_TYPES_CLASSIFICATIONS_RULES:  # noqa
            raise ValidationError(
                f'product_type:{product_type} is not valid.', ['product_type']
            )
