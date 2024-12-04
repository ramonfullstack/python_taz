from copy import deepcopy
from io import BytesIO
from typing import Optional, Tuple
from unittest.mock import Mock, patch

import pytest
from PIL import Image
from simple_settings.utils import settings_stub

from taz.core.medias.exceptions import (
    MediaDimensionsException,
    MediaResizeFailedException
)
from taz.core.medias.media import (
    ImageDimension,
    MediaDownloadOutput,
    MediaType
)
from taz.core.medias.media_processor import MediaProcessor
from taz.core.medias.tests.conftest import generate_image


class TestMediaProcessor:
    @pytest.fixture
    def mock_media_processor(self) -> MediaProcessor:
        return MediaProcessor()

    @pytest.fixture
    def patch_media_processor_resize_image(self) -> MediaProcessor:
        return patch.object(MediaProcessor, '_resize_image')

    def test_when_get_with_success_image_dimensions_then_return_dimension(
        self,
        mock_media_processor: MediaProcessor,
        mock_expected_media_output: MediaDownloadOutput,
        valid_image_file_size: BytesIO
    ):
        mock_expected_media_output.data = valid_image_file_size
        image_dimension: ImageDimension = (
            mock_media_processor.get_image_dimensions(
                mock_expected_media_output
            )
        )

        assert image_dimension == ImageDimension(width=50, height=50)

    def test_when_failed_get_image_dimensions_then_return_dimension(
        self,
        mock_media_processor: MediaProcessor,
        mock_expected_media_output: MediaDownloadOutput
    ):
        with pytest.raises(MediaDimensionsException) as error:
            mock_media_processor.get_image_dimensions(
                mock_expected_media_output
            )

        assert (
            f'Error getting dimensions from type:{mock_expected_media_output.media_type} '  # noqa
            f'url:{mock_expected_media_output.url} error:cannot identify image file'  # noqa
        ) in error.value.message

    @pytest.mark.parametrize('size,expected', [
        ((3000, 3000), (2500, 2500)),
        ((2500, 2500), (2500, 2500)),
        ((4000, 5000), (2000, 2500))
    ])
    def test_when_get_resize_aspect_ratio_return_expected_size(
        self,
        mock_media_processor: MediaProcessor,
        size: Tuple[int, int],
        expected: Tuple[int, int]
    ):
        assert mock_media_processor._get_resize_aspect_ratio(
            width=size[0],
            height=size[1]
        ) == expected

    @pytest.mark.parametrize('size,expected', [
        ((3000, 3000), True),
        ((200, 500), False)
    ])
    def test_when_check_resize_image_then_return_expected(
        self,
        mock_media_processor: MediaProcessor,
        size: Tuple[int, int],
        expected: bool
    ):
        assert mock_media_processor._should_resize_image(
            width=size[0],
            height=size[1]
        ) == expected

    @pytest.mark.parametrize('size,expected', [
        ((3000, 3000), (2500, 2500)),
        ((2500, 2500), (2500, 2500))
    ])
    def test_when_resize_image_then_return_image_resized(
        self,
        mock_media_processor: MediaProcessor,
        size: Tuple[int, int],
        expected: Tuple[int, int]
    ):
        new_img = mock_media_processor._make_image_resize(
            image=Image.new('RGBA', size)
        )
        assert new_img.size == expected

    @pytest.mark.parametrize('orientation,size,expected_size', [
        (Image.TRANSPOSE, (200, 500), (500, 200)),
        (Image.TRANSVERSE, (200, 500), (500, 200)),
        (7, (200, 500), (500, 200)),
        (8, (200, 500), (500, 200)),
        (8, (2500, 2500), (2500, 2500)),
        (8, (3000, 3000), (2500, 2500)),
    ])
    def test_when_resizing_and_remove_exif_tags_then_return_resized_image(
        self,
        mock_media_processor: MediaProcessor,
        orientation: int,
        size: Tuple[int, int],
        expected_size: Tuple[int, int],
        mock_expected_media_output: MediaDownloadOutput
    ):
        image_name: str = 'test_image.jpeg'
        mock_image: BytesIO = generate_image(
            filename=image_name,
            orientation=orientation,
            width=size[0],
            height=size[1],
            write_on_disc=False
        )

        mock_expected_media_output.data = mock_image
        new_image, image_dimension = mock_media_processor._resize_image(
            media=mock_expected_media_output,
            enable_white_background=True
        )

        with Image.open(new_image) as new_img:
            new_orientation = new_img.getexif().get(274)
            width, height = new_img.size

        assert not new_orientation
        assert (width, height) == expected_size
        assert image_dimension == ImageDimension(width=width, height=height)

    @pytest.mark.parametrize('data', [None, BytesIO(b'')])
    def test_when_resize_without_data_then_return(
        self,
        mock_media_processor: MediaProcessor,
        mock_expected_media_output: MediaDownloadOutput,
        data: Optional[BytesIO]
    ):
        mock_expected_media_output.media_type = MediaType.images.value
        with settings_stub(IMAGE_RESIZE_ENABLE=True):
            mock_expected_media_output.data = data
            assert not mock_media_processor.resize(
                mock_expected_media_output
            )

    def test_when_resize_is_disabled_then_not_resize(
        self,
        mock_media_processor: MediaProcessor,
        mock_expected_media_output: MediaDownloadOutput,
        valid_image_file_size: BytesIO,
        patch_media_processor_resize_image: Mock
    ):
        mock_expected_media_output.data = valid_image_file_size
        mock_expected_media_output.media_type = MediaType.images.value
        with settings_stub(IMAGE_RESIZE_ENABLE=False):
            with patch_media_processor_resize_image as mock_resize_image:
                assert not mock_media_processor.resize(
                    mock_expected_media_output
                )
                assert not mock_resize_image.called

    @pytest.mark.parametrize('media_type', [
        MediaType.audios,
        MediaType.podcasts,
        MediaType.videos
    ])
    def test_when_resize_media_type_different_images_then_not_resize(
        self,
        mock_media_processor: MediaProcessor,
        mock_expected_media_output: MediaDownloadOutput,
        valid_image_file_size: BytesIO,
        patch_media_processor_resize_image: Mock,
        media_type: MediaType
    ):
        mock_expected_media_output.data = valid_image_file_size
        mock_expected_media_output.media_type = media_type.value
        with settings_stub(IMAGE_RESIZE_ENABLE=True):
            with patch_media_processor_resize_image as mock_resize_image:
                assert not mock_media_processor.resize(
                    mock_expected_media_output
                )
                assert not mock_resize_image.called

    @pytest.mark.parametrize('image_transparency_enabled', [True, False])
    def test_when_enabled_transparency_but_image_not_png_then_not_apply_white_background(  # noqa
        self,
        mock_media_processor: MediaProcessor,
        mock_expected_media_output: MediaDownloadOutput,
        patch_media_processor_resize_image: Mock,
        valid_image_file_size: BytesIO,
        image_transparency_enabled: bool
    ):
        with settings_stub(
            IMAGE_RESIZE_ENABLE=True,
            IMAGE_TRANSPARENCY_ENABLE=image_transparency_enabled
        ):
            with patch_media_processor_resize_image as mock_resize_image:
                mock_resize_image.return_value = (
                    valid_image_file_size, ImageDimension(width=50, height=50)
                )
                assert mock_media_processor.resize(
                    mock_expected_media_output
                )
                assert not mock_resize_image.call_args_list[0][1][
                    'enable_white_background'
                ]

    @pytest.mark.parametrize('image_transparency_enabled,apply_white_background', [  # noqa
        (True, True),
        (False, False)
    ])
    def test_when_check_transparency_and_image_is_png_then_apply_white_background(  # noqa
        self,
        mock_media_processor: MediaProcessor,
        mock_expected_media_output: MediaDownloadOutput,
        patch_media_processor_resize_image: Mock,
        valid_image_file_size: BytesIO,
        image_transparency_enabled: bool,
        apply_white_background: bool
    ):
        with settings_stub(
            IMAGE_RESIZE_ENABLE=True,
            IMAGE_TRANSPARENCY_ENABLE=image_transparency_enabled
        ):
            mock_expected_media_output.extension = '.png'
            with patch_media_processor_resize_image as mock_resize_image:
                mock_resize_image.return_value = (
                    valid_image_file_size, ImageDimension(width=50, height=50)
                )
                assert mock_media_processor.resize(
                    mock_expected_media_output
                )
                assert mock_resize_image.call_args_list[0][1][
                    'enable_white_background'
                ] == apply_white_background

    @pytest.mark.parametrize('orientation,size,expected_size', [
        (Image.TRANSPOSE, (200, 500), (500, 200)),
        (Image.TRANSVERSE, (200, 500), (500, 200)),
        (7, (200, 500), (500, 200)),
        (8, (200, 500), (500, 200)),
        (8, (2500, 2500), (2500, 2500)),
        (8, (3000, 3000), (2500, 2500)),
    ])
    def test_when_success_resize_image_then_return_change_image_dimension(
        self,
        mock_media_processor: MediaProcessor,
        orientation: int,
        size: Tuple[int, int],
        expected_size: Tuple[int, int],
        mock_image_internet_url: str,
        mock_image_content_type: str
    ):
        image_name: str = '6425a28b8bf6f1e9b622352b.jpeg'
        mock_image: BytesIO = generate_image(
            filename=image_name,
            orientation=orientation,
            width=size[0],
            height=size[1],
            write_on_disc=False
        )

        media_output = MediaDownloadOutput(
            url=mock_image_internet_url,
            media_type=MediaType.images.value,
            data=mock_image,
            content_type=mock_image_content_type,
            width=size[0],
            height=size[1]
        )

        old_md5 = deepcopy(media_output.md5)
        assert mock_media_processor.resize(media=media_output)

        with Image.open(media_output.data) as new_img:
            new_orientation = new_img.getexif().get(274)
            width, height = new_img.size

        assert not new_orientation
        assert old_md5 != media_output.md5
        assert (width, height) == expected_size
        assert ImageDimension(
            width=media_output.width,
            height=media_output.height
        ) == ImageDimension(width=width, height=height)

    def test_when_resize_raise_exception_then_raise_resize_failed_exception(
        self,
        mock_media_processor: MediaProcessor,
        mock_expected_media_output: MediaDownloadOutput,
        valid_image_file_size: BytesIO,
        patch_media_processor_resize_image: Mock
    ):
        mock_expected_media_output.data = valid_image_file_size
        mock_expected_media_output.media_type = MediaType.images.value
        with pytest.raises(MediaResizeFailedException) as error:
            with settings_stub(IMAGE_RESIZE_ENABLE=True):
                with patch_media_processor_resize_image as mock_resize_image:
                    mock_resize_image.side_effect = Exception('Failed resize')
                    assert mock_media_processor.resize(
                        mock_expected_media_output
                    )

        assert mock_resize_image.called
        assert error.value.message == (
            f'Failed resize media type:images url:{mock_expected_media_output.url} '  # noqa
            'error:Failed resize'
        )
