import logging

import falcon
from simple_settings import settings

from taz.api.common.exceptions import BadRequest, NotFound
from taz.api.common.handlers.base import BaseHandler

from .models import ScoreCriteriaModel

logger = logging.getLogger(__name__)


class ScoreCriteriaHandler(BaseHandler):

    def on_get(self, request, response, entity_name):
        payload = ScoreCriteriaModel.objects(
            entity_name=entity_name,
            score_version=settings.SCORE_VERSION
        ).first()

        if not payload:
            raise NotFound(
                message='Criteria entity_name:{} not found'.format(entity_name)
            )

        self.write_response(response, falcon.HTTP_200, payload.to_json())

    def on_post(self, request, response):
        payload = request.context or {}

        if not payload:
            raise BadRequest(message='Invalid payload')

        payload['score_version'] = settings.SCORE_VERSION

        ScoreCriteriaModel.objects(
            entity_name=payload['entity_name'],
            score_version=payload['score_version']
        ).update(**payload, upsert=True)

        logger.info('Save criteria with payload:{}'.format(payload))
        self.write_response(response, falcon.HTTP_200, payload)

    def on_delete(self, request, response, entity_name):
        payload = ScoreCriteriaModel.objects(
            entity_name=entity_name,
            score_version=settings.SCORE_VERSION
        ).first()

        if not payload:
            raise NotFound(
                message='Criteria entity_name:{} not found'.format(entity_name)
            )

        payload.delete()

        logger.info('Delete criteria entity_name:{}'.format(entity_name))
        self.write_response(response, falcon.HTTP_204)


class ScoreCriteriaListHandler(BaseHandler):

    def on_get(self, request, response):
        payload = ScoreCriteriaModel.objects()

        self.write_response(response, falcon.HTTP_200, payload.to_json())
