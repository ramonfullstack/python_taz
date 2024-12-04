import datetime
import hashlib
import json
from copy import deepcopy
from io import BytesIO
from logging import StreamHandler
from typing import Dict, List
from unittest.mock import ANY, Mock, call, patch
from uuid import uuid4 as uuid

import pytest
import requests
from PIL import Image
from pymongo.collection import Collection
from redis import Redis
from simple_settings.utils import settings, settings_stub
from slugify import slugify

from taz.constants import (
    CREATE_ACTION,
    DELETE_ACTION,
    MAGAZINE_LUIZA_SELLER_ID,
    MEDIA_SUCCESS_CODE,
    MEDIA_SUCCESS_MESSAGE,
    MEDIA_UNFINISHED_PROCESS,
    NON_DOWNLOADABLE_MEDIA_TYPES,
    NON_UPLOADABLE_MEDIA_TYPES,
    SOURCE_METABOOKS,
    SOURCE_METADATA_VERIFY,
    SOURCE_SMARTCONTENT,
    UPDATE_ACTION,
    VALID_MEDIA_TYPES
)
from taz.consumers.media.consumer import Media, MediaRecordProcessor
from taz.core.medias.exceptions import (
    MediaNotFoundException,
    MediaUnprocessableException,
    MediaWithoutContentType,
    TimedOutMediaException
)
from taz.core.medias.media import MediaDownloadOutput, MediaType
from taz.core.medias.media_service import MediaService
from taz.core.medias.tests.conftest import generate_image, make_image_file_size


