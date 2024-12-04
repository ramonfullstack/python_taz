import logging

from marshmallow import Schema, fields, validate
from simple_settings import settings

from taz.constants import MAGAZINE_LUIZA_SELLER_ID
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.google.storage import StorageManager
from taz.consumers.core.google.stream import StreamPublisherManager
from taz.consumers.rebuild.scopes.base import BaseRebuild
from taz.core.common.list_media import ListMedia

logger = logging.getLogger(__name__)


class MediaRebuildSchema(Schema):
    seller_id = fields.String(
        validate=[validate.Length(min=1, max=250)],
        required=True
    )
    sku = fields.String()
    from_bucket = fields.Bool(
        required=False,
    )


class MediaRebuild(MongodbMixin, BaseRebuild):
    schema_class = MediaRebuildSchema
    scope = 'media_rebuild'
    collection_name = 'medias'
    origin = 'rebuild'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collection_medias = self.get_collection('medias')
        self.__pubsub = StreamPublisherManager()
        self.storage_manager = StorageManager(settings.MEDIA_LIST_BUCKET)

    def get_media_by_seller_and_sku(self, seller_id, sku):
        criteria = {
            'seller_id': seller_id,
            'sku': sku,
        }
        fields = {
            '_id': 0,
            'sku': 1,
            'seller_id': 1,
            'original_images': 1,
            'images': 1,
            'videos': 1,
            'audios': 1,
            'podcasts': 1,
        }
        media = self.collection_medias.find_one(
            criteria,
            fields,
            no_cursor_timeout=True
        )
        if not media or not media.get('original_images'):
            return None

        return {
            'sku': media.get('sku'),
            'seller_id': media.get('seller_id'),
            'images': media.get('original_images'),
            'videos': media.get('videos'),
            'audios': media.get('audios'),
            'podcasts': media.get('podcasts'),
        }

    def mount_media_payload(self, seller_id, sku):
        paths = ListMedia.find_skus_paths(sku, self.storage_manager)
        return {
            'sku': sku,
            'seller_id': seller_id,
            'images': paths.get('images', []),
            'audios': paths.get('audios', []),
            'podcasts': paths.get('podcasts', []),
        }

    def _rebuild(self, action, data):
        logger.info(
            'Starting media rebuild with action: {}, request:{}'
            .format(action, data)
        )

        seller_id = data.get('seller_id')
        sku = data.get('sku')
        if not seller_id or not sku:
            logger.warning(f'Invalid seller_id:{seller_id} or sku:{sku}')
            return False

        is_from_bucket = str(data.get('from_bucket', '')).lower() == 'true'
        if not is_from_bucket:
            media = self.get_media_by_seller_and_sku(seller_id, sku)
        elif seller_id != MAGAZINE_LUIZA_SELLER_ID:
            return False
        else:
            media = self.mount_media_payload(seller_id, sku)

        if not media:
            logger.info(
                'Media rebuild finished for {}/{}.'.format(seller_id, sku)
            )
            return True

        try:
            self._send_stream(media, action)
        except Exception as e:
            logger.exception(
                'Encountered an exception while '
                'rebuild medias for {}/{}: {}'.format(seller_id, sku, e)
            )
        return True

    def _send_stream(self, media, action):
        sku = media.get('sku')
        seller_id = media.get('seller_id')
        logger.info(
            'Media rebuild for sku:{sku} seller_id:{seller_id} '
            'medias:{scope}'
            .format(
                scope=self.scope,
                sku=sku,
                seller_id=seller_id,
            )
        )
        payload = {'origin': 'rebuild', **media}
        message = {
            'action': action,
            'data': payload
        }

        self.__pubsub.publish(
            ordering_key=f"{payload['seller_id']}/{payload['sku']}",
            content=message,
            topic_name=settings.PUBSUB_MEDIA_TOPIC_NAME,
            project_id=settings.PUBSUB_NOTIFY_PROJECT_ID
        )
