from contextlib import closing
from io import BytesIO
from typing import Optional, Tuple

import requests
from simple_settings import settings

from taz.core.medias.exceptions import (
    MediaContentException,
    MediaGenericDownloadException,
    MediaNotFoundException,
    MediaUnprocessableException,
    MediaWithoutContentType,
    TimedOutMediaException
)
from taz.core.medias.media import MediaDownloadInput
from taz.core.medias.strategies.base import DownloadMediaStrategy


class DownloadMediaInternet(DownloadMediaStrategy):
    def __init__(self) -> None:
        super().__init__(starts_url='')

    def is_this_strategy(self, url: str) -> bool:
        return True

    def _download(
        self,
        media: MediaDownloadInput
    ) -> Tuple[Optional[BytesIO], Optional[str]]:
        try:
            with closing(
                requests.get(
                    media.url,
                    stream=True,
                    timeout=(
                        float(settings.CONNECTION_TIMEOUT_REQUEST_MEDIA),
                        float(settings.READ_TIMEOUT_REQUEST_MEDIA)
                    )
                )
            ) as response:
                if response.status_code == 404:
                    raise MediaNotFoundException(media)
                elif 400 <= response.status_code < 600:
                    raise MediaUnprocessableException(
                        media=media,
                        error=Exception(
                            'Request returned '
                            f'status_code:{response.status_code}'
                        )
                    )

                try:
                    content_type = response.headers['content-type']
                    bytes_io = BytesIO()
                    bytes_io.write(response.content)
                except KeyError:
                    raise MediaWithoutContentType(media=media)
                except Exception as e:
                    raise MediaContentException(media=media, error=e)

                return bytes_io, content_type
        except requests.exceptions.Timeout:
            raise TimedOutMediaException(media=media)
        except requests.exceptions.RequestException as e:
            raise MediaGenericDownloadException(media=media, error=e)
