import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from functools import cached_property, partial
from typing import Dict, List, Optional

from maaslogger import base_logger
from pymongo.results import UpdateResult
from simple_settings import settings
from slugify import slugify

from taz import constants
from taz.constants import (
    CREATE_ACTION,
    MAGAZINE_LUIZA_SELLER_ID,
    MEDIA_FAILURE_CODE,
    MEDIA_FAILURE_MESSAGE,
    MEDIA_PARTIAL_ERROR_CODE,
    MEDIA_PARTIAL_ERROR_MESSAGE,
    MEDIA_SUCCESS_CODE,
    MEDIA_SUCCESS_MESSAGE,
    NON_UPLOADABLE_MEDIA_TYPES,
    SOURCE_METABOOKS,
    SOURCE_METADATA_VERIFY,
    SOURCE_SMARTCONTENT,
    VALID_MEDIA_TYPES
)
from taz.consumers.core.brokers.stream import (
    ACKNOWLEDGE,
    PubSubBroker,
    PubSubRecordProcessorWithRequiredFields
)
from taz.consumers.core.cache.redis import CacheMixin
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.exceptions import (
    RequiredFieldException,
    RequiredNonEmptyFieldException
)
from taz.consumers.core.google.storage import StorageManager
from taz.consumers.core.google.stream import StreamPublisherManager
from taz.consumers.core.notification import Notification
from taz.core.medias.exceptions import (
    MediaBaseException,
    MediaNotFoundException,
    MediaUnprocessableException,
    TimedOutMediaException
)
from taz.core.medias.helpers import MediaHelper
from taz.core.medias.media import (
    MediaDownloadInput,
    MediaDownloadOutput,
    MediaType
)
from taz.core.medias.media_service import MediaService
from taz.core.notification.notification_sender import NotificationSender

logger = base_logger.get_logger(__name__)


SCOPE = 'media'
JSON_FILENAME = '{seller_id}/json/{sku}.json'
JSON_V2_FILENAME = '{seller_id}/json_v2/{sku}.json'
DOWNLOAD_SUCCESSFULLY: bool = True


class Media:
    __slots__ = [
        'seller_id',
        'sku',
        'media_type',
        'url',
        'md5',
        'content_type',
        'width',
        'height',
        'image_details',
        'entry_hash'
    ]

    def __init__(
        self,
        seller_id: str,
        sku: str,
        media_type: str,
        url: str,
        md5: Optional[str],
        content_type: Optional[str],
        entry_hash: Optional[str] = None
    ):
        self.seller_id = seller_id
        self.sku = sku
        self.media_type = media_type
        self.url = url
        self.md5 = md5
        self.content_type = content_type
        self.image_details = {}
        self.entry_hash = entry_hash


