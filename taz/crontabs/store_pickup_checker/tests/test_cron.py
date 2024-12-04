from unittest.mock import patch

import pytest

from taz.core.matching.common.samples import ProductSamples
from taz.crontabs.store_pickup_checker.cache import APICacheController
from taz.crontabs.store_pickup_checker.cron import StorePickupCheckerCrontab


class TestStorePickupCheckerCrontab:

    @pytest.fixture
    def crontab(self):
        return StorePickupCheckerCrontab()

    @pytest.fixture
    def save_raw_products(self, mongo_database):
        products = [
            ProductSamples.magazineluiza_sku_216131400(),
            ProductSamples.madeiramadeira_openapi_sku_302110()
        ]

        for product in products:
            mongo_database.raw_products.save(product)

    @pytest.fixture
    def save_enriched_product_pickup_store(self, mongo_database):
        mongo_database.enriched_products.save({
            'seller_id': 'magazineluiza',
            'sku': '216131400',
            'source': 'api_luiza_pickupstore',
            'stores': [
                {
                    'trading_id': 729,
                    'trading_name': 'AR729',
                    'zipcode': '57300005',
                    'type': 'Convencional',
                    'location': {
                        'latitude': -9.750622,
                        'longitude': -36.659513
                    }
                },
                {
                    'trading_id': 1203,
                    'trading_name': 'CP1203',
                    'zipcode': '57230000',
                    'type': 'Convencional',
                    'location': {
                        'latitude': -10.127432,
                        'longitude': -36.175045
                    }
                },
                {
                    'trading_id': 782,
                    'trading_name': 'AG782',
                    'zipcode': '48005105',
                    'type': 'Convencional',
                    'location': {
                        'latitude': -12.13837,
                        'longitude': -38.423156
                    }
                },
                {
                    'trading_id': 853,
                    'trading_name': 'BR853',
                    'zipcode': '47800358',
                    'type': 'Convencional',
                    'location': {
                        'latitude': -12.145477,
                        'longitude': -44.992059
                    }
                }
            ]
        })

    def test_storepickup_cron_started_to_run(self, crontab, caplog):
        crontab.run()
        assert caplog.records[0].getMessage() == (
            'StorePickupCheckerCrontab crontab started'
        )

    def test_crontab_should_save_enriched_product_store_pickup(
        self,
        crontab,
        logger_stream,
        save_raw_products,
        patch_requests_get,
        mock_valid_product_store_pickup,
        mongo_database
    ):
        with patch_requests_get as mock:
            mock.return_value = mock_valid_product_store_pickup
            crontab.run()

        product_pickup_store = mongo_database.enriched_products.find_one({
            'sku': '216131400',
            'seller_id': 'magazineluiza',
            'source': 'api_luiza_pickupstore'
        })

        del product_pickup_store['_id']
        assert product_pickup_store == {
            'seller_id': 'magazineluiza',
            'sku': '216131400',
            'source': 'api_luiza_pickupstore',
            'has_pickustore': True
        }

    def test_cron_should_delete_enriched_product_store_pickup_when_not_found(
            self,
            crontab,
            save_raw_products,
            patch_requests_get,
            mock_not_found_store_pickup,
            save_enriched_product_pickup_store,
            mongo_database
    ):
        with patch_requests_get as mock:
            mock.return_value = mock_not_found_store_pickup
            crontab.run()

        product_pickup_store = mongo_database.enriched_products.find_one({
            'sku': '216131400',
            'seller_id': 'magazineluiza',
            'source': 'api_luiza_pickupstore'
        })
        assert product_pickup_store is None

    def test_should_run_crontab_returns_not_found(
            self,
            crontab,
            caplog,
            patch_requests_get
    ):
        with patch_requests_get as mock:
            assert crontab.run() is None

        assert mock.call_count == 0
        log = caplog.records[1].getMessage()

        assert log == 'Products not found for seller:magazineluiza'

    @patch.object(APICacheController, 'get_token')
    def test_cron_start_with_api_token(
        self,
        patch_cache_get_token,
        fake_jwt_token
    ):
        patch_cache_get_token.return_value = fake_jwt_token
        cron = StorePickupCheckerCrontab()
        assert cron.client.token == fake_jwt_token
