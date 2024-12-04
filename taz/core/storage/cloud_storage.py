import logging
from abc import ABC, abstractmethod
from typing import Optional, Union

logger = logging.getLogger(__name__)


class CloudStorageInteface(ABC):

    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name

    @abstractmethod
    def upload(
        self,
        data: Union[bytes, str],
        filename: str,
        content_type: Optional[str] = None,
    ):
        ...  # pragma: no cover

    @abstractmethod
    def delete(self, filename: str):
        ...  # pragma: no cover

    @abstractmethod
    def get_file(self, filename: str):
        ...  # pragma: no cover

    @abstractmethod
    def get_json(self, filename: str):
        ...  # pragma: no cover

    @abstractmethod
    def get_blob(self, filename: str):
        ...  # pragma: no cover

    @abstractmethod
    def get_blob_with_hash(self, filename: str):
        ...  # pragma: no cover

    @abstractmethod
    def find_objects(self, prefix: str, timeout: int = 60, retries: int = 1):
        ...  # pragma: no cover
