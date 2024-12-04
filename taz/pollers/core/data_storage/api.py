from simple_settings import settings

from taz.pollers.core.data.sources import Api
from taz.pollers.core.exceptions import UrlNotProvided

from .base import DataStorageBase


class ApiDataStorage(DataStorageBase):

    scope = None

    def __init__(self, url=None):
        self.api = Api(scope=self.scope)
        self.url = url or self._get_url()

    def _get_url(self):
        try:
            url = settings.POLLERS[self.scope]['api']['url']
        except KeyError:
            url = None

        return url

    def fetch(self):
        if self.url is None:
            raise UrlNotProvided('No URL was specified for Poller')

        return self.api.execute(url=self.url)

    def is_batch(self):  # pragma: no cover
        return True

    def batch_key(self):  # pragma: no cover
        raise NotImplementedError
