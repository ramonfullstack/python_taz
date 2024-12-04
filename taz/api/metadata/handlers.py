import logging
from functools import cached_property

import falcon
from simple_settings import settings

from taz.api.common.exceptions import BadRequest
from taz.api.common.handlers.base import BaseHandler
from taz.api.common.utils import parse_base64_to_dict
from taz.consumers.core.google.stream import StreamPublisherManager

logger = logging.getLogger(__name__)


class MetadataInputHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @cached_property
    def pubsub(self):
        return StreamPublisherManager()

    def on_post(self, request, response):
        payload = request.context or {}

        if not payload:
            raise BadRequest(
                f'Invalid parameters for payload:{request.context}'
            )

        if payload.get('message'):
            payload = parse_base64_to_dict(payload['message']['data'])

        logger.info(f'Send request to metadata input with {payload}')

        self.pubsub.publish(
            topic_name=settings.PUBSUB_METADATA_INPUT_TOPIC_NAME,
            project_id=settings.GOOGLE_PROJECT_ID,
            content=payload
        )

        self.write_response(response, falcon.HTTP_200, payload)
