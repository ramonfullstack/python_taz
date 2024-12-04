from marshmallow import Schema, fields


class MatchingSchema(Schema):
    task_id = fields.String(required=True)
    seller_id = fields.String(required=True)
    sku = fields.String(required=True)
