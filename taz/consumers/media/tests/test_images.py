from unittest.mock import Mock, patch

import pytest
from simple_settings.utils import settings_stub

from taz.consumers.media.consumer import Media
from taz.consumers.media.images import ImageQueuer
from taz.core.matching.common.samples import ProductSamples


class TestImageQueuer:

    @pytest.fixture
    def patch_sqs(self):
        return patch('taz.consumers.media.images.SQSManager')

    @pytest.fixture
    def mock_sqs(self):
        return Mock()

    @pytest.fixture
    def image_queuer(self, patch_sqs, mock_sqs):
        with patch_sqs as mock:
            mock.return_value = mock_sqs
            return ImageQueuer()

    @pytest.fixture
    def variation_dict(self):
        return ProductSamples.whirlpool_sku_1227()

    @pytest.fixture
    def media_dict(self, variation_dict):
        return Media(
            sku=variation_dict['sku'],
            seller_id=variation_dict['seller_id'],
            media_type='images',
            url='http://luizalabs.com/fda3e9f79d0d63d4e5ea1a99dac34fbc.jpg',
            md5='dac2124b5c19b5a10c9b4e1c83910b81',
            content_type='image/jpeg'
        )

    @pytest.fixture
    def medias(self, media_dict):
        return {
            'images': [media_dict]
        }

    def test_process_image_successfully(
        self,
        image_queuer,
        variation_dict,
        medias,
        mock_sqs
    ):
        result = image_queuer.process_images(variation_dict, medias)

        assert mock_sqs.put.called
        assert result == {
            'action': 'create',
            'acme_id': '9106668',
            'images': ['https://x.xx.xxx/1500x1500/lavadora-brastemp-15kg/whirlpool/1227/dac2124b5c19b5a10c9b4e1c83910b81.jpg']  # noqa
        }

    def test_process_image_successfully_duplicated(
        self,
        image_queuer,
        variation_dict,
        medias,
        mock_sqs
    ):
        image_queuer.process_images(variation_dict, medias)
        image_queuer.process_images(variation_dict, medias)

        assert mock_sqs.put.call_count == 1

    @settings_stub(DISABLE_FTP_IMAGE=True)
    def test_disable_ftp_image(
        self,
        image_queuer,
        mock_sqs,
        variation_dict,
        medias
    ):
        image_queuer.process_images(variation_dict, medias)
        assert not mock_sqs.put.called

    def test_process_image_returns_empty(
        self, mock_sqs, image_queuer, variation_dict, medias
    ):
        variation_dict['seller_id'] = 'magazineluiza'

        result = image_queuer.process_images(variation_dict, medias)
        assert not result
