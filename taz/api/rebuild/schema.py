from marshmallow import Schema, fields, validate
from marshmallow.exceptions import ValidationError
from simple_settings import settings

from taz.constants import (
    CREATE_ACTION,
    DELETE_ACTION,
    SOURCE_DATASHEET,
    SOURCE_GENERIC_CONTENT,
    SOURCE_HECTOR,
    SOURCE_METABOOKS,
    SOURCE_OMNILOGIC,
    SOURCE_RECLASSIFICATION_PRICE_RULE,
    SOURCE_SMARTCONTENT,
    SOURCE_WAKKO,
    UPDATE_ACTION
)


class CatalogNotificationSchema(Schema):

    NOTIFICATION_TYPES = (
        'product',
        'price',
        'product_score',
        'enriched_product',
        'matching',
        'checkout_price',
        'metadata_verify',
        'factsheet',
        'reviews',
        'matching_product'
    )

    ACTION_TYPES = (
        CREATE_ACTION,
        UPDATE_ACTION,
        DELETE_ACTION
    )

    type = fields.String(required=True)
    sku = fields.String(required=False)
    seller_id = fields.String(required=False)
    navigation_id = fields.String(required=False)
    action = fields.String(required=True)

    def validate(self, message):
        self._validate_required_fields(message)
        self._validate_notification_type(message['type'])
        self._validate_action_type(message['action'])
        self._validate_notification_product_fields(
            sku=message.get('sku'),
            seller_id=message.get('seller_id'),
            navigation_id=message.get('navigation_id'),
        )

    def _validate_required_fields(self, message):
        errors = super().validate(message)

        if errors:
            raise ValidationError(f'Missing fields:{errors}')

    def _validate_notification_product_fields(
        self,
        sku,
        seller_id,
        navigation_id
    ):

        if not navigation_id and (
            not sku or not seller_id
        ):
            raise ValidationError(
                'Notification must have at least: '
                'navigation_id or seller_id, sku informed '
                f'sku:{sku} seller_id:{seller_id} '
                f'navigation_id:{navigation_id}'
            )

    def _validate_notification_type(self, type):
        if type not in self.NOTIFICATION_TYPES:
            raise ValidationError(
                f'Invalid notification type:{type}'
            )

    def _validate_action_type(self, action):
        if action not in self.ACTION_TYPES:
            raise ValidationError(f'Invalid action type:{action}')


class RebuildDatalakeSchema(Schema):

    NOTIFICATION_TYPES = (
        'product',
        'enriched_product',
        'badge',
        'product_score',
        'price',
        'stock',
        'media',
        'score',
        'factsheet',
        'metadata_verify'
    )

    ACTION_TYPES = (
        CREATE_ACTION,
        UPDATE_ACTION,
        DELETE_ACTION
    )

    SOURCE_TYPES = (
        SOURCE_OMNILOGIC,
        SOURCE_WAKKO,
        SOURCE_DATASHEET,
        SOURCE_HECTOR,
        SOURCE_RECLASSIFICATION_PRICE_RULE,
        SOURCE_GENERIC_CONTENT,
        SOURCE_METABOOKS,
        SOURCE_SMARTCONTENT
    )

    type = fields.String(required=True)
    sku = fields.String(required=True)
    seller_id = fields.String(required=True)
    navigation_id = fields.String(required=True)
    action = fields.String(required=True)
    source = fields.String(required=False)

    def validate(self, message):
        self._validate_required_fields(message)
        self._validate_notification_type(message['type'])
        self._validate_action_type(message['action'])
        source = message.get('source')
        self._validate_source_type(source)

    def _validate_required_fields(self, message):
        errors = super().validate(message)

        if errors:
            raise ValidationError(
                f'Missing fields:{errors}'
            )

    def _validate_notification_type(self, type):
        if type not in self.NOTIFICATION_TYPES:
            raise ValidationError(
                f'Invalid notification type:{type}'
            )

    def _validate_action_type(self, action):
        if action not in self.ACTION_TYPES:
            raise ValidationError(
                f'Invalid action type:{action}'
            )

    def _validate_source_type(self, source):
        if source is not None and source not in self.SOURCE_TYPES:
            raise ValidationError(
                f'Invalid source type:{source}'
            )


class RebuildMediaSchema(Schema):
    sku = fields.String(
        required=True,
        validate=[validate.Length(min=1)]
    )
    seller_id = fields.String(
        required=True,
        validate=[validate.Length(min=1)]
    )
    from_bucket = fields.Boolean(
        required=False,
    )

    def validate(self, message):
        self._validate_required_fields(message)

    def _validate_required_fields(self, message):
        errors = super().validate(message)

        if errors:
            raise ValidationError(
                f'Missing fields:{errors}'
            )


class RebuilPriceRulesSchema(Schema):
    sku = fields.String(required=True)
    seller_id = fields.String(required=True)
    navigation_id = fields.String(required=True)

    def validate(self, message):
        self._validate_required_fields(message)

    def _validate_required_fields(self, message):
        errors = super().validate(message)

        if errors:
            raise ValidationError(
                f'Missing fields:{errors}'
            )


class RebuildProductExporterSchema(Schema):
    seller_id = fields.String(required=True)
    sku = fields.String(required=True)
    type = fields.String()

    def validate(self, message):
        self.validate_type(message['type'])
        self._validate_required_fields(message)

    def validate_type(self, type):
        if type not in settings.PRODUCT_EXPORTER_SCOPES:
            raise ValidationError(
                f'Type {type} does not exist'
            )

    def _validate_required_fields(self, message):
        errors = super().validate(message)

        if errors:
            raise ValidationError(
                f'Missing fields:{errors}'
            )
