import logging
import operator
import string
from typing import Dict, List

from simple_settings import settings

IMAGE_PATH = f'{settings.MEDIA_BASE_PATH}/{settings.IMAGE_BASE_PATH}'
AUDIO_PATH = f'{settings.MEDIA_BASE_PATH}/{settings.AUDIO_BASE_PATH}'
PODCAST_PATH = f'{settings.MEDIA_BASE_PATH}/{settings.PODCAST_BASE_PATH}'

logger = logging.getLogger(__name__)


class ListMedia:
    @staticmethod
    def image_path_prefix(sku: str) -> str:
        return f'{IMAGE_PATH}/{sku[:2]}/{sku}'

    @staticmethod
    def audio_path_prefix(sku: str) -> str:
        return f'{AUDIO_PATH}/{sku[:3]}/{sku[3:6]}/{sku[6:9]}/{sku}'

    @staticmethod
    def podcast_path_prefix(sku: str) -> str:
        return f'{PODCAST_PATH}/{sku[0:7]}'

    @staticmethod
    def get_filename(file_path: str) -> str:
        try:
            return file_path.split('/')[-1].split('.')[0]
        except Exception:
            return file_path

    @staticmethod
    def get_bucket_items(bucket_prefix, storage_manager, media_type):
        types_extensions = {
            'images': 'jpg',
            'podcasts': 'mp3',
            'audios': 'mp3'
        }
        letters = ['']
        letters.extend(list(string.ascii_lowercase))
        valid_blobs = []
        for letter in letters:
            extension = types_extensions.get(media_type, 'jpg')
            filename = f'{bucket_prefix}{letter}.{extension}'
            blob = storage_manager.get_blob_with_hash(filename)
            if not blob:
                break

            valid_blobs.append(blob)
        return valid_blobs

    @staticmethod
    def find_skus_paths(sku: str, storage_manager) -> Dict[str, List]:
        if not sku or len(sku) < settings.SKU_MIN_SIZE:
            logger.debug(f'no medias for {sku}...')
            return {
                'images': [],
                'audios': [],
                'podcasts': [],
            }
        media_blobs = {
            'images': ListMedia.get_bucket_items(
                ListMedia.image_path_prefix(sku),
                storage_manager,
                media_type='images'
            ),
            'audios': ListMedia.get_bucket_items(
                ListMedia.audio_path_prefix(sku),
                storage_manager,
                media_type='audios'
            ),
            'podcasts': ListMedia.get_bucket_items(
                ListMedia.podcast_path_prefix(sku),
                storage_manager,
                media_type='podcasts'
            )
        }

        medias_paths = {
            'images': [],
            'audios': [],
            'podcasts': [],
        }
        for media_type, blobs in media_blobs.items():
            for blob in blobs:
                filename = ListMedia.get_filename(blob.name)
                if not len(filename) <= len(sku) + 1:
                    continue

                medias_paths[media_type].append({
                    'url': blob.public_url,
                    'hash': blob.crc32c,
                })

        medias_paths['images'].sort(key=operator.itemgetter('url'))
        medias_paths['audios'].sort(key=operator.itemgetter('url'))
        medias_paths['podcasts'].sort(key=operator.itemgetter('url'))
        logger.debug(f'{sku} medias: {medias_paths}')
        return medias_paths
