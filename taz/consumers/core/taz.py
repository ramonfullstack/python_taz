import requests
from maaslogger import base_logger
from simple_settings import settings

from taz.helpers.json import json_dumps

logger = base_logger.get_logger(__name__)


class TazRequest:

    request_args = {
        'headers': {
            'Content-type': 'application/json',
            'Authorization': settings.APIS['taz']['token']
        },
        'timeout': settings.APIS['taz']['timeout']
    }

    def delete_enriched_product(self, seller_id, sku, source):
        method = 'delete'
        url = '{url}/enriched_product/sku/{sku}/seller/{seller_id}/source/{source}'.format( # noqa
            url=settings.APIS['taz']['url'],
            sku=sku,
            seller_id=seller_id,
            source=source,
        )
        return self._fetch(method, url)

    def post_notification(self, source, payload):
        method = 'post'
        url = '{url}/notification/{source}'.format(
            url=settings.APIS['taz']['url'],
            source=source,
        )
        return self._fetch(method, url, payload)

    def _fetch(self, method, url, payload=None):
        request_method = getattr(requests, method)

        if payload:
            self.request_args['data'] = json_dumps(payload)

        try:
            response = request_method(url, **self.request_args)
            response.raise_for_status()

            logger.info(
                f'Call to the Taz successfully with url:{url} '
                f'payload:{payload}'
            )

            try:
                content = response.json()
            except Exception:
                content = response.content.decode('utf-8')

            return content
        except Exception as e:
            if e.response.status_code == 404:
                logger.warning(
                    f'URL {url} not found on Taz'
                )
                return

            logger.error(
                f'Error to call Taz with url:{url} payload:{payload} error:{e}'
            )

            raise