class TestMediaRecordProcessor:

    IMAGE_HASH = 'bc92c770ad72fc410374a470612b9747'

    @pytest.fixture
    def sku(self):
        return str(uuid())

    @pytest.fixture
    def record_processor(self):
        return MediaRecordProcessor('media')

    @pytest.fixture
    def patch_media_service_download_and_resize(self):
        return patch.object(MediaService, 'download_and_resize')

    @pytest.fixture
    def fake_record_processor(self, record_processor):
        record_processor._create = Mock(side_effect=Exception())
        return record_processor

    @pytest.fixture
    def medias_collection(self, mongo_database):
        return mongo_database.get_collection('medias')

    @pytest.fixture
    def raw_products(self, mongo_database):
        return mongo_database.get_collection('raw_products')

    @pytest.fixture
    def patch_resize_image(self):
        return patch.object(MediaRecordProcessor, '_resize_image')

    @pytest.fixture
    def patch_enriched_products(self):
        return patch.object(MediaRecordProcessor, 'enriched_products')

    @pytest.fixture
    def patch_build_media_list(self):
        return patch.object(MediaRecordProcessor, '_build_media_list')

    @pytest.fixture
    def patch_storage_manager_property(self):
        return patch.object(MediaRecordProcessor, 'storage_manager')

    @pytest.fixture
    def patch_pubsub_property(self):
        return patch.object(MediaRecordProcessor, 'pubsub')

    @pytest.fixture
    def media_object(self, sku):
        return {
            'seller_id': 'foo',
            'sku': sku,
            'media_type': 'images',
            'url': 'google.com/murcho',
            'md5': 'murcho',
            'content_type': 'application/json'
        }

    @pytest.fixture
    def data_dict(self, sku):
        return {
            'seller_id': 'epoca',
            'sku': sku,
            'images': [],
            'videos': [],
            'audios': [],
            'podcasts': []
        }

    @pytest.fixture
    def mock_media_message_with_images(self, data_dict):
        return {
            'seller_id': data_dict['seller_id'],
            'sku': data_dict['seller_id'],
            'images': [{
                'url': 'https://api.metabooks.com/api/v1/cover/9788572551137?access_token=',  # noqa
                'hash': '0bc6b2bb-4dfc-4430-920a-f98be0191898'
            }]
        }

    @pytest.fixture
    def images(self):
        return [
            {
                'url': 'https://img.magazineluiza.com.br/1500x1500/x-088064100a.jpg',  # noqa
                'hash': self.IMAGE_HASH
            }, {
                'url': 'https://img.magazineluiza.com.br/1500x1500/x-088064100.jpg',  # noqa
                'hash': self.IMAGE_HASH
            }
        ]

    @pytest.fixture
    def data_dict_with_images(self, sku, images):
        return {
            'images': images,
            'podcasts': [],
            'audios': [],
            'seller_id': 'Magazineluiza',
            'videos': [],
            'sku': sku
        }

    @pytest.fixture
    def data_dict_with_invalid_images(self, sku):
        return {
            'images': [
                {
                    'url': 'https://img.magazineluiza.com.br/teste.jpg',
                    'hash': self.IMAGE_HASH
                },
                {
                    'url': 'https://img.magazineluiza.com.br/testea.jpg',
                    'hash': self.IMAGE_HASH
                }
            ],
            'podcasts': [],
            'audios': [],
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'videos': [],
            'sku': sku
        }

    @pytest.fixture
    def data_dict_with_podcast(self, sku, images):
        return {
            'images': [images[0]],
            'podcasts': ['https://img.magazineluiza.com.br/podcast/2190064.mp3'],  # noqa
            'audios': [],
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'videos': [],
            'sku': sku
        }

    @pytest.fixture
    def data_dict_with_metabooks_images(self, sku):
        return {
            'images': [
                {
                    'url': 'https://taz-metadata-images-sandbox.magalu.com/metabooks/9788580576580/9788580576580.jpg',  # noqa
                    'hash': 'd97b8cf0047b406921b9cd5cdc809834'
                },
                {
                    'url': 'https://taz-metadata-images-sandbox.magalu.com/metabooks/9788580576580/9788580576580_imagensadicionais_02.jpg',  # noqa
                    'hash': 'b1d8b282a2ca57db2272f001ec7c426a'
                }
            ],
            'podcasts': [],
            'audios': [],
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'videos': [],
            'sku': sku
        }

    @pytest.fixture
    def mock_downloaded_metabooks_images(
        self,
        data_dict_with_metabooks_images
    ):
        images_md5 = [
            '88e89f5b8ff55ea42960b92851c39ade',
            'c68fa1dd38284eed43f5b7231b281f3e'
        ]
        return [
            MediaDownloadOutput(
                url=image['url'],
                media_type='images',
                data=generate_image(
                    filename=f'{md5}.jpg',
                    orientation=Image.TRANSPOSE,
                    write_on_disc=False
                ),
                content_type='image/jpg',
                md5=md5,
                width=100,
                height=100
            )
            for image, md5 in zip(
                data_dict_with_metabooks_images['images'],
                images_md5
            )
        ]

    @pytest.fixture
    def hashed_image(self):
        return '{}.jpg'.format(self.IMAGE_HASH)

    @pytest.fixture
    def pubsub_create_payload(self, sku, images, hashed_image):
        original_images = [x['url'] for x in images]
        return {
            'images': [
                hashed_image,
                hashed_image
            ],
            'videos': [],
            'audios': [],
            'podcasts': [],
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'sku': sku,
            'message_timestamp': 1502734827.997473,
            'original_images': sorted(original_images),
            'action': CREATE_ACTION
        }

    @pytest.fixture
    def pubsub_create_payload_with_podcast(self, sku, images, hashed_image):
        return {
            'images': [hashed_image],
            'videos': [],
            'audios': [],
            'podcasts': ['9d748005156d08ba7031d203ca49adc0.mp3'],
            'original_images': [images[0]['url']],
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'sku': sku,
            'message_timestamp': 1502734827.997473,
            'action': CREATE_ACTION
        }

    @pytest.fixture
    def pubsub_create_metabooks_payload(
        self,
        sku,
        data_dict_with_metabooks_images
    ):
        return {
            'images': [
                '8e54c3d53096e1c6f4154f198914a783.jpg',
                'c68fa1dd38284eed43f5b7231b281f3e.jpg'
            ],
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'sku': sku,
            'message_timestamp': 1502734827.997473,
            'original_images': [
                image['url']
                for image in data_dict_with_metabooks_images['images']
            ]
        }

    @pytest.fixture
    def pubsub_delete_payload(self, sku):
        return {
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'sku': sku,
            'message_timestamp': 1502734827.997473,
            'action': DELETE_ACTION
        }

    @pytest.fixture
    def image_queue_message(self):
        return {
            'action': 'create',
            'acme_id': '123456789',
            'images': ['a', 'b', 'c']
        }

    @pytest.fixture
    def mock_response_bytes(self):
        response = requests.Response()
        response.status_code = 200
        response.raw = make_image_file_size()
        response.headers = {'content-type': 'image/jpeg'}
        response.raw.release_conn = lambda: None
        return response

    @pytest.fixture
    def mock_downloaded_image(self):
        return MediaDownloadOutput(
            url='https://test.png',
            media_type='images',
            data=generate_image(
                filename='test.png',
                orientation=Image.TRANSPOSE,
                write_on_disc=False
            ),
            content_type='image/png',
            width=100,
            height=100
        )

    @pytest.fixture
    def mock_saved_medias(self, sku):
        return {
            'sku': sku,
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'images': ['https://image.com'],
            'videos': ['https://video.com'],
        }

    @pytest.fixture
    def mock_response_unsupported_media_type_error(self):
        return Mock(status_code=415)

    @pytest.fixture
    def hash_of_response_bytes(self, mock_response_bytes):
        md5 = hashlib.md5()
        md5.update(mock_response_bytes.raw.getbuffer())
        mock_response_bytes.raw.seek(0)

        return md5.hexdigest()

    @pytest.fixture(params=NON_DOWNLOADABLE_MEDIA_TYPES)
    def non_downloadable_media_type(self, request):
        return request.param

    @pytest.fixture(
        params=set(VALID_MEDIA_TYPES) - set(NON_DOWNLOADABLE_MEDIA_TYPES)
    )
    def downloadable_media_type(self, request):
        return request.param

    @pytest.fixture
    def product(self, raw_products, data_dict):
        product = {
            'sku': data_dict['sku'],
            'seller_id': data_dict['seller_id'],
            'navigation_id': '123456789',
            'title': 'título do produto'
        }
        raw_products.insert_one(product)
        return product

    @pytest.fixture
    def media_murcho_message_data(
        self,
        sku: str,
        mock_product_medias_message_data: Dict
    ):
        mock_product_medias_message_data.update(
            {'seller_id': 'murcho', 'sku': sku}
        )
        return mock_product_medias_message_data

    @pytest.fixture
    def media_from_db_expected_murcho(
        self,
        sku: str,
        mock_product_images_with_details: Dict
    ):
        mock_product_images_with_details.update(
            {'seller_id': 'murcho', 'sku': sku}
        )
        return mock_product_images_with_details

    def mount_expected_verified_images(
        self,
        saved_medias: Dict,
        necessary_process: bool = False
    ) -> Dict:
        return {
            image['url']: {
                **image_detail,
                **{'necessary_process': necessary_process}
            }
            for image_detail, image in zip(
                saved_medias['image_details'],
                saved_medias['original']['images']
            )
        }

    def test_record_processor_using_multi_process_without_broken_flow(
        self,
        record_processor: MediaRecordProcessor,
        data_dict: Dict,
        non_downloadable_media_type,
        patch_publish_manager: Mock,
    ):
        data_dict[non_downloadable_media_type].append('non_downloadable')
        message = {
            'data': data_dict,
            'action': 'create'
        }
        with patch_publish_manager:
            assert record_processor.process_message(
                message
            ) is True

    def test_multi_processor_record_processor_dont_checkpoint_if_some_exception_raise(  # noqa
        self,
        fake_record_processor: MediaRecordProcessor,
        data_dict: Dict,
        non_downloadable_media_type,
        patch_publish_manager
    ):
        data_dict['images'] = {'invalid': 'dict'}
        message = {
            'data': data_dict,
            'action': 'create'
        }
        with pytest.raises(Exception):
            with patch_publish_manager:
                assert fake_record_processor.process_message(
                    message
                ) is False

    def test_record_processor_dont_upload_non_downloadable_media(
        self,
        patch_storage_manager_upload,
        record_processor: MediaRecordProcessor,
        data_dict: Dict,
        non_downloadable_media_type,
        patch_publish_manager: Mock,
    ):
        data_dict[non_downloadable_media_type].append('non_downloadable')
        with patch_storage_manager_upload as mock_storage:
            with patch_publish_manager:
                record_processor.create(data_dict)

        assert mock_storage.call_count == 0

    def test_when_action_create_process_with_success_then_should_send_metabooks_medias_to_pubsub( # noqa
        self,
        patch_publish_manager: Mock,
        record_processor: MediaRecordProcessor,
        data_dict_with_metabooks_images: Dict,
        pubsub_create_metabooks_payload,
        patch_storage_manager_upload,
        patch_time,
        sku,
        medias_collection
    ):
        original_images = [
            data['url']
            for data in data_dict_with_metabooks_images['images']
        ]
        original_hashs = [
            data['hash']
            for data in data_dict_with_metabooks_images['images']
        ]
        with patch_storage_manager_upload:
            with patch_time, patch_publish_manager as mock_pubsub:
                record_processor.create(data_dict_with_metabooks_images)

        pubsub_images = mock_pubsub.call_args_list[0][1]['content']['original_images'] # noqa
        pubsub_hashs = mock_pubsub.call_args_list[0][1]['content']['images']
        pubsub_image_payload = mock_pubsub.call_args_list[0][1]['content']

        assert pubsub_image_payload['images'] == [
            '22a2551ad3dacd39867bc4b4e71d3286.jpg',
            'c68fa1dd38284eed43f5b7231b281f3e.jpg'
        ]

        assert pubsub_image_payload['original_images'] == [
            image['url'] for image in data_dict_with_metabooks_images['images']
        ]

        assert pubsub_image_payload['sku'] == sku
        assert pubsub_image_payload['seller_id'] == MAGAZINE_LUIZA_SELLER_ID

        assert original_hashs != pubsub_hashs
        assert pubsub_images == original_images

    def test_when_delete_process_with_success_then_should_send_medias_to_pubsub( # noqa
        self,
        patch_publish_manager: Mock,
        record_processor: MediaRecordProcessor,
        data_dict_with_images,
        pubsub_delete_payload,
        patch_storage_manager_upload,
        patch_time
    ):
        with patch_storage_manager_upload:
            with patch_time, patch_publish_manager as mock_pubsub:
                record_processor.delete(data_dict_with_images)

        assert mock_pubsub.call_args_list[0][1]['content'] == pubsub_delete_payload  # noqa

    @settings_stub(IMAGE_RESIZE_ENABLE=False)
    def test_when_process_with_success_then_should_upload_downloadable_media( # noqa
        self,
        patch_storage_manager_upload,
        record_processor: MediaRecordProcessor,
        data_dict: Dict,
        mock_response_bytes,
        patch_requests_get,
        hash_of_response_bytes,
        medias_collection: Collection,
        patch_publish_manager: Mock,
    ):
        seller_id = data_dict['seller_id']
        sku = data_dict['sku']

        media_type: str = MediaType.audios.value
        data_dict[media_type].append('https://murcho.com/foo.mp3')

        with patch_storage_manager_upload as mock_storage:
            with patch_requests_get as mock_get:
                with patch_publish_manager as mock_pubsub:
                    mock_get.return_value = mock_response_bytes
                    record_processor.create(data_dict)

        expected_filename = '{}/{}/{}/{}.mp3'.format(
            seller_id,
            media_type,
            slugify(sku),
            hash_of_response_bytes
        )

        _, filename = mock_storage.call_args_list[0][0]
        documents = list(medias_collection.find(
            {'seller_id': seller_id, 'sku': sku},
            {'_id': 0}
        ))

        assert filename == expected_filename
        assert mock_get.called
        assert mock_pubsub.call_count == 3
        assert mock_storage.call_count == 1
        assert len(documents) == 1
        assert documents[0][media_type][0] == f'{hash_of_response_bytes}.mp3'

    def test_record_processor_upload_downloadable_media_with_content_type(
        self,
        patch_storage_manager_upload,
        record_processor: MediaRecordProcessor,
        data_dict: Dict,
        mock_response_bytes,
        patch_requests_get,
        patch_publish_manager: Mock,
    ):
        data_dict['images'] = [{
            'url': 'https://murcho.com/foo.jpeg',
            'hash': self.IMAGE_HASH
        }]

        with patch_publish_manager as mock_pubsub:
            with patch_storage_manager_upload as mock_storage:
                with patch_requests_get as mock_get:
                    mock_get.return_value = mock_response_bytes
                    record_processor.create(data_dict)

        content_type = mock_storage.call_args_list[0][1]['content_type']
        assert content_type == mock_response_bytes.headers['content-type']
        assert mock_get.called
        assert mock_pubsub.call_count == 3

    def test_record_processor_raise_exception_for_invalid_content_type(
        self,
        record_processor: MediaRecordProcessor,
        data_dict: Dict,
        mock_response_bytes,
        patch_requests_get,
        patch_publish_manager
    ):
        data_dict['images'] = [{
            'url': 'https://murcho.com/foo.jpeg',
            'hash': self.IMAGE_HASH
        }]
        del mock_response_bytes.headers['content-type']
        with patch_requests_get as mock_get:
            with patch_publish_manager:
                mock_get.return_value = mock_response_bytes
                with pytest.raises(MediaWithoutContentType):
                    record_processor.create(data_dict)

    def test_record_processor_process_media_with_url_in_a_dict(
        self,
        patch_storage_manager_upload: Mock,
        record_processor: MediaRecordProcessor,
        data_dict: Dict,
        mock_response_bytes,
        patch_requests_get,
        medias_collection: Collection,
        patch_publish_manager: Mock,
    ):
        seller_id = data_dict['seller_id']
        sku = data_dict['sku']

        expected_hash = '54feac265d76248d89be12fd7b8c67ab'
        data_dict['images'].append(
            {'url': 'https://murcho.com/foo.bmp', 'hash': expected_hash}
        )
        with patch_storage_manager_upload as mock_storage:
            with patch_requests_get as mock_get:
                with patch_publish_manager as mock_pubsub:
                    mock_get.return_value = mock_response_bytes
                    record_processor.create(data_dict)

        expected_filename = '{}/images/{}/{}.bmp'.format(
            seller_id, slugify(sku), expected_hash
        )

        bytes_io, filename = mock_storage.call_args_list[0][0]
        assert filename == expected_filename
        assert mock_get.called
        assert mock_pubsub.call_count == 3

        document = medias_collection.find_one(
            {'seller_id': seller_id, 'sku': sku},
            {'_id': 0, 'images': 1}
        )

        assert document['images'][0] == f'{expected_hash}.bmp'

    def test_consumer_to_delete_non_existent_file(
        self,
        record_processor: MediaRecordProcessor,
        data_dict: Dict,
        patch_storage_manager_delete,
        medias_collection: Collection,
        patch_publish_manager
    ):
        with patch_storage_manager_delete as mock_storage:
            with patch_publish_manager as mock_pubsub:
                record_processor.delete(data_dict)

        expected_filename = '{seller_id}/json_v2/{sku}.json'.format(
            sku=slugify(data_dict['sku']),
            seller_id=data_dict['seller_id']
        )

        assert mock_storage.call_args[0][0] == expected_filename
        assert mock_pubsub.call_count == 1

    def test_when_process_delete_then_delete_medias_with_success(
        self,
        record_processor: MediaRecordProcessor,
        data_dict: Dict,
        patch_storage_manager_delete,
        medias_collection: Collection,
        patch_publish_manager
    ):
        seller_id = data_dict['seller_id']
        sku = data_dict['sku']
        query_document = {'seller_id': seller_id, 'sku': sku}

        medias_collection.insert_one(query_document)

        with patch_storage_manager_delete as mock_storage:
            with patch_publish_manager as mock_pubsub:
                record_processor.delete(data_dict)

                expected_calls = [
                    call('{}/{}/{}/'.format(seller_id, media_type, slugify(sku)))  # noqa
                    for media_type in data_dict.keys()
                    if (media_type in VALID_MEDIA_TYPES and
                        media_type not in NON_UPLOADABLE_MEDIA_TYPES)
                ]

                mock_storage.assert_has_calls(expected_calls, any_order=True)
                assert medias_collection.find_one(query_document)
                assert mock_pubsub.call_count == 1

    def test_register_medias_respect_media_order(
        self,
        record_processor: MediaRecordProcessor,
        medias_collection: Collection
    ):
        seller_id = 'murcho'
        sku = '1234567'
        extension = '.jpg'

        images_ordered = [
            f'{seller_id}-{image}{extension}' for image in range(5)
        ]
        medias_payload: Dict = {
            'seller_id': seller_id,
            'sku': sku,
            'images': images_ordered
        }

        record_processor.register_medias(
            seller_id,
            sku,
            medias_payload
        )

        document = medias_collection.find_one(
            {'seller_id': seller_id, 'sku': sku}
        )

        assert len(document['images']) == 5
        assert document['images'] == images_ordered

    def test_when_register_medias_with_origin_rebuild_then_ignore_not_changed_content(  # noqa
        self,
        record_processor: MediaRecordProcessor,
        media_object: Dict,
        medias_collection
    ):
        seller_id = 'murcho'
        sku = '1234567'

        media_payload: Dict = {
            'sku': sku,
            'seller_id': seller_id,
            'images': ['murcho.jpg'],
            'image_details': [],
            'original': {
                'images': [
                    {'url': f'{seller_id}.jpg', 'hash': self.IMAGE_HASH}
                ]
            }
        }

        medias_collection.insert_one(media_payload)

        assert record_processor.register_medias(
            seller_id=seller_id,
            sku=sku,
            document=media_payload,
            origin='rebuild'
        ) != {}

    def test_register_videos(
        self,
        record_processor: MediaRecordProcessor,
        medias_collection: Collection,
        patch_publish_manager: Mock,
        patch_storage_manager_upload: Mock,
        data_dict: Dict,
        mock_product_videos_message_data: List
    ):
        data_dict['videos'].extend(mock_product_videos_message_data)
        with patch_storage_manager_upload:
            with patch_publish_manager as mock_pubsub:
                record_processor.create(data_dict)

            document = medias_collection.find_one(
                {'seller_id': data_dict['seller_id'], 'sku': data_dict['sku']},
                {'_id': 0, 'videos': 1}
            )
            assert len(document['videos']) == 1
            assert document['videos'] == mock_product_videos_message_data
            assert mock_pubsub.call_count == 3

    def test_register_invalid_videos(
        self,
        record_processor: MediaRecordProcessor,
        medias_collection: Collection, data_dict: Dict,
        patch_storage_manager_upload,
        patch_publish_manager: Mock,
    ):
        expected_url = 'https://magazineluiza.com.br/'
        data_dict['videos'].append(expected_url)

        with patch_storage_manager_upload:
            with patch_publish_manager as mock_pubsub:
                record_processor.create(data_dict)

        document = medias_collection.find_one(
            {'seller_id': data_dict['seller_id'], 'sku': data_dict['sku']},
            {'_id': 0, 'videos': 1}
        )
        assert len(document['videos']) == 0
        assert mock_pubsub.call_count == 3

    def test_register_medias_dont_duplicated_register(
        self,
        record_processor: MediaRecordProcessor,
        medias_collection: Collection,
        media_from_db_expected_murcho: Dict
    ):
        seller_id: str = media_from_db_expected_murcho['seller_id']
        sku: str = media_from_db_expected_murcho['sku']
        for _ in range(5):
            record_processor.register_medias(
                seller_id,
                sku,
                media_from_db_expected_murcho
            )

        assert medias_collection.count_documents(
            {'seller_id': seller_id, 'sku': sku}
        ) == 1

    def test_not_register_medias_with_empty_url(
        self,
        record_processor: MediaRecordProcessor,
        non_downloadable_media_type,
        patch_publish_manager: Mock,
        caplog
    ):
        data_dict = {
            'images': [{
                'url': '',
                'hash': None
            }],
            'seller_id': 'madeiramadeira-openapi',
            'sku': '177071'
        }

        message = {
            'data': data_dict,
            'action': 'create'
        }

        with patch_publish_manager:
            assert record_processor.process_message(
                message
            ) is True
            assert 'Media without url. Skip media process for' in caplog.text

    def test_cache_should_be_the_same_redis_instance(
        self,
        record_processor
    ):
        redis_instance = record_processor.cache()
        redis_instance_from_same_class = record_processor.cache()

        other_record_processor = (
            MediaRecordProcessor(
                'media'
            )
        )

        redis_instance_from_other_record_processor = (
            other_record_processor.cache()
        )
        assert isinstance(redis_instance, Redis)
        assert redis_instance is redis_instance_from_same_class
        assert redis_instance_from_other_record_processor is redis_instance

    def test_when_product_existing_then_send_media_notify_pubsub(
        self,
        record_processor: MediaRecordProcessor,
        patch_publish_manager: Mock,
        data_dict_with_images,
        patch_notification_raw_products
    ):
        data_dict_with_images['tracking_id'] = 'fake'
        with patch_publish_manager as mock_pubsub:
            with patch_notification_raw_products as mock_raw_products:
                mock_raw_products.find_one.return_value = {
                    'navigation_id': 'fake'
                }
                record_processor.create(data_dict_with_images)

        content = mock_pubsub.call_args_list[1][1]['content']
        assert content == {
            'sku': data_dict_with_images['sku'],
            'seller_id': slugify(data_dict_with_images['seller_id']),
            'navigation_id': 'fake',
            'action': 'create',
            'type': 'media',
            'origin': 'media',
            'task_id': ANY,
            'timestamp': 0,
            'tracking_id': 'fake'
        }

        assert mock_pubsub.call_count == 3

    def test_record_processor_not_save_a_empty_media(
        self,
        record_processor: MediaRecordProcessor,
        data_dict: Dict,
        medias_collection
    ):
        data_dict['seller_id'] = MAGAZINE_LUIZA_SELLER_ID
        record_processor.create(data_dict)
        assert medias_collection.count_documents({}) == 0

    def test_process_media_successfully_should_send_notification(
        self,
        record_processor: MediaRecordProcessor,
        data_dict_with_images,
        mock_response_bytes,
        patch_patolino_product_post,
        patch_storage_manager_upload,
        patch_publish_manager: Mock,
        raw_products,
        patch_notification_put,
        mock_downloaded_image,
        sku,
        patch_media_service_download_and_resize
    ):
        raw_products.insert_one({
            'sku': data_dict_with_images['sku'],
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'navigation_id': '123456789',
            'title': 'título do produto'
        })

        def mock_process_media(*args, **kwargs):
            return True

        def mock_successfully(*args, **kwargs):
            return True

        with patch_publish_manager:
            with patch_patolino_product_post as patolino_mock:
                with patch_storage_manager_upload, patch_notification_put:
                    with patch_media_service_download_and_resize as mock_download_and_resize:  # noqa
                        mock_download_and_resize.return_value = mock_downloaded_image  # noqa
                        record_processor._process_media = mock_process_media
                        record_processor._all_successfully_processed = mock_successfully  # noqa
                        record_processor.create(data_dict_with_images)

        assert patolino_mock.called
        patolino_payload_request = patolino_mock.call_args[0][0]
        assert patolino_payload_request['sku'] == sku
        assert patolino_payload_request['seller_id'] == MAGAZINE_LUIZA_SELLER_ID  # noqa
        assert patolino_payload_request['code'] == MEDIA_SUCCESS_CODE
        assert patolino_payload_request['message'] == MEDIA_SUCCESS_MESSAGE  # noqa
        assert len(patolino_payload_request['payload']['medias']) == 2

        medias = patolino_payload_request['payload']['medias']
        medias = sorted(medias, key=lambda m: m['url'])

        expected_medias = sorted(
            [x['url'] for x in data_dict_with_images['images']]
        )
        assert medias[0]['url'] == expected_medias[0]
        assert medias[0]['success'] is True

        assert medias[1]['url'] == expected_medias[1]
        assert medias[1]['success'] is True

    def test_process_media_when_not_enriched_product_should_process(
        self,
        record_processor: MediaRecordProcessor,
        data_dict_with_metabooks_images: Dict,
        patch_patolino_product_post,
        patch_storage_manager_upload,
        patch_publish_manager: Mock,
        logger_stream: StreamHandler,
        patch_enriched_products,
        patch_build_media_list
    ):
        data_dict_with_metabooks_images['seller_id'] = MAGAZINE_LUIZA_SELLER_ID

        with patch_storage_manager_upload:
            with patch_publish_manager, patch_patolino_product_post:
                with patch_enriched_products as mock_enriched_products:
                    with patch_build_media_list as mock_build_medias:
                        mock_enriched_products.find.return_value = []
                        record_processor.create(data_dict_with_metabooks_images) # noqa

        sku = data_dict_with_metabooks_images['sku'],
        seller_id = data_dict_with_metabooks_images['seller_id']

        assert mock_build_medias.call_count == 1
        assert (
            'Message skips because product was enriched by one of the sources '
            f'{[SOURCE_METABOOKS]} from sku:{sku} seller_id:{seller_id} and '
            'source not is metadata_verify'
        ) not in logger_stream.getvalue()

    def test_process_media_when_source_metadata_verify_should_process(
        self,
        record_processor: MediaRecordProcessor,
        data_dict_with_metabooks_images: Dict,
        patch_patolino_product_post,
        patch_storage_manager_upload,
        patch_publish_manager: Mock,
        logger_stream: StreamHandler,
        patch_build_media_list,
        patch_enriched_products,
        mock_downloaded_image,
        patch_media_service_download_and_resize
    ):
        product = {
            'sku': data_dict_with_metabooks_images['sku'],
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'navigation_id': '123456789',
            'title': 'título do produto',
            'source': SOURCE_METABOOKS
        }

        data_dict_with_metabooks_images['seller_id'] = MAGAZINE_LUIZA_SELLER_ID
        data_dict_with_metabooks_images['source'] = SOURCE_METADATA_VERIFY

        with patch_storage_manager_upload:
            with patch_publish_manager, patch_patolino_product_post:
                with patch_enriched_products as mock_enriched_products:
                    with patch_build_media_list as mock_build_medias:
                        with patch_media_service_download_and_resize as mock_download_and_resize:  # noqa
                            mock_enriched_products.find.return_value = [
                                product
                            ]
                            mock_download_and_resize.return_value = mock_downloaded_image  # noqa
                            record_processor.create(
                                data_dict_with_metabooks_images
                            )

        sku = data_dict_with_metabooks_images['sku'],
        seller_id = data_dict_with_metabooks_images['seller_id']

        assert mock_build_medias.call_count == 1
        assert (
            'Message skips because product was enriched by one of the sources'
            f'{settings.SKIP_ENRICHED_SOURCES_WHEN_NOT_METADATA_VERIFY} from '
            f'sku:{sku} seller_id:{seller_id} and source not is metadata_verify'  # noqa
        ) not in logger_stream.getvalue()

    def test_process_media_when_not_source_metadata_verify_should_not_process(
        self,
        record_processor: MediaRecordProcessor,
        data_dict_with_metabooks_images: Dict,
        patch_patolino_product_post,
        patch_storage_manager_upload,
        patch_publish_manager: Mock,
        logger_stream: StreamHandler,
        patch_build_media_list,
        patch_enriched_products,
        mock_downloaded_image,
        patch_media_service_download_and_resize
    ):
        product = {
            'sku': data_dict_with_metabooks_images['sku'],
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'navigation_id': '123456789',
            'title': 'título do produto',
            'source': SOURCE_METABOOKS
        }

        data_dict_with_metabooks_images['seller_id'] = MAGAZINE_LUIZA_SELLER_ID
        data_dict_with_metabooks_images['source'] = 'test'

        with patch_storage_manager_upload:
            with patch_publish_manager, patch_patolino_product_post as patolino_mock: # noqa
                with patch_enriched_products as mock_enriched_products:
                    with patch_build_media_list as mock_build_medias:
                        with patch_media_service_download_and_resize as mock_download_and_resize:  # noqa
                            mock_enriched_products.find.return_value = [
                                product
                            ]
                            mock_download_and_resize.return_value = mock_downloaded_image  # noqa
                            record_processor.create(
                                data_dict_with_metabooks_images
                            )

        assert not mock_build_medias.called
        assert patolino_mock.called

        sku = data_dict_with_metabooks_images['sku']
        seller_id = data_dict_with_metabooks_images['seller_id']

        assert (
            f'Message was skipped because the product sku:{sku} '
            f'seller_id:{seller_id} was enriched by Metabooks and '
            'no Smarcontent'
        ) in logger_stream.getvalue()

    def test_process_media_when_source_metabooks_and_smartcontent_should_process(  # noqa
        self,
        record_processor: MediaRecordProcessor,
        data_dict_with_metabooks_images: Dict,
        patch_patolino_product_post,
        patch_storage_manager_upload,
        patch_publish_manager: Mock,
        logger_stream: StreamHandler,
        patch_enriched_products,
        mock_downloaded_metabooks_images,
        patch_media_service_download_and_resize,
        medias_collection
    ):
        data_dict_with_metabooks_images.update({
            'seller_id': MAGAZINE_LUIZA_SELLER_ID
        })
        sku = data_dict_with_metabooks_images['sku']
        seller_id = data_dict_with_metabooks_images['seller_id']

        product_metabooks = {
            'sku': sku,
            'seller_id': seller_id,
            'navigation_id': '123456789',
            'title': 'título do produto',
            'source': SOURCE_METABOOKS
        }
        product_smartcontent = {
            'sku': sku,
            'seller_id': seller_id,
            'navigation_id': '123456789',
            'title': 'título do produto',
            'source': SOURCE_SMARTCONTENT
        }

        data_dict_with_metabooks_images.update({
            'seller_id': seller_id,
            'source': 'test'
        })

        with patch_storage_manager_upload as mock_upload:
            with patch_publish_manager as mock_publish, patch_patolino_product_post:  # noqa
                with patch_enriched_products as mock_enriched_products:
                    with patch_media_service_download_and_resize as mock_download_and_resize:  # noqa
                        mock_enriched_products.find.return_value = [
                            product_metabooks,
                            product_smartcontent
                        ]
                        mock_download_and_resize.side_effect = mock_downloaded_metabooks_images  # noqa
                        record_processor.create(
                            data_dict_with_metabooks_images
                        )
        document = {
            'images': [
                image.mount_file_name()
                for image in mock_downloaded_metabooks_images
            ],
            'podcasts': [],
            'audios': [],
            'videos': [],
            'image_details': [
                {
                    'dimensions': {
                        'width': image.width,
                        'height': image.height
                    },
                    'hash': image.mount_file_name()
                }
                for image in mock_downloaded_metabooks_images
            ],
            'original': {
                'images': data_dict_with_metabooks_images['images']
            },
            'original_images': [image['url'] for image in data_dict_with_metabooks_images['images']],  # noqa
            'seller_id': seller_id,
            'sku': sku
        }

        assert medias_collection.find_one(
            {'sku': sku, 'seller_id': seller_id}, {'_id': 0}
        ) == document
        assert mock_upload.call_count == 2
        assert mock_publish.call_count == 2
        assert (
            f'Media saved successfully for sku:{sku} seller_id:{seller_id} '
            f'document:{document}'
        ) in logger_stream.getvalue()

    def test_process_media_when_source_metabooks_and_smartcontent_from_metadata_verify_should_not_process( # noqa
        self,
        record_processor: MediaRecordProcessor,
        data_dict_with_metabooks_images: Dict,
        patch_patolino_product_post,
        patch_storage_manager_upload,
        patch_publish_manager: Mock,
        logger_stream: StreamHandler,
        patch_build_media_list,
        patch_enriched_products,
        mock_downloaded_image,
        patch_media_service_download_and_resize
    ):
        product_metabooks = {
            'sku': data_dict_with_metabooks_images['sku'],
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'navigation_id': '123456789',
            'title': 'título do produto',
            'source': SOURCE_METABOOKS
        }
        product_smartcontent = {
            'sku': data_dict_with_metabooks_images['sku'],
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'navigation_id': '123456789',
            'title': 'título do produto',
            'source': SOURCE_SMARTCONTENT
        }

        data_dict_with_metabooks_images['seller_id'] = MAGAZINE_LUIZA_SELLER_ID
        data_dict_with_metabooks_images['source'] = SOURCE_METADATA_VERIFY

        with patch_storage_manager_upload:
            with patch_publish_manager, patch_patolino_product_post as patolino_mock: # noqa
                with patch_enriched_products as mock_enriched_products:
                    with patch_build_media_list as mock_build_medias:
                        with patch_media_service_download_and_resize as mock_download_and_resize:  # noqa
                            mock_enriched_products.find.return_value = [
                                product_metabooks,
                                product_smartcontent
                            ]
                            mock_download_and_resize.return_value = mock_downloaded_image  # noqa
                            record_processor.create(
                                data_dict_with_metabooks_images
                            )

        sku = data_dict_with_metabooks_images['sku']
        seller_id = data_dict_with_metabooks_images['seller_id']

        assert not mock_build_medias.called
        assert patolino_mock.called
        assert (
            f'Message was skipped because the product sku:{sku} '
            f'seller_id:{seller_id} was enriched by multiple sources '
            'including Smarcontent, which is the ultimate source for '
            '1P products'
        ) in logger_stream.getvalue()

    # TODO: Bug when image not found should not be saved
    def test_process_media_unsuccessfully_should_not_send_notification(
        self,
        record_processor: MediaRecordProcessor,
        data_dict_with_invalid_images,
        patch_storage_manager_upload,
        patch_publish_manager: Mock,
        raw_products,
        patch_notification_put,
        logger_stream: StreamHandler,
        patch_media_service_download_and_resize,
        patch_datetime,
        patch_time
    ):
        raw_products.insert_one({
            'sku': data_dict_with_invalid_images['sku'],
            'seller_id': data_dict_with_invalid_images['seller_id'],
            'navigation_id': '123456789',
            'title': 'título do produto'
        })

        mock_current_datetime = datetime.datetime(2022, 1, 1, 0, 0, 0)
        images_urls: List[str] = [
            image['url'] for image in data_dict_with_invalid_images['images']
        ]

        with patch_publish_manager as mock_publish, patch_time:
            with patch_notification_put as mock_notification_put:
                with patch_storage_manager_upload as mock_upload:
                    with patch_media_service_download_and_resize as mock_download_and_resize:  # noqa
                        with patch_datetime as mock_datetime:
                            mock_datetime.utcnow.return_value = mock_current_datetime  # noqa
                            mock_download_and_resize.side_effect = [
                                MediaNotFoundException(
                                    media=Mock(media_type='images', url=url)
                                )
                                for url in images_urls
                            ]
                            record_processor.create(
                                data_dict_with_invalid_images
                            )

        assert mock_notification_put.called
        assert mock_publish.call_args_list[0][1] == {
            'content': {
                'seller_id': data_dict_with_invalid_images['seller_id'],
                'sku': data_dict_with_invalid_images['sku'],
                'audios': [],
                'images': ['None.jpg', 'None.jpg'],
                'original_images': images_urls, 'podcasts': [], 'videos': [],
                'message_timestamp': 1502734827.997473,
                'action': CREATE_ACTION
            },
            'topic_name': settings.PUBSUB_MEDIA_EXPORT_TOPIC_NAME,
            'project_id': settings.GOOGLE_PROJECT_ID
        }

        expected_patolino_content = mock_publish.call_args_list[1][1]
        expected_patolino_content['content']['payload']['medias'] = sorted(
            expected_patolino_content['content']['payload']['medias'],
            key=lambda x: x['url']
        )

        assert expected_patolino_content == {
            'content': {
                'sku': data_dict_with_invalid_images['sku'],
                'seller_id': data_dict_with_invalid_images['seller_id'],
                'code': MEDIA_SUCCESS_CODE,
                'message': 'Successfully processed medias',
                'payload': {
                    'medias': [
                        {'url': 'https://img.magazineluiza.com.br/teste.jpg', 'success': True},  # noqa
                        {'url': 'https://img.magazineluiza.com.br/testea.jpg', 'success': True}  # noqa
                    ]
                },
                'action': UPDATE_ACTION,
                'last_updated_at': mock_current_datetime.isoformat()
            },
            'topic_name': settings.PATOLINO_STREAM_TOPIC_NAME,
            'project_id': settings.GOOGLE_PROJECT_ID,
            'attributes': {
                'seller_id': data_dict_with_invalid_images['seller_id'],
                'code': MEDIA_SUCCESS_CODE,
                'has_tracking': 'false'
            }
        }

        assert not mock_upload.called
        assert all(
            True for message in [
                f'Not found media type:images url:{url}' for url in images_urls
            ]
            if message in logger_stream.getvalue()
        )

    def test_record_processor_returns_unsupported_media_type_error(
        self,
        record_processor: MediaRecordProcessor,
        data_dict: Dict,
        patch_media_service_download_and_resize,
        patch_storage_manager_upload,
        patch_publish_manager
    ):
        data_dict['images'] = [
            {'url': 'https://murcho.com/foo.jpg', 'hash': self.IMAGE_HASH}
        ]
        images_urls: List[str] = [
            image['url'] for image in data_dict['images']
        ]

        with patch_publish_manager as mock_publish:
            with patch_storage_manager_upload as mock_upload:
                with patch_media_service_download_and_resize as mock_download_and_resize:  # noqa
                    mock_download_and_resize.side_effect = [
                        MediaUnprocessableException(
                            media=Mock(media_type='images', url=url)
                        )
                        for url in images_urls
                    ]
                    record_processor.create(data_dict)

        assert not mock_upload.called
        assert mock_publish.call_count == 3

    def test_record_processor_should_exception_error_for_timeout(
        self,
        record_processor: MediaRecordProcessor,
        patch_storage_manager_upload,
        media_object,
        logger_stream: StreamHandler,
        patch_media_service_download_and_resize
    ):
        with patch_storage_manager_upload as mock_upload:
            with patch_media_service_download_and_resize as mock_download_and_resize:  # noqa
                mock_download_and_resize.side_effect = TimedOutMediaException(
                    media=Mock(
                        media_type=media_object['media_type'],
                        url=media_object['url']
                    )
                )
                media = Media(**media_object)
                record_processor._process_media(media, {})

        assert not mock_upload.called
        assert (
            f'Skipping upload media sku:{media.sku} seller_id:{media.seller_id}. '  # noqa
            f'Message:Could not download the media type:images url:{media.url} '  # noqa
            'because is timed out.'
        ) in logger_stream.getvalue()

    def test_record_processor_should_exception_error_generic(
        self,
        record_processor: MediaRecordProcessor,
        patch_storage_manager_upload,
        media_object,
        logger_stream: StreamHandler,
        patch_media_service_download_and_resize
    ):
        with pytest.raises(Exception):
            with patch_storage_manager_upload as mock_upload:
                with patch_media_service_download_and_resize as mock_download_and_resize:  # noqa
                    mock_download_and_resize.side_effect = Exception(
                        'An generic exception'
                    )
                    media = Media(**media_object)
                    record_processor._process_media(media)

        assert not mock_upload.called

    def test_when_not_detected_changes_images_on_register_medias_then_skip_notification(  # noqa
        self,
        raw_products,
        record_processor: MediaRecordProcessor,
        data_dict_with_images,
        patch_patolino_product_post,
        patch_pubsub_client,
        medias_collection: Collection,
        media_from_db_expected_murcho,
        logger_stream: StreamHandler,
        patch_media_service_download_and_resize,
        patch_datetime,
        patch_storage_manager_property,
        mock_product_images_message_data: Dict
    ):
        sku = media_from_db_expected_murcho['sku']
        seller_id = media_from_db_expected_murcho['seller_id']
        product = {
            'sku': sku,
            'seller_id': seller_id,
            'navigation_id': '123456789',
            'title': 'título do produto'
        }
        data_dict_with_images.update({'sku': sku, 'seller_id': seller_id})
        data_dict_with_images['images'][0] = mock_product_images_message_data[0]  # noqa

        raw_products.insert_one(product)
        medias_collection.insert_one(media_from_db_expected_murcho)

        mock_current_datetime = datetime.datetime(2022, 1, 1, 0, 0, 0)
        with patch_storage_manager_property as mock_storage_manager:
            with patch_patolino_product_post as patolino_mock:
                with patch_pubsub_client as mock_pubsub:
                    with patch_media_service_download_and_resize as mock_download_and_resize:  # noqa
                        with patch_datetime as mock_datetime:
                            mock_datetime.utcnow.return_value = mock_current_datetime  # noqa
                            mock_download_and_resize.side_effect = [
                                MediaDownloadOutput(
                                    url=image['url'],
                                    media_type='images',
                                    data=BytesIO(b'image'),
                                    content_type='image/jpg',
                                    md5=image['hash'],
                                    width=details['dimensions']['width'],
                                    height=details['dimensions']['height'],
                                )
                                for image, details in zip(
                                    data_dict_with_images['images'],
                                    media_from_db_expected_murcho['image_details']  # noqa
                                )
                            ]
                            record_processor.create(data_dict_with_images)

        assert not mock_storage_manager.upload.called
        assert patolino_mock.call_args == call(
            {
                'sku': sku,
                'seller_id': seller_id,
                'code': MEDIA_UNFINISHED_PROCESS,
                'message': f'Couldn\'t finish processing sku:{sku} seller_id:{seller_id} reason: Media unmodified or not available',  # noqa
                'payload': {'navigation_id': None, 'action': UPDATE_ACTION},
                'action': UPDATE_ACTION,
                'last_updated_at': mock_current_datetime.isoformat()
            },
            {
                'seller_id': seller_id,
                'code': MEDIA_UNFINISHED_PROCESS,
                'has_tracking': 'false'
            }
        )

        assert not mock_pubsub.called
        assert 'Unmodified media for sku:' in logger_stream.getvalue()

    def test_when_change_order_images_then_not_process_but_notify_acme(
        self,
        raw_products,
        record_processor: MediaRecordProcessor,
        data_dict_with_images,
        patch_patolino_product_post,
        patch_storage_manager_property,
        patch_pubsub_property,
        medias_collection: Collection,
        media_from_db_expected_murcho: Dict,
        mock_product_images_message_data: Dict
    ):
        product = {
            'sku': data_dict_with_images['sku'],
            'seller_id': media_from_db_expected_murcho['seller_id'],
            'navigation_id': '123456789',
            'title': 'título do produto'
        }

        data_dict_with_images['seller_id'] = product['seller_id']
        data_dict_with_images['images'][0] = mock_product_images_message_data[0]  # noqa

        media_from_db_expected_murcho['image_details'] = sorted(
            media_from_db_expected_murcho['image_details'],
            key=lambda d: d['hash'],
            reverse=True
        )
        media_from_db_expected_murcho['images'] = sorted(
            media_from_db_expected_murcho['images'],
            reverse=True
        )
        media_from_db_expected_murcho['original']['images'] = sorted(
            media_from_db_expected_murcho['original']['images'],
            key=lambda d: d['hash'],
            reverse=True
        )
        raw_products.insert_one(product)
        medias_collection.insert_one(media_from_db_expected_murcho)

        with patch_storage_manager_property as mock_storage_manager:
            with patch_pubsub_property as mock_pubsub:
                with patch_patolino_product_post as patolino_mock:
                    record_processor.create(data_dict_with_images)

        assert not mock_storage_manager.upload.called
        assert patolino_mock.called
        assert mock_pubsub.publish.call_args_list[0][1]['content']['images'] == [  # noqa
            '52de9b80208f08270e62616e42fac68a.jpg',
            'bc92c770ad72fc410374a470612b9747.jpg'
        ]
        assert mock_pubsub.publish.call_args_list[0][1]['content']['original_images'] == [  # noqa
            image['url'] for image in mock_product_images_message_data
        ]

    def test_when_notification_patolino_with_tracking_id_then_send_tracking_id(
        self,
        record_processor: MediaRecordProcessor,
        data_dict_with_images,
        patch_patolino_product_post
    ):
        process_media_result = [
            {'url': image['url'], 'success': True}
            for image in data_dict_with_images['images']
        ]

        with patch_patolino_product_post as patolino_mock:
            record_processor._send_notification(
                seller_id=data_dict_with_images['seller_id'],
                sku=data_dict_with_images['sku'],
                process_media_result=process_media_result,
                tracking_id='fake'
            )

        assert patolino_mock.called
        assert patolino_mock.call_args_list[0][0][0]['tracking_id'] == 'fake'

    def test_when_create_process_with_success_then_should_send_event_to_pubsub(
        self,
        patch_pubsub_client,
        record_processor: MediaRecordProcessor,
        data_dict_with_images,
        pubsub_create_payload,
        patch_storage_manager_upload,
        patch_time
    ):
        with patch_storage_manager_upload:
            with patch_time, patch_pubsub_client as mock_pubsub:
                record_processor.create(data_dict_with_images)

        assert mock_pubsub.call_args_list[0][1]['topic'] == 'projects/maga-homolog/topics/taz-media-export-sandbox' # noqa
        assert json.loads(mock_pubsub.call_args_list[0][1]['data']) == pubsub_create_payload  # noqa

    @pytest.mark.parametrize(
        'data, expected',
        [
            (({'videos': ['https://video.com']}), False),
            (({'images': ['https://images.com']}), False),
            (({'audios': ['https://audios.com']}), False),
            (({'podcasts': ['https://audios.com']}), False),
            (({}), True),
        ]
    )
    def test_is_empty_media(self, data, expected):
        assert MediaRecordProcessor.is_empty_media(data) == expected

    def test_record_processor_return_and_log_with_is_a_empty_media(
        self,
        record_processor: MediaRecordProcessor,
        caplog
    ):
        sku = '1234'
        data = {
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'sku': sku
        }
        expected_msg_payload = {
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'sku': sku
        }
        assert record_processor.create(data)
        assert f'Skipping empty media:{expected_msg_payload}' in caplog.text

    def test_save_should_return_a_empty_dict_when_it_is_equal(
        self,
        record_processor: MediaRecordProcessor,
        medias_collection: Collection,
        mock_saved_medias
    ):
        medias_collection.insert_one(mock_saved_medias)
        has_update: bool = record_processor._save(mock_saved_medias)
        assert not has_update

    def test_save_should_return_created_document_with_it_doesnt_exists(
        self, record_processor: MediaRecordProcessor, mock_saved_medias
    ):
        has_update: bool = record_processor._save(mock_saved_medias)
        assert has_update

    def test_save_should_return_updated_document(
        self, record_processor: MediaRecordProcessor, mock_saved_medias
    ):
        mock_saved_medias_new = deepcopy(mock_saved_medias)
        mock_saved_medias['videos'] = []
        record_processor._save(mock_saved_medias)
        has_update: bool = record_processor._save(mock_saved_medias_new)
        assert has_update

    def test_when_not_changed_input_images_then_return_all_images_unnecessary_process(  # noqa
        self,
        record_processor: MediaRecordProcessor,
        medias_collection: Collection,
        media_from_db_expected_murcho: Dict,
        media_murcho_message_data: Dict
    ):
        saved_medias = deepcopy(media_from_db_expected_murcho)
        medias_collection.insert_one(media_from_db_expected_murcho)

        verified_images: Dict = record_processor._check_has_necessary_process_images(  # noqa
            saved_medias=saved_medias,
            message_data=media_murcho_message_data
        )

        expected_verified_images = self.mount_expected_verified_images(
            media_from_db_expected_murcho
        )
        assert verified_images == expected_verified_images

    def test_when_changed_order_input_images_then_return_all_images_unnecessary_process(  # noqa
        self,
        record_processor: MediaRecordProcessor,
        medias_collection: Collection,
        media_from_db_expected_murcho: Dict,
        media_murcho_message_data: Dict
    ):
        saved_medias = deepcopy(media_from_db_expected_murcho)
        medias_collection.insert_one(media_from_db_expected_murcho)

        media_from_db_expected_murcho['original']['images'].append(
            media_from_db_expected_murcho['original']['images'].pop(0)
        )
        media_from_db_expected_murcho['image_details'].append(
            media_from_db_expected_murcho['image_details'].pop(0)
        )
        media_from_db_expected_murcho['images'].pop(0)
        media_murcho_message_data['images'] = media_from_db_expected_murcho['original']['images']  # noqa

        verified_images: Dict = record_processor._check_has_necessary_process_images(  # noqa
            saved_medias=saved_medias,
            message_data=media_murcho_message_data
        )

        expected_verified_images = self.mount_expected_verified_images(
            media_from_db_expected_murcho
        )
        assert verified_images == expected_verified_images

    def test_when_unprocessed_image_on_input_images_then_return_only_added_image_necessary_process(  # noqa
        self,
        record_processor: MediaRecordProcessor,
        media_from_db_expected_murcho: Dict,
        media_murcho_message_data: Dict
    ):
        image: Dict = media_from_db_expected_murcho['original']['images'].pop(0)  # noqa
        details = media_from_db_expected_murcho['image_details'].pop(0)
        image_name = media_from_db_expected_murcho['images'].pop(0)

        saved_medias = deepcopy(media_from_db_expected_murcho)

        media_from_db_expected_murcho['original']['images'].append(image)
        media_from_db_expected_murcho['image_details'].append(details)
        media_from_db_expected_murcho['images'].append(image_name)
        media_murcho_message_data['images'] = media_from_db_expected_murcho['original']['images']  # noqa

        verified_images: Dict = record_processor._check_has_necessary_process_images(  # noqa
            saved_medias=saved_medias,
            message_data=media_murcho_message_data
        )

        expected_verified_images = self.mount_expected_verified_images(
            media_from_db_expected_murcho
        )
        expected_verified_images[image['url']] = {'necessary_process': True}

        assert verified_images == expected_verified_images

    def test_when_saved_medias_without_original_field_then_return_all_necessary_process(  # noqa
        self,
        record_processor: MediaRecordProcessor,
        media_from_db_expected_murcho: Dict,
        media_murcho_message_data: Dict
    ):
        images: List[Dict] = media_from_db_expected_murcho['original']['images']  # noqa
        media_from_db_expected_murcho.pop('original')
        media_murcho_message_data['images'] = images

        verified_images: Dict = record_processor._check_has_necessary_process_images(  # noqa
            saved_medias=media_from_db_expected_murcho,
            message_data=media_murcho_message_data
        )

        assert verified_images == {
            image['url']: {'necessary_process': True}
            for image in images
        }

    def test_when_message_without_images_then_return_empty_dict(  # noqa
        self,
        record_processor: MediaRecordProcessor,
        media_from_db_expected_murcho: Dict,
        media_murcho_message_data: Dict
    ):
        saved_medias = deepcopy(media_from_db_expected_murcho)
        media_murcho_message_data['images'] = []

        verified_images: Dict = record_processor._check_has_necessary_process_images(  # noqa
            saved_medias=saved_medias,
            message_data=media_murcho_message_data
        )

        assert verified_images == {}

    def test_when_check_has_necessary_process_images_changed_image_saved_then_return_process_images(  # noqa
        self,
        record_processor: MediaRecordProcessor,
        media_from_db_expected_murcho: Dict,
        media_murcho_message_data: Dict
    ):
        image: Dict = media_from_db_expected_murcho['original']['images'][0]  # noqa
        details = media_from_db_expected_murcho['image_details'][0]
        image_name = media_from_db_expected_murcho['images'][0]

        media_murcho_message_data['images'] = [
            media_from_db_expected_murcho['original']['images'][1]
        ]

        media_from_db_expected_murcho['original'] = {'images': [image]}
        media_from_db_expected_murcho['image_details'] = [details]
        media_from_db_expected_murcho['images'] = [image_name]
        media_from_db_expected_murcho['original_images'] = [
            media_from_db_expected_murcho['original_images'][0]
        ]

        verified_images: Dict = record_processor._check_has_necessary_process_images(  # noqa
            media_from_db_expected_murcho,
            media_murcho_message_data
        )

        expected = {
            media_murcho_message_data['images'][0]['url']: {'necessary_process': True},  # noqa
            image['url']: {**details, **{'necessary_process': True}}
        }
        assert verified_images == expected

    def test_when_message_not_changed_images_then_skip_message_without_upload(
        self,
        record_processor: MediaRecordProcessor,
        medias_collection: Collection,
        patch_patolino_product_post: Mock,
        patch_storage_manager_property: Mock,
        patch_pubsub_property: Mock,
        media_from_db_expected_murcho: Dict,
        media_murcho_message_data: Dict
    ):
        medias_collection.insert_one(media_from_db_expected_murcho)
        with patch_storage_manager_property as mock_storage_manager:
            with patch_patolino_product_post as patolino_mock:
                with patch_pubsub_property as mock_pubsub:
                    assert record_processor.create(media_murcho_message_data)

        assert not mock_storage_manager.upload.called
        assert patolino_mock.call_count == 1
        assert patolino_mock.call_args[0][1]['code'] == MEDIA_UNFINISHED_PROCESS  # noqa
        assert not mock_pubsub.publish.called

    def test_when_message_not_changed_images_but_origin_rebuild_then_send_message_without_upload(  # noqa
        self,
        record_processor: MediaRecordProcessor,
        medias_collection: Collection,
        patch_patolino_product_post: Mock,
        patch_storage_manager_property: Mock,
        patch_pubsub_property: Mock,
        media_from_db_expected_murcho: Dict,
        media_murcho_message_data: Dict
    ):
        media_murcho_message_data.update({'origin': 'rebuild'})
        medias_collection.insert_one(media_from_db_expected_murcho)
        with patch_storage_manager_property as mock_storage_manager:
            with patch_patolino_product_post as patolino_mock:
                with patch_pubsub_property as mock_pubsub:
                    assert record_processor.create(media_murcho_message_data)

        assert not mock_storage_manager.upload.called
        assert patolino_mock.call_count == 1
        assert patolino_mock.call_args[0][1]['code'] == MEDIA_SUCCESS_CODE  # noqa
        assert mock_pubsub.publish.called

    def test_when_message_not_changed_images_but_included_video_then_skip_upload_but_process_message(  # noqa
        self,
        record_processor: MediaRecordProcessor,
        medias_collection: Collection,
        patch_patolino_product_post: Mock,
        patch_storage_manager_property: Mock,
        patch_pubsub_property: Mock,
        patch_notification_put: Mock,
        media_from_db_expected_murcho: Dict,
        media_murcho_message_data: Dict,
        mock_product_videos_message_data: List
    ):
        medias_collection.insert_one(media_from_db_expected_murcho)
        media_murcho_message_data['videos'] = mock_product_videos_message_data

        with patch_storage_manager_property as mock_storage_manager:
            with patch_patolino_product_post as patolino_mock:
                with patch_pubsub_property as mock_pubsub:
                    with patch_notification_put as mock_notification_put:
                        assert record_processor.create(
                            media_murcho_message_data
                        )

        assert not mock_storage_manager.upload.called
        assert patolino_mock.call_count == 1
        assert patolino_mock.call_args[0][1]['code'] == MEDIA_SUCCESS_CODE  # noqa
        assert mock_pubsub.publish.called
        assert mock_notification_put.called

    def test_when_message_changed_images_then_upload_and_notify(  # noqa
        self,
        record_processor: MediaRecordProcessor,
        medias_collection: Collection,
        patch_patolino_product_post: Mock,
        patch_storage_manager_property: Mock,
        patch_pubsub_property: Mock,
        patch_notification_put: Mock,
        media_from_db_expected_murcho: Dict,
        media_murcho_message_data: Dict,
    ):
        image: Dict = media_from_db_expected_murcho['original']['images'][0]  # noqa
        details = media_from_db_expected_murcho['image_details'][0]
        image_name = media_from_db_expected_murcho['images'][0]

        media_murcho_message_data['images'] = [
            media_from_db_expected_murcho['original']['images'][1]
        ]

        media_from_db_expected_murcho['original'] = {'images': [image]}
        media_from_db_expected_murcho['image_details'] = [details]
        media_from_db_expected_murcho['images'] = [image_name]
        media_from_db_expected_murcho['original_images'] = [
            media_from_db_expected_murcho['original_images'][0]
        ]

        medias_collection.insert_one(media_from_db_expected_murcho)

        with patch_storage_manager_property as mock_storage_manager:
            with patch_patolino_product_post as patolino_mock:
                with patch_pubsub_property as mock_pubsub:
                    with patch_notification_put as mock_notification_put:
                        assert record_processor.create(
                            media_murcho_message_data
                        )

        assert mock_storage_manager.upload.called
        assert patolino_mock.call_count == 1
        assert patolino_mock.call_args[0][1]['code'] == MEDIA_SUCCESS_CODE  # noqa
        assert mock_pubsub.publish.called
        assert mock_notification_put.called

    def test_when_check_has_changed_medias_without_saved_images_then_return_true(  # noqa
        self,
        record_processor: MediaRecordProcessor,
        media_from_db_expected_murcho: Dict,
    ):
        assert record_processor._has_changed_medias(
            saved_medias={},
            new_medias=media_from_db_expected_murcho
        )

    def test_when_check_has_changed_medias_without_changes_then_return_false(
        self,
        record_processor: MediaRecordProcessor,
        media_from_db_expected_murcho: Dict,
    ):
        assert not record_processor._has_changed_medias(
            saved_medias=media_from_db_expected_murcho,
            new_medias=media_from_db_expected_murcho
        )

    @pytest.mark.parametrize('field', ['audios', 'videos', 'podcasts'])
    def test_when_check_has_changed_medias_partial_processing_then_return_true(
        self,
        record_processor: MediaRecordProcessor,
        media_from_db_expected_murcho: Dict,
        field: str
    ):
        new_medias = deepcopy(media_from_db_expected_murcho)
        for delete_field in list(new_medias.keys()):
            if delete_field not in {field, 'seller_id', 'sku'}:
                new_medias.pop(delete_field, None)

        assert record_processor._has_changed_medias(
            saved_medias=media_from_db_expected_murcho,
            new_medias=new_medias
        )

    def test_when_check_has_changed_medias_without_original_field_then_return_true(  # noqa
        self,
        record_processor: MediaRecordProcessor,
        media_from_db_expected_murcho: Dict,
    ):
        saved_medias = deepcopy(media_from_db_expected_murcho)
        saved_medias.pop('original', None)
        assert record_processor._has_changed_medias(
            saved_medias=saved_medias,
            new_medias=media_from_db_expected_murcho
        )

    def test_when_check_has_changed_medias_changed_order_images_then_return_true(  # noqa
        self,
        record_processor: MediaRecordProcessor,
        media_from_db_expected_murcho: Dict,
    ):
        new_medias = deepcopy(media_from_db_expected_murcho)
        new_medias['original']['images'].append(
            new_medias['original']['images'].pop(0)
        )
        for image_field in {'image_details', 'original_images'}:
            new_medias[image_field].append(new_medias[image_field].pop(0))

        assert record_processor._has_changed_medias(
            saved_medias=media_from_db_expected_murcho,
            new_medias=new_medias
        )

    def test_when_check_has_changed_medias_changed_disorder_image_content_then_return_false(  # noqa
        self,
        record_processor: MediaRecordProcessor,
        media_from_db_expected_murcho: Dict,
    ):
        image = media_from_db_expected_murcho['original']['images'].pop()
        new_medias = deepcopy(media_from_db_expected_murcho)
        saved_medias = deepcopy(media_from_db_expected_murcho)

        new_medias['original']['images'].append(
            {'hash': image['hash'], 'url': image['url']}
        )

        saved_medias['original']['images'].append(
            {'url': image['url'], 'hash': image['hash']}
        )

        assert not record_processor._has_changed_medias(
            saved_medias=saved_medias,
            new_medias=new_medias
        )
