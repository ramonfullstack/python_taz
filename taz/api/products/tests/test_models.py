import json
from unittest import mock

import pytest

from taz import constants
from taz.api.common.exceptions import NotFound
from taz.api.products.models import RawProductModel, UnpublishProductModel
from taz.core.matching.common.samples import ProductSamples


class TestProductModel:

    def test_product_list_by_strategy_and_seller_returns_success(self):
        product = ProductSamples.seller_a_variation_with_parent()
        product['matching_strategy'] = constants.SINGLE_SELLER_STRATEGY

        RawProductModel(**product).save()

        response = RawProductModel.product_list_by_strategy_and_seller(
            strategy=product['matching_strategy'],
            seller_id=product['seller_id']
        )

        assert response[0]['sku'] == product['sku']
        assert response[0]['seller_id'] == product['seller_id']

    def test_product_list_by_strategy_and_seller_returns_empty(self):
        product = ProductSamples.seller_a_variation_with_parent()
        product['matching_strategy'] = constants.SINGLE_SELLER_STRATEGY
        product['disable_on_matching'] = True

        RawProductModel(**product).save()

        response = RawProductModel.product_list_by_strategy_and_seller(
            strategy=product['matching_strategy'],
            seller_id=product['seller_id']
        )

        assert not response

    def test_sellers_list(self):
        product = ProductSamples.seller_a_variation_with_parent()

        RawProductModel(**product).save()

        response = RawProductModel.get_sellers()

        assert response

    def test_sellers_list_should_return_empty(self):

        response = RawProductModel.get_sellers()

        assert not response


class TestUnpublishProductModel:

    @pytest.fixture
    def product(self):
        return {
            'navigation_id': '123123',
            'user': 'bugsbunny'
        }

    def test_get_product_by_navigation_id(self, product):
        UnpublishProductModel(**product).save()

        unpublished_product = UnpublishProductModel.get(
            navigation_id=product['navigation_id']
        )

        assert unpublished_product['navigation_id'] == product['navigation_id']

    def test_should_return_exception_getting_product_by_navigation_id(self):
        with pytest.raises(NotFound):
            UnpublishProductModel.get(navigation_id='test')

    def test_get_product_list(self, product):
        UnpublishProductModel(**product).save()

        unpublished_product = UnpublishProductModel.list()

        assert (
            unpublished_product[0]['navigation_id'] == product['navigation_id']
        )

    def test_get_product_list_with_navigation_id(self, product):
        UnpublishProductModel(**product).save()

        unpublished_product = UnpublishProductModel.list(
            product['navigation_id']
        )

        assert (
            unpublished_product[0]['navigation_id'] == product['navigation_id']
        )

    def test_should_return_exception_getting_product_list(self):
        with pytest.raises(NotFound):
            UnpublishProductModel.list()

    def test_list_unpublished_filter_query(self, product):
        class FakeProduct:
            def to_json(self, *args, **kwargs):
                return json.dumps({**product})

            def order_by(self, *args, **kwargs):
                return self

        UnpublishProductModel.objects = (
            mock.MagicMock(return_value=FakeProduct())
        )
        UnpublishProductModel.list(navigation_id='123123')
        query = {
            '$or': [{
                'navigation_id': '123123000'
            }, {
                'navigation_id': '123123'
            }]
        }
        UnpublishProductModel.objects.assert_called_with(__raw__=query)

    def test_list_unpublished_filters_result(self):
        products = [
            {
                'navigation_id': '123123',
                'user': 'bugsbunny'
            },
            {
                'navigation_id': '123123000',
                'user': 'bugsbunny'
            }
        ]
        for product in products:
            UnpublishProductModel(**product).save()

        result = UnpublishProductModel.list(navigation_id='123123')
        assert result
        assert len(result) == 2
