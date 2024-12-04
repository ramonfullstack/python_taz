import pytest


class TestProductMediasSkuSellerHandler:

    @pytest.fixture
    def mock_url(self):
        return '/product/medias/seller/{seller}/sku/{sku}'

    def test_list_medias(
        self,
        client,
        save_medias,
        save_product,
        product,
        mock_url
    ):
        response = client.get(
            mock_url.format(
                sku=product['sku'],
                seller=product['seller_id']
            )
        )

        assert response.status_code == 200
        assert 'images' in response.json['data']
        assert response.json['data']['images'] == [
            'https://x.xx.xxx/600x400/fritadeira-eletrica-air-fryer-sem-oleo-mondial-af-14-32l-timer/magazineluiza/023384700/d2e14e48997a911745931e6a2991b2cf.jpg' # noqa
        ]

    def test_list_medias_should_return_404_when_no_product_found(
        self,
        client,
        product,
        mock_url
    ):
        response = client.get(
            mock_url.format(
                sku=product['sku'],
                seller=product['seller_id']
            )
        )

        assert response.status_code == 404


class TestProductMediasNavigationIdHandler:

    @pytest.fixture
    def mock_url(self):
        return '/product/medias/navigation_id/{navigation_id}'

    def test_list_medias(
        self,
        client,
        save_medias,
        save_product,
        product,
        mock_url
    ):
        response = client.get(
            mock_url.format(
                navigation_id=product['navigation_id'],
            )
        )

        assert response.status_code == 200
        assert 'images' in response.json['data']
        assert response.json['data']['images'] == [
            'https://x.xx.xxx/600x400/fritadeira-eletrica-air-fryer-sem-oleo-mondial-af-14-32l-timer/magazineluiza/023384700/d2e14e48997a911745931e6a2991b2cf.jpg' # noqa
        ]

    def test_list_medias_should_return_404_when_no_medias_found(
        self,
        client,
        save_product,
        product,
        mock_url
    ):
        response = client.get(
            mock_url.format(
                navigation_id=product['navigation_id'],
            )
        )

        assert response.status_code == 404
