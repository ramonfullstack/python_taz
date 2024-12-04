from unittest.mock import PropertyMock, patch

import pytest

from taz import constants
from taz.api import RemoveMatchingHandler
from taz.api.products.models import RawProductModel
from taz.constants import UPDATE_ACTION
from taz.consumers.matching.consumer import MatchingRecordProcessor
from taz.core.matching.common.samples import ProductSamples


class TestMatchingHandler:

    @pytest.fixture
    def mock_url(self):
        return '/matching/seller/{}/sku/{}/'

    def test_matching_returns_success(
        self,
        client,
        save_raw_products,
        save_medias,
        save_prices,
        mock_url
    ):
        product = ProductSamples.seller_a_variation_with_parent()
        sku, seller_id = product['sku'], product['seller_id']

        result = client.get(
            mock_url.format(seller_id, sku)
        )

        sellers = result.json['data']['variations'][0]['sellers']

        media_expected = {
            'images': [
                '/{w}x{h}/caneca-xablau-branca-450ml-cxb450ml/seller_a/82323jjjj3/d2e14e48997a911745931e6a2991b2cf.jpg'  # noqa
            ]
        }

        price_expected = {
            'stock_type': 'on_seller',
            'stock_count': 321,
            'price': '123.45',
            'list_price': '234.56',
            'delivery_availability': 'nationwide',
            'seller_id': 'seller_a',
            'sku': '82323jjjj3'
        }

        assert len(sellers) == 3
        assert sellers[0]['title'] == product['title']
        assert sellers[0]['reference'] == product['reference']
        assert sellers[0]['brand'] == product['brand']
        assert sellers[0]['attributes'] == product['attributes']
        assert sellers[0]['navigation_id'] == product['navigation_id']
        assert sellers[0]['media'] == media_expected
        assert sellers[0]['price'] == price_expected

    def test_matching_returns_not_found(self, client, mock_url):
        product = ProductSamples.seller_a_variation_with_parent()
        sku, seller_id = product['sku'], product['seller_id']

        result = client.get(
            mock_url.format(seller_id, sku)
        )

        assert result.status_code == 404

    def test_matching_returns_price_empty(self, client, mock_url):
        product = ProductSamples.seller_a_variation_with_parent()
        sku, seller_id = product['sku'], product['seller_id']

        RawProductModel(**product).save()

        result = client.get(
            mock_url.format(seller_id, sku)
        )

        sellers = result.json['data']['variations'][0]['sellers']

        assert result.status_code == 200
        assert sellers[0]['price'] == {}

    def test_matching_returns_without_any_matching(
        self, client, save_prices, mock_url
    ):
        product = ProductSamples.seller_a_variation_with_parent()
        sku, seller_id = product['sku'], product['seller_id']

        RawProductModel(**product).save()

        result = client.get(
            mock_url.format(seller_id, sku)
        )

        sellers = result.json['data']['variations'][0]['sellers']

        assert len(sellers) == 1
        assert sellers[0]['title'] == product['title']
        assert sellers[0]['reference'] == product['reference']


class TestRemoveMatchingHandler:

    @pytest.fixture
    def consumer(self):
        return MatchingRecordProcessor(
            persist_changes=False,
            exclusive_strategy=False
        )

    @pytest.fixture
    def mock_matching_pubsub(self):
        return patch.object(
            RemoveMatchingHandler,
            'pubsub',
            new_callable=PropertyMock
        )

    def test_remove_matching_returns_success(
        self,
        client,
        mongo_database,
        patch_sqs_manager_put,
        consumer,
        mock_matching_pubsub,
    ):
        variations = [
            ProductSamples.magazineluiza_sku_011704201(),
            ProductSamples.whirlpool_sku_192(),
            ProductSamples.cookeletroraro_sku_2000160(),
            ProductSamples.magazineluiza_sku_011704400(),
            ProductSamples.cookeletroraro_sku_2000159(),
            ProductSamples.magazineluiza_sku_011704500(),
            ProductSamples.whirlpool_sku_335(),
            ProductSamples.magazineluiza_sku_011704301(),
            ProductSamples.cookeletroraro_sku_2000837(),
            ProductSamples.whirlpool_sku_334()
        ]

        for variation in variations:
            variation['matching_strategy'] = constants.AUTO_BUYBOX_STRATEGY

        mongo_database.raw_products.insert_many(variations)

        variation = ProductSamples.magazineluiza_sku_011704400()
        message = {
            'action': UPDATE_ACTION,
            'sku': variation['sku'],
            'seller_id': variation['seller_id'],
            'task_id': '186e1006ae3541128b6055b99bab7ca1',
            'timestamp': 0.1
        }

        consumer.persist_changes = True
        with patch_sqs_manager_put:
            consumer.process_message(message)

        assert mongo_database.unified_objects.count_documents({}) == 1

        navigation_id = variation['navigation_id']
        with mock_matching_pubsub:
            result = client.delete(f'/matching/remove/{navigation_id}/')

        assert result.status_code == 200

        with patch_sqs_manager_put:
            consumer.process_message(message)

        assert mongo_database.unified_objects.count_documents({}) == 2

    def test_remove_matching_returns_not_found(
        self,
        client,
        save_raw_products
    ):
        product = ProductSamples.seller_a_variation_with_parent()
        navigation_id = product['navigation_id']

        result = client.delete(f'/matching/remove/{navigation_id}/')
        assert result.status_code == 404
