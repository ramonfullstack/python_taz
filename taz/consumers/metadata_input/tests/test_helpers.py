import pytest

from taz.constants import SOURCE_METABOOKS
from taz.consumers.metadata_input.helpers import _get_images


class TestHelperGetImages:

    @pytest.fixture
    def taz_images(self):
        return {
            'medias': {
                'images': [
                    'https://img-tweety-sandbox.mlcdn.com.br/8806098430031/image/044af14b50ea8110d1911d6aaba1dbad.JPEG',  # noqa
                    'https://img-tweety-sandbox.mlcdn.com.br/8806098430031/image/045aa14b50eb8120d1912d6baba1dbad.JPEG',  # noqa
                    'https://img-tweety-sandbox.mlcdn.com.br/8806098430031/image/046ad14b50ec8130d1913d6caba1dbad.JPEG',  # noqa
                    'https://img-tweety-sandbox.mlcdn.com.br/8806098430031/image/047at14b50ed8140d1914d6daba1dbad.JPEG'  # noqa
                ],
                'videos': [],
                'podcasts': [],
                'manuals': []
            }
        }

    @pytest.fixture
    def metabooks_images(self):
        return {
            'supportingResources': [
                {
                    'resourceMode': '03',
                    'resourceForm': '02',
                    'fileFormat': 'D502',
                    'exportedLink': 'https://api.metabooks.com/api/v1/cover/9788577533350/m',  # noqa
                    'resourceContentType': '01',
                    'md5Hash': '8b47732-af36b31fbcc6-3e1d84-e6613ae',
                    'contentAudience': [
                        '00'
                    ]
                },
                {
                    'resourceMode': '03',
                    'resourceForm': '02',
                    'fileFormat': 'D502',
                    'exportedLink': 'https://api.metabooks.com/api/v1/asset/mmo/file/f3e096aba4d948f281299e16bb9016f8',  # noqa
                    'resourceContentType': '02',
                    'contentAudience': [
                        '00'
                    ]
                },
                {
                    'resourceMode': '04',
                    'resourceForm': '02',
                    'fileFormat': 'E107',
                    'filename': '9788577533350_1_capitulo.pdf',
                    'filesizeExact': 1263982,
                    'md5Hash': '8b47732af36b31fbcc63e1d84e6613ae',
                    'sha256Hash': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',  # noqa
                    'exportedLink': 'https://api.metabooks.com/api/v1/asset/mmo/file/b7bcfd94c0a940839ae3176f283bab5a',  # noqa
                    'lastUpdated': '20190118',
                    'resourceContentType': '15',
                    'contentAudience': [
                        '00'
                    ]
                }
            ]
        }

    def test_should_get_images_from_metabooks(self, metabooks_images):
        images = _get_images(metabooks_images, SOURCE_METABOOKS)
        assert len(images) == 2

        for image in images:
            assert '-' not in image['hash']

    def test_should_get_ordered_images_from_metabooks(self, metabooks_images):
        metabooks_images['supportingResources'] = sorted(
            metabooks_images['supportingResources'],
            key=lambda r: r['resourceContentType'],
            reverse=True
        )

        images = _get_images(metabooks_images, SOURCE_METABOOKS)
        assert images[0]['hash'] == '8b47732af36b31fbcc63e1d84e6613ae'

    def test_should_get_images_from_other_sources(self, taz_images):
        images = _get_images(taz_images, 'murcho')
        assert len(images) == 4

        for image in images:
            assert '-' not in image['hash']

    def test_should_get_ordered_images_other_sources(self, taz_images):
        images = _get_images(taz_images, 'murcho')
        assert images[0]['hash'] == '044af14b50ea8110d1911d6aaba1dbad'
