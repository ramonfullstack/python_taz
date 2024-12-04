import logging
from functools import cached_property
from typing import Optional

import falcon
from marshmallow.exceptions import ValidationError
from simple_settings import settings

from taz.api.common.exceptions import BadRequest, NotFoundWithMessage
from taz.api.common.handlers.base import BaseHandler
from taz.api.notification.schema import NotificationSchema
from taz.constants import SOURCE_DATASHEET
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.google.storage import StorageManager
from taz.consumers.core.google.stream import StreamPublisherManager
from taz.core.cache.layers import RedisCache
from taz.helpers.json import json_dumps

logger = logging.getLogger(__name__)


class NotificationHandler(BaseHandler, MongodbMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pubsub = StreamPublisherManager()

    @cached_property
    def data_storage(self):
        return StorageManager(settings.METADATA_INPUT_BUCKET)

    @cached_property
    def cache(self):
        return RedisCache(
            key_pattern=settings.DATASHEET_NOTFOUND_KEY_PATTERN,
            ttl=int(settings.EXPIRES_DATASHEET_NOTFOUND_KEY_PATTERN),
            host=settings.REDIS_SETTINGS['host'],
            port=settings.REDIS_SETTINGS['port'],
            password=settings.REDIS_SETTINGS.get('password')
        )

    @cached_property
    def schema(self) -> NotificationSchema:
        return NotificationSchema()

    def get_metadata(self, source: str, identifier: str) -> Optional[dict]:
        file_name = f'{source}/{identifier}.json'
        return self.data_storage.get_blob_with_hash(file_name)

    def on_post(self, request, response, source):
        payload = request.context or {}
        payload.update({'source': source})

        try:
            payload = self.schema.load(payload)
        except ValidationError as ex:
            errors: str = json_dumps(ex.messages)
            raise BadRequest(message=errors)

        if source == SOURCE_DATASHEET:
            identifier = payload.get('identifier')
            if not self.cache.get(identifier):
                if not self.get_metadata(SOURCE_DATASHEET, identifier):
                    raise NotFoundWithMessage(message='Datasheet not found')
                self.cache.set(identifier, True)

        logger.info(f'Send request to notification with {payload}')
        self.pubsub.publish(
            content=payload,
            project_id=settings.GOOGLE_PROJECT_ID,
            topic_name=settings.PUBSUB_NOTIFICATION_TOPIC_NAME,
        )
        self.write_response(response, falcon.HTTP_200)
