import requests
from maaslogger import base_logger
from simple_settings import settings

from taz.helpers.json import json_dumps

logger = base_logger.get_logger(__name__)


class FrajolaRequest:

    def put(self, product_id, payload):
        return self._fetch('put', product_id, payload)

    def get(self, product_id):
        return self._fetch('get', product_id)

    def _fetch(self, method, product_id, payload=None):
        request_method = getattr(requests, method)

        url = self._get_url(product_id)

        request_args = {
            'headers': {'Content-type': 'application/json'},
            'timeout': settings.APIS['frajola']['timeout']
        }

        if payload:
            request_args['data'] = json_dumps(payload)

        try:
            response = request_method(url, **request_args)
            response.raise_for_status()

            logger.info(
                'Call to the Frajola successfully with id:{product_id} '
                'payload:{payload} request_args:{request_args}'.format(
                    payload=payload,
                    product_id=product_id,
                    request_args=request_args
                )
            )

            try:
                content = response.json()
            except Exception:
                content = response.content.decode('utf-8')

            return content
        except Exception as e:
            if e.response.status_code == 404:
                logger.warning(
                    'Product {} not found on Frajola'.format(product_id)
                )
                return

            logger.error(
                'Error to call Frajola with id:{product_id} payload:{payload} '
                'error:{error}'.format(
                    payload=payload,
                    error=e,
                    product_id=product_id
                )
            )

            raise

    def _get_url(self, product_id):
        return '{endpoint}/product/{product_id}/?token={token}'.format(
            endpoint=settings.APIS['frajola']['url'],
            product_id=product_id,
            token=settings.APIS['frajola']['token']
        )
