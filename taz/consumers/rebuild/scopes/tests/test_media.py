from unittest.mock import patch

import pytest

from taz import constants
from taz.consumers.rebuild.scopes.media import MediaRebuild
from taz.core.common.list_media import ListMedia
from taz.core.matching.common.samples import ProductSamples


class TestMediaRebuild:
    @pytest.fixture
    def product(self):
        return ProductSamples.magazineluiza_sku_193389600()

    @pytest.fixture
    def media(self):
        product = ProductSamples.magazineluiza_sku_193389600()
        return {
            'seller_id': product['seller_id'],
            'sku': product['sku'],
            'audios': ['/seller_a/audios/82323jjjj3/d2e14e48997a911745931e6a2991b2cf.wav'],  # noqa
            'videos': ['d2e14e48997a911745931e6a2991b2cf.mp4'],
            'podcasts': ['/seller_a/podcasts/82323jjjj3/d2e14e48997a911745931e6a2991b2cf.wav'],  # noqa
            'images': ['1.jpeg', '2.jpeg'],
            'original_images': [
                'https://site.com/1.jpeg',
                'https://site.com/2.jpeg',
            ]
        }

    @pytest.fixture
    def media_bucket(self):
        return {
            'audios': [
                '/seller_a/audios/82323jjjj3/d2e14e48997a911745931e6a2991b2cf.wav' # noqa
            ],
            'videos': [
                'd2e14e48997a911745931e6a2991b2cf.mp4'
            ],
            'podcasts': [
                '/seller_a/podcasts/82323jjjj3/d2e14e48997a911745931e6a2991b2cf.wav' # noqa
            ],
            'images': [
                'https://site.com/1.jpeg',
                'https://site.com/2.jpeg'
            ],
        }

    @pytest.fixture
    def rebuild(self):
        return MediaRebuild()

    def test_media_rebuild_successfully(
        self,
        rebuild,
        patch_publish_manager,
        mongo_database,
        product,
        media
    ):
        mongo_database.raw_products.insert_one(product)
        mongo_database.medias.insert_one(media)

        data = {
            'sku': product['sku'],
            'seller_id': product['seller_id']
        }

        with patch_publish_manager as mock_stream:
            ret = rebuild.rebuild('update', data)

        assert mock_stream.call_count == 1

        expected_args = {
            'action': 'update',  # noqa
            'data': {
                'images': [
                    'https://site.com/1.jpeg',
                    'https://site.com/2.jpeg'
                ],
                'origin': 'rebuild',
                'videos': ['d2e14e48997a911745931e6a2991b2cf.mp4'],
                'audios': ['/seller_a/audios/82323jjjj3/d2e14e48997a911745931e6a2991b2cf.wav'],  # noqa
                'podcasts': ['/seller_a/podcasts/82323jjjj3/d2e14e48997a911745931e6a2991b2cf.wav'],  # noqa
                **data,
            }
        }

        assert mock_stream.call_args_list[0][1].get('content') == expected_args
        assert ret is True

    def test_media_rebuild_without_medias(
        self,
        rebuild,
        patch_publish_manager,
        mongo_database,
        product,
    ):
        mongo_database.raw_products.insert_one(product)

        data = {
            'sku': product['sku'],
            'seller_id': product['seller_id']
        }

        with patch_publish_manager as mock_stream:
            ret = rebuild.rebuild('update', data)

        assert mock_stream.call_count == 0
        assert ret is True

    @pytest.mark.parametrize('seller_id,sku', [
        ('test', ''),
        ('', 'test'),
        ('', ''),
    ])
    def test_media_rebuild_without_required_params(
        self,
        rebuild,
        patch_publish_manager,
        mongo_database,
        product,
        media,
        seller_id,
        sku,
    ):
        mongo_database.raw_products.insert_one(product)
        mongo_database.medias.insert_one(media)

        data = {
            'seller_id': seller_id,
            'sku': sku
        }

        with patch_publish_manager as mock_stream:
            rebuild.rebuild('update', data)

        assert mock_stream.call_count == 0

    def test_media_rebuild_with_from_bucket_param_true(
        self,
        rebuild,
        patch_publish_manager,
        media_bucket,
    ):
        sku = 'test'
        seller_id = constants.MAGAZINE_LUIZA_SELLER_ID
        data = {
            'seller_id': seller_id,
            'sku': sku,
            'from_bucket': 'true'
        }

        with patch.object(ListMedia, 'find_skus_paths') as mock_list_media:
            with patch_publish_manager as mock_stream:
                mock_list_media.return_value = media_bucket
                rebuild.rebuild('update', data)

        assert mock_stream.call_count == 1
        assert mock_list_media.call_count == 1

        expected_args = {
            'action': 'update',  # noqa
            'data': {
                'images': [
                    'https://site.com/1.jpeg',
                    'https://site.com/2.jpeg'
                ],
                'origin': 'rebuild',
                'audios': ['/seller_a/audios/82323jjjj3/d2e14e48997a911745931e6a2991b2cf.wav'],  # noqa
                'podcasts': ['/seller_a/podcasts/82323jjjj3/d2e14e48997a911745931e6a2991b2cf.wav'],  # noqa
                'sku': sku,
                'seller_id': seller_id
            }
        }

        assert mock_stream.call_args_list[0][1].get('content') == expected_args

    def test_media_rebuild_with_from_bucket_param_false_dont_call_list_media(
        self,
        rebuild,
        patch_publish_manager,
    ):
        data = {
            'seller_id': 'test',
            'sku': 'test',
            'from_bucket': 'false'
        }

        with patch.object(ListMedia, 'find_skus_paths') as mock_list_media:
            with patch_publish_manager:
                rebuild.rebuild('update', data)
                assert mock_list_media.call_count == 0

    def test_media_rebuild_with_from_bucket_and_a_invalid_seller_id(
        self,
        rebuild,
        patch_publish_manager,
    ):
        data = {
            'seller_id': 'test',
            'sku': 'test',
            'from_bucket': 'true'
        }

        with patch.object(ListMedia, 'find_skus_paths') as mock_list_media:
            with patch_publish_manager:
                rebuild.rebuild('update', data)
                assert mock_list_media.call_count == 0
