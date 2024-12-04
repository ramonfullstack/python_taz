import logging

import falcon

from taz.api.common.exceptions import BadRequest
from taz.api.common.handlers.base import BaseHandler

from .models import BlacklistModel

logger = logging.getLogger(__name__)


class BlacklistHandler(BaseHandler):
    def on_post(self, request, response):
        payload = request.context or {}

        if not payload or not payload.get('term') or not payload.get('field'):
            raise BadRequest(message='Invalid payload')

        BlacklistModel(**payload).save()

        logger.info('Save blacklist with payload:{}'.format(payload))

        self.write_response(response, falcon.HTTP_200, payload)

    def on_delete(self, request, response):
        payload = request.context or {}

        if not payload or not payload.get('term') or not payload.get('field'):
            raise BadRequest(message='Invalid payload')

        BlacklistModel.objects(
            term=payload['term'],
            field=payload['field']
        ).delete()

        self.write_response(response, falcon.HTTP_204)


class BlacklistListHandler(BaseHandler):

    def on_get(self, request, response):
        payload = BlacklistModel.objects()
        self.write_response(response, falcon.HTTP_200, payload.to_json())
