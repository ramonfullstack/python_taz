import json

import pytest
from simple_settings.utils import settings_stub

from taz import constants
from taz.api.pending.models import PendingProductModel
from taz.api.products.models import RawProductModel
from taz.core.matching.common.samples import ProductSamples


class TestListPendingHandler:

    @pytest.fixture
    def mock_list_url(self):
        return '/pending/list'

    @pytest.mark.parametrize('query_string,expected_data', [
        ('', 3),
        ('seller=seller_a', 1),
    ])
    def test_list_pending_products(
        self,
        client,
        save_pending_products,
        mock_list_url,
        query_string,
        expected_data
    ):
        response = client.get(
            mock_list_url,
            query_string=query_string
        )

        assert len(response.json['data']) == expected_data

    def test_list_pending_products_with_filter_and_without_results(
        self, client, mock_list_url
    ):
        response = client.get(mock_list_url, query_string='seller=seller_a')

        assert len(response.json['data']) == 0

    def test_list_pending_products_without_results(
        self, client, mock_list_url
    ):
        response = client.get(mock_list_url)

        assert len(response.json['data']) == 0


class TestPendingHandler:

    @pytest.fixture
    def mock_url(self):
        return '/pending/seller/{}/sku/{}'

    @pytest.fixture
    def invalid_parameter(self):
        return {'test': 'murcho'}

    @pytest.fixture
    def valid_parameter(self):
        return {
            'sellers': [
                {'sku': '82323jjjj3', 'seller_id': 'seller_a'},
                {'sku': '098asdwe28', 'seller_id': 'seller_b'},
                {'sku': 'ou23ou23ou', 'seller_id': 'seller_c'},
            ]
        }

    def test_get_pending_product(
        self, client, save_pending_products, mock_url
    ):
        product = ProductSamples.seller_a_variation_with_parent()

        response = client.get(mock_url.format(
            product['seller_id'], product['sku']
        ))

        assert response.json['seller_id'] == product['seller_id']
        assert response.json['sku'] == product['sku']

    def test_get_pending_product_returns_not_found(
        self, client, mock_url
    ):
        product = ProductSamples.seller_a_variation_with_parent()

        response = client.get(mock_url.format(
            product['seller_id'], product['sku']
        ))

        assert response.status_code == 404

    def test_remove_pending_product(
        self, client, save_raw_products, save_pending_products, mock_url
    ):
        product = ProductSamples.seller_a_variation_with_parent()

        response = client.delete(mock_url.format(
            product['seller_id'], product['sku']
        ))

        assert response.status_code == 204

        raw_product = RawProductModel.objects.get(
            seller_id=product['seller_id'],
            sku=product['sku']
        )

        assert raw_product['matching_strategy'] == constants.SINGLE_SELLER_STRATEGY  # noqa
        assert raw_product['disable_on_matching'] is False

    def test_remove_pending_product_when_not_exists(
        self, client, save_raw_products, mock_url
    ):
        product = ProductSamples.seller_a_variation_with_parent()

        response = client.delete(mock_url.format(
            product['seller_id'], product['sku']
        ))

        assert response.status_code == 204

    @settings_stub(
        DEFAULT_MATCHING_STRATEGY=constants.AUTO_BUYBOX_STRATEGY
    )
    def test_put_pending_product_returns_success(
        self, client, save_pending_products, save_raw_products,
        valid_parameter, mock_url
    ):
        product = ProductSamples.seller_a_variation_with_parent()
        seller_id, sku = product['seller_id'], product['sku']

        response = client.put(
            mock_url.format(seller_id, sku),
            body=json.dumps(valid_parameter)
        )

        assert response.status_code == 200
        assert RawProductModel.objects().count() == 3

        raw_products = RawProductModel.objects()
        for raw_product in raw_products:
            assert 'title' in raw_product
            assert 'reference' in raw_product
            assert 'brand' in raw_product
            assert 'parent_sku' in raw_product
            assert 'ean' in raw_product
            assert 'categories' in raw_product
            assert 'dimensions' in raw_product
            assert raw_product['matching_strategy'] == constants.AUTO_BUYBOX_STRATEGY  # noqa
            assert raw_product['disable_on_matching'] is False

        assert PendingProductModel.objects.count() == 0

    def test_put_pending_duplicated_unifies_and_returns_success(
        self, client, save_pending_products, valid_parameter, mock_url
    ):
        raw_products = [
            ProductSamples.seller_a_variation_with_parent(),
            ProductSamples.seller_b_variation_with_parent(),
            ProductSamples.seller_c_variation_with_parent(),
            ProductSamples.seller_a_variation_with_parent(),
            ProductSamples.seller_b_variation_with_parent(),
            ProductSamples.seller_c_variation_with_parent()
        ]

        for product in raw_products:
            RawProductModel(**product).save()

        product = ProductSamples.seller_a_variation_with_parent()
        seller_id, sku = product['seller_id'], product['sku']

        response = client.put(
            mock_url.format(seller_id, sku),
            body=json.dumps(valid_parameter)
        )

        assert response.status_code == 500

    @settings_stub(
        DEFAULT_MATCHING_STRATEGY=constants.AUTO_BUYBOX_STRATEGY
    )
    def test_put_pending_product_returns_success_with_pending_not_found(
        self, client, save_raw_products, valid_parameter, mock_url
    ):
        product = ProductSamples.seller_a_variation_with_parent()
        PendingProductModel(**product).save()

        seller_id, sku = product['seller_id'], product['sku']

        response = client.put(
            mock_url.format(seller_id, sku),
            body=json.dumps(valid_parameter)
        )

        assert response.status_code == 200

        raw_products = RawProductModel.objects()
        for raw_product in raw_products:
            assert raw_product['matching_strategy'] == constants.AUTO_BUYBOX_STRATEGY  # noqa

        assert PendingProductModel.objects.count() == 0

    def test_put_pending_product_returns_bad_request_invalid_parameter(
        self, client, mock_url
    ):
        product = ProductSamples.seller_a_variation_with_parent()
        seller_id, sku = product['seller_id'], product['sku']

        response = client.put(
            mock_url.format(seller_id, sku)
        )

        assert response.status_code == 400

    def test_put_pending_product_returns_bad_request_comparison(
        self, client, save_pending_products, save_raw_products, mock_url
    ):
        product = ProductSamples.seller_a_variation_with_parent()
        seller_id, sku = product['seller_id'], product['sku']

        sellers = {'sellers': [{'sku': 'ABC', 'seller_id': 'murcho'}]}

        response = client.put(
            mock_url.format(seller_id, sku),
            body=json.dumps(sellers)
        )

        assert response.status_code == 400

    def test_put_pending_product_returns_bad_request_and_not_records_database(
        self, client, save_pending_products, save_raw_products,
        invalid_parameter, mock_url
    ):
        product = ProductSamples.seller_a_variation_with_parent()
        seller_id, sku = product['seller_id'], product['sku']

        response = client.put(
            mock_url.format(seller_id, sku),
            body=json.dumps(invalid_parameter)
        )

        assert response.status_code == 400

    def test_put_pending_product_returns_pending_not_found(
        self, client, valid_parameter, mock_url
    ):
        product = ProductSamples.seller_a_variation_with_parent()

        response = client.put(mock_url.format(
            product['seller_id'], product['sku']
        ), body=json.dumps(valid_parameter))

        assert response.status_code == 404


class TestPendingSellerHandler:

    def test_get_pending_sellers_list(self, client, save_pending_products):
        response = client.get('/pending/sellers')

        sellers = response.json['data']
        assert len(sellers) == 3
        assert sellers[0] == 'seller_a'

    def test_get_pending_sellers_returns_empty_list(self, client):
        response = client.get('/pending/sellers')
        assert len(response.json['data']) == 0
