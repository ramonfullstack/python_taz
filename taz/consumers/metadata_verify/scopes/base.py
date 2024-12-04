
import logging
from abc import ABCMeta, abstractmethod
from functools import cached_property
from typing import Optional, Tuple

from simple_settings import settings

from taz.consumers.core.exceptions import NotFound
from taz.consumers.core.google.storage import StorageManager

logger = logging.getLogger(__name__)


class BaseScope(metaclass=ABCMeta):  # pragma: no cover

    @cached_property
    def data_storage(self):
        return StorageManager(settings.METADATA_INPUT_BUCKET)

    @cached_property
    def image_storage(self):
        return StorageManager(settings.METADATA_IMAGE_BUCKET)

    def get_metadata(self, source: str, identifier: str) -> Optional[dict]:
        file_name = f'{source}/{identifier}.json'
        return self.data_storage.get_json(file_name)

    def get_media(self, source: str, identifier: str) -> Optional[dict]:
        file_name = f'{source}/{identifier}/images.json'
        return self.image_storage.get_json(file_name)

    def process(self, identifier: str, product: dict) -> Optional[dict]:
        try:
            sku = product['sku']
            seller_id = product['seller_id']
            navigation_id = product.get('navigation_id')
            return self._process(
                identifier=identifier,
                sku=sku,
                seller_id=seller_id,
                navigation_id=navigation_id
            )
        except NotFound as e:
            logger.debug(
                f'Failed process scope with error:{e} for product '
                f'sku:{sku} seller_id:{seller_id} '
                f'navigation_id:{navigation_id}'
            )
            return None

    @abstractmethod
    def is_allowed(self, product: dict) -> Tuple[bool, str]:
        ...

    @abstractmethod
    def _process(
        self,
        identifier: str,
        sku: str,
        seller_id: str,
        navigation_id: str
    ) -> Optional[dict]:
        ...

    @abstractmethod
    def _factsheet_process(
        self,
        sku: str,
        seller_id: str,
        navigation_id: str,
        metadata: dict
    ) -> Optional[dict]:
        ...

    @abstractmethod
    def _enriched_product_process(
        self,
        sku: str,
        seller_id: str,
        navigation_id: str,
        metadata: dict
    ) -> dict:
        ...

    @abstractmethod
    def _media_process(
        self,
        sku: str,
        seller_id: str,
        navigation_id: str,
        media_payload: dict
    ) -> Optional[dict]:
        ...
