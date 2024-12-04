from typing import List
from unittest.mock import Mock, patch
from urllib.parse import quote_plus

import pytest
from google.api_core.exceptions import Forbidden, NotFound

from taz.core.medias.exceptions import (
    MediaGenericDownloadException,
    MediaNotFoundException,
    MediaUnprocessableException
)
from taz.core.medias.media import MediaDownloadInput, MediaType
from taz.core.medias.strategies.bucket_gcp import (
    DownloadMediaGenericStorageInternal
)


class FakeBlob:
    def __init__(self, data: bytes, content_type: str) -> None:
        self.data = data
        self.content_type = content_type

    def download_as_bytes(self):
        return self.data


class TestDownloadMediaGenericStorageInternal:

    @pytest.fixture
    def mock_media_download_input(
        self,
        mock_bucket_img_internal_url: str
    ) -> MediaDownloadInput:
        return MediaDownloadInput(
            url=mock_bucket_img_internal_url,
            media_type=MediaType.images.value
        )

    @pytest.fixture
    def patch_storage(self):
        return patch.object(DownloadMediaGenericStorageInternal, 'storage')

    @pytest.fixture
    def mock_strategy(
        self,
        mock_fake_bucket_name: str
    ) -> DownloadMediaGenericStorageInternal:
        return DownloadMediaGenericStorageInternal(
            bucket_name=mock_fake_bucket_name,
            starts_url='https://fake.googleapis.com/'
        )

    @pytest.mark.parametrize('starts_url,expected_starts_url', [
        ('', []),
        ('https://fake.googleapis.com/', ['https://fake.googleapis.com/'])
    ])
    def test_when_load_starts_url_then_return_expected_urls(
        self,
        mock_fake_bucket_name: str,
        starts_url: List[str],
        expected_starts_url: List[str]
    ):
        assert DownloadMediaGenericStorageInternal(
            bucket_name=mock_fake_bucket_name,
            starts_url=starts_url
        ).starts_url == expected_starts_url

    def test_when_is_this_strategy_then_return_true(
        self,
        mock_strategy: DownloadMediaGenericStorageInternal
    ):
        assert mock_strategy.is_this_strategy(
            'https://fake.googleapis.com/21/213445900.jpg'
        )

    @pytest.mark.parametrize('media_url,expected_file_path', [
        ('https://fake.googleapis.com/metabooks/9788532524874/9788532524874.jpg', 'metabooks/9788532524874/9788532524874.jpg'),  # noqa
        ('https://fake.googleapis.com/21/213445900.jpg', '21/213445900.jpg')
    ])
    def test_when_start_with_ended_with_char_path_get_file_path_then_return_file_path(  # noqa
        self,
        mock_strategy: DownloadMediaGenericStorageInternal,
        media_url: str,
        expected_file_path: str
    ):
        assert mock_strategy.get_file_path(media_url) == expected_file_path

    @pytest.mark.parametrize('media_url,expected_file_path', [
        ('https://fake.googleapis.com/metabooks/9788532524874/9788532524874.jpg', 'metabooks/9788532524874/9788532524874.jpg'),  # noqa
        ('https://fake.googleapis.com/21/213445900.jpg', '21/213445900.jpg')
    ])
    def test_when_start_with_not_ended_with_char_path_get_file_path_then_return_file_path(  # noqa
        self,
        mock_fake_bucket_name: str,
        media_url: str,
        expected_file_path: str
    ):
        strategy = DownloadMediaGenericStorageInternal(
            bucket_name=mock_fake_bucket_name,
            starts_url='https://fake.googleapis.com'
        )
        assert strategy.get_file_path(media_url) == expected_file_path

    @pytest.mark.parametrize('media_url', [
        'gs://other-fake/21/213445900.jpg',
        'gs://taz-metadata-images./metabooks/9786588444511/9786588444511.png',  # noqa
        'https://files-product.magalu.com/6425a28b8bf6f1e9b622352b.jpeg',
        'https://taz-metadata-images.storage.googleapis.com/metabooks/9788532524874/9788532524874.jpg',  # noqa
        'http://img.magazineluiza.com.br/21/213445900.jpg'
    ])
    def test_when_is_this_strategy_then_return_false(
        self,
        mock_strategy: DownloadMediaGenericStorageInternal,
        media_url: str
    ):
        assert not mock_strategy.is_this_strategy(media_url)

    def test_when_get_blob_then_return_data(
        self,
        patch_storage: Mock,
        mock_strategy: DownloadMediaGenericStorageInternal,
        mock_media_download_input: MediaDownloadInput,
        mock_image_data: bytes
    ):
        mock_content_type: str = 'image/jpg;charset=UTF-8'
        with patch_storage as mock_storage:
            mock_storage.get_blob.return_value = FakeBlob(
                data=mock_image_data,
                content_type=mock_content_type
            )
            downloaded_image_data, downloaded_content_type = mock_strategy._download(  # noqa
                mock_media_download_input
            )

        mock_storage.get_blob.assert_called_with('21/213445900.jpg')
        assert downloaded_image_data.getbuffer() == mock_image_data
        assert downloaded_content_type == mock_content_type

    def test_when_get_blob_with_incomplete_url_then_raises_exception(
        self,
        patch_storage: Mock,
        mock_strategy: DownloadMediaGenericStorageInternal,
        mock_media_download_input: MediaDownloadInput
    ):
        mock_media_download_input.url = 'https://fake.googleapis.com/'
        with pytest.raises(MediaUnprocessableException) as error:
            with patch_storage as mock_storage:
                mock_strategy._download(mock_media_download_input)

        assert not mock_storage.get_blob.called
        assert error.value.message == (
            f'Could not process the media type:{mock_media_download_input.media_type} '  # noqa
            f'url:{mock_media_download_input.url} error:File not informed'
        )

    def test_when_get_blob_not_founded_then_raises_not_found_exception(
        self,
        patch_storage: Mock,
        mock_strategy: DownloadMediaGenericStorageInternal,
        mock_media_download_input: MediaDownloadInput
    ):
        file_path: str = mock_strategy.get_file_path(
            mock_media_download_input.url
        )
        file_path_parsed: str = quote_plus(file_path)
        message_error: str = (
            f'GET https://storage.googleapis.com/download/storage/v1/b/fake/o/{file_path_parsed}?alt=media: '  # noqa
            f'No such object: fake/{file_path}: '
            f'(\'Request failed with status code\', 404, \'Expected one of\', <HTTPStatus.OK: 200>, <HTTPStatus.PARTIAL_CONTENT: 206>)'  # noqa
        )
        with pytest.raises(MediaNotFoundException) as error:
            with patch_storage as mock_storage:
                mock_storage.get_blob.side_effect = NotFound(message_error)
                mock_strategy._download(mock_media_download_input)

        assert mock_storage.get_blob.called
        assert error.value.message == (
            f'Not found media type:images url:{mock_media_download_input.url}'
        )

    def test_when_get_blob_forbidden_exception_then_raise_forbidden_exception(
        self,
        patch_storage: Mock,
        mock_strategy: DownloadMediaGenericStorageInternal,
        mock_media_download_input: MediaDownloadInput
    ):
        message_error: str = (
            'GET https://storage.googleapis.com/storage/v1/b/fake?projection=noAcl&prettyPrint=false: '  # noqa
            'sa@project-id.iam.gserviceaccount.com does not have storage.buckets.get access to the Google Cloud Storage bucket. '  # noqa
            'Permission \'storage.buckets.get\' denied on resource (or it may not exist).'  # noqa
        )
        with pytest.raises(MediaGenericDownloadException) as error:
            with patch_storage as mock_storage:
                mock_storage.get_blob.side_effect = Forbidden(message_error)
                mock_strategy._download(mock_media_download_input)

        assert mock_storage.get_blob.called
        assert error.value.message == (
            'An error occurred while downloading media type:images'
            f' url:{mock_media_download_input.url} error:403 {message_error}'
        )
