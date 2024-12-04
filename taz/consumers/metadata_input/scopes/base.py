from abc import abstractmethod
from typing import Dict, Optional

import requests
from requests import Response

from taz.consumers.core.exceptions import NotFound


class BaseScope:

    @abstractmethod
    def get_headers(self):
        ...

    @abstractmethod
    def get_url(self, identified: str):
        ...

    @abstractmethod
    def handler_response(self, response: Response) -> Dict:
        ...

    def process(self, identified: str) -> Optional[Dict]:
        response = requests.get(
            url=self.get_url(identified),
            headers=self.get_headers()
        )

        if response.status_code == 200:
            return self.handler_response(response)
        elif response.status_code == 404:
            raise NotFound(f'Identifier {identified} not found')

        response.raise_for_status()
