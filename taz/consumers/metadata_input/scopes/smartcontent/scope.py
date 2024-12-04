import logging
from typing import Dict

from requests import Response
from simple_settings import settings

from taz.consumers.metadata_input.scopes.base import BaseScope

logger = logging.getLogger(__name__)


class Scope(BaseScope):

    def get_headers(self):
        return {'Authorization': settings.SMARTCONTENT_TOKEN}

    def get_url(self, identified: str):
        return f'{settings.SMARTCONTENT_URL}/export/{identified}/'

    def handler_response(self, response: Response) -> Dict:
        return response.json().get('data')
