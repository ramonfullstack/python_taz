from marshmallow import Schema, fields


class CompleteProductSchema(Schema):
    sku = fields.String(required=True)
    seller_id = fields.String(required=True)
    action = fields.String(required=True)
