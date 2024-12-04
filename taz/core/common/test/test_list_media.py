from unittest.mock import patch

import pytest
from google.cloud import storage
from simple_settings import settings

from taz.consumers.core.google.storage import StorageManager
from taz.core.common.list_media import (
    AUDIO_PATH,
    IMAGE_PATH,
    PODCAST_PATH,
    ListMedia
)


class StorageMock:
    def __init__(self, name, public_url):
        self.name = name
        self.public_url = f'{public_url}/{name}'
        self.crc32c = 'fake-hash'


class TestListMedia:
    @pytest.fixture
    def public_url(self):
        return (
            f'https://storage.googleapis.com/{settings.MEDIA_LIST_BUCKET}/'
            'magazineluiza/img'
        )

    @pytest.fixture
    def sku(self):
        return '123456789'

    @pytest.fixture
    def images(self, sku, public_url):
        path = public_url + '/produto_grande/' + sku[:2]
        return [
            StorageMock(f'{sku}{letter}.jpg', path)
            for letter in 'a,b,c'.split(',')
        ] + [
            StorageMock(f'{sku}121213{letter}.jpg', path)
            for letter in 'a,b,c'.split(',')
        ]

    @pytest.fixture
    def audios(self, sku, public_url):
        path = public_url + f'/audio/{sku[:3]}/{sku[3:6]}/{sku[6:9]}'
        return [
            StorageMock(f'{sku}{letter}.mp3', path)
            for letter in 'a,b,c'.split(',')
        ] + [
            StorageMock(f'{sku}121213{letter}.mp3', path)
            for letter in 'a,b,c'.split(',')
        ]

    @pytest.fixture
    def podcasts(self, sku, public_url):
        path = public_url + f'/podCast/{sku[0:7]}'
        return [
            StorageMock(f'{sku}{letter}.mp3', path)
            for letter in 'a,b,c'.split(',')
        ] + [
            StorageMock(f'{sku}121213{letter}.mp3', path)
            for letter in 'a,b,c'.split(',')
        ]

    def test_get_filename(self, sku):
        assert ListMedia.get_filename(
            f'magazineluiza/img/produto_grande/{sku[:2]}/{sku}.jpg'
        ) == sku

    def test_image_path_prefix(self, sku):
        expected = f'{IMAGE_PATH}/12/123456789'
        assert ListMedia.image_path_prefix(sku) == expected

    def test_audio_path_prefix(self, sku):
        expected = f'{AUDIO_PATH}/123/456/789/123456789'
        assert ListMedia.audio_path_prefix(sku) == expected

    def test_podcast_path_prefix(self, sku):
        expected = f'{PODCAST_PATH}/1234567'
        assert ListMedia.podcast_path_prefix(sku) == expected

    @pytest.mark.parametrize('invalid_sku', [
        (False), (None), (''), ('1'), ('11'), ('111'),
        ('1111'), ('11111'), ('111111'), ('1111111'), ('11111111')
    ])
    def test_find_with_invalid_sku(self, invalid_sku):
        storage_manager = StorageManager(settings.MEDIA_LIST_BUCKET)
        assert ListMedia.find_skus_paths(invalid_sku, storage_manager) == {
            'images': [],
            'audios': [],
            'podcasts': [],
        }

    @patch.object(storage, 'Client')
    def test_get_bucket_items(self, gcp_mock, sku, public_url):
        def fake_get_blob_with_hash(bucket_prefix):
            return StorageMock(bucket_prefix, bucket_prefix)

        alphabet_size = 26
        storage_manager = StorageManager(settings.MEDIA_LIST_BUCKET)
        storage_manager.get_blob_with_hash = fake_get_blob_with_hash

        prefix = f'{public_url}/image/{sku[:3]}/{sku[3:6]}/{sku[6:9]}/{sku}'
        result = ListMedia.get_bucket_items(
            prefix,
            storage_manager,
            media_type='images'
        )
        assert len(result) == alphabet_size + 1

    @patch.object(storage, 'Client')
    def test_find_skus_paths(
        self,
        gcp_mock,
        sku,
        public_url,
        images,
        audios,
        podcasts
    ):
        def fake_get_items(bucket_prefix, *args, **kwargs):
            if 'produto_grande' in bucket_prefix:
                return images
            elif 'audio' in bucket_prefix:
                return audios
            elif 'podCast' in bucket_prefix:
                return podcasts
            return []

        ListMedia.get_bucket_items = fake_get_items
        audio_path = (
            f'{public_url}/audio/{sku[:3]}/{sku[3:6]}/{sku[6:9]}/{sku}'
        )
        expected = {
            'images': [
                {
                    'url': f'{public_url}/produto_grande/{sku[:2]}/{sku}a.jpg',
                    'hash': 'fake-hash'
                },
                {
                    'url': f'{public_url}/produto_grande/{sku[:2]}/{sku}b.jpg',
                    'hash': 'fake-hash'
                },
                {
                    'url': f'{public_url}/produto_grande/{sku[:2]}/{sku}c.jpg',
                    'hash': 'fake-hash'
                },
            ],
            'audios': [
                {
                    'url': f'{audio_path}a.mp3',
                    'hash': 'fake-hash'
                },
                {
                    'url': f'{audio_path}b.mp3',
                    'hash': 'fake-hash'
                },
                {
                    'url': f'{audio_path}c.mp3',
                    'hash': 'fake-hash'
                },
            ],
            'podcasts': [
                {
                    'url': f'{public_url}/podCast/{sku[0:7]}/{sku}a.mp3',
                    'hash': 'fake-hash'
                },
                {
                    'url': f'{public_url}/podCast/{sku[0:7]}/{sku}b.mp3',
                    'hash': 'fake-hash'
                },
                {
                    'url': f'{public_url}/podCast/{sku[0:7]}/{sku}c.mp3',
                    'hash': 'fake-hash'
                },
            ]
        }
        storage_manager = StorageManager(settings.MEDIA_LIST_BUCKET)
        result = ListMedia.find_skus_paths(sku, storage_manager)
        assert result == expected
