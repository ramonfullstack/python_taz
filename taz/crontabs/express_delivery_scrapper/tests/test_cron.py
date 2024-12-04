from unittest import mock

import pytest
from simple_settings.utils import settings_stub

from taz import constants
from taz.crontabs.express_delivery_scrapper.cron import (
    ExpressDeliveryScrapperCrontab
)
from taz.helpers.test_utils import mock_response


class TestExpressDeliveryScrapperCrontab:

    @pytest.fixture
    def crontab(self):
        return ExpressDeliveryScrapperCrontab()

    @pytest.fixture
    def product_id(self):
        return '220907400'

    @pytest.fixture
    def seller_id(self):
        return constants.MAGAZINE_LUIZA_SELLER_ID

    @pytest.fixture
    def save_product(self, mongo_database, product_id, seller_id):
        mongo_database.raw_products.save({
            'sku': product_id,
            'seller_id': seller_id,
            'navigation_id': product_id,
            'disable_on_matching': False
        })

    @pytest.fixture
    def save_price(self, mongo_database, product_id, seller_id):
        mongo_database.prices.save({
            'sku': product_id,
            'seller_id': seller_id,
            'price': 1099
        })

    @pytest.fixture
    def save_enriched_products(self, mongo_database, product_id, seller_id):
        mongo_database.enriched_products.save({
            'sku': product_id,
            'seller_id': seller_id,
            'source': 'murcho'
        })

    def test_should_run_crontab_returns_not_found(
        self,
        crontab,
        logger_stream
    ):
        crontab.run()

        log = logger_stream.getvalue()
        assert 'Products not found for seller:magazineluiza\n' in log

    def test_should_run_crontab_returns_price_not_found(
        self,
        crontab,
        logger_stream,
        save_product
    ):
        crontab.run()

        log = logger_stream.getvalue()
        assert 'Price not found for sku:220907400' in log

    @mock.patch('requests.post')
    def test_should_run_crontab_returns_success(
        self,
        mock_get,
        crontab,
        save_product,
        save_price,
        save_enriched_products,
        mongo_database,
        mock_deliveries
    ):
        mock_get.return_value = mock_response(json_data=mock_deliveries)
        crontab.run()

        enriched_product = mongo_database.enriched_products.find_one(
            {'source': constants.SOURCE_API_LUIZA_EXPRESS_DELIVERY},
            {'_id': 0}
        )

        assert enriched_product == {
            'sku': '220907400',
            'seller_id': 'magazineluiza',
            'delivery_days': 1,
            'source': constants.SOURCE_API_LUIZA_EXPRESS_DELIVERY
        }

    @mock.patch('requests.post')
    def test_should_run_crontab_already_document_returns_success(
        self,
        mock_get,
        crontab,
        save_product,
        save_price,
        mongo_database,
        mock_deliveries
    ):
        mongo_database.enriched_products.save({
            'sku': '220907400',
            'seller_id': 'magazineluiza',
            'source': constants.SOURCE_API_LUIZA_EXPRESS_DELIVERY,
            'delivery_days': 2
        })

        mock_get.return_value = mock_response(json_data=mock_deliveries)
        crontab.run()

        enriched_product = mongo_database.enriched_products.find_one(
            {'source': constants.SOURCE_API_LUIZA_EXPRESS_DELIVERY},
            {'_id': 0}
        )

        assert mongo_database.enriched_products.count() == 1

        assert enriched_product == {
            'sku': '220907400',
            'seller_id': 'magazineluiza',
            'delivery_days': 1,
            'source': constants.SOURCE_API_LUIZA_EXPRESS_DELIVERY
        }

    @settings_stub(CRON_STOP='true')
    @settings_stub(CHANNEL_GCHAT='http://urlfake1.com')
    @mock.patch('requests.post')
    def test_should_run_crontab_returns_stopped(
        self,
        mock_post,
        crontab,
        logger_stream
    ):
        crontab.start()

        log = logger_stream.getvalue()

        assert 'CRON_STOP=True, the cron is stopped' in log
        assert mock_post.called
