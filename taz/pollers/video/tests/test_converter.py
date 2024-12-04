import pytest

from taz.constants import MAGAZINE_LUIZA_SELLER_ID
from taz.pollers.video.converter import VideoConverter


class TestVideoConverter:
    @pytest.fixture
    def database_row(self):
        return {
            'batch_key': '012345678',
            'video': 'http://video.com',
        }

    @pytest.fixture
    def converter(self):
        return VideoConverter()

    def test_should_convert_row(self, converter, database_row):
        converter.from_source([database_row])
        expected = {
            '012345678': {
                '012345678': {
                    'seller_id': MAGAZINE_LUIZA_SELLER_ID,
                    'sku': '012345678',
                    'videos': ['http://video.com'],
                }
            }
        }
        assert len(converter.get_items()) == 1
        assert expected == converter.get_items()

    def test_should_return_none_without_a_valid_row(self, converter):
        converter.from_source([None])
        assert len(converter.get_items()) == 0
