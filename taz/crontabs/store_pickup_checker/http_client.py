import logging

import requests
from simple_settings import settings

from taz.crontabs.store_pickup_checker.cache import APICacheController
from taz.http_status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND
)

logger = logging.getLogger(__name__)


class PickupStoresHttpClient():

    URL = (
        '{base_path}{endpoint}'
    )

    def __init__(self):
        self.api_cache = APICacheController()
        self.token = self.api_cache.get_token()

    def get_oauth_token(self) -> str:
        url = self.URL.format(
            base_path=settings.APIS['apiluiza']['url'],
            endpoint=settings.APIS['apiluiza']['accesstoken']['path'],
        )

        try:
            data = {
                'client_id': settings.APIS['apiluiza']['client_id'],
                'client_secret': settings.APIS['apiluiza']['client_secret'],
                'grant_type': 'client_credentials',
            }

            response = requests.post(url, data=data)
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
                f'Error requesting access token to ApiLuiza '
                f'error:{error}'
            )

    def refresh_token(self):
        self.token = self.get_oauth_token()
        return self.api_cache.update_token(self.token)

    def get_pickup_stores(self, sku) -> dict:
        query_string = '?products[0].quantity=1&products[0].sku={sku}'
        url = (self.URL + query_string).format(
            base_path=settings.APIS['apiluiza']['url'],
            endpoint=settings.APIS['apiluiza']['pickup_store']['path'],
            sku=sku
        )

        try:
            attempts = 0
            total_attempts = settings.APIS['apiluiza']['total_attempts_token']
            headers = {
                'Authorization': self.token
            }

            while attempts < total_attempts:
                response = requests.get(url, headers=headers)

                if response.status_code in (
                    HTTP_404_NOT_FOUND,
                    HTTP_400_BAD_REQUEST
                ):
                    logger.warning(
                        f'No pickup stores found for '
                        f'sku:{sku} url:{url}'
                    )
                    return {}

                elif response.status_code == HTTP_401_UNAUTHORIZED:
                    attempts += 1
                    logger.warning(
                        f'Attempt {attempts} failed to '
                        f'request API authorization: sku:{sku} url:{url}'
                    )

                    if not self.refresh_token():
                        logger.error(
                            f'Attempt {attempts} Error updating '
                            f'token: sku:{sku} url:{url}'
                        )
                        return {}

                    headers['Authorization'] = self.token

                else:
                    break

            response.raise_for_status()

            return {'has_pickustore': True}
        except Exception as error:
            logger.error(
                f'Error requesting ApiLuiza pickup store for sku:{sku} '
                f'error:{error} url:{url}'
            )

            return {}
