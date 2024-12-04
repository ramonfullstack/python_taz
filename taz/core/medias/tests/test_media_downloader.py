from io import BytesIO
from unittest.mock import Mock, patch

import pytest
from simple_settings.utils import settings_stub

from taz.core.medias.exceptions import (
    MediaBaseException,
    MediaContentException,
    MediaDownloadStrategyException,
    MediaGenericDownloadException,
    MediaNotFoundException,
    MediaUnprocessableException,
    MediaWithoutContentType,
    TimedOutMediaException
)
from taz.core.medias.media import (
    MediaDownloadInput,
    MediaDownloadOutput,
    MediaType
)
from taz.core.medias.media_downloader import MediaDownloader
from taz.core.medias.strategies.base import DownloadMediaStrategy
from taz.core.medias.strategies.bucket_gcp import (
    DownloadMediaGenericStorageInternal
)
from taz.core.medias.strategies.internet import DownloadMediaInternet


class TestMediaDownloader:

    @pytest.fixture
    def mock_media_downloader(self) -> MediaDownloader:
        return MediaDownloader()

    @pytest.fixture
    def patch_get_strategy(self):
        return patch.object(MediaDownloader, '_get_strategy')

    def test_when_not_configured_strategies_then_load_internet_strategy(
        self,
        mock_media_downloader: MediaDownloader
    ):
        with settings_stub(MEDIA_SERVICE_STRATEGY={}):
            assert len(mock_media_downloader.strategies) == 1
            assert isinstance(
                mock_media_downloader.strategies[0],
                DownloadMediaInternet
            )

    @pytest.mark.parametrize('bucket_name,starts_url', [
        ('fake', 'https://fake.googleapis.com'),
        ('fake', 'https://fake.googleapis.com,https://fake.magalu.com')
    ])
    def test_when_configured_strategies_then_load_internet_strategy(
        self,
        mock_media_downloader: MediaDownloader,
        bucket_name: str,
        starts_url: str
    ):
        with settings_stub(MEDIA_SERVICE_STRATEGY={bucket_name: starts_url}):
            assert len(mock_media_downloader.strategies) == 2
            assert isinstance(
                mock_media_downloader.strategies[0],
                DownloadMediaGenericStorageInternal
            )
            assert mock_media_downloader.strategies[0]._bucket_name == bucket_name  # noqa
            assert mock_media_downloader.strategies[0].starts_url == starts_url.split(',')  # noqa
            assert isinstance(
                mock_media_downloader.strategies[1],
                DownloadMediaInternet
            )

    def test_when_success_download_media_then_return_data(
        self,
        mock_media_download_internet_input: MediaDownloadInput,
        mock_media_downloader: MediaDownloader,
        patch_get_strategy: Mock,
        mock_image_data: bytes,
        mock_image_content_type: str,
        mock_expected_media_output: MediaDownloadOutput
    ):
        with patch_get_strategy as mock_get_strategy:
            mock_strategy = Mock()
            mock_download = Mock()
            mock_download.return_value = BytesIO(mock_image_data), mock_image_content_type  # noqa
            mock_strategy._download.side_effect = mock_download
            mock_get_strategy.return_value = mock_strategy
            media_result: MediaDownloadOutput = mock_media_downloader.download(
                mock_media_download_internet_input
            )

        assert media_result.url == mock_expected_media_output.url
        assert media_result.media_type == mock_expected_media_output.media_type
        assert media_result.data.getbuffer() == mock_expected_media_output.data.getbuffer()  # noqa
        assert media_result.content_type == mock_expected_media_output.content_type  # noqa
        assert media_result.extension == mock_expected_media_output.extension
        assert media_result.md5 == mock_expected_media_output.md5

    @pytest.mark.parametrize('url,expected_strategy', [
        ('https://taz-metadata-images-sandbox.storage.googleapis.com/metabooks/9786588484609/9786588484609.jpg', DownloadMediaGenericStorageInternal),  # noqa
        ('https://files-product.magalu.com/6425a28b8bf6f1e9b622352b.jpeg', DownloadMediaInternet),  # noqa
        ('https://img.magazineluiza.com.br/1500x1500/x-213445900.jpg', DownloadMediaInternet),  # noqa
        ('https://storage.googleapis.com/img.magazineluiza.com.br/magazineluiza/img/produto_grande/22/229889200k.jpg', DownloadMediaInternet)  # noqa
    ])
    def test_when_get_strategy_then_return_expected_strategy(
        self,
        mock_media_download_internet_input: MediaDownloadInput,
        mock_media_downloader: MediaDownloader,
        url: str,
        expected_strategy: DownloadMediaStrategy
    ):
        mock_media_download_internet_input.url = url
        assert isinstance(
            mock_media_downloader._get_strategy(
                mock_media_download_internet_input
            ),
            expected_strategy
        )

    @pytest.mark.parametrize('url,media_type', [
        ('ftp://arquivo.mp3', MediaType.audios.value),
        ('ftp://arquivo.jpg', MediaType.images.value),
        ('scp://arquivo.jpg', MediaType.images.value)
    ])
    def test_when_not_founded_strategy_then_raise_exception(
        self,
        mock_media_download_internet_input: MediaDownloadInput,
        mock_media_downloader: MediaDownloader,
        url: str,
        media_type: str,
        patch_is_this_strategy: Mock,
        patch_internet_is_this_strategy: Mock
    ):
        mock_media_download_internet_input.url = url
        mock_media_download_internet_input.media_type = media_type
        with pytest.raises(MediaDownloadStrategyException) as error:
            with patch_is_this_strategy as mock_is_this_strategy:
                with patch_internet_is_this_strategy as mock_internet_is_this_strategy:  # noqa
                    mock_is_this_strategy.side_effect = [False, False, False]
                    mock_internet_is_this_strategy.return_value = False
                    mock_media_downloader._get_strategy(
                        mock_media_download_internet_input
                    )

        assert error.value.message == (
            f'Strategy not defined for media type:{media_type} url:{url}'
        )

    @pytest.mark.parametrize('url', ['', None])
    def test_when_download_media_without_url_then_return_data_none(  # noqa
        self,
        mock_media_download_internet_input: MediaDownloadInput,
        mock_media_downloader: MediaDownloader,
        url: str
    ):
        mock_media_download_internet_input.url = url
        media_result: MediaDownloadOutput = mock_media_downloader.download(
            mock_media_download_internet_input
        )
        assert media_result.data is None
        assert media_result.content_type is None

    def test_when_download_non_downloadable_url_then_return_bytecode_url(
        self,
        mock_media_download_internet_input: MediaDownloadInput,
        mock_media_downloader: MediaDownloader,
        mock_video_internet_url: str
    ):
        mock_media_download_internet_input.url = mock_video_internet_url
        mock_media_download_internet_input.media_type = MediaType.videos.value
        media_result: MediaDownloadOutput = mock_media_downloader.download(
            mock_media_download_internet_input
        )
        assert media_result.data.getbuffer() == mock_video_internet_url.encode()  # noqa
        assert media_result.content_type == 'text/plain'

    @pytest.mark.parametrize('url,media_type', [
        ('ftp://arquivo.mp3', MediaType.audios.value),
        ('ftp://arquivo.jpg', MediaType.images.value),
        ('scp://arquivo.jpg', MediaType.images.value)
    ])
    def test_when_download_and_not_founded_strategy_then_raise_exception(
        self,
        mock_media_download_internet_input: MediaDownloadInput,
        mock_media_downloader: MediaDownloader,
        url: str,
        media_type: str,
        patch_is_this_strategy: Mock,
        patch_internet_is_this_strategy: Mock
    ):
        mock_media_download_internet_input.url = url
        mock_media_download_internet_input.media_type = media_type
        with pytest.raises(MediaDownloadStrategyException) as error:
            with patch_is_this_strategy as mock_is_this_strategy:
                with patch_internet_is_this_strategy as mock_internet_is_this_strategy:  # noqa
                    mock_is_this_strategy.side_effect = [False, False, False]
                    mock_internet_is_this_strategy.return_value = False
                    mock_media_downloader.download(
                        mock_media_download_internet_input
                    )

        assert error.value.message == (
            f'Strategy not defined for media type:{media_type} url:{url}'
        )

    @pytest.mark.parametrize('exception', [
        TimedOutMediaException,
        MediaContentException,
        MediaNotFoundException,
        MediaGenericDownloadException,
        MediaUnprocessableException,
        MediaWithoutContentType
    ])
    def test_when_download_raised_exception_then_raise_exception(
        self,
        mock_media_download_internet_input: MediaDownloadInput,
        mock_media_downloader: MediaDownloader,
        patch_get_strategy: Mock,
        exception: MediaBaseException
    ):
        with pytest.raises(exception):
            with patch_get_strategy as mock_get_strategy:
                mock_strategy = Mock()
                mock_strategy._download.side_effect = exception(
                    media=mock_media_download_internet_input
                )
                mock_get_strategy.return_value = mock_strategy
                mock_media_downloader.download(
                    mock_media_download_internet_input
                )
