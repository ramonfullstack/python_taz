import logging
from functools import cached_property
from typing import Dict

from taz import constants
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.core.common.media import build_media

logger = logging.getLogger(__name__)


class Scope(MongodbMixin):
    name = 'media'

    def __init__(
        self,
        sku: str,
        seller_id: str,
        **kwargs
    ):
        self.__sku = sku
        self.__seller_id = seller_id

    @cached_property
    def medias(self):
        return self.get_collection('medias')

    def get_data(self):
        media = self.medias.find_one(
            {
                'sku': self.__sku,
                'seller_id': self.__seller_id
            },
            {
                '_id': 0
            }
        )

        if not media:
            logger.warning(
                f'Media not found with scope:{self.name} '
                f'sku:{self.__sku} seller_id:{self.__seller_id}'
            )
            return []

        for media_type in constants.MEDIA_TYPES:
            if media_type in media:
                media[media_type] = build_media(
                    self.__sku,
                    'titulo',
                    'descricao',
                    self.__seller_id,
                    media_type,
                    media[media_type]
                )

        self.__format_payload(media)
        return media

    @staticmethod
    def __format_payload(media: dict) -> None:
        for field in {
            'seller_id', 'sku', 'images', 'image_details',
            'original_images', 'audios', 'podcasts', 'videos'
        }:
            media[field] = media.get(field)

        medias_original: Dict = media.pop('original', {})
        if medias_original:
            media['original_images'] = [
                image['url'] for image in medias_original.get('images') or []
            ]
