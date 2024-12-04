from http import HTTPStatus
from unittest.mock import Mock

import pytest
from requests.exceptions import Timeout

from taz.core.medias.exceptions import (
    MediaContentException,
    MediaNotFoundException,
    MediaUnprocessableException,
    MediaWithoutContentType,
    TimedOutMediaException
)
from taz.core.medias.media import MediaDownloadInput, MediaType
from taz.core.medias.strategies.internet import DownloadMediaInternet


class TestDownloadMediaInternet:

    @pytest.fixture
    def mock_strategy(self) -> DownloadMediaInternet:
        return DownloadMediaInternet()

    @pytest.fixture
    def mock_media_download_input(
        self,
        mock_image_internet_url: str
    ) -> MediaDownloadInput:
        return MediaDownloadInput(
            url=mock_image_internet_url,
            media_type=MediaType.images.value
        )

    def test_when_load_starts_url_then_return_expected_urls(self):
        assert DownloadMediaInternet().starts_url == []

    @pytest.mark.parametrize('url', [
        'https://files-product.magalu.com/6425a28b8bf6f1e9b622352b.jpeg',
        'https://taz-metadata-images.storage.googleapis.com/metabooks/9788532524874/9788532524874.jpg',  # noqa
        'http://img.magazineluiza.com.br/1500x1500/x-213445900.jpg',
        'https://storage.googleapis.com/img.magazineluiza.com.br/magazineluiza/img/produto_grande/22/229889200k.jpg',  # noqa
        'gs://fake/21/213445900.jpg',
        'ftp://ftp.fake/21/213445900.jpg'
    ])
    def test_when_is_this_strategy_then_return_true(
        self,
        mock_strategy: DownloadMediaInternet,
        url: str
    ):
        assert mock_strategy.is_this_strategy(url=url)

    def test_when_download_media_with_success_then_return_data(
        self,
        mock_strategy: DownloadMediaInternet,
        mock_media_download_input: MediaDownloadInput,
        patch_requests_get: Mock,
        mock_image_internet_url: str,
        mock_image_data: bytes
    ):
        mock_content_type: str = 'image/jpeg'
        with patch_requests_get as mock_requests_get:
            mock_requests_get.return_value = Mock(
                status_code=200,
                headers={'content-type': mock_content_type},
                content=mock_image_data
            )
            downloaded_image_data, downloaded_content_type = mock_strategy._download(  # noqa
                mock_media_download_input
            )

        mock_requests_get.assert_called_with(
            mock_image_internet_url,
            stream=True,
            timeout=(5, 10)
        )
        assert downloaded_image_data.getbuffer() == mock_image_data
        assert downloaded_content_type == mock_content_type

    def test_when_download_media_not_found_then_raise_not_found_exception(
        self,
        mock_strategy: DownloadMediaInternet,
        mock_media_download_input: MediaDownloadInput,
        patch_requests_get: Mock,
        mock_image_internet_url: str
    ):
        with pytest.raises(MediaNotFoundException) as error:
            with patch_requests_get as mock_requests_get:
                mock_requests_get.return_value = Mock(
                    status_code=HTTPStatus.NOT_FOUND.value
                )
                mock_strategy._download(mock_media_download_input)

        assert error.value.message == (
            f'Not found media type:images url:{mock_image_internet_url}'
        )

    @pytest.mark.parametrize('status_code', [
        HTTPStatus.UNAUTHORIZED.value,
        HTTPStatus.BAD_GATEWAY.value
    ])
    def test_when_download_media_server_error_then_unprocessable_exception(
        self,
        mock_strategy: DownloadMediaInternet,
        mock_media_download_input: MediaDownloadInput,
        patch_requests_get: Mock,
        mock_image_internet_url: str,
        status_code: int
    ):
        with pytest.raises(MediaUnprocessableException) as error:
            with patch_requests_get as mock_requests_get:
                mock_requests_get.return_value = Mock(
                    status_code=status_code
                )
                mock_strategy._download(mock_media_download_input)

        assert error.value.message == (
            f'Could not process the media type:images url:{mock_image_internet_url} '  # noqa
            f'error:Request returned status_code:{status_code}'
        )

    def test_when_download_media_without_content_type_then_raise_without_content_type_exception(  # noqa
        self,
        mock_strategy: DownloadMediaInternet,
        mock_media_download_input: MediaDownloadInput,
        patch_requests_get: Mock,
        mock_image_internet_url: str,
        mock_image_data: bytes
    ):
        with pytest.raises(MediaWithoutContentType) as error:
            with patch_requests_get as mock_requests_get:
                mock_requests_get.return_value = Mock(
                    status_code=HTTPStatus.OK.value,
                    headers={},
                    content=mock_image_data
                )
                mock_strategy._download(mock_media_download_input)

        assert error.value.message == (
            'Cannot determine content-type of type:images '
            f'url:{mock_image_internet_url}'
        )

    def test_when_download_media_invalid_content_then_raise_media_content_exception(  # noqa
        self,
        mock_strategy: DownloadMediaInternet,
        mock_media_download_input: MediaDownloadInput,
        patch_requests_get: Mock,
        mock_image_internet_url: str
    ):
        with pytest.raises(MediaContentException) as error:
            with patch_requests_get as mock_requests_get:
                mock_requests_get.return_value = Mock(
                    status_code=HTTPStatus.OK.value,
                    headers={'content-type': 'text/html'},
                    content='<html>image</html>'
                )
                mock_strategy._download(mock_media_download_input)

        assert error.value.message == (
           f'Could not process the media type:images url:{mock_image_internet_url} '  # noqa
           'error:a bytes-like object is required, not \'str\''
        )

    def test_when_download_media_returned_timeout_error_then_raise_timeout_exception(  # noqa
        self,
        mock_strategy: DownloadMediaInternet,
        mock_media_download_input: MediaDownloadInput,
        patch_requests_get: Mock,
        mock_image_internet_url: str
    ):
        with pytest.raises(TimedOutMediaException) as error:
            with patch_requests_get as mock_requests_get:
                mock_requests_get.side_effect = Timeout
                mock_strategy._download(mock_media_download_input)

        assert error.value.message == (
           f'Could not download the media type:images url:{mock_image_internet_url} '  # noqa
           'because is timed out.'
        )
