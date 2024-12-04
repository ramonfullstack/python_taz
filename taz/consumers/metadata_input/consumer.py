import importlib
from functools import cached_property
from io import BytesIO
from typing import Dict, List, Optional, Tuple

import requests
from maaslogger import base_logger
from simple_settings import settings

from taz.constants import (
    SOURCE_DATASHEET,
    SOURCE_METABOOKS,
    SOURCE_SMARTCONTENT
)
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.exceptions import InvalidScope, NotFound
from taz.consumers.core.google.storage import StorageManager
from taz.consumers.core.google.stream import StreamPublisherManager
from taz.helpers.json import json_dumps
from taz.helpers.url import remove_url_param
from taz.http_status import HTTP_404_NOT_FOUND

from ...utils import format_ean
from ..core.brokers.stream import PubSubBroker, PubSubRecordProcessor
from .helpers import _create_image_payload, _get_images

logger = base_logger.get_logger(__name__)


class MetadataInputRecordProcessor(MongodbMixin, PubSubRecordProcessor):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @cached_property
    def raw_products(self):
        return self.get_collection('raw_products')

    @cached_property
    def enriched_products(self):
        return self.get_collection('enriched_products')

    @cached_property
    def data_storage(self):
        return StorageManager(settings.METADATA_INPUT_BUCKET)

    @cached_property
    def image_storage(self):
        return StorageManager(settings.METADATA_IMAGE_BUCKET)

    @cached_property
    def pubsub(self):
        return StreamPublisherManager()

    def publish(self, payload: dict):
        self.pubsub.publish(
            topic_name=settings.PUBSUB_METADATA_VERIFY_TOPIC_NAME,
            project_id=settings.GOOGLE_PROJECT_ID,
            content=payload,
        )

    def process_message(self, message: Dict) -> bool:
        identified = message.get('identified')
        source = message.get('source')

        if self._is_invalid_message(message):
            return True

        scope = self._get_scope(source).Scope()

        try:
            payload = scope.process(identified)
        except NotFound:
            logger.warning(
                f'Not found metadata for identifier:{identified} '
                f'source:{source}'
            )
            return True

        if not payload:
            logger.warning(
                f'Metadata was not processed for '
                f'identifier:{identified} source:{source}'
            )
            return False

        identified = format_ean(identified)

        result = self._save_images(identified, payload, source)
        if not result:
            return True

        self._save(identified, payload, source)
        self._notify(identified, source)

        logger.info(
            f'Metadata successfully processed for '
            f'identifier:{identified} source:{source}'
        )

        return True

    def _notify(
        self,
        identified: str,
        source: str
    ) -> None:
        products = self._find_by_source(source, identified)

        for product in products:
            self.publish({
                'sku': product['sku'],
                'seller_id': product['seller_id']
            })

    @staticmethod
    def _is_invalid_message(
        message: Dict
    ) -> bool:
        identified = message.get('identified')
        source = message.get('source')

        if not identified or not source:
            logger.warning(
                f'Remove message from queue because is '
                f'invalid payload:{message}'
            )
            return True

        if source not in settings.SCOPES_METADATA_INPUT:
            logger.warning(f'Source is unknown for payload:{message}')
            return True

        return False

    def _find_by_source(
        self,
        source: str,
        identified: str
    ) -> Optional[List]:
        if source == SOURCE_SMARTCONTENT or source == SOURCE_METABOOKS:
            query = {'$or': [{'isbn': identified}, {'ean': identified}]}
            return self.raw_products.find(
                query, {'_id': 0, 'sku': 1, 'seller_id': 1}
            )

        if source == SOURCE_DATASHEET:
            query = {'identifier': identified, 'source': source}
            return self.enriched_products.find(
                query, {'_id': 0, 'sku': 1, 'seller_id': 1}
            )

        return []

    def _save_images(
        self,
        identified: str,
        payload: Dict,
        source: str
    ) -> bool:
        images = _get_images(payload, source)

        for image in images:
            data, content_type = self._download_image(image['url'])

            if not data or not content_type:
                logger.info(
                    f'Skip process download images to identifier:{identified} '
                    f'and source:{source} because a error occurred'
                )
                return False

            self._upload_image(
                image['filename'],
                data,
                content_type,
                identified,
                source
            )

        payload = _create_image_payload(images, identified, source)
        self._upload_json(payload, identified, source)
        return True

    def _upload_image(
        self,
        filename: str,
        data: BytesIO,
        content_type: str,
        identified: str,
        source: str
    ) -> None:
        filename = f'{source}/{identified}/{filename}'

        logger.info(
            f'Uploading identified:{identified} filename:{filename} '
            f'of type content_type:{content_type}'
        )

        self.image_storage.upload(
            data,
            filename,
            content_type=content_type
        )

    def _upload_json(
        self,
        payload: List,
        identified: str,
        source: str
    ) -> None:
        filename = f'{source}/{identified}/images.json'
        content_type = 'application/json'

        self.image_storage.upload(
            json_dumps(payload),
            filename,
            content_type=content_type
        )

    def _save(
        self,
        identified: str,
        payload: str,
        source: str
    ) -> None:
        filename = f'{source}/{identified}.json'
        content_type = 'application/json'

        self.data_storage.upload(
            json_dumps(payload),
            filename,
            content_type=content_type
        )

    @staticmethod
    def _download_image(
        url: str
    ) -> Tuple[Optional[BytesIO], Optional[str]]:

        max_retries = settings.METADATA_INPUT_DOWNLOAD_IMAGES_MAX_RETRIES
        parsed_url = remove_url_param(url, 'access_token')

        while max_retries > 0:
            try:
                response = requests.get(url, stream=True)

                if response.status_code == HTTP_404_NOT_FOUND:
                    logger.warning(f'Image not found url:{parsed_url}')
                    max_retries = 0
                elif 400 <= response.status_code < 600:
                    logger.error(
                        f'Could not process url:{parsed_url} '
                        f'status_code:{response.status_code}'
                    )
                    max_retries -= 1
                else:
                    content_type = response.headers['content-type']
                    bytes_io = BytesIO()
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            bytes_io.write(chunk)

                    return bytes_io, content_type
            except Exception as e:
                logger.error(
                    f'Error process download with url:{parsed_url} error:{e}'
                )
                max_retries -= 1

        return None, None

    @staticmethod
    def _get_scope(
        scope_name: str
    ):
        try:
            scope = f'taz.consumers.metadata_input.scopes.{scope_name}'
            return importlib.import_module(scope)
        except Exception:
            raise InvalidScope(scope_name=scope_name)


class MetadataInputConsumer(PubSubBroker):
    scope = 'metadata_input'
    project_name = settings.GOOGLE_PROJECT_ID
    record_processor_class = MetadataInputRecordProcessor
