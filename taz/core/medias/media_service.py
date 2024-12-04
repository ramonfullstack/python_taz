
import logging
from functools import cached_property

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

logger = logging.getLogger(__name__)


class MediaService:

    @cached_property
    def media_downloader(self) -> MediaDownloader:
        return MediaDownloader()

    @cached_property
    def media_processor(self) -> MediaProcessor:
        return MediaProcessor()

    def _fill_image_dimensions(
        self,
        media_output: MediaDownloadOutput
    ) -> None:
        if (
            media_output.media_type == MediaType.images.value and
            not media_output.is_empty()
        ):
            try:
                image_dimension: ImageDimension = (
                    self.media_processor.get_image_dimensions(
                        media=media_output
                    )
                )
                media_output.change_image_dimensions(image_dimension)
            except MediaDimensionsException as e:
                logger.warning(e.message)

    def download(self, media: MediaDownloadInput) -> MediaDownloadOutput:
        media_output: MediaDownloadOutput = self.media_downloader.download(
            media=media
        )
        self._fill_image_dimensions(media_output=media_output)
        return media_output

    def download_and_resize(
        self,
        media: MediaDownloadInput
    ) -> MediaDownloadOutput:
        try:
            media_output: MediaDownloadOutput = self.download(media=media)
            if media_output.is_empty():
                return media_output

            if self.media_processor.resize(media=media_output):
                logger.debug(
                    f'Successfully resize image type:{media.media_type} '
                    f'url:{media.url}'
                )
            return media_output
        except MediaResizeFailedException as e:
            logger.error(f'Skipping resize image because {e.message}')

        return media_output
