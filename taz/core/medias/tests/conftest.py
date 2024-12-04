import os
from io import BytesIO
from unittest.mock import patch

import pytest
from PIL import Image

from taz.core.medias.media import (
    MediaDownloadInput,
    MediaDownloadOutput,
    MediaType
)
from taz.core.medias.strategies.base import DownloadMediaStrategy
from taz.core.medias.strategies.internet import DownloadMediaInternet


@pytest.fixture
def mock_fake_bucket_name() -> str:
    return 'fake'


@pytest.fixture
def mock_bucket_img_internal_url(mock_fake_bucket_name: str) -> str:
    return f'https://{mock_fake_bucket_name}.googleapis.com/21/213445900.jpg'


@pytest.fixture
def mock_image_internet_url() -> str:
    return 'https://files-product.magalu.com/6425a28b8bf6f1e9b622352b.jpeg'


@pytest.fixture
def mock_video_internet_url() -> str:
    return 'https://www.youtube.com/v/L76al18mF3Y?hl=pt&'


@pytest.fixture
def mock_image_data() -> bytes:
    return b'image'


@pytest.fixture
def mock_image_md5() -> str:
    return '78805a221a988e79ef3f42d7c5bfd418'


@pytest.fixture
def mock_image_content_type() -> str:
    return 'image/jpeg'


@pytest.fixture
def mock_content_type_png() -> str:
    return 'image/png'


@pytest.fixture
def mock_media_download_internet_input(
    mock_image_internet_url: str
) -> MediaDownloadInput:
    return MediaDownloadInput(
        url=mock_image_internet_url,
        media_type=MediaType.images.value
    )


@pytest.fixture
def mock_expected_media_output(
    mock_media_download_internet_input: MediaDownloadInput,
    mock_image_data: bytes,
    mock_image_content_type: str
) -> MediaDownloadOutput:
    return MediaDownloadOutput(
        url=mock_media_download_internet_input.url,
        media_type=mock_media_download_internet_input.media_type,
        data=BytesIO(mock_image_data),
        content_type=mock_image_content_type
    )


def make_image_file_size() -> BytesIO:
    file = BytesIO()
    image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file


@pytest.fixture
def valid_image_file_size() -> BytesIO:
    return make_image_file_size()


@pytest.fixture
def mock_image_media_download_output(
    valid_image_file_size: BytesIO,
    mock_content_type_png: str
) -> MediaDownloadOutput:
    return MediaDownloadOutput(
        url='https://img/test.png',
        media_type=MediaType.images.value,
        data=valid_image_file_size,
        content_type=mock_content_type_png
    )


def mount_file_path(file_name: str) -> str:
    return os.path.join(os.path.dirname(__file__), file_name)


def write_on_disc(file_name: str, media: MediaDownloadOutput) -> None:
    with open(mount_file_path(file_name), 'wb') as file:
        file.write(media.data.getvalue())


def read_on_disc(file_name: str) -> BytesIO:
    with open(mount_file_path(file_name), 'rb') as f:
        return BytesIO(f.read())


def delete_on_disc(file_name: str) -> None:
    os.remove(mount_file_path(file_name))


def generate_image(
    filename: str,
    orientation: int,
    width: int = 100,
    height: int = 100,
    format: str = 'JPEG',
    write_on_disc: bool = True
) -> BytesIO:
    file = BytesIO()
    file.name = filename

    image = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    exif_data = image.getexif()
    if orientation:
        exif_data[274] = orientation

    image.save(file, format=format, exif=exif_data)
    if write_on_disc:
        image.save(mount_file_path(filename), format=format, exif=exif_data)
    return file


@pytest.fixture
def patch_is_this_strategy():
    return patch.object(DownloadMediaStrategy, 'is_this_strategy')


@pytest.fixture
def patch_internet_is_this_strategy():
    return patch.object(DownloadMediaInternet, 'is_this_strategy')
