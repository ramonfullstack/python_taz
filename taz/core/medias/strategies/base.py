from abc import abstractmethod
from io import BytesIO
from typing import List, Optional, Tuple

from taz.core.medias.media import MediaDownloadInput


class DownloadMediaStrategy:
    def __init__(self, starts_url: str) -> None:
        self.starts_url: List[str] = [
            url.strip()
            for url in starts_url.split(',') or []
            if url.strip()
        ]

    @abstractmethod
    def _download(
        self,
        media: MediaDownloadInput
    ) -> Tuple[Optional[BytesIO], Optional[str]]:
        pass

    def is_this_strategy(self, url: str) -> bool:
        return any(
            url.startswith(start_url)
            for start_url in self.starts_url
        )
