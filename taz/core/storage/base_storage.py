import abc
import logging
from functools import cached_property

from taz.consumers.core.exceptions import NotFound
from taz.consumers.core.google.storage import StorageManager

logger = logging.getLogger(__name__)


class BaseStorage:
    def __init__(self, bucket: str):
        self.__bucket = bucket
        self.__charset = 'application/json; charset=utf-8'

    @cached_property
    def storage_manager(self):
        return StorageManager(self.__bucket)

    @abc.abstractmethod
    def generate_filename(self, sku, seller_id):
        pass

    @abc.abstractmethod
    def generate_external_url(self, sku, seller_id):
        pass

    def get_bucket_data(self, sku, seller_id):
        filename = self.generate_filename(sku, seller_id)
        storage = None

        try:
            storage = self.storage_manager.get_json(filename)
        except NotFound:
            logger.warning(
                f'File:{filename} not found in bucket:{self.__bucket} '
                f'with sku:{sku} seller_id:{seller_id}'
            )

        return storage

    def upload_bucket_data(self, sku, seller_id, payload):
        filename = self.generate_filename(sku, seller_id)
        self.storage_manager.upload(payload, filename, self.__charset)

        logger.info(
            f'Successfully upload file:{filename} sku:{sku} '
            f'seller_id:{seller_id} to bucket:{self.__bucket}'
        )

    def delete_bucket_data(self, sku, seller_id):
        filename = self.generate_filename(sku, seller_id)
        self.storage_manager.delete(filename)

        logger.info(
            f'Successfully deleted file:{filename} sku:{sku} '
            f'seller_id:{seller_id} in bucket:{self.__bucket}'
        )
