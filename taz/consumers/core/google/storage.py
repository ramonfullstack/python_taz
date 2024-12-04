import json

import google
from google.api_core.retry import Retry
from google.cloud import storage
from maaslogger import base_logger
from requests.adapters import HTTPAdapter
from simple_settings import settings

from taz.consumers.core.exceptions import NotFound
from taz.core.storage.cloud_storage import CloudStorageInteface

logger = base_logger.get_logger(__name__)


class StorageManager(CloudStorageInteface):
    __adapter = HTTPAdapter(
        pool_connections=int(settings.MEDIA_LIST_MAX_POLL_CONNECTIONS),
        pool_maxsize=int(settings.MEDIA_LIST_MAX_POLL_MAXSIZE),
        pool_block=settings.MEDIA_LIST_MAX_POLL_BLOCK
    )
    __client = None

    def __init__(self, bucket):
        self.bucket_name = bucket
        self.client = StorageManager.get_gcp_client()
        self.bucket = self.client.get_bucket(bucket)

    @classmethod
    def get_gcp_client(cls):
        if cls.__client is None:
            StorageManager.__client = storage.Client()
            StorageManager.__client._http.mount("https://", cls.__adapter)
        return cls.__client

    def upload(self, data, filename, content_type=None):
        logger.info(
            f'Uploading file:{filename} to storage bucket:{self.bucket_name}'
        )

        blob = (
            self.bucket.get_blob(filename)
            if settings.ENABLED_RETRY_STORAGE
            else None
        ) or self.bucket.blob(filename)

        if isinstance(data, str):
            blob.upload_from_string(
                data=data,
                content_type=content_type,
                if_generation_match=blob.generation
            )
        else:
            blob.upload_from_file(
                data,
                size=data.tell(),
                rewind=True,
                content_type=content_type,
                if_generation_match=blob.generation
            )

    def delete(self, filename):
        blob = self.bucket.blob(filename)
        try:
            blob.delete()
        except Exception as e:
            if e.code.value == 404:
                logger.warning(
                    f'File {filename} not found in Google Storage'
                )

                return
            raise e

        logger.info(
            f'Deleting file:{filename} to storage bucket:{self.bucket_name}'
        )

    def get_file(self, filename):
        blob = self.bucket.blob(filename)

        payload = blob.download_as_string()
        return payload.decode()

    def get_json(self, filename):
        try:
            payload = self.get_file(filename)
        except google.api_core.exceptions.NotFound:
            raise NotFound(f'Storage file:{filename} not found')
        if not payload:
            return {}

        return json.loads(payload)

    def get_blob(self, filename):
        return self.bucket.blob(filename)

    def get_blob_with_hash(self, filename):
        return self.bucket.get_blob(filename)

    def find_objects(self, prefix, timeout=60, retries=1):
        return list(
            self.bucket.list_blobs(
                prefix=prefix,
                timeout=timeout,
                retry=Retry(total=retries)
            )
        )
