import json
import logging

from mongoengine import DynamicDocument
from mongoengine.queryset import DoesNotExist

from taz import constants
from taz.core.common.media import build_media, build_url_image

logger = logging.getLogger(__name__)


class MediaModel(DynamicDocument):
    meta = {
        'collection': 'medias',
        'shard_key': ('sku', 'seller_id',)
    }

    @classmethod
    def get_media(cls, seller_id, sku, product):
        try:
            payload = MediaModel.objects.get(seller_id=seller_id, sku=sku)
            media = json.loads(payload.to_json())

            medias = {}
            for media_type in constants.MEDIA_TYPES:
                if media_type not in media:
                    continue

                medias[media_type] = build_media(
                    sku,
                    product['title'],
                    product['reference'],
                    seller_id,
                    media_type,
                    media[media_type]
                )

            return medias

        except DoesNotExist:
            logger.debug('Media sku:{} seller:{} not found'.format(
                sku, seller_id
            ))

            return {}

    @classmethod
    def get_image_urls(cls, seller_id, sku, product):
        media = cls.get_media(seller_id, sku, product)
        return [build_url_image(image) for image in media.get('images') or []]
