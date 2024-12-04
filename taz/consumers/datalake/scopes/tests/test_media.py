from typing import Dict
from unittest.mock import patch

import pytest
from pymongo.database import Database

from taz.consumers.datalake.scopes.media import Scope
from taz.core.matching.common.samples import ProductSamples


class TestMediaScope:

    @pytest.fixture
    def patch_medias(self):
        return patch.object(Scope, 'medias')

    @staticmethod
    def expected_result():
        return {
            'audios': ['/seller_a/audios/82323jjjj3/d2e14e48997a911745931e6a2991b2cf.wav'], # noqa
            'images': [
                '/{w}x{h}/titulo-descricao/seller_a/82323jjjj3/d2e14e48997a911745931e6a2991b2cf.jpg', # noqa
                '/{w}x{h}/titulo-descricao/seller_a/82323jjjj3/d2e14e48997a911745931e6a299saass.jpg' # noqa
            ],
            'seller_id': 'seller_a',
            'sku': '82323jjjj3',
            'videos': ['d2e14e48997a911745931e6a2991b2cf.mp4'],
            'image_details': None,
            'original_images': None,
            'podcasts': None
        }

    @pytest.fixture
    def mock_media_payload(self):
        product = ProductSamples.seller_a_variation_with_parent()
        return {
            'images': [
                'd2e14e48997a911745931e6a2991b2cf.jpg',
                'd2e14e48997a911745931e6a299saass.jpg'
            ],
            'audios': [
                'd2e14e48997a911745931e6a2991b2cf.wav'
            ],
            'videos': [
                'd2e14e48997a911745931e6a2991b2cf.mp4'
            ],
            'seller_id': product['seller_id'],
            'sku': product['sku']
        }

    @pytest.fixture
    def media_scope(self):
        return Scope(sku='82323jjjj3', seller_id='seller_a')

    @pytest.fixture
    def media_invalid_scope(self):
        return Scope(sku='mock', seller_id='mock')

    def test_get_data_should_return_media(
        self,
        media_scope,
        mock_media_payload,
        patch_medias
    ):
        with patch_medias as mock_medias:
            mock_medias.find_one.return_value = mock_media_payload
            scope_media = media_scope.get_data()

        assert scope_media == self.expected_result()

    def test_when_get_data_with_field_original_then_return_original_images_filled(  # noqa
        self,
        media_scope: Scope,
        mock_product_images_with_details: Dict,
        mongo_database: Database
    ):
        product = ProductSamples.seller_a_variation_with_parent()
        mock_product_images_with_details.update(
            {'seller_id': product['seller_id'], 'sku': product['sku']}
        )
        mongo_database.medias.insert_one(mock_product_images_with_details)

        payload = media_scope.get_data()
        assert 'original' not in payload
        assert payload['original_images'] == [
            image['url']
            for image in mock_product_images_with_details['original']['images']
        ]
