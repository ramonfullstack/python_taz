from marshmallow import EXCLUDE, Schema, fields
from marshmallow.validate import Range


class MinimumOrderQuantity(Schema):
    value = fields.Integer(
        required=True,
        validate=Range(min=2, error='O campo value precisa ser maior que 1')
    )
    user = fields.String(required=True)

    class Meta:
        unknown = EXCLUDE
