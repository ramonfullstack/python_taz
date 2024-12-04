import pytest


class TestExportsSimpleProductHandler:

    @pytest.fixture
    def db_currency_price(self, mongo_database):
        price_with_currency = {
            'sku': '193389600',
            'seller_id': 'magazineluiza',
            'list_price': 234.56,
            'price': 123.45,
            'delivery_availability': 'nationwide',
            'stock_count': 321,
            'stock_type': 'on_seller',
            'checkout_price': 234.56,
            'currency': 'USD',
            'last_updated_at': '2024-06-01T00:21:25.866255'
        }

        mongo_database.prices.insert_one(price_with_currency)
        return price_with_currency

    def test_success_when_get_simple_product_with_currency(
        self,
        client,
        mongo_database,
        db_currency_price,
        mock_raw_products_payload
    ):

        for key, value in db_currency_price.items():
            if key in mock_raw_products_payload:
                mock_raw_products_payload[key] = value

        mock_raw_products_payload['currency'] = db_currency_price['currency']

        mongo_database.raw_products.insert_one(mock_raw_products_payload)
        response = client.get(
            '/exports/simple_product/seller_id/{seller_id}/sku/{sku}'.format(
                **mock_raw_products_payload
            )
        )
        assert response.status_code == 200

        data = response.json['data']
        assert data['currency'] == mock_raw_products_payload['currency']
        assert data['seller_id'] == mock_raw_products_payload['seller_id']
        assert data['sku'] == mock_raw_products_payload['sku']
        assert data['navigation_id'] == mock_raw_products_payload['navigation_id']  # noqa

    def test_when_get_simple_product_payload_then_return_payload(
        self,
        client,
        mongo_database,
        mock_raw_products_payload
    ):
        mongo_database.raw_products.insert_one(mock_raw_products_payload)
        response = client.get(
            '/exports/simple_product/seller_id/{seller_id}/sku/{sku}'.format(
                **mock_raw_products_payload
            )
        )
        assert response.status_code == 200

        data = response.json['data']
        assert data['seller_id'] == mock_raw_products_payload['seller_id']
        assert data['sku'] == mock_raw_products_payload['sku']
        assert data['navigation_id'] == mock_raw_products_payload['navigation_id']  # noqa

    def test_when_get_simple_product_payload_then_not_found(
        self,
        client
    ):
        response = client.get('/exports/simple_product/seller_id/fake/sku/fake')  # noqa
        assert response.status_code == 404


class TestExportsSimpleProductByNavigationIDHandler:

    def test_when_get_simple_product_by_navigation_id_payload_then_return_payload(  # noqa
        self,
        client,
        mongo_database,
        mock_raw_products_payload
    ):
        mongo_database.raw_products.insert_one(mock_raw_products_payload)
        response = client.get(
            '/exports/simple_product/navigation_id/{navigation_id}'.format(
                **mock_raw_products_payload
            )
        )
        assert response.status_code == 200

        data = response.json['data']
        assert data['seller_id'] == mock_raw_products_payload['seller_id']
        assert data['sku'] == mock_raw_products_payload['sku']
        assert data['navigation_id'] == mock_raw_products_payload['navigation_id']  # noqa

    def test_when_get_simple_product_by_navigation_id_payload_then_not_found(
        self,
        client
    ):
        response = client.get('/exports/simple_product/navigation_id/fake')
        assert response.status_code == 404


class TestExportsSourceProductHandler:

    def test_when_get_source_product_payload_then_return_payload(
        self,
        client,
        patch_raw_products_storage_get_bucket_data,
        mock_raw_products_payload
    ):
        with patch_raw_products_storage_get_bucket_data as mock_get_raw_product:  # noqa
            mock_get_raw_product.return_value = mock_raw_products_payload
            response = client.get(
                '/exports/source_product/seller_id/{seller_id}/sku/{sku}'.format(  # noqa
                    **mock_raw_products_payload
                )
            )
        assert response.status_code == 200

        data = response.json['data']
        assert data['seller_id'] == mock_raw_products_payload['seller_id']
        assert data['sku'] == mock_raw_products_payload['sku']
        assert data['navigation_id'] == mock_raw_products_payload['navigation_id']  # noqa

    def test_when_get_source_product_payload_then_not_found(
        self,
        client,
        patch_raw_products_storage_get_bucket_data
    ):
        with patch_raw_products_storage_get_bucket_data as mock_get_raw_product:  # noqa
            mock_get_raw_product.return_value = None
            response = client.get('/exports/source_product/seller_id/fake/sku/fake')  # noqa

        assert response.status_code == 404


class TestExportSourceProductByNavigationIDHandler:

    def test_when_get_source_product_by_navigation_id_payload_then_return_payload(  # noqa
        self,
        client,
        patch_raw_products_storage_get_bucket_data,
        mongo_database,
        mock_raw_products_payload
    ):
        mongo_database.raw_products.insert_one(mock_raw_products_payload)
        with patch_raw_products_storage_get_bucket_data as mock_get_raw_product:  # noqa
            mock_get_raw_product.return_value = mock_raw_products_payload
            response = client.get(
                '/exports/source_product/navigation_id/{navigation_id}'.format(  # noqa
                    **mock_raw_products_payload
                )
            )
        assert response.status_code == 200

        data = response.json['data']
        assert data['seller_id'] == mock_raw_products_payload['seller_id']
        assert data['sku'] == mock_raw_products_payload['sku']
        assert data['navigation_id'] == mock_raw_products_payload['navigation_id']  # noqa

    def test_when_get_source_product_by_navigation_id_payload_then_not_found(
        self,
        client,
        patch_raw_products_storage_get_bucket_data
    ):
        with patch_raw_products_storage_get_bucket_data as mock_get_raw_product:  # noqa
            mock_get_raw_product.return_value = None
            response = client.get('/exports/source_product/navigation_id/fake')  # noqa

        assert response.status_code == 404
