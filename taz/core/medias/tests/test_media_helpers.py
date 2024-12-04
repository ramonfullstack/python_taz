import pytest

from taz.core.medias.helpers import MediaHelper
from taz.core.medias.media import MediaType


class TestMediaHelper:

    @pytest.mark.parametrize('media_type,url,expected_extension', [
        (MediaType.audios.value, 'a.mp3', '.mp3'),
        (MediaType.podcasts.value, 'a.mp3', '.mp3'),
        (MediaType.videos.value, 'a.mp4', ''),
        (MediaType.images.value, 'a.jpeg', '.jpeg'),
        (MediaType.images.value, 'a.jpg', '.jpg'),
        (MediaType.images.value, 'a.png', '.png'),
        (MediaType.images.value, '', ''),
        (MediaType.images.value, None, '')
    ])
    def test_when_get_extension_return_file_extension(
        self,
        media_type: str,
        url: str,
        expected_extension: str
    ):
        assert MediaHelper.get_media_extension(
            media_type=media_type,
            url=url
        ) == expected_extension

    @pytest.mark.parametrize('url, expected', [
        ('https://www.youtube.com/v/OuRhidy92co?hl=pt&', True),
        ('https://www.youtube.com/v/bP8irVgrdCg?hl=pt&', True),
        ('https://www.youtube.com/v/__dmPDx2V1Q?hl=pt&', True),
        ('https://www.youtube.com/watch?v=6OWvSq4OXNM', True),
        ('Novo6YQQk8nL5Pw?hl=pt&', False),
        ('https://www.magazineluiza', False),
        ('', False),
    ])
    def test_when_video_url_validation_return_expected_validation(
        self,
        url: str,
        expected: bool
    ):
        assert MediaHelper.video_url_validation(url) == expected
