import pytest

from taz.core.common.media import _build_images, build_media, build_url_image
from taz.core.matching.common.samples import ProductSamples


@pytest.mark.parametrize(
    'sku,title,reference,seller_id,media_type,items,expected', [(
        '0123456 78',
        'Foo Bar',
        'Reference',
        'foobar',
        'images',
        [
            '02797ab37e154c2602411a444a8135ae.jpg',
            '07ce030d37e0ddc964522ff1e3d7a1cd.jpg',
            '094a38d9b88053098235bcb9f73eca21.jpg',
            'b0bf826a207f9ae90a5d98bcfac2ecd0.jpg'
        ],
        [
            '/{w}x{h}/foo-bar-reference/foobar/0123456-78/02797ab37e154c2602411a444a8135ae.jpg',  # noqa
            '/{w}x{h}/foo-bar-reference/foobar/0123456-78/07ce030d37e0ddc964522ff1e3d7a1cd.jpg',  # noqa
            '/{w}x{h}/foo-bar-reference/foobar/0123456-78/094a38d9b88053098235bcb9f73eca21.jpg',  # noqa
            '/{w}x{h}/foo-bar-reference/foobar/0123456-78/b0bf826a207f9ae90a5d98bcfac2ecd0.jpg'  # noqa
        ]
    ), (
        '012345678',
        'Foo Bar',
        'Reference',
        'foobar',
        'images',
        [
            {
                'hash': '32aa5a74194fbfb3827be141b8590239',
                'url': 'http://i.mlcdn.com.br/1500x1500/x-020902000.jpg'
            },
            {
                'hash': '5a2813e7cb347f594c2aa7a6627ab015',
                'url': 'http://i.mlcdn.com.br/1500x1500/x-020902000b.jpg'
            },
            {
                'hash': '7b5f59adf03e4aa5c135ced1645039de',
                'url': 'http://i.mlcdn.com.br/1500x1500/x-020902000d.jpg'
            },
            {
                'hash': 'e95643dba662a37490e1205e45f21ce1',
                'url': 'http://i.mlcdn.com.br/1500x1500/x-020902000a.jpg'
            }
        ],
        [
            '/{w}x{h}/foo-bar-reference/foobar/012345678/32aa5a74194fbfb3827be141b8590239.jpg',  # noqa
            '/{w}x{h}/foo-bar-reference/foobar/012345678/5a2813e7cb347f594c2aa7a6627ab015.jpg',  # noqa
            '/{w}x{h}/foo-bar-reference/foobar/012345678/7b5f59adf03e4aa5c135ced1645039de.jpg',  # noqa
            '/{w}x{h}/foo-bar-reference/foobar/012345678/e95643dba662a37490e1205e45f21ce1.jpg'  # noqa
        ]
    ), (
        '012345678',
        'Foo Bar',
        'Reference',
        'foobar',
        'videos',
        ['05a9b6d4e857a06d9e77905ad08de7ba'],
        ['05a9b6d4e857a06d9e77905ad08de7ba']
    ), (
        '012345678',
        'Foo Bar',
        'Reference',
        'foobar',
        'audios',
        ['f31426b646795fb58bbe460f9e40f75b.mp3'],
        ['/foobar/audios/012345678/f31426b646795fb58bbe460f9e40f75b.mp3']
    ), (
        '012345678',
        'Foo Bar',
        'Reference',
        'foobar',
        'podcasts',
        ['f31426b646795fb58bbe460f9e40f75b.mp3'],
        ['/foobar/podcasts/012345678/f31426b646795fb58bbe460f9e40f75b.mp3']
    )]
)
def test_build_media(
    sku,
    title,
    reference,
    seller_id,
    media_type,
    items,
    expected
):
    build_medias = build_media(
        sku,
        title,
        reference,
        seller_id,
        media_type,
        items
    )
    assert build_medias == expected


def test_build_url_image():
    image = '/{w}x{h}/fritadeira-eletrica-air-fryer-sem-oleo-mondial-af-14-32l-timer/magazineluiza/023384700/d2e14e48997a911745931e6a2991b2cf.jpg' # noqa

    assert build_url_image(image) == 'https://x.xx.xxx/600x400/fritadeira-eletrica-air-fryer-sem-oleo-mondial-af-14-32l-timer/magazineluiza/023384700/d2e14e48997a911745931e6a2991b2cf.jpg' # noqa


def test_when_product_has_images_then_should_build_images_with_success(
    mock_product_images,
    mongo_database
):
    product = ProductSamples.magazineluiza_sku_011704400()
    images = _build_images(product, mongo_database.medias)

    assert images == [
        'https://x.xx.xxx/600x400/lava-loucas-brastemp-ative-blf08as-8-servicos/magazineluiza/011704400/d4a9dda16aebf1d8fe2bb115669c4155.jpg', # noqa
        'https://x.xx.xxx/600x400/lava-loucas-brastemp-ative-blf08as-8-servicos/magazineluiza/011704400/d4a9dda16aebf1d8fe2bb115669c4155.jpg', # noqa
        'https://x.xx.xxx/600x400/lava-loucas-brastemp-ative-blf08as-8-servicos/magazineluiza/011704400/c2d88c66d6d53a082e52787df7790c01.jpg', # noqa
        'https://x.xx.xxx/600x400/lava-loucas-brastemp-ative-blf08as-8-servicos/magazineluiza/011704400/4ba8da09a782be6a190a79419f4d51a9.jpg' # noqa
    ]


def test_when_product_no_has_images_then_should_return_empty_list(
    mongo_database
):
    product = ProductSamples.magazineluiza_sku_011704400()
    images = _build_images(product, mongo_database.medias)

    assert images == []
