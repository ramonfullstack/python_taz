from functools import cached_property
from io import BytesIO
from typing import Tuple

from PIL import Image, ImageOps
from simple_settings import settings

from taz.core.medias.exceptions import (
    MediaDimensionsException,
    MediaResizeFailedException
)
from taz.core.medias.media import (
    ImageDimension,
    MediaDownloadOutput,
    MediaType
)

Image.MAX_IMAGE_PIXELS = settings.MEDIA_MAX_IMAGE_PIXELS


class MediaProcessor:

    @cached_property
    def resize_algo(self):
        try:
            return Image.Resampling.HAMMING
        except AttributeError:
            return Image.HAMMING

    def _get_resize_aspect_ratio(self, width: int, height: int) -> Tuple:
        if width >= height:
            wpercent = settings.IMAGE_RESIZE_MAX_WIDTH / float(width)
            hsize = int((float(height) * float(wpercent)))
            return (settings.IMAGE_RESIZE_MAX_WIDTH, hsize)
        else:
            wpercent = settings.IMAGE_RESIZE_MAX_WIDTH / float(height)
            hsize = int((float(width) * float(wpercent)))
            return (hsize, settings.IMAGE_RESIZE_MAX_WIDTH)

    def _should_resize_image(self, width: int, height: int) -> bool:
        return (
            width > settings.IMAGE_RESIZE_MAX_WIDTH or
            height > settings.IMAGE_RESIZE_MAX_HEIGHT
        )

    def _make_image_resize(self, image: Image) -> Image:
        new_size: Tuple[float, float] = self._get_resize_aspect_ratio(
            width=image.width,
            height=image.height
        )
        return image.resize(new_size, self.resize_algo)

    def _resize_image(
        self,
        media: MediaDownloadOutput,
        enable_white_background: bool = False
    ) -> Tuple[BytesIO, ImageDimension]:
        quality = int(settings.IMAGE_RESIZE_QUALITY)
        new_img = BytesIO()

        with Image.open(media.data) as image:
            image = ImageOps.exif_transpose(image)

            if enable_white_background:
                im: Image = image.convert('RGBA')
                new_image = Image.new('RGBA', image.size, 'WHITE')
                new_image.paste(im, mask=im)
                im: Image = new_image.convert('RGB')
                new_image.close()
            else:
                im: Image = image.convert('RGB')

            if self._should_resize_image(im.width, im.height):
                im: Image = self._make_image_resize(im)

            im.save(new_img, optimize=True, quality=quality, format='JPEG')

        media.data.close()
        return new_img, ImageDimension(width=im.width, height=im.height)

    def resize(self, media: MediaDownloadOutput) -> bool:
        if (
            media.media_type != MediaType.images.value or
            not bool(settings.IMAGE_RESIZE_ENABLE) or
            media.is_empty()
        ):
            return False

        enable_white_background: bool = (
            bool(settings.IMAGE_TRANSPARENCY_ENABLE) and
            media.is_image_png()
        )

        try:
            img_resized, image_dimension = self._resize_image(
                media=media,
                enable_white_background=enable_white_background
            )
        except Exception as e:
            raise MediaResizeFailedException(media=media, error=e)

        media.change_image_data(
            data=img_resized,
            width=image_dimension.width,
            height=image_dimension.height
        )
        return True

    def get_image_dimensions(
        self,
        media: MediaDownloadOutput
    ) -> ImageDimension:
        try:
            with Image.open(media.data) as img:
                return ImageDimension(img.width, img.height)
        except Exception as e:
            raise MediaDimensionsException(media=media, error=e)