class MediaRecordProcessor(
    MongodbMixin,
    CacheMixin,
    PubSubRecordProcessorWithRequiredFields
):
    required_fields = ['seller_id', 'sku']
    required_fields_delete = ['seller_id', 'sku']

    max_threads_workers = int(settings.PROCESSOR_MAX_THREAD_WORKERS)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @cached_property
    def notification(self) -> 'Notification':
        return Notification()

    @cached_property
    def pubsub(self) -> 'StreamPublisherManager':
        return StreamPublisherManager()

    @cached_property
    def notification_sender(self) -> 'NotificationSender':
        return NotificationSender()

    @cached_property
    def medias(self):
        return self.get_collection('medias')

    @cached_property
    def enriched_products(self):
        return self.get_collection('enriched_products')

    @property
    def storage_manager(self):
        return StorageManager(settings.MEDIA_BUCKET)

    @classmethod
    def cache(cls):
        return cls.get_cache(cls)

    @cached_property
    def media_service(self):
        return MediaService()

    def process_message(self, message):
        try:
            action = message.get('action')
            data = message.get('data')
        except Exception as e:
            logger.warning(
                'Encountered a generic error: {error} scope: {scope} '
                'parsing data with message: {message}'.format(
                    error=e,
                    scope=self.scope,
                    message=message
                ),
                detail={
                    "scope": self.scope,
                    "error": e,
                    "message": message,
                }
            )
            return False

        try:
            if not data or not action:
                logger.error(
                    'Invalid data for scope: {scope}: {data}'.format(
                        scope=self.scope,
                        data=data
                    ),
                    detail={
                        "scope": self.scope,
                        "message": message,
                        "data": data
                    }
                )
                return False

            _action = action if not action == 'remove' else 'delete'
            if action in ['create', 'update', 'remove', 'delete']:
                logger.info(
                    'Processing action:{action} for scope:{scope} '
                    'with data:{data}'.format(
                        action=action,
                        scope=self.scope,
                        data=data
                    ),
                    detail={
                        "scope": self.scope,
                        "message": message,
                        "data": data
                    }
                )
                getattr(self, _action)(data)
            else:
                logger.warning(
                    'Unknown action {action} for scope {scope} '
                    'with data: {data}'.format(
                        action=action,
                        scope=self.scope,
                        data=data
                    ),
                    detail={
                        "scope": self.scope,
                        "message": message,
                        "data": data
                    }
                )
        except RequiredNonEmptyFieldException as e:
            logger.warning(
                'Required non empty field exception with action:{action} '
                'scope:{scope} error:{error}'.format(
                    action=action,
                    scope=self.scope,
                    error=e
                ),
                detail={
                    "scope": self.scope,
                    "error": e,
                    "message": message,
                    "data": data,
                    "action": action
                }
            )
        except Exception as e:
            logger.exception(
                'Encountered generic exception for action:{action} '
                'scope: {scope}, error:{error}'.format(
                    action=action,
                    scope=self.scope,
                    error=e
                ),
                detail={
                    "scope": self.scope,
                    "error": e,
                    "message": message,
                    "data": data,
                    "action": action
                }
            )
            return False

        return True

    def _validations(self, data, action):
        self._validate_required_fields(data, action)
        self._validate_required_non_empty_fields(data, action)

    def _validate_required_non_empty_fields(self, data, action):
        required_non_empty_fields = getattr(
            self, 'required_non_empty_fields_{}'.format(action)
        )
        required_non_empty_fields = (
            required_non_empty_fields or self.required_non_empty_fields
        )
        if not required_non_empty_fields:
            return

        empty_fields = [
            f for f in required_non_empty_fields
            if f not in data or not bool(data[f])
        ]
        if empty_fields:
            raise RequiredNonEmptyFieldException(
                empty_fields, self.scope, action, data
            )

    def _validate_required_fields(self, data, action):
        required_fields = getattr(self, 'required_fields_{}'.format(action))
        required_fields = required_fields or self.required_fields

        if not required_fields:
            return

        missing_fields = [
            field for field in required_fields
            if field not in data
        ]

        if missing_fields:
            logger.warning(
                'Required fields {fields} of scope {scope} is missing for '
                'action {action}'.format(
                    fields=missing_fields,
                    scope=self.scope,
                    action=action
                ),
                detail={
                    "scope": self.scope,
                    "fields": missing_fields,
                    "data": data,
                    "action": action
                }
            )

            raise RequiredFieldException(
                missing_fields, self.scope, action, data
            )

    def create(self, data):
        self._validations(data, 'create')
        self._create(data)

    def update(self, data):
        self._validations(data, 'update')
        self._update(data)

    def delete(self, data):
        self._validations(data, 'delete')
        self._delete(data)

    @staticmethod
    def is_empty_media(data: Dict):
        def validate_media_required_fields(field):
            return (
                field in data and
                data.get(field) is not None and
                isinstance(data[field], List) and
                len(data[field]) > 0
            )

        return not any(map(validate_media_required_fields, VALID_MEDIA_TYPES))

    def _check_has_necessary_process_images(
        self,
        saved_medias: Dict,
        message_data: Dict,
    ) -> Dict:
        message_images: List[Dict] = message_data.get('images') or []
        if not message_images:
            return {}

        verified_images: Dict = {
            image['url']: {'necessary_process': True}
            for image in message_images
        }

        saved_images: List[Dict] = saved_medias.get(
            'original', {}
        ).get('images', [])
        if not saved_images:
            return verified_images

        message_images = {
            image['url']: image['hash']
            for image in message_images
        }

        for image_detail, image in zip(
            saved_medias['image_details'],
            saved_images
        ):
            necessary_process: bool = (
                message_images.get(image['url']) != image['hash']
            )
            verified_images.setdefault(image['url'], {}).update({
                **image_detail,
                **{'necessary_process': necessary_process}
            })

        return verified_images

    def _has_changed_medias(
        self,
        saved_medias: Dict,
        new_medias: Dict
    ) -> bool:
        if not saved_medias or 'original' not in saved_medias:
            return True

        return saved_medias != new_medias

    def _create(self, data: Dict) -> bool:
        if not data or self.is_empty_media(data):
            logger.info(f'Skipping empty media:{data}')
            return ACKNOWLEDGE

        seller_id, sku, tracking_id, origin = (
            slugify(data['seller_id']),
            data['sku'],
            data.get('tracking_id'),
            data.get('origin')
        )

        logger.info(
            f'Request item with sku:{sku}'
            f'seller_id:{seller_id} payload:{data}',
            detail={
                "scope": self.scope,
                "sku": sku,
                "seller_id": seller_id,
            }
        )

        skip_reason = self._process_is_not_allowed(data)
        if skip_reason:
            logger.warning(skip_reason)
            self.notification_sender.notify_patolino_about_unfinished_process( # noqa
                data,
                constants.UPDATE_ACTION,
                skip_reason,
                constants.MEDIA_UNFINISHED_PROCESS,
                tracking_id
            )
            return ACKNOWLEDGE

        saved_medias: Dict = self.medias.find_one(
            {'seller_id': seller_id, 'sku': sku},
            {'_id': 0}
        ) or {}

        verified_images: Dict = self._check_has_necessary_process_images(
            saved_medias=saved_medias, message_data=data
        )

        medias = self._build_media_list(data)

        process_media_result = self._process_medias(
            medias, verified_images
        )

        medias_payload: Dict = self._mount_medias_payload(
            seller_id=seller_id, sku=sku, medias=medias
        )

        if origin != 'rebuild' and not self._has_changed_medias(
            saved_medias=saved_medias,
            new_medias=medias_payload
        ):
            logger.info(
                f'Unmodified media for sku:{sku} '
                f'seller_id:{seller_id} origin:{origin} data:{data}'
            )
            self.notification_sender.notify_patolino_about_unfinished_process(
                data,
                constants.UPDATE_ACTION,
                constants.MEDIA_UNFINISHED_MESSAGE,
                constants.MEDIA_UNFINISHED_PROCESS,
                tracking_id
            )
            return ACKNOWLEDGE

        updated_medias: Dict = self.register_medias(
            seller_id, sku, medias_payload, origin
        )

        if updated_medias:
            self._send_acme_notification(
                action=constants.CREATE_ACTION,
                payload=updated_medias
            )

            self._notify(
                action=CREATE_ACTION,
                seller_id=seller_id,
                sku=sku,
                tracking_id=tracking_id
            )
            self._send_notification(
                seller_id,
                sku,
                process_media_result,
                tracking_id
            )
            return ACKNOWLEDGE

        self.notification_sender.notify_patolino_about_unfinished_process(
            data,
            constants.UPDATE_ACTION,
            constants.MEDIA_UNFINISHED_MESSAGE,
            constants.MEDIA_UNFINISHED_PROCESS,
            tracking_id
        )
        return ACKNOWLEDGE

    def _update(self, data: Dict) -> bool:
        return self.create(data)

    def _delete(self, data: Dict) -> bool:
        seller_id = slugify(data['seller_id'])
        sku = data['sku']

        media_types = [i for i in data.keys() if i in VALID_MEDIA_TYPES]

        logger.info(
            f'Request delete item with sku:{sku} '
            f'seller_id:{seller_id} payload:{data}',
            detail={
                "scope": self.scope,
                "sku": sku,
                "seller_id": seller_id,
                "data": data
            }
        )

        self._delete_medias(seller_id, sku, media_types)
        self._delete_json(data)

        self._send_acme_notification(
            action=constants.DELETE_ACTION,
            payload={
                'sku': sku,
                'seller_id': seller_id
            }
        )
        return ACKNOWLEDGE

    def _process_is_not_allowed(self, data: Dict) -> Optional[str]:
        seller_id, sku = slugify(data['seller_id']), data['sku']
        enriched_product = self.enriched_products.find(
            {
                'sku': sku,
                'seller_id': seller_id,
                'source': {
                    '$in': [SOURCE_METABOOKS, SOURCE_SMARTCONTENT]
                }
            },
            {'_id': 0, 'source': 1}
        )

        enriched_product = list(enriched_product)
        sources = [a['source'] for a in enriched_product]
        return self._skip_sources(sources, data)

    @staticmethod
    def _skip_sources(sources: List, data: Dict) -> Optional[str]:
        sku = data.get('sku')
        seller_id = data.get('seller_id')

        if SOURCE_METABOOKS in sources:
            if (
                SOURCE_SMARTCONTENT in sources and
                data.get('source') == SOURCE_METADATA_VERIFY
            ):
                return (
                    f'Message was skipped because the product sku:{sku} '
                    f'seller_id:{seller_id} was enriched by multiple sources '
                    'including Smarcontent, which is the ultimate source '
                    'for 1P products'
                )

            if (
                SOURCE_SMARTCONTENT not in sources and
                data.get('source') != SOURCE_METADATA_VERIFY
            ):
                return (
                    f'Message was skipped because the product sku:{sku} '
                    f'seller_id:{seller_id} was enriched by Metabooks '
                    'and no Smarcontent'
                )

        return None

    def _mount_medias_payload(
        self,
        seller_id: str,
        sku: str,
        medias: defaultdict
    ) -> Dict:
        document = {
            key: [
                (
                    f'{i.md5}'
                    f'{MediaHelper.get_media_extension(i.media_type, i.url)}'
                )
                for i in items
            ]
            for key, items in medias.items()
            if key != MediaType.videos.value
        }

        if MediaType.videos.value in medias:
            document[MediaType.videos.value] = []
            for i in medias[MediaType.videos.value]:
                if not MediaHelper.video_url_validation(i.url):
                    logger.warning(
                        f'Video with invalid url:{i.url} for '
                        f'sku:{sku} seller_id:{seller_id}',
                        detail={
                            "scope": self.scope,
                            "sku": sku,
                            "seller_id": seller_id,
                            "url_video": i.url
                        }
                    )
                    continue

                document['videos'].append(i.url)

        if MediaType.images.value in document:
            image_details: List[Dict] = []
            original_images: List[Dict] = []
            for image in medias.get(MediaType.images.value) or []:
                original_images.append(
                    {'url': image.url, 'hash': image.entry_hash}
                )
                if image.image_details:
                    image_details.append(image.image_details)

            document['image_details'] = image_details
            document['original'] = {'images': original_images}
            document['original_images'] = [
                image['url'] for image in original_images
            ]

        document.update({'seller_id': seller_id, 'sku': sku})
        return document

    def register_medias(
        self,
        seller_id: str,
        sku: str,
        document: Dict,
        origin: Optional[str] = None
    ) -> Optional[Dict]:
        if not document:
            logger.warning(
                f'No valid medias for sku:{sku} seller_id:{seller_id}',
                detail={
                    "scope": self.scope,
                    "sku": sku,
                    "seller_id": seller_id,
                }
            )

        document.update({'seller_id': seller_id, 'sku': sku})

        logger.info(f'Registering media from sku:{sku} seller_id:{seller_id}',
                    detail={
                        "scope": self.scope,
                        "sku": sku,
                        "seller_id": seller_id,
                    })

        has_update: bool = self._save(document)
        must_send_notification: bool = has_update or (origin == 'rebuild')
        if must_send_notification:
            logger.info(
                f'Media saved successfully for sku:{sku} '
                f'seller_id:{seller_id} document:{document}',
                detail={
                    "scope": self.scope,
                    "sku": sku,
                    "document": document,
                }
            )
        else:
            logger.info(
                f'Unmodified media for sku:{sku} '
                f'seller_id:{seller_id} document:{document}',
                detail={
                    "scope": self.scope,
                    "sku": sku,
                    "seller_id": seller_id,
                    "document": document
                }
            )

        return must_send_notification

    def _save(self, data: Dict) -> bool:
        seller_id, sku = data['seller_id'], data['sku']
        result: UpdateResult = self.medias.update_one(
            {'sku': sku, 'seller_id': seller_id},
            {'$set': data},
            upsert=True
        )

        return (
            not result or
            result.modified_count != 0 or
            result.upserted_id is not None
        )

    def _delete_json(self, data: Dict) -> None:
        seller_id, sku = data['seller_id'], data['sku']

        filename = JSON_V2_FILENAME.format(
            seller_id=seller_id,
            sku=slugify(sku)
        )

        logger.info(f'Deleting the file:{filename}',
                    detail={
                        "scope": self.scope,
                        "sku": sku,
                        "seller_id": seller_id,
                        "filename": filename
                    })

        self.storage_manager.delete(filename)

    def _delete_medias(
        self,
        seller_id: str,
        sku: str,
        media_types: List
    ) -> None:
        delete_method = partial(self._delete_media, seller_id, sku)
        with ThreadPoolExecutor(
            max_workers=self.max_threads_workers
        ) as executor:
            futures = {
                executor.submit(delete_method, media_type): media_type
                for media_type in media_types
            }

        for future in as_completed(futures):
            future.result()
            media_type = futures[future]

        logger.info(
            f'Successfully deleted all medias of sku:{sku} '
            f'seller_id:{seller_id} type:{media_type} from Storage',
            detail={
                "scope": self.scope,
                "sku": sku,
                "seller_id": seller_id,
                "media_type": media_type
            }
        )

    def _delete_media(self, seller_id: str, sku: str, media_type: str) -> None:
        if media_type in NON_UPLOADABLE_MEDIA_TYPES:
            return

        directory = f'{seller_id}/{media_type}/{slugify(sku)}/'
        self.storage_manager.delete(directory)

        logger.info(
            f'Successfully deleted sku:{sku} seller_id:{seller_id} '
            f'type:{media_type} from Storage',
            detail={
                "scope": self.scope,
                "sku": sku,
                "seller_id": seller_id,
                "media_type": media_type
            }
        )

    def _process_medias(
        self,
        medias: defaultdict,
        verified_images: Dict
    ) -> List[Dict]:
        with ThreadPoolExecutor(
            max_workers=self.max_threads_workers
        ) as executor:
            futures = {}
            for media_list in medias.values():
                for media in media_list:
                    futures[
                        executor.submit(
                            self._process_media,
                            media,
                            (
                                verified_images.get(media.url) or {}
                                if media.media_type == MediaType.images.value
                                else {}
                            )
                        )
                    ] = media

        process_media_result = []
        for future in as_completed(futures):
            media: Media = futures[future]
            success: bool = future.result()
            process_media_result.append({
                'url': media.url,
                'success': success
            })

        return process_media_result

    def _send_notification(
        self,
        seller_id: str,
        sku: str,
        process_media_result: List,
        tracking_id: str = None
    ) -> None:
        message = MEDIA_PARTIAL_ERROR_MESSAGE
        code = MEDIA_PARTIAL_ERROR_CODE

        if self._all_successfully_processed(process_media_result):
            message = MEDIA_SUCCESS_MESSAGE
            code = MEDIA_SUCCESS_CODE
        elif self._all_unsuccessfully_processed(process_media_result):
            message = MEDIA_FAILURE_MESSAGE
            code = MEDIA_FAILURE_CODE

        self.notification_sender.send(
            sku=sku,
            seller_id=seller_id,
            code=code,
            message=message,
            payload={'medias': process_media_result},
            tracking_id=tracking_id
        )

    @staticmethod
    def _all_successfully_processed(process_media_result: List) -> bool:
        return all([result['success'] for result in process_media_result])

    @staticmethod
    def _all_unsuccessfully_processed(process_media_result: List) -> bool:
        return all([not result['success'] for result in process_media_result])

    def _process_media(self, media: Media, verified_image: Dict) -> bool:
        if media.media_type in NON_UPLOADABLE_MEDIA_TYPES:
            logger.info(
                f'Media type not uploadable. Skip media process for '
                f'sku:{media.sku} seller_id:{media.seller_id} payload:{media}',
                detail={
                    "scope": self.scope,
                    "sku": media.sku,
                    "seller_id": media.seller_id,
                    "media": media
                }
            )
            return DOWNLOAD_SUCCESSFULLY

        if not media.url:
            logger.info(
                f'Media without url. Skip media process for '
                f'sku:{media.sku} seller_id:{media.seller_id} payload:{media}',
                detail={
                    "scope": self.scope,
                    "sku": media.sku,
                    "seller_id": media.seller_id,
                    "media": media
                }
            )
            return True

        try:
            media_download_output: MediaDownloadOutput = (
                self.media_service.download_and_resize(
                    MediaDownloadInput(
                        url=media.url,
                        media_type=media.media_type
                    )
                )
            )
        except (
            MediaUnprocessableException,
            MediaNotFoundException,
            TimedOutMediaException
        ) as e:
            logger.error(
                f'Skipping upload media sku:{media.sku} '
                f'seller_id:{media.seller_id}. Message:{e.message}',
                detail={
                    "scope": self.scope,
                    "sku": media.sku,
                    "seller_id": media.seller_id,
                    "message": e.message
                }
            )
            return DOWNLOAD_SUCCESSFULLY
        except MediaBaseException as e:
            logger.warning(
                f'Could not process media for sku:{media.sku} '
                f'seller_id:{media.seller_id} type:{media.media_type} '
                f'url:{media.url} md5:{media.md5}. Message:{e.message}',
                detail={
                    "scope": self.scope,
                    "sku": media.sku,
                    "seller_id": media.seller_id,
                    "md5": media.md5,
                    "url": media.url,
                    "media_type": media.media_type
                }
            )
            raise e

        if media_download_output.is_empty():
            logger.warning(
                f'Empty media sku:{media.sku} seller_id:{media.seller_id} '
                f'url:{media.url}',
                detail={
                    "scope": self.scope,
                    "sku": media.sku,
                    "seller_id": media.seller_id,
                    "md5": media.md5,
                    "url": media.url,
                    "media_type": media.media_type
                }
            )
            return DOWNLOAD_SUCCESSFULLY

        media.content_type = media_download_output.content_type
        media.md5 = media_download_output.md5
        if media.media_type == 'images':
            media.image_details = {
                'dimensions': {
                    'width': media_download_output.width,
                    'height': media_download_output.height
                },
                'hash': media_download_output.mount_file_name()
            }

        self._upload_media(media, media_download_output)
        media_download_output.data.close()

        logger.info(
            f'Successfully processed media for sku:{media.sku} '
            f'seller_id:{media.seller_id} type:{media.media_type} '
            f'url:{media.url} md5:{media.md5}',
            detail={
                "scope": self.scope,
                "sku": media.sku,
                "seller_id": media.seller_id,
                "md5": media.md5,
                "url": media.url,
                "media_type": media.media_type
            }
        )

        return DOWNLOAD_SUCCESSFULLY

    def _upload_media(
        self,
        media: Media,
        media_downloaded: MediaDownloadOutput
    ) -> None:
        file_name: str = (
            f'{media.seller_id}/{media.media_type}/'
            f'{slugify(media.sku)}/{media_downloaded.mount_file_name()}'
        )

        logger.info(
            f'Uploading sku:{media.sku} seller_id:{media.seller_id} '
            f'filename:{file_name} of type content_type:{media.content_type}',
            detail={
                "scope": self.scope,
                "sku": media.sku,
                "seller_id": media.seller_id,
                "md5": media.md5,
                "url": media.url,
                "media_type": media.media_type,
                "content_type": media.content_type
            }
        )

        self.storage_manager.upload(
            media_downloaded.data,
            file_name,
            content_type=media.content_type
        )

    @staticmethod
    def _build_media_list(data: Dict) -> defaultdict:
        sku = slugify(data['sku'])
        seller_id = slugify(data['seller_id'])
        medias = defaultdict(list)

        for media_type, items in data.items():
            if media_type not in VALID_MEDIA_TYPES:
                continue

            medias[media_type] = []
            for item in items:
                url: str = item['url'] if isinstance(item, dict) else item
                medias[media_type].append(
                    Media(
                        seller_id=seller_id,
                        sku=sku,
                        media_type=media_type,
                        url=url,
                        md5=None,
                        content_type=None,
                        entry_hash=(
                            item['hash']
                            if media_type == MediaType.images.value
                            else None
                        )
                    )
                )

        if (
            'images' in medias and len(medias['images']) >= 1 and
            seller_id == MAGAZINE_LUIZA_SELLER_ID
        ):
            is_main_seller_image = (
                settings.MAGAZINELUIZA_IMG_URL in medias['images'][0].url
            )
            if is_main_seller_image:
                medias['images'] = sorted(
                    medias['images'], key=lambda i: i.url
                )

        return medias

    def _send_acme_notification(self, action: str, payload: Dict) -> None:
        message: Dict = deepcopy(payload)
        message.update({'message_timestamp': time.time(), 'action': action})
        for delete_key in ('_id', 'image_details', 'original'):
            message.pop(delete_key, None)

        seller_id = message.get('seller_id')
        sku = message.get('sku')
        try:
            self.pubsub.publish(
                content=message,
                topic_name=settings.PUBSUB_MEDIA_EXPORT_TOPIC_NAME,
                project_id=settings.PUBSUB_NOTIFY_PROJECT_ID
            )
            logger.info(
                f'Image sku:{sku} seller_id:{seller_id} sent successfully '
                f'for topic:{settings.PUBSUB_MEDIA_EXPORT_TOPIC_NAME} '
                f'with action:{action}',
                detail={
                    "scope": self.scope,
                    "sku": sku,
                    "seller_id": seller_id,
                    "action": action
                }
            )
        except Exception as e:
            logger.error(
                f'Failed to sent image sku:{sku} seller_id:{seller_id} '
                f'on topic:{settings.PUBSUB_MEDIA_EXPORT_TOPIC_NAME} with '
                f'error:{e} payload:{message}',
                detail={
                    "scope": self.scope,
                    "sku": sku,
                    "seller_id": seller_id,
                    "topic": settings.PUBSUB_MEDIA_EXPORT_TOPIC_NAME,
                    "message": message
                }
            )
            raise

    def _notify(
        self,
        action: str,
        seller_id: str,
        sku: str,
        navigation_id: str = None,
        tracking_id: str = None
    ):
        payload = {
            'navigation_id': navigation_id,
            'sku': sku,
            'seller_id': seller_id,
            'tracking_id': tracking_id
        }
        self.notification.put(payload, self.scope, action, self.scope, False)


class MediaConsumer(PubSubBroker):
    project_name = settings.GOOGLE_PROJECT_ID
    scope = SCOPE
    record_processor_class = MediaRecordProcessor
