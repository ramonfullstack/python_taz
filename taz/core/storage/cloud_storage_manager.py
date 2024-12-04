import logging
from typing import Dict, Type

from simple_settings import settings

from taz.constants import GOOGLE_CLOUD_NAME
from taz.consumers.core.google.storage import StorageManager
from taz.core.storage.cloud_storage import CloudStorageInteface

logger = logging.getLogger(__name__)


class CloudStorageManager:

    __storage_managers: Dict[str, Type[CloudStorageInteface]] = {
        GOOGLE_CLOUD_NAME: StorageManager,
    }

    def __init__(self, bucket_config: dict):
        self.bucket_config = bucket_config

    def _get_storage_instance(self, storage_type: str, bucket_name: str):
        storage_class = self.__storage_managers.get(storage_type)
        if not storage_class:
            raise ValueError(f'Unsupported storage type: {storage_type}')

        return storage_class(bucket_name)

    def write_bucket_data(self, data: str, file_name: str):
        write_buckets = settings.BUCKET_CONFIG['write']
        for bucket_config in write_buckets:
            storage_type, bucket_name, active = bucket_config.values()
            if not active:
                continue

            storage_instance = self._get_storage_instance(
                storage_type,
                bucket_name,
            )
            storage_instance.upload(data=data, filename=file_name)

    def read_bucket_data(self, file_name: str):
        read_buckets = settings.BUCKET_CONFIG['read']
        for bucket_config in read_buckets:
            storage_type, bucket_name, active = bucket_config.values()
            if not active:
                continue

            storage_instance = self._get_storage_instance(
                storage_type,
                bucket_name,
            )
            storage_instance.get_file(filename=file_name)
