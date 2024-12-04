from unittest.mock import patch

import pytest

from taz.api.unified_objects.models import UnifiedObjectModel


class TestBuyBoxHandler:

    @pytest.fixture
    def seller_id(self):
        return 'magazineluiza'

    @pytest.fixture
    def sku(self):
        return '011704400'

    def test_get_buybox_products_returns_success(
        self,
        client,
        save_buybox_unified,
        seller_id,
        sku,
        logger_stream
    ):
        result = client.get('/buybox/seller/{}/sku/{}'.format(
            seller_id, sku
        ))

        product = result.json['data']
        unified_object = UnifiedObjectModel.objects.first()

        assert unified_object['title'] == product['title']
        assert unified_object['attributes'] == product['attributes']
        assert unified_object['categories'] == product['categories']
        assert 'Get buybox detail from sku' in logger_stream.getvalue()

    def test_get_buybox_products_returns_empty_result(self, client, seller_id):
        result = client.get('/buybox/seller/{}/sku/00000'.format(seller_id))
        assert result.status_code == 404

    def test_unified_objects_not_found(
        self,
        client,
        seller_id,
        save_buybox_unified,
        sku,
    ):
        with patch.object(UnifiedObjectModel, 'get') as mock:
            mock.return_value = {}
            result = client.get('/buybox/seller/{}/sku/{}'.format(
                seller_id, sku
            ))

        assert result.json == {'error_message': 'Not Found'}
        assert result.status_code == 404


class TestBuyBoxSellerHandler:

    def test_get_buybox_sellers_returns_success(
        self,
        client,
        save_buybox_product
    ):
        result = client.get('/buybox/sellers')
        assert len(result.json['data']) == 3

    def test_get_buybox_sellers_returns_not_found(self, client):
        result = client.get('/buybox/sellers')
        assert len(result.json['data']) == 0


class TestBuyBoxProductListHandler:

    @pytest.fixture
    def seller_id(self):
        return 'whirlpool'

    @pytest.fixture
    def seller_id_does_not_exists(self):
        return 'murcho'

    def test_buybox_product_list_returns_success(
        self,
        client,
        save_buybox_product,
        seller_id
    ):
        result = client.get('/buybox/products/{}'.format(seller_id))
        assert len(result.json['data']) == 1

    def test_buybox_product_list_returns_empty_list(
        self,
        client,
        save_buybox_product,
        seller_id_does_not_exists
    ):
        result = client.get('/buybox/products/{}'.format(
            seller_id_does_not_exists
        ))
        assert len(result.json['data']) == 0
