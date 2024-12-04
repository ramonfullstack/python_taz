import logging

import falcon
from redis import Redis
from simple_settings import settings

from taz.api.common.handlers.base import BaseHandler

logger = logging.getLogger(__name__)


class RedisPollerHandler(BaseHandler):

    def __init__(self):
        self.cache = Redis(
            host=settings.REDIS_SETTINGS['host'],
            port=settings.REDIS_SETTINGS['port'],
            password=settings.REDIS_SETTINGS.get('password')
        )

    def on_get(self, request, response, key):
        payload = self.cache.get(key) or {}

        logger.info(
            'Get poller redis for key:{key} and payload:{payload}'.format(
                key=key,
                payload=payload
            )
        )

        self.write_response(response, falcon.HTTP_200, payload)

    def on_delete(self, request, response, key):
        self.cache.delete(key)

        logger.info('Delete poller redis for key:{key}'.format(key=key))

        self.write_response(response, falcon.HTTP_204)
