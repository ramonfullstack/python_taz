import logging

import falcon
from simple_settings import settings

from taz.api.common.exceptions import BadRequest, NotFound
from taz.api.common.handlers.base import BaseHandler

from .models import ScoreWeightModel

logger = logging.getLogger(__name__)


class ScoreWeightHandler(BaseHandler):

    def on_get(self, request, response, entity_name, criteria_name):
        payload = ScoreWeightModel.objects(
            entity_name=entity_name,
            criteria_name=criteria_name,
            score_version=settings.SCORE_VERSION
        ).first()

        if not payload:
            raise NotFound(message=(
                'Score weight entity:{entity_name} criteria:{criteria_name} '
                'not found'
            ).format(
                entity_name=entity_name,
                criteria_name=criteria_name
            ))

        self.write_response(response, falcon.HTTP_200, payload.to_json())

    def on_post(self, request, response):
        payload = request.context or {}

        if not payload:
            raise BadRequest(message='Invalid payload')

        payload['score_version'] = settings.SCORE_VERSION

        score_weight = ScoreWeightModel.objects(
            entity_name=payload['entity_name'],
            criteria_name=payload['criteria_name'],
            score_version=payload['score_version']
        )

        if score_weight:
            score_weight.delete()

        ScoreWeightModel(**payload).save()

        logger.info('Save score weight with payload:{}'.format(payload))
        self.write_response(response, falcon.HTTP_200, payload)

    def on_delete(self, request, response, entity_name, criteria_name):
        payload = ScoreWeightModel.objects(
            entity_name=entity_name,
            criteria_name=criteria_name,
            score_version=settings.SCORE_VERSION
        ).first()

        if not payload:
            raise NotFound(message=(
                'Score weight entity:{entity_name} criteria:{criteria_name} '
                'not found'
            ).format(
                entity_name=entity_name,
                criteria_name=criteria_name
            ))

        payload.delete()

        logger.info(
            'Delete score weight entity:{entity_name} '
            'criteria:{criteria_name}'.format(
                entity_name=entity_name,
                criteria_name=criteria_name
            )
        )

        self.write_response(response, falcon.HTTP_204)


class ScoreWeightListHandler(BaseHandler):

    def on_get(self, request, response):
        payload = ScoreWeightModel.objects()

        self.write_response(response, falcon.HTTP_200, payload.to_json())
