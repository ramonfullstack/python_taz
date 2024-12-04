from copy import deepcopy
from unittest.mock import Mock, patch

import pytest

from taz.core.medias.exceptions import (
    MediaDimensionsException,
    MediaResizeFailedException
)
from taz.core.medias.media import (
    ImageDimension,
    MediaDownloadInput,
    MediaDownloadOutput,
    MediaType
)
from taz.core.medias.media_downloader import MediaDownloader
from taz.core.medias.media_processor import MediaProcessor
from taz.core.medias.media_service import MediaService


class TestMediaService:

    @pytest.fixture
    def mock_media_service(self) -> MediaService:
        return MediaService()

    @pytest.fixture
    def patch_get_image_dimensions(self):
        return patch.object(MediaProcessor, 'get_image_dimensions')

    @pytest.fixture
    def patch_image_resize(self):
        return patch.object(MediaProcessor, 'resize')

    @pytest.fixture
    def patch_media_downloader_download(self):
        return patch.object(MediaDownloader, 'download')

    def test_when_download_image_then_return_image_with_dimensions(
        self,
        mock_media_service: MediaService,
        patch_media_downloader_download: Mock,
        mock_media_download_internet_input: MediaDownloadInput,
        mock_image_media_download_output: MediaDownloadOutput
    ):
        old_md5: str = deepcopy(mock_image_media_download_output.md5)
        old_image_dimension = ImageDimension(
            width=mock_image_media_download_output.width,
            height=mock_image_media_download_output.height
        )
        with patch_media_downloader_download as mock_media_downloader_download:
            mock_media_downloader_download.return_value = (
                mock_image_media_download_output
            )
            media_output: MediaDownloadOutput = (
                mock_media_service.download(
                    mock_media_download_internet_input
                )
            )

        assert old_md5 == media_output.md5
        assert old_image_dimension == ImageDimension(None, None)
        assert media_output.width == 50
        assert media_output.height == 50

    def test_when_failed_get_dimension_image_on_download_then_return_image_without_dimensions(  # noqa
        self,
        mock_media_service: MediaService,
        patch_media_downloader_download: Mock,
        mock_media_download_internet_input: MediaDownloadInput,
        mock_image_media_download_output: MediaDownloadOutput,
        patch_get_image_dimensions: Mock
    ):
        old_md5: str = deepcopy(mock_image_media_download_output.md5)
        old_image_dimension = ImageDimension(
            width=mock_image_media_download_output.width,
            height=mock_image_media_download_output.height
        )
        with patch_media_downloader_download as mock_media_downloader_download:
            with patch_get_image_dimensions as mock_get_image_dimensions:
                mock_get_image_dimensions.side_effect = (
                    MediaDimensionsException(
                        media=mock_image_media_download_output
                    )
                )
                mock_media_downloader_download.return_value = (
                    mock_image_media_download_output
                )
                media_output: MediaDownloadOutput = (
                    mock_media_service.download(
                        mock_media_download_internet_input
                    )
                )

        assert mock_get_image_dimensions.called
        assert old_md5 == media_output.md5
        assert old_image_dimension == ImageDimension(None, None)
        assert media_output.width is None
        assert media_output.height is None

    @pytest.mark.parametrize('media_type', [
        MediaType.audios,
        MediaType.podcasts,
        MediaType.videos
    ])
    def test_when_download_others_media_then_return_data(
        self,
        mock_media_service: MediaService,
        patch_media_downloader_download: Mock,
        mock_media_download_internet_input: MediaDownloadInput,
        mock_image_media_download_output: MediaDownloadOutput,
        media_type: MediaType,
        patch_get_image_dimensions: Mock
    ):
        old_md5: str = deepcopy(mock_image_media_download_output.md5)
        old_image_dimension = ImageDimension(
            width=mock_image_media_download_output.width,
            height=mock_image_media_download_output.height
        )
        mock_image_media_download_output.media_type = media_type.value
        with patch_media_downloader_download as mock_media_downloader_download:
            with patch_get_image_dimensions as mock_get_image_dimensions:
                mock_media_downloader_download.return_value = mock_image_media_download_output  # noqa
                media_output: MediaDownloadOutput = (
                    mock_media_service.download(
                        mock_media_download_internet_input
                    )
                )

        assert not mock_get_image_dimensions.called
        assert old_md5 == media_output.md5
        assert old_image_dimension == ImageDimension(None, None)
        assert media_output.width is None
        assert media_output.height is None

    def test_when_download_and_resize_applying_white_background_image_then_return_image_without_changes_dimension(  # noqa
        self,
        mock_media_service: MediaService,
        patch_media_downloader_download: Mock,
        mock_media_download_internet_input: MediaDownloadInput,
        mock_image_media_download_output: MediaDownloadOutput
    ):
        old_md5: str = deepcopy(mock_image_media_download_output.md5)
        old_image_dimension = ImageDimension(
            width=mock_image_media_download_output.width,
            height=mock_image_media_download_output.height
        )
        with patch_media_downloader_download as mock_media_downloader_download:
            mock_media_downloader_download.return_value = (
                mock_image_media_download_output
            )
            media_output: MediaDownloadOutput = (
                mock_media_service.download_and_resize(
                    mock_media_download_internet_input
                )
            )

        assert old_md5 != media_output.md5
        assert old_image_dimension == ImageDimension(None, None)
        assert media_output.width == 50
        assert media_output.height == 50

    def test_when_download_and_failed_resize_image_then_return_image(
        self,
        mock_media_service: MediaService,
        patch_media_downloader_download: Mock,
        mock_media_download_internet_input: MediaDownloadInput,
        mock_image_media_download_output: MediaDownloadOutput,
        patch_image_resize: Mock
    ):
        old_md5: str = deepcopy(mock_image_media_download_output.md5)
        old_image_dimension = ImageDimension(
            width=mock_image_media_download_output.width,
            height=mock_image_media_download_output.height
        )
        with patch_media_downloader_download as mock_media_downloader_download:
            with patch_image_resize as mock_image_resize:
                mock_media_downloader_download.return_value = (
                    mock_image_media_download_output
                )
                mock_image_resize.side_effect = MediaResizeFailedException(
                    media=mock_image_media_download_output
                )
                media_output: MediaDownloadOutput = (
                    mock_media_service.download_and_resize(
                        mock_media_download_internet_input
                    )
                )

        assert old_md5 == media_output.md5
        assert old_image_dimension == ImageDimension(None, None)
        assert media_output.width == 50
        assert media_output.height == 50

    def test_when_download_and_failed_resize_and_get_dimension_image_then_return_image_without_dimension(  # noqa
        self,
        mock_media_service: MediaService,
        patch_media_downloader_download: Mock,
        mock_media_download_internet_input: MediaDownloadInput,
        mock_image_media_download_output: MediaDownloadOutput,
        patch_get_image_dimensions: Mock,
        patch_image_resize: Mock
    ):
        old_md5: str = deepcopy(mock_image_media_download_output.md5)
        old_image_dimension = ImageDimension(
            width=mock_image_media_download_output.width,
            height=mock_image_media_download_output.height
        )
        with patch_media_downloader_download as mock_media_downloader_download:
            with patch_get_image_dimensions as mock_get_image_dimensions:
                with patch_image_resize as mock_image_resize:
                    mock_get_image_dimensions.side_effect = (
                        MediaDimensionsException(
                            media=mock_image_media_download_output
                        )
                    )

                    mock_media_downloader_download.return_value = (
                        mock_image_media_download_output
                    )
                    mock_image_resize.side_effect = MediaResizeFailedException(
                        media=mock_image_media_download_output
                    )
                    media_output: MediaDownloadOutput = (
                        mock_media_service.download_and_resize(
                            mock_media_download_internet_input
                        )
                    )

        assert old_md5 == media_output.md5
        assert old_image_dimension == ImageDimension(None, None)
        assert media_output.width is None
        assert media_output.height is None

    def test_when_download_return_empty_data_then_dont_call_resize(
        self,
        mock_media_service: MediaService,
        patch_media_downloader_download: Mock,
        mock_media_download_internet_input: MediaDownloadInput,
        mock_image_media_download_output: MediaDownloadOutput,
        patch_get_image_dimensions: Mock,
        patch_image_resize: Mock
    ):
        mock_image_media_download_output.data = None
        with patch_media_downloader_download as mock_media_downloader_download:
            with patch_get_image_dimensions as mock_get_image_dimensions:
                with patch_image_resize as mock_image_resize:
                    mock_media_downloader_download.return_value = (
                        mock_image_media_download_output
                    )
                    mock_media_service.download_and_resize(
                        mock_media_download_internet_input
                    )

        assert not mock_image_resize.called
        assert not mock_get_image_dimensions.called
