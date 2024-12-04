from taz.api.medias.models import MediaModel


class TestMediaModel:

    def test_get_media(self, save_medias, save_product, product):
        media = MediaModel.get_media(
            seller_id=product['seller_id'],
            sku=product['sku'],
            product=product
        )

        assert 'images' in media
        assert media['images'] == (
            ['/{w}x{h}/fritadeira-eletrica-air-fryer-sem-oleo-mondial-af-14-32l-timer/magazineluiza/023384700/d2e14e48997a911745931e6a2991b2cf.jpg'] # noqa
        )

    def test_get_media_should_return_empty_dict_when_no_media(self, product):
        media = MediaModel.get_media(
            seller_id=product['seller_id'],
            sku=product['sku'],
            product=product
        )

        assert media == {}
