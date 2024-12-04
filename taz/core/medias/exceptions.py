from typing import Optional

from taz.core.medias.media import MediaDownloadInput, MediaDownloadOutput


class MediaBaseException(Exception):
    def _format_message(self, message: str, error: Optional[Exception]) -> str:
        return message if not error else f'{message} error:{error}'

    def __init__(
        self,
        media: MediaDownloadInput,
        error: Optional[Exception] = None
    ):
        self.media = media
        self.message = self._format_message(
            message=(
                f'An exception for media type:{media.media_type} '
                f'url:{media.url}'
            ),
            error=error
        )


class MediaWithoutContentType(MediaBaseException):
    def __init__(
        self,
        media: MediaDownloadInput,
        error: Optional[Exception] = None
    ):
        super().__init__(media, error)
        self.message = self._format_message(
            message=(
                f'Cannot determine content-type of type:{media.media_type} '
                f'url:{media.url}'
            ),
            error=error
        )


class MediaUnprocessableException(MediaBaseException):
    def __init__(
        self,
        media: MediaDownloadInput,
        error: Optional[Exception] = None
    ):
        super().__init__(media, error)
        self.message = self._format_message(
            message=(
                f'Could not process the media type:{media.media_type} '
                f'url:{media.url}'
            ),
            error=error
        )


class MediaGenericDownloadException(MediaBaseException):
    def __init__(
        self,
        media: MediaDownloadInput,
        error: Optional[Exception] = None
    ):
        super().__init__(media, error)
        self.message = self._format_message(
            message=(
                'An error occurred while downloading media '
                f'type:{media.media_type} url:{media.url}'
            ),
            error=error
        )


class MediaResizeFailedException(MediaBaseException):
    def __init__(
        self,
        media: MediaDownloadOutput,
        error: Optional[Exception] = None
    ):
        super().__init__(media, error)
        self.message = self._format_message(
            message=(
                f'Failed resize media type:{media.media_type} url:{media.url}'
            ),
            error=error
        )


class MediaDimensionsException(MediaBaseException):
    def __init__(
        self,
        media: MediaDownloadInput,
        error: Optional[Exception] = None
    ):
        super().__init__(media, error)
        self.message = self._format_message(
            message=(
                f'Error getting dimensions from type:{media.media_type} '
                f'url:{media.url}'
            ),
            error=error
        )


class MediaNotFoundException(MediaBaseException):
    def __init__(
        self,
        media: MediaDownloadInput,
        error: Optional[Exception] = None
    ):
        super().__init__(media, error)
        self.message = self._format_message(
            message=(
                f'Not found media type:{media.media_type} url:{media.url}'
            ),
            error=error
        )


class MediaContentException(MediaBaseException):
    def __init__(
        self,
        media: MediaDownloadInput,
        error: Optional[Exception] = None
    ):
        super().__init__(media, error)
        self.message = self._format_message(
            message=(
                f'Could not process the media type:{media.media_type} '
                f'url:{media.url}'
            ),
            error=error
        )


class TimedOutMediaException(MediaBaseException):
    def __init__(
        self,
        media: MediaDownloadInput,
        error: Optional[Exception] = None
    ):
        super().__init__(media, error)
        self.message = self._format_message(
            message=(
                f'Could not download the media type:{media.media_type} '
                f'url:{media.url} because is timed out.'
            ),
            error=error
        )


class MediaDownloadStrategyException(MediaBaseException):
    def __init__(
        self,
        media: MediaDownloadInput,
        error: Optional[Exception] = None
    ):
        super().__init__(media, error)
        self.message = self._format_message(
            message=(
                f'Strategy not defined for media type:{media.media_type} '
                f'url:{media.url}'
            ),
            error=error
        )
