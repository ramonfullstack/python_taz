import logging
from datetime import datetime
from functools import cached_property
from typing import Dict, List
from uuid import uuid4

import falcon
from marshmallow import EXCLUDE
from marshmallow.exceptions import ValidationError
from pymongo.collection import Collection
from pymongo.results import UpdateResult
from simple_settings import settings

from taz.api.classifications_rules.schemas import (
    FIELDS_ENABLED_INPUT,
    ClassificationsRules,
    ClassificationsRulesStatus
)
from taz.api.common.exceptions import BadRequest
from taz.api.common.handlers.base import BaseHandler
from taz.api.middlewares.authorization_owner import AuthOwner
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.helpers.json import json_dumps

logger = logging.getLogger(__name__)


def get_current_datetime() -> datetime:
    return datetime.now()


class ClassificationsRulesHandler(BaseHandler, MongodbMixin):

    @cached_property
    def schema(self) -> ClassificationsRules:
        return ClassificationsRules(only=FIELDS_ENABLED_INPUT, unknown=EXCLUDE)

    @cached_property
    def classifications_rules(self) -> Collection:
        return self.get_collection('classifications_rules')

    def on_get(self, request: falcon.Request, response: falcon.Response):
        classifications_rules: List[Dict] = list(
            self.classifications_rules.find({'active': True})
        )
        for rule in classifications_rules:
            rule['id'] = rule.pop('_id')

        self.write_response(
            response,
            falcon.HTTP_200,
            {'data': classifications_rules}
        )

    @AuthOwner(
        allowed_owners=settings.ALLOWED_OWNERS_WRITE_CLASSIFICATIONS_RULES
    )
    def on_post(self, request: falcon.Request, response: falcon.Response):
        payload: Dict = request.context or {}

        try:
            payload = self.schema.load(payload)
            payload['operation'] = payload['operation'].value
        except ValidationError as ex:
            errors: str = json_dumps(ex.messages)
            logger.error(
                f'Failed create classification rule with '
                f'payload:{json_dumps(payload)} '
                f'errors:{errors}'
            )
            raise BadRequest(message=errors)

        classification_rule: Dict = self.classifications_rules.find_one({
            'product_type': payload['product_type'],
            'operation': payload['operation']
        }) or {}

        if classification_rule.get('active'):
            raise BadRequest(
                message='There is already a classification rule for '
                'product type {} and operation {}'.format(
                    payload['product_type'],
                    payload['operation']
                )
            )

        classification_rule.update({
            **payload,
            '_id': classification_rule.get('_id', str(uuid4())),
            'active': True,
            'created_at': get_current_datetime(),
            'status': ClassificationsRulesStatus.created.value
        })

        logger.info(
            f'Save classification rule with payload:{classification_rule}'
        )
        self.classifications_rules.update_one(
            {
                'product_type': classification_rule['product_type'],
                'operation': classification_rule['operation']
            },
            {'$set': classification_rule},
            upsert=True
        )

        classification_rule['id'] = classification_rule.pop('_id')
        self.write_response(
            response,
            falcon.HTTP_201,
            classification_rule
        )

    @AuthOwner(
        allowed_owners=settings.ALLOWED_OWNERS_WRITE_CLASSIFICATIONS_RULES
    )
    def on_put(
        self,
        request: falcon.Request,
        response: falcon.Response,
    ):
        payload: Dict = request.context or {}

        try:
            payload = self.schema.load(payload)
            payload['operation'] = payload['operation'].value
        except ValidationError as ex:
            errors: str = json_dumps(ex.messages)
            logger.error(
                f'Failed update classification rule with '
                f'payload:{json_dumps(payload)} '
                f'errors:{errors}'
            )
            raise BadRequest(message=errors)

        id = str(payload.pop('_id', ''))
        classification_rule: Dict = self.classifications_rules.find_one({
            '_id': id,
        }) or {}

        if not classification_rule:
            return self.write_response(response, falcon.HTTP_404)

        payload.update({
            'active': True,
            'updated_at': get_current_datetime(),
            'status': ClassificationsRulesStatus.updated.value
        })

        classification_rule.update(payload)

        self.classifications_rules.update_one(
            {'_id': id},
            {'$set': classification_rule},
        )

        classification_rule['id'] = classification_rule.pop('_id')
        self.write_response(
            response,
            falcon.HTTP_OK,
            classification_rule
        )


class ClassificationsRulesByIdHandler(BaseHandler, MongodbMixin):

    @cached_property
    def classifications_rules(self) -> Collection:
        return self.get_collection('classifications_rules')

    @AuthOwner(
        allowed_owners=settings.ALLOWED_OWNERS_WRITE_CLASSIFICATIONS_RULES
    )
    def on_delete(
        self,
        request: falcon.Request,
        response: falcon.Response,
        id: str
    ):
        result: UpdateResult = self.classifications_rules.update_one(
            {'_id': id},
            {
                '$set': {
                    'status': ClassificationsRulesStatus.deleted.value,
                    'active': False,
                    'updated_at': get_current_datetime()
                }
            }
        )

        if result.modified_count == 0:
            raise BadRequest(message=f'Classification rule id:{id} not found')

        self.write_response(response, falcon.HTTP_200)

    def on_get(
        self,
        request: falcon.Request,
        response: falcon.Response,
        id: str
    ):
        classification_rule: Dict = self.classifications_rules.find_one({
            '_id': id
        }) or {}

        if not classification_rule:
            return self.write_response(response, falcon.HTTP_404)

        classification_rule['id'] = classification_rule.pop('_id')
        self.write_response(
            response,
            falcon.HTTP_200,
            {'data': classification_rule}
        )
