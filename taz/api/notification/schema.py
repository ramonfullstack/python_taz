from marshmallow import (
    INCLUDE,
    Schema,
    ValidationError,
    fields,
    validates_schema
)

from taz.constants import SOURCE_DATASHEET


class NotificationSchema(Schema):
    seller_id = fields.String(required=True)
    sku = fields.String(required=True)

    @validates_schema
    def validate(self, data, **kwargs):
        if (
                data.get('source', '') == SOURCE_DATASHEET and
                str(data['identifier']) != ''
        ):
            try:
                int(data['identifier'])
            except ValueError:
                raise ValidationError('Invalid identifier')

    class Meta:
        unknown = INCLUDE
