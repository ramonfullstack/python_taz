from datetime import timedelta
from functools import cached_property
from typing import Dict, Optional

import requests
from maaslogger import base_logger
from simple_settings import settings

from taz.constants import UPDATE_ACTION
from taz.consumers.core.google.stream import StreamPublisherManager
from taz.crontabs.store_pickup_checker.cache import APICacheController
from taz.http_status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED
)

logger = base_logger.get_logger(__name__)


class MaasProductHTTPClient(APICacheController):
    CACHE_KEY: str = 'maas-product-auth'
    TOKEN_TTL: timedelta = timedelta(seconds=1800)
    SETTINGS_API_KEY: str = 'maas-product'

    @cached_property
    def pubsub(self):
        return StreamPublisherManager()

    def reprocess(self, payload: dict) -> bool:
        seller_id, sku = payload['seller_id'], payload['sku']

        product = self._get_product_data(sku, seller_id)

        if not product:
            logger.warning(
                f'Error to receive product sku:{sku} '
                f'seller_id:{seller_id} from maas-product'
            )
        elif not product.get('datasheet'):
            self._send_factsheet_to_clean(sku, seller_id)

        return self.__send_product_to_reprocess(sku, seller_id)

    def _get_product_data(self, sku: str, seller_id: str) -> Optional[Dict]:
        url = '{endpoint}/api/v1/products/{sku}'.format(
            endpoint=settings.APIS[self.SETTINGS_API_KEY]['url'],
            sku=sku
        )
        max_retries = settings.APIS[self.SETTINGS_API_KEY]['max_retries']

        while max_retries > 0:
            try:
                response = requests.get(
                    url=url,
                    headers=self.__get_headers(seller_id, self.__get_token()),
                    timeout=settings.APIS[self.SETTINGS_API_KEY]['timeout']
                )

                logger.debug(
                    f'Request to maas-product endpoint:{url} '
                    f'returned status_code:{response.status_code}'
                )

                if response.status_code == HTTP_200_OK:
                    return response.json()
                elif response.status_code == HTTP_401_UNAUTHORIZED:
                    max_retries = (
                        max_retries - 1
                        if self.refresh_token()
                        else 0
                    )
                else:
                    response.raise_for_status()
            except Exception as e:
                logger.error(
                    f'Failed request maas-product endpoint:{url} for '
                    f'seller_id:{seller_id} sku:{sku} with error:{e}'
                )
                max_retries -= 1

    def __send_product_to_reprocess(self, sku: str, seller_id: str) -> bool:
        url = '{endpoint}/api/v1/admin/products/reprocess'.format(
            endpoint=settings.APIS[self.SETTINGS_API_KEY]['url'],
        )
        max_retries = settings.APIS[self.SETTINGS_API_KEY]['max_retries']

        while max_retries > 0:
            try:
                payload = self.__format_payload(sku)
                response = requests.post(
                    url=url,
                    headers=self.__get_headers(seller_id, self.__get_token()),
                    json=payload,
                    timeout=settings.APIS[self.SETTINGS_API_KEY]['timeout']
                )

                logger.debug(
                    f'Request to maas-product with payload:{payload} '
                    f'returned status_code:{response.status_code}'
                )

                if response.status_code == HTTP_401_UNAUTHORIZED:
                    max_retries = (
                        max_retries - 1
                        if self.refresh_token()
                        else 0
                    )
                elif response.status_code == HTTP_400_BAD_REQUEST:
                    max_retries = 0
                else:
                    response.raise_for_status()
                    return 200 <= response.status_code < 300
            except Exception as e:
                logger.error(
                    f'Failed request to maas-product endpoint:{url} for '
                    f'seller_id:{seller_id} sku:{sku} with error:{e}'
                )
                max_retries -= 1
        return False

    def _send_factsheet_to_clean(self, sku: str, seller_id: str) -> None:
        payload = {
            'sku': sku,
            'seller_id': seller_id,
            'items': []
        }
        message = {
            'action': UPDATE_ACTION,
            'data': payload
        }
        self.pubsub.publish(
            content=message,
            topic_name=settings.PUBSUB_FACTSHEET_TOPIC_NAME,
            project_id=settings.GOOGLE_PROJECT_ID,
        )
        logger.info(
            f'Clean factsheet for sku:{sku} seller_id:{seller_id} '
            f'sent to the stream successfully'
        )

    def refresh_token(self) -> bool:
        token = self.__get_oauth_token()
        return self.update_token(token) if token else False

    def __get_oauth_token(self) -> str:
        try:
            data = {
                'client_id': settings.APIS[
                    self.SETTINGS_API_KEY
                ]['client_id'],
                'client_secret': settings.APIS[
                    self.SETTINGS_API_KEY
                ]['client_secret'],
                'grant_type': 'client_credentials',
            }

            response = requests.post(
                url=settings.APIS[
                    self.SETTINGS_API_KEY]
                ['authorization_server_url'],
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                data=data
            )
            if response.status_code != HTTP_200_OK:
                logger.error(
                    f'Error when requesting a token: '
                    f'status_code:{response.status_code}'
                )
                return ''

            token = response.json()['access_token']
            return f'Bearer {token}'

        except Exception as error:
            logger.error(
                f'Error requesting access token to {self.SETTINGS_API_KEY} '
                f'error:{error}'
            )
            return ''

    @staticmethod
    def __get_headers(seller_id: str, token: str) -> dict:
        return {
            'Content-Type': 'application/json',
            'X-Tenant-Id': seller_id,
            'Authorization': token
        }

    def __get_token(self) -> str:
        token = self.get_token()
        if not token:
            if self.refresh_token():
                token = self.get_token()
            else:
                raise Exception('Error set token in cache')
        return token

    @staticmethod
    def __format_payload(sku: str) -> dict:
        return {
            'product_skus': [sku],
            'operation': 'ALL_PUBLISHING_STEPS'
        }
