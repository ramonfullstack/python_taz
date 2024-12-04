from functools import cached_property
from io import BytesIO
from typing import Optional, Tuple

from google.api_core.exceptions import Forbidden, NotFound

from taz.consumers.core.google.storage import StorageManager
from taz.core.medias.exceptions import (
    MediaGenericDownloadException,
    MediaNotFoundException,
    MediaUnprocessableException
)
from taz.core.medias.media import MediaDownloadInput
from taz.core.medias.strategies.base import DownloadMediaStrategy


class DownloadMediaGenericStorageInternal(DownloadMediaStrategy):
    def __init__(self, bucket_name: str, starts_url: str) -> None:
        super().__init__(starts_url=starts_url)
        self._bucket_name = bucket_name

    def get_file_path(self, url: str) -> str:
        for start_with in self.starts_url:
            if start_with in url:
                return (
                    url.replace(start_with, '')
                    if start_with.endswith('/')
                    else url.replace(f'{start_with}/', '')
                )
        return ''

    @cached_property
    def storage(self):
        return StorageManager(self._bucket_name)

    def _download(
        self,
        media: MediaDownloadInput
    ) -> Tuple[Optional[BytesIO], Optional[str]]:
        try:
            file_path: str = self.get_file_path(url=media.url or '')
            if not file_path:
                raise MediaUnprocessableException(
                    media=media,
                    error=Exception('File not informed')
                )
            blob = self.storage.get_blob(file_path)
            return BytesIO(blob.download_as_bytes()), blob.content_type
        except NotFound:
            raise MediaNotFoundException(media=media)
        except Forbidden as e:
            raise MediaGenericDownloadException(media=media, error=e)
