from functools import cached_property
from typing import Dict, List, Optional

from maaslogger import base_logger
from marshmallow import EXCLUDE, Schema, fields
from marshmallow.exceptions import ValidationError
from simple_settings import settings

from taz.constants import MAGAZINE_LUIZA_SELLER_ID, UPDATE_ACTION
from taz.consumers.core.brokers.stream import (
    PubSubBroker,
    PubSubRecordProcessor
)
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.notification import Notification

logger = base_logger.get_logger(__name__)


class LabelMessageSchema(Schema):

    seller_id = fields.String(required=True)
    sku = fields.String(required=True)
    navigation_id = fields.String(required=True)
    label = fields.String(required=True)
    in_out = fields.String(required=True)
    rules_version = fields.String(required=True)

    def _check_is_empty(self, message):
        for field_key, field_value in message.items():

            if not field_value.strip():
                raise ValidationError(f'Required fields is empty:{field_key}')

    def validate(self, message: Dict):
        self._check_is_empty(message)
        errors = super().validate(message)
        if errors:
            raise ValidationError(f'Errors in fields:{errors}')


class LabelProcessor(PubSubRecordProcessor, MongodbMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @cached_property
    def raw_products(self):
        return self.get_collection('raw_products')

    @cached_property
    def notification(self):
        return Notification()

    @cached_property
    def schema(self):
        return LabelMessageSchema(unknown=EXCLUDE)

    def process_message(self, message: Dict):
        logger.debug(f'Processing label with payload:{message}')
        try:
            self.schema.validate(message)
        except ValidationError as error:
            logger.error(
                f'Error to validate payload:{message} error:{error}',
                detail={
                    "error": error
                }
            )
            return True

        seller_id, sku, navigation_id, label, in_out = (
            message['seller_id'],
            message['sku'],
            message['navigation_id'],
            message['label'],
            message['in_out']
        )

        if seller_id != MAGAZINE_LUIZA_SELLER_ID:
            logger.info(
                f'Skipped message:{message} because the seller '
                'is not magazineluiza',
                detail={
                    "message": message
                }
            )
            return True

        raw_products = self._get_product(seller_id, sku, navigation_id)
        if not raw_products:
            logger.warning(
                f'Product seller_id:{seller_id} sku:{sku} '
                f'navigation_id:{navigation_id} not found',
                detail={
                    "sku": sku,
                    "seller_id": seller_id,
                    "navigation_id": navigation_id,
                }
            )
            return True

        seller_id, sku, navigation_id = (
            raw_products['seller_id'],
            raw_products['sku'],
            raw_products['navigation_id']
        )
        extra_data = self.__is_different_data(raw_products, label, in_out)
        has_changed = True
        if extra_data is None:
            has_changed = False
        else:
            criteria = {'seller_id': seller_id, 'sku': sku}
            if extra_data:
                result = self.raw_products.update_many(
                    criteria,
                    {'$set': {'extra_data': extra_data}}
                )
            else:
                result = self.raw_products.update_many(
                    criteria,
                    {'$unset': {'extra_data': ''}}
                )

            has_changed = (result.modified_count > 0)
            if has_changed:
                payload = {
                    'sku': sku,
                    'seller_id': seller_id,
                    'navigation_id': navigation_id
                }
                self.notification.put(payload, 'product', UPDATE_ACTION)

        logger.info(
            f'Successfully processed message scope:{self.scope} for product '
            f'seller_id:{seller_id} sku:{sku} navigation_id:{navigation_id} '
            f'label:{label} action:{in_out} with changes:{has_changed}',
            detail={
                "sku": sku,
                "seller_id": seller_id,
                "navigation_id": navigation_id,
                "scope": self.scope,
                "label": label,
                "has_changed": has_changed,
                "in_out": in_out
            }
        )
        return True

    def __is_different_data(
        self,
        raw_products: dict,
        label: str,
        in_out: str
    ) -> Optional[List]:
        old_extra_data = raw_products.get('extra_data') or []
        extra_data = [
            item for item in old_extra_data
            if item['name'] != label
        ]

        if in_out == 'in':
            extra_data.append({'name': label, 'value': 'true'})

        return (
            extra_data
            if len(extra_data) != len(old_extra_data)
            else None
        )

    def _get_product(
        self,
        seller_id: str,
        sku: str,
        navigation_id: str
    ) -> Optional[Dict]:
        fields = {
            '_id': 0,
            'seller_id': 1,
            'sku': 1,
            'navigation_id': 1,
            'extra_data': 1
        }
        raw_products = self.raw_products.find_one(
            {'sku': sku, 'seller_id': seller_id},
            fields
        )
        if not raw_products:
            raw_products = self.raw_products.find_one(
                {'navigation_id': navigation_id},
                fields
            )
        return raw_products


class LabelConsumer(PubSubBroker):
    project_name = settings.GOOGLE_PROJECT_ID
    scope = 'label'
    record_processor_class = LabelProcessor
