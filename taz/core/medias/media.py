from collections import namedtuple
from enum import Enum
from hashlib import md5
from io import BytesIO
from typing import Optional

from taz.core.medias.helpers import MediaHelper

ImageDimension = namedtuple('Dimension', ['width', 'height'])


class MediaType(Enum):
    images: str = 'images'
    audios: str = 'audios'
    videos: str = 'videos'
    podcasts: str = 'podcasts'


class MediaDownloadInput:
    __slots__ = ['url', 'media_type', 'extension']

    def __init__(self, url: str, media_type: str) -> None:
        self.url: str = url
        self.media_type: str = media_type
        self.extension = MediaHelper.get_media_extension(
            media_type=media_type,
            url=url
        )


class MediaDownloadOutput:
    __slots__ = [
        'url', 'media_type', 'data', 'content_type', 'md5',
        'width', 'height', 'extension'
    ]

    def __init__(
        self,
        url: str,
        media_type: str,
        data: Optional[BytesIO],
        content_type: Optional[str] = None,
        md5: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None
    ) -> None:
        if data:
            assert isinstance(data, BytesIO)
        self.url = url
        self.media_type = media_type
        self.data = data
        self.content_type = content_type
        self.md5 = md5 or self.calculate_md5(data)
        self.width = width
        self.height = height
        self.extension: str = MediaHelper.get_media_extension(
            media_type=media_type,
            url=url
        )

    @staticmethod
    def calculate_md5(data: BytesIO) -> Optional[str]:
        return md5(data.getbuffer()).hexdigest() if data else None  # NOSONAR

    def mount_file_name(self) -> str:
        if self.md5 and self.extension:
            return f'{self.md5}{self.extension}'
        return ''

    def change_image_data(
        self,
        data: BytesIO,
        md5: str = None,
        width: Optional[int] = None,
        height: Optional[int] = None
    ):
        assert isinstance(data, BytesIO)
        self.data = data
        self.md5 = md5 or self.calculate_md5(data)
        self.width = width
        self.height = height

    def change_image_dimensions(self, dimension: ImageDimension) -> None:
        self.width = dimension.width
        self.height = dimension.height

    def is_image_png(self) -> bool:
        return (
            self.media_type == MediaType.images.value and
            self.extension == '.png'
        )

    def is_empty(self) -> bool:
        return not self.data or self.data.getbuffer().nbytes == 0
