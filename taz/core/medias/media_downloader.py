import logging
import time
from functools import cached_property
from io import BytesIO
from typing import List

from simple_settings import settings

from taz.constants import NON_DOWNLOADABLE_MEDIA_TYPES
from taz.core.medias.exceptions import MediaDownloadStrategyException
from taz.core.medias.media import MediaDownloadInput, MediaDownloadOutput
from taz.core.medias.strategies.base import DownloadMediaStrategy
from taz.core.medias.strategies.bucket_gcp import (
    DownloadMediaGenericStorageInternal
)
from taz.core.medias.strategies.internet import DownloadMediaInternet

logger = logging.getLogger(__name__)


class MediaDownloader:

    @cached_property
    def strategies(self) -> List[DownloadMediaStrategy]:
        defined_strategies: List[DownloadMediaStrategy] = [
            DownloadMediaGenericStorageInternal(
                bucket_name=bucket_name,
                starts_url=urls
            )
            for bucket_name, urls in settings.MEDIA_SERVICE_STRATEGY.items()
        ]
        defined_strategies.append(DownloadMediaInternet())
        return defined_strategies

    def _get_strategy(
        self,
        media: MediaDownloadInput
    ) -> DownloadMediaStrategy:
        for strategy in self.strategies:
            if strategy.is_this_strategy(media.url):
                return strategy

        raise MediaDownloadStrategyException(media=media)

    def download(self, media: MediaDownloadInput) -> MediaDownloadOutput:
        if not media.url:
            return MediaDownloadOutput(
                url=media.url,
                media_type=media.media_type,
                data=None,
            )

        if media.media_type in NON_DOWNLOADABLE_MEDIA_TYPES:
            logger.info(
                'Skipping non downloadable media '
                f'url:{media.url} type:{media.media_type}'
            )
            return MediaDownloadOutput(
                url=media.url,
                media_type=media.media_type,
                data=BytesIO(media.url.encode()),
                content_type='text/plain'
            )

        try:
            logger.debug(
                f'Downloading media type:{media.media_type} url:{media.url}'
            )
            strategy: DownloadMediaStrategy = self._get_strategy(media=media)
            start_time: float = time.time()
            media_bytes, content_type = strategy._download(media=media)
            logger.debug(
                f'Finished download media type:{media.media_type} '
                f'url:{media.url} in {time.time()-start_time:.3f}s'
            )
        except MediaDownloadStrategyException as e:
            logger.error(e.message)
            raise e

        return MediaDownloadOutput(
            url=media.url,
            media_type=media.media_type,
            data=media_bytes,
            content_type=content_type
        )
