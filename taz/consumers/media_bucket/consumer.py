
import re

from maaslogger import base_logger
from redis import Redis
from simple_settings import settings

from taz.constants import MAGAZINE_LUIZA_SELLER_ID
from taz.consumers.core.brokers.stream import (
    PubSubBrokerRawEvent,
    PubSubRecordProcessor
)
from taz.consumers.core.google.storage import StorageManager
from taz.consumers.core.google.stream import StreamPublisherManager
from taz.core.common.list_media import ListMedia
from taz.utils import convert_id_to_nine_digits

SCOPE = 'media_bucket'
logger = base_logger.get_logger(__name__)


class MediaBucketProcessor(PubSubRecordProcessor):
    scope = SCOPE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = Redis(
            host=settings.REDIS_LOCK_SETTINGS['host'],
            port=settings.REDIS_LOCK_SETTINGS['port'],
            password=settings.REDIS_LOCK_SETTINGS.get('password')
        )
        self.cache_expire = {
            'media_process_ttl': int(
                settings.BUCKET_MEDIA_TTL
            ),
            'video_ttl': int(
                settings.BUCKET_MEDIA_VIDEO_TTL
            )
        }
        self.storage_manager = StorageManager(settings.MEDIA_LIST_BUCKET)
        self.__pubsub = StreamPublisherManager()

    def get_process_cache_key(self, sku):
        return f'media_bucket::{sku}'

    def process_message(self, event):
        event_attrs = event.attributes
        sku = self.get_event_sku(event_attrs)
        logger.info(f'processing sku:{sku} attrs:{event_attrs}',
                    detail={
                        "scope": self.scope,
                        "sku": sku,
                        "attrs": event_attrs,
                    })

        if (
            not sku or (
                len(sku) != settings.SKU_SIZE_VALIDATION_RANGE[0] and
                len(sku) != settings.SKU_SIZE_VALIDATION_RANGE[1]
            )
        ):
            logger.info(f'skipping {sku} with invalid value or size...',
                        detail={
                            "scope": self.scope,
                            "sku": sku
                        })
            return True

        process_lock_key = self.get_process_cache_key(sku)
        process_lock = self.cache.lock(
            process_lock_key,
            timeout=float(settings.BUCKET_MEDIA_LOCK_TIMEOUT)
        )
        if not process_lock.acquire(
            blocking=settings.BUCKET_MEDIA_LOCK_BLOCKING,
            blocking_timeout=float(settings.BUCKET_MEDIA_LOCK_ACQUIRE_TIMEOUT)
        ):
            return False

        logger.info(f'lock required for sku:{sku}',
                    detail={
                        "scope": self.scope,
                        "sku": sku
                    })
        paths = self.get_sku_media_paths(sku)
        payload = self.mount_payload(sku, paths)
        message = {
            'action': 'create',
            'data': payload
        }

        self.__pubsub.publish(
            ordering_key=f"{payload['seller_id']}/{payload['sku']}",
            content=message,
            topic_name=settings.PUBSUB_MEDIA_TOPIC_NAME,
            project_id=settings.PUBSUB_NOTIFY_PROJECT_ID
        )
        process_lock.release()
        logger.info(f'lock released for sku:{sku}',
                    detail={
                        "scope": self.scope,
                        "sku": sku
                    })
        return True

    def get_event_sku(self, event_attrs: dict):
        sku_path = event_attrs['objectId']
        logger.debug(
            f'event sku path:{sku_path}',
            detail={
                "scope": self.scope,
                "sku_path": sku_path
            }
        )
        sku_with_letter = sku_path.split('/')[-1].split('.')[0]
        sku = re.sub('[a-zA-Z]{1}$', '', sku_with_letter)
        logger.debug(f'event sku:{sku}')
        return convert_id_to_nine_digits(sku)

    def get_sku_media_paths(self, sku):
        paths = ListMedia.find_skus_paths(sku, self.storage_manager)
        if not paths:
            logger.warning(
                f'not found media sku:{sku}'.format(sku=sku),
                detail={
                    "scope": self.scope,
                    "sku": sku,
                }
            )

        logger.debug(
            f'get path:{paths} for sku:{sku}',
            detail={
                "scope": self.scope,
                "sku": sku
            }
        )
        return paths

    def mount_payload(self, sku, paths):
        payload = {
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'sku': sku,
            'images': paths['images'],
            'audios': paths['audios'],
            'podcasts': paths['podcasts'],
        }
        logger.debug(
            f'mounted sku:{sku} payload:{payload}',
            detail={
                "scope": self.scope,
                "sku": sku,
                "seller_id": MAGAZINE_LUIZA_SELLER_ID,
                "images": paths['images'],
                "audios": paths['audios'],
                "podcasts": paths['podcasts']
            }
        )
        return payload


class MediaBucketConsumer(PubSubBrokerRawEvent):
    scope = SCOPE
    record_processor_class = MediaBucketProcessor
    project_name = settings.GOOGLE_PROJECT_ID
