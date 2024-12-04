import requests
from maaslogger import base_logger
from simple_settings import settings

from taz.helpers.json import json_dumps

logger = base_logger.get_logger(__name__)


class MarvinRequest:

    def post(self, payload):
        return self._fetch('post', payload)

    def _fetch(self, method, payload):
        request_method = getattr(requests, method)

        url = '{endpoint}/register/google/'.format(
            endpoint=settings.APIS['marvin']['url'],
        )

        request_args = {
            'headers': {'Content-type': 'application/json'},
        }

        if payload:
            request_args['data'] = json_dumps(payload)

        response = request_method(url, **request_args)
        response.raise_for_status()

        logger.info(
            'Call to Marvin was successful with payload:{payload}'.format(
                payload=payload,
            )
        )

        try:
            content = response.json()
        except Exception:
            content = response.content.decode('utf-8')
        return content
