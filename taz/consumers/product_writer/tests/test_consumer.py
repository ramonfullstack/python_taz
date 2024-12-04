import datetime
import time
from copy import deepcopy
from unittest import mock
from unittest.mock import Mock, patch

import pytest
from pymongo import MongoClient
from redis import Redis
from simple_settings import settings
from simple_settings.utils import settings_stub
from slugify import slugify

from taz.constants import (
    AUTO_BUYBOX_STRATEGY,
    PRODUCT_WRITER_NO_CORRELATION_FOUND_CODE,
    PRODUCT_WRITER_NO_CORRELATION_FOUND_MESSAGE,
    PRODUCT_WRITER_PRICE_NOT_FOUND_CODE,
    PRODUCT_WRITER_PRICE_NOT_FOUND_MESSAGE,
    PRODUCT_WRITER_PRODUCT_DISABLE_CODE,
    PRODUCT_WRITER_PRODUCT_DISABLE_MESSAGE,
    PRODUCT_WRITER_SUCCESS_CODE,
    PRODUCT_WRITER_SUCCESS_MESSAGE,
    SINGLE_SELLER_STRATEGY
)
from taz.consumers.matching.consumer import MatchingRecordProcessor
from taz.consumers.product_writer.consumer import SCOPE as PRODUCT_WRITER_SCOPE
from taz.consumers.product_writer.consumer import ProductWriterProcessor
from taz.consumers.product_writer.tests.helpers import _save_badges_cache
from taz.core.matching.common.enriched_products import EnrichedProductSamples
from taz.core.matching.common.samples import ProductSamples
from taz.utils import convert_id_to_nine_digits


class TestProductWriterConsumer:

    client = MongoClient(settings.MONGO_URI)

    redis = Redis(
        host=settings.REDIS_LOCK_SETTINGS['host'],
        port=settings.REDIS_LOCK_SETTINGS['port']
    )

    @pytest.fixture
    def cache(self):
        return self.redis

    @pytest.fixture
    def patch_redis_get(self):
        return patch.object(Redis, 'get')

    @pytest.fixture
    def consumer(self):
        return ProductWriterProcessor(scope=PRODUCT_WRITER_SCOPE)

    @pytest.fixture
    def database(self):
        return self.client.taz_tests

    def _store_variation_media(self, database, variation):
        database.medias.insert_many([
            {
                'seller_id': slugify(variation['seller_id']),
                'sku': variation['sku'],
                'videos': [
                    '{}'.format(
                        variation['sku']
                    )
                ]
            },
            {
                'seller_id': slugify(variation['seller_id']),
                'sku': variation['sku'],
                'audios': [
                    '{}.mp3'.format(variation['sku'])
                ]
            },
            {
                'seller_id': slugify(variation['seller_id']),
                'sku': variation['sku'],
                'podcasts': [
                    '{}.mp3'.format(variation['sku'])
                ],
            },
            {
                'seller_id': slugify(variation['seller_id']),
                'sku': variation['sku'],
                'images': [
                    '{}.jpg'.format(variation['sku']),
                    '{}-A.jpg'.format(variation['sku'])
                ]
            }
        ])

    @pytest.fixture
    def matching(self):
        return MatchingRecordProcessor()

    @pytest.fixture
    def create_message(self, database, matching, prices):
        variations_to_store = [
            ProductSamples.variation_without_parent_reference(),
            ProductSamples.variation_a_with_parent(),
            ProductSamples.ml_parent_variation(),
            ProductSamples.ml_variation_a_with_parent(),
            ProductSamples.seller_a_variation_with_parent(),
            ProductSamples.seller_b_variation_with_parent(),
            ProductSamples.seller_c_variation_with_parent(),
        ]
        variation = ProductSamples.unmatched_ml_variation_with_parent()

        for v in variations_to_store:
            database.raw_products.insert_one(v)
            self._store_variation_media(database, v)

        database.raw_products.insert_one(variation)

        matching.process_message({
            'sku': variation['sku'],
            'action': 'create',
            'timestamp': 0.1,
            'seller_id': variation['seller_id']
        })

        self._store_variation_media(database, variation)

        prices.append({
            'sku': variation['sku'],
            'seller_id': variation['seller_id'],
            'list_price': 234.56,
            'price': 123.45,
            'delivery_availability': 'nationwide',
            'stock_count': 82,
            'stock_type': 'on_seller',
            'last_updated_at': datetime.datetime.now()
        })

        for price in prices:
            database.prices.insert_one(price)

        self._save_categories(database)

        return {
            'sku': variation['sku'],
            'action': 'create',
            'seller_id': variation['seller_id']
        }

    def _save_categories(self, database):
        categories = [
            {
                'id': 'EP',
                'description': 'Eletroportáteis',
                'slug': 'eletroportateis',
                'parent_id': 'ML'
            },
            {
                'id': 'ELCO',
                'description': 'Eletroportáteis para Cozinha',
                'slug': 'eletroportateis-para-cozinha',
                'parent_id': 'EP'
            },
            {
                'id': 'LIQU',
                'description': 'Liquidificadores',
                'slug': 'lquidificadores',
                'parent_id': 'EP'
            },
            {
                'id': 'UD',
                'description': 'Utilidades Domesticas',
                'slug': 'utilidades-domesticas',
                'parent_id': 'ML'
            },
            {
                'id': 'PR',
                'description': 'Presentes',
                'slug': 'presentes',
                'parent_id': 'ML'
            },
            {
                'id': 'UDCA',
                'description': 'Canecas',
                'slug': 'canecas',
                'parent_id': 'UD'
            },
            {
                'id': 'UDCG',
                'description': 'Canecas Gigantes',
                'slug': 'canecas-gigantes',
                'parent_id': 'UD'
            },
            {
                'id': 'PRCA',
                'description': 'Canecas',
                'slug': 'canecas',
                'parent_id': 'PR'
            },
            {
                'description': "Recém Chegados",
                'id': 'RC',
                'parent_id': 'ML',
                'slug': 'recem-chegados',
                'url': 'recem-chegados/l/rc/'
            },
            {
                'description': 'No Magalu',
                'id': 'RCNM',
                'parent_id': 'RC',
                'slug': 'no-magalu',
                'url': 'no-magalu/recem-chegados/s/rc/rcnm/'
            }
        ]

        for category in categories:
            database.categories.insert_one(category)

    @pytest.fixture
    def delete_variation(self, database, matching, prices):
        self._save_categories(database)
        variation = ProductSamples.ml_parent_variation()
        database.raw_products.save(variation)
        self._store_variation_media(database, variation)
        matching.process_message({
            'timestamp': 0.1,
            'sku': variation['sku'],
            'action': 'create',
            'seller_id': variation['seller_id']
        })
        database.prices.insert_one({
            'sku': variation['sku'],
            'seller_id': variation['seller_id'],
            'list_price': 234.56,
            'price': 123.45,
            'delivery_availability': 'nationwide',
            'stock_count': 82,
            'stock_type': 'on_seller',
            'last_updated_at': datetime.datetime.now()
        })

        variation = ProductSamples.unmatched_ml_variation_with_parent()
        database.raw_products.save(variation)
        self._store_variation_media(database, variation)
        matching.process_message({
            'timestamp': 0.1,
            'sku': variation['sku'],
            'action': 'create',
            'seller_id': variation['seller_id']
        })
        database.prices.insert_one({
            'sku': variation['sku'],
            'seller_id': variation['seller_id'],
            'list_price': 234.56,
            'price': 123.45,
            'delivery_availability': 'nationwide',
            'stock_count': 82,
            'stock_type': 'on_seller',
            'last_updated_at': datetime.datetime.now()
        })

        variation['disable_on_matching'] = True
        database.raw_products.save(variation)

        message = {
            'sku': variation['sku'],
            'action': 'delete',
            'seller_id': variation['seller_id'],
            'timestamp': 0.1
        }
        matching.process_message(message)

        return message

    @pytest.fixture
    def delete_product(self, database, matching, prices):
        self._save_categories(database)
        variation = ProductSamples.unmatched_ml_variation_with_parent()
        database.raw_products.insert_one(variation)
        self._store_variation_media(database, variation)
        matching.process_message({
            'timestamp': 0.1,
            'sku': variation['sku'],
            'action': 'create',
            'seller_id': variation['seller_id']
        })
        database.prices.insert_one({
            'sku': variation['sku'],
            'seller_id': variation['seller_id'],
            'list_price': 234.56,
            'price': 123.45,
            'delivery_availability': 'nationwide',
            'stock_count': 82,
            'stock_type': 'on_seller',
            'last_updated_at': datetime.datetime.now()
        })

        variation['disable_on_matching'] = True
        database.raw_products.save(variation)

        message = {
            'sku': variation['sku'],
            'action': 'delete',
            'seller_id': variation['seller_id'],
            'timestamp': 0.1,
        }
        matching.process_message(message)

        return message

    @pytest.fixture
    def imageless_product(self, database, create_message):
        product_id = database.id_correlations.find_one({
            'sku': create_message['sku']
        })['product_id']

        database.medias.delete_one({'sku': create_message['sku']})
        database.medias.insert_one({
            'seller_id': create_message['seller_id'],
            'sku': create_message['sku'],
            'images': []
        })

        o = database.unified_objects.find_one({'id': product_id})

        for variation in o['variations']:
            if 'images' in variation.get('media', {}):
                variation['media']['images'] = []

        database.unified_objects.update_one(
            {'id': product_id},
            {'$set': o}
        )

        return create_message

    @pytest.fixture
    def mock_time(self):
        mock_time = Mock()
        mock_time.return_value = 1502734827.997473
        return patch('time.time', mock_time)

    @pytest.fixture
    def mock_sku_213445800_price_payload(self, mock_time):
        return {
            'sku': '213445800',
            'seller_id': 'magazineluiza',
            'delivery_availability': 'nationwide',
            'stock_count': 82,
            'stock_type': 'on_seller',
            'last_updated_at': datetime.datetime(2022, 9, 28, 0, 0, 0, 0)
        }

    @pytest.fixture
    def mock_sku_10621_price_payload(self):
        return {
            'md5': '34a29ac3a49a1b8c546ceaf995e4795f',
            'last_updated_at': '2015-12-22T17:21:25.866255',
            'stock_count': 0,
            'delivery_availability': 'nationwide',
            'sku': '10621',
            'seller_id': 'livrariascuritiba',
            'list_price': 165,
            'stock_type': 'on_seller',
            'price': 165
        }

    @pytest.mark.parametrize('enabled_fulfillment,enabled_parent_matching', [
        (True, False),
        (False, True),
        (False, False),
        (True, True),
    ])
    def test_build_payload(
        self,
        consumer,
        create_message,
        mock_time,
        priceless_product,
        expected_priced_product,
        enabled_fulfillment,
        save_stocks,
        enabled_parent_matching
    ):
        for variation in expected_priced_product['variations']:
            for seller in variation['sellers']:
                if not enabled_fulfillment:
                    fulfillment = seller.get('fulfillment')
                    if fulfillment is not None:
                        del seller['fulfillment']
                if not enabled_parent_matching:
                    if 'parent_matching_uuid' in seller:
                        del seller['parent_matching_uuid']

        with mock_time:
            with settings_stub(
                ENABLE_FULFILLMENT=enabled_fulfillment,
                ENABLE_PARENT_MATCHING=enabled_parent_matching,
            ):
                product_with_price = consumer._build_payload(
                    priceless_product
                )

                expected_priced_product['variations'] = sorted(
                    expected_priced_product['variations'],
                    key=lambda v: int(v['is_delivery_available']),
                    reverse=True
                )

                assert '_id' not in product_with_price
                assert product_with_price == expected_priced_product

    @settings_stub(ENABLE_FULFILLMENT=True)
    @settings_stub(ENABLE_PARENT_MATCHING=True)
    def test_build_payload_minimum_order_quantity(
        self,
        consumer,
        create_message,
        mock_time,
        priceless_product,
        expected_priced_product,
        save_stocks
    ):
        with mock_time:
            product_with_price = consumer._build_payload(
                priceless_product
            )

            expected_priced_product['variations'] = sorted(
                expected_priced_product['variations'],
                key=lambda v: int(v['is_delivery_available']),
                reverse=True
            )
            assert product_with_price == expected_priced_product

    @pytest.fixture
    def mock_message_categories(self):
        return {
            'id': '723829300',
            'sellers': [
                {
                    'description': 'Magazine Luiza',
                    'id': 'magazineluiza',
                    'sku': '723829300',
                    'delivery_availability': 'nationwide',
                    'list_price': 234.56,
                    'price': 123.45,
                    'currency': 'BRL',
                    'stock_count': 21,
                    'stock_type': 'on_seller',
                    'sold_count': 31,
                    'sells_to_company': False,
                    'score': 1,
                    'store_pickup_available': False,
                    'delivery_plus_1': False,
                    'delivery_plus_2': False,
                    'status': 'published',
                    'order': 0
                }
            ],
            'created_at': '2016-08-17T06:17:03.503000',
            'updated_at': '2016-08-17T06:17:03.503000',
            'url': 'caneca-xablau-branca-250ml-cxb250ml/p/7238293/ud/udca/',
            'categories': [
                {
                    'id': 'UD',
                    'subcategories': [
                        {
                            'id': 'UDCA'
                        }
                    ]
                }
            ],
            'is_delivery_available': True,
            'media': {}
        }

    def test_extract_skus(
        self,
        consumer,
        priceless_product,
        expected_extracted_skus
    ):
        skus = consumer._extract_skus(priceless_product)

        assert all(
            expected_sku in skus
            for expected_sku in expected_extracted_skus
        )

    def test_process_message_create_item_matching_buybox(
        self,
        consumer,
        prices,
        database,
        matching,
        expected_product_matched_builded
    ):
        variations = [
            ProductSamples.ml_similar_product_a(),
            ProductSamples.ml_similar_product_b(),
            ProductSamples.seller_similar_product_a()
        ]

        for variation in variations:
            variations_to_store = variations.copy()
            variations_to_store.remove(variation)

            for v in variations_to_store:
                database.raw_products.save(v)
                self._store_variation_media(database, v)

            database.raw_products.save(variation)

            product = matching.process_message({
                'sku': variation['sku'],
                'action': 'create',
                'timestamp': 0.1,
                'seller_id': variation['seller_id']
            })

            self._store_variation_media(database, variation)

            prices.append({
                'sku': variation['sku'],
                'seller_id': variation['seller_id'],
                'list_price': 234.56,
                'price': 123.45,
                'delivery_availability': 'nationwide',
                'stock_count': 82,
                'stock_type': 'on_seller',
                'last_updated_at': datetime.datetime.now()
            })

            for price in prices:
                database.prices.save(price)

            self._save_categories(database)

            product_matched_builded = consumer._build_payload(dict(product))

            product_matched_builded['variations'] = sorted(
                expected_product_matched_builded['variations'],
                key=lambda v: int(v['is_delivery_available']),
                reverse=True
            )
            product_matched_builded['canonical_ids'].sort()

            assert '_id' not in product_matched_builded
            itens_to_compare = [
                'attributes', 'brand', 'canonical_ids',
                'categories', 'id', 'title', 'variations'
            ]
            for assert_key in itens_to_compare:
                assert product_matched_builded[assert_key] == (
                    expected_product_matched_builded[assert_key]
                )

    @settings_stub(
        PUBLISH_STREAM=False
    )
    def test_process_message_create_item_with_acme_notify(
        self,
        consumer,
        create_message,
        patch_kinesis_put,
        patch_publish_manager,
        patch_patolino_product_post
    ):
        mock_response = mock.Mock()
        mock_response.status_code = 201

        with patch_publish_manager, patch_kinesis_put:
            with patch_patolino_product_post as patolino_mock:
                with mock.patch('requests.post') as mock_requests:
                    mock_requests.return_value = mock_response
                    status = consumer.process_message(create_message)

        assert status is True
        assert patolino_mock.called
        assert 'url' in patolino_mock.call_args[0][0]['payload']
        assert mock_requests.called
        assert mock_requests.call_count == 1

    def test_create_item_without_unified_object_postpone_its_creation(
        self,
        database,
        consumer,
        create_message,
        patch_kinesis_put,
        patch_publish_manager
    ):
        criteria = {
            'sku': create_message['sku'],
            'seller_id': create_message['seller_id'],
        }
        correlation = database.id_correlations.find_one(criteria)
        database.unified_objects.delete_one({'id': correlation['product_id']})
        database.id_correlations.update_one(criteria, {
            '$set': {'product_id': None, 'old_product_ids': []}
        })

        with patch_kinesis_put as mock_kinesis:
            with patch_publish_manager as mock_pubsub:
                status = consumer.process_message(create_message)

        assert status is False
        assert not mock_kinesis.called
        assert not mock_pubsub.called

    def test_create_item_with_old_product_ids_in_unified_object(
        self,
        database,
        consumer,
        create_message,
        patch_publish_manager,
        patch_kinesis_put,
        patch_patolino_product_post
    ):
        criteria = {
            'sku': create_message['sku'],
            'seller_id': create_message['seller_id'],
        }

        correlation = database.id_correlations.find_one(criteria)
        database.id_correlations.update_one(criteria, {
            '$set': {
                'old_product_ids': [correlation['product_id']],
                'variation_id': convert_id_to_nine_digits(
                    correlation['product_id']
                )
            }
        })

        with patch_patolino_product_post as patolino_mock:
            with patch_publish_manager as mock_pubsub:
                with patch_kinesis_put as mock_kinesis:
                    status = consumer.process_message(create_message)

        assert status is True
        assert patolino_mock.called
        assert 'url' in patolino_mock.call_args[0][0]['payload']
        assert mock_pubsub.called
        assert mock_kinesis.called

    def test_process_message_delete_variation(
        self,
        consumer,
        delete_variation,
        patch_publish_manager,
        patch_kinesis_put,
        patch_patolino_product_post
    ):
        with patch_patolino_product_post as patolino_mock:
            with patch_publish_manager as mock_pubsub:
                with patch_kinesis_put:
                    status = consumer.process_message(delete_variation)

        assert status is True
        assert patolino_mock.called
        assert mock_pubsub.called

    @settings_stub(PUBLISH_STREAM=False)
    def test_process_message_delete_variation_with_acme_notify(
        self,
        consumer,
        delete_variation,
        database
    ):
        mock_response = mock.Mock()
        mock_response.status_code = 204

        database.raw_products.remove

        products = database.raw_products.find()
        for product in products:
            product['disable_on_matching'] = True
            database.raw_products.save(product)

        with mock.patch('requests.delete') as mock_requests:
            mock_requests.return_value = mock_response
            status = consumer.process_message(delete_variation)

        assert status is True
        assert mock_requests.called

    def test_process_message_delete_variation_with_disable_on_matching(
        self,
        consumer,
        delete_variation,
        patch_publish_manager,
        patch_kinesis_put,
        patch_patolino_product_post
    ):
        delete_variation['disable_on_matching'] = True

        with patch_patolino_product_post as patolino_mock:
            with patch_publish_manager as mock_pubsub:
                with patch_kinesis_put:
                    status = consumer.process_message(delete_variation)

        assert status is True
        assert patolino_mock.called
        assert mock_pubsub.called

    @settings_stub(PUBLISH_STREAM=False)
    def test_process_message_delete_variation_with_disable_on_matching_with_acme_notify(  # noqa
        self,
        consumer,
        delete_variation,
        database
    ):
        mock_response = mock.Mock()
        mock_response.status_code = 204

        database.raw_products.remove

        products = database.raw_products.find()
        for product in products:
            product['disable_on_matching'] = True
            database.raw_products.save(product)

        with mock.patch('requests.delete') as mock_requests:
            mock_requests.return_value = mock_response
            status = consumer.process_message(delete_variation)

        assert status is True
        assert mock_requests.called

    def test_process_message_delete_product(
        self,
        consumer,
        delete_product,
        patch_publish_manager,
        patch_kinesis_put
    ):
        with patch_publish_manager as mock_pubsub:
            with patch_kinesis_put:
                status = consumer.process_message(delete_product)

        assert status is True
        assert mock_pubsub.called

    @settings_stub(PUBLISH_STREAM=False)
    def test_process_message_delete_product_with_acme_notify(
        self,
        consumer,
        delete_product
    ):
        mock_response = mock.Mock()
        mock_response.status_code = 204

        with mock.patch('requests.delete') as mock_requests:
            mock_requests.return_value = mock_response
            status = consumer.process_message(delete_product)

        assert status is True
        assert mock_requests.called

    def test_process_message_delete_product_with_none_product_id(
        self,
        database,
        consumer,
        delete_product,
        patch_publish_manager,
        patch_patolino_product_post,
        patch_datetime,
        patch_kinesis_put
    ):
        criteria = {
            'sku': delete_product['sku'],
            'seller_id': delete_product['seller_id'],
        }

        correlation = database.id_correlations.find_one(criteria)
        database.id_correlations.update_one(criteria, {
            '$set': {
                'product_id': None,
                'old_product_ids': [
                    correlation['product_id'],
                    '123456789'
                ]
            }
        })

        datetime_utcnow = datetime.datetime(2022, 1, 24, 0, 0, 0)
        with patch_patolino_product_post as patolino_mock:
            with patch_publish_manager as mock_pubsub:
                with patch_datetime as mock_datetime:
                    with patch_kinesis_put:
                        mock_datetime.utcnow.return_value = datetime_utcnow
                        status = consumer.process_message(delete_product)

        assert patolino_mock.called
        assert patolino_mock.call_args_list[0][0][0] == {
            'sku': '8weuwe88we',
            'seller_id': 'magazineluiza',
            'code': PRODUCT_WRITER_NO_CORRELATION_FOUND_CODE,
            'message': PRODUCT_WRITER_NO_CORRELATION_FOUND_MESSAGE,
            'payload': {'navigation_id': '8weuwe88we'},
            'action': 'update',
            'last_updated_at': '2022-01-24T00:00:00'
        }
        assert patolino_mock.call_args_list[1][0][0] == {
            'sku': '8weuwe88we',
            'seller_id': 'magazineluiza',
            'code': PRODUCT_WRITER_PRODUCT_DISABLE_CODE,
            'message': PRODUCT_WRITER_PRODUCT_DISABLE_MESSAGE,
            'payload': {'navigation_id': '8weuwe88we'},
            'action': 'update',
            'last_updated_at': '2022-01-24T00:00:00'
        }
        assert status is True
        assert mock_pubsub.called

    def test_message_stuck_on_queue_with_none_product_id_and_no_older_ids(
        self,
        database,
        consumer,
        delete_product,
        patch_kinesis_put,
        patch_publish_manager
    ):
        database.id_correlations.update_one({
            'sku': delete_product['sku'],
            'seller_id': delete_product['seller_id'],
        }, {'$set': {'product_id': None, 'old_product_ids': []}})

        with patch_kinesis_put as mock_kinesis:
            with patch_publish_manager as mock_pubsub:
                status = consumer.process_message(delete_product)

        assert status is False
        assert not mock_kinesis.called
        assert not mock_pubsub.called

    def test_product_validation_on_process_message(
        self,
        consumer,
        imageless_product,
        patch_patolino_product_post,
        patch_kinesis_put,
        patch_publish_manager
    ):
        with patch_patolino_product_post, patch_publish_manager:
            with patch_kinesis_put:
                assert consumer.process_message(imageless_product)

    @pytest.mark.parametrize(
        'func,func_filter,func_param,expected_status,expected_to_be_called', [(  # noqa
            client.taz_tests.raw_products.remove,
            {},
            {},
            True,
            True
        ), (
            client.taz_tests.categories.remove,
            {},
            {},
            True,
            False
        ), (
            client.taz_tests.medias.remove,
            {},
            {},
            True,
            True
        ), (
            None,
            {},
            {},
            True,
            True
        ), (
            client.taz_tests.raw_products.update_many,
            {},
            {'$set': {'disable_on_matching': True}},
            True,
            True
        )]
    )
    def test_process_message_missing_step_skips_processing(
        self,
        func,
        consumer,
        func_param,
        func_filter,
        create_message,
        expected_status,
        expected_to_be_called,
        patch_publish_manager,
        patch_kinesis_put
    ):
        if func:
            if not func_param:
                func(func_filter)
            else:
                func(func_filter, func_param)

        with patch_publish_manager as mock_pubsub:
            with patch_kinesis_put:
                status = consumer.process_message(create_message)

        assert mock_pubsub.called == expected_to_be_called
        assert status == expected_status

    def test_find_product_id_returns_without_product(self, consumer):
        product = consumer._find_product_id({
            'product_id': None,
            'old_product_ids': ['01023421'],
            'sku': '123456',
            'seller_id': 'murcho'
        })

        assert not product

    @pytest.mark.parametrize('remove_price_skus', [
        (['819283iqw', '723829300', '623728900'])
    ])
    def test_when_build_payload_with_sku_missing_price_then_return_payload_without_skus_priceless( # noqa
        self,
        consumer,
        create_message,
        priceless_product,
        database,
        remove_price_skus
    ):
        database.prices.delete_many({'$or': [
            {'sku': sku} for sku in remove_price_skus]
        })

        priceless_product_skus = sorted([
            seller['sku']
            for variation in priceless_product['variations']
            for seller in variation['sellers']
            if seller['sku'] not in remove_price_skus
        ])

        product_with_price = consumer._build_payload(
            priceless_product,
        )

        product_with_price_skus = sorted([
            seller['sku']
            for variation in product_with_price['variations']
            for seller in variation['sellers']
        ])

        assert priceless_product_skus == product_with_price_skus

    def test_list_price_merger_then_return_merged_filtered_list(
        self,
        consumer
    ):
        variation_template = {
            '_id': '608abd49a8a7617ef6195984',
            'last_updated_at': '2022-07-05T20:02:19.173864',
            'md5': 'eb81a0f0b1ac8837794156c3f8e7694a',
            'source': 'pricing',
        }
        variations_prices = [
            {
                **variation_template,
                'seller_id': 'magazineluiza',
                'sku': '230277300',
                'list_price': 54.9,
                'price': 36.8,
                'delivery_availability': 'nationwide',
                'stock_type': 'on_seller',
                'stock_count': 1
            },
            {
                **variation_template,
                'seller_id': 'authenticlivros',
                'sku': '1170618',
                'delivery_availability': 'nationwide',
                'stock_type': 'on_seller',
                'stock_count': 1
            },
            {
                **variation_template,
                'list_price': 54.9,
                'price': 49.41,
                'seller_id': 'authenticlivros',
                'sku': '1170618',
            },
            {
                **variation_template,
                'seller_id': 'amolivroscomdelivrosltda',
                'sku': '36f1306ab70c11eb939f4201ac18500e',
                'delivery_availability': 'nationwide',
                'stock_type': 'on_seller',
                'stock_count': 1
            },
        ]
        new_variations_prices = consumer._list_price_merger(
            variations_prices
        )

        assert new_variations_prices == [
            {
                **variation_template,
                'seller_id': 'magazineluiza',
                'sku': '230277300',
                'list_price': 54.9,
                'price': 36.8,
                'delivery_availability': 'nationwide',
                'stock_type': 'on_seller',
                'stock_count': 1
            },
            {
                **variation_template,
                'seller_id': 'authenticlivros',
                'sku': '1170618',
                'list_price': 54.9,
                'price': 49.41,
                'delivery_availability': 'nationwide',
                'stock_type': 'on_seller',
                'stock_count': 1
            },
        ]

    def test_get_one_badges(self, consumer, badge_dict, database, cache):
        database.badges.insert_one(badge_dict)
        _save_badges_cache(cache, badge_dict)

        for product in badge_dict['products']:
            payload = consumer._get_badges(
                product['sku'],
                product['seller_id']
            )

            assert len(payload) == 1
            assert 'products' not in payload[0]

            for badge in payload:
                assert badge['name'] == badge_dict['name']

    def test_get_two_badges(self, consumer, badge_dict, database, cache):
        badge_name = badge_dict['name']
        for i in range(2):
            badge_dict['name'] = '{}_{}'.format(badge_name, i)
            database.badges.insert_one(badge_dict.copy())
            _save_badges_cache(cache, badge_dict)

        for product in badge_dict['products']:
            payload = consumer._get_badges(
                product['sku'],
                product['seller_id']
            )

            assert len(payload) == 2

    def test_get_badges_returns_empty_list(
        self,
        consumer,
        badge_dict,
        database
    ):
        database.badges.insert_one(badge_dict)

        for product in badge_dict['products']:
            payload = consumer._get_badges(
                product['sku'],
                product['seller_id']
            )

            assert len(payload) == 0

    @patch('taz.core.cache.layered_cache.LayeredCache')
    def test_build_payload_with_badges(
        self,
        layered_cache,
        consumer,
        create_message,
        priceless_product,
        expected_priced_product,
        database,
        badge_dict,
        cache,
        patch_redis_get
    ):
        badge_dict['products'] = [{
            'sku': create_message['sku'],
            'seller_id': create_message['seller_id']
        }]
        database.badges.insert_one(badge_dict)
        _save_badges_cache(cache, badge_dict)

        with patch_redis_get as mock_redis:
            mock_redis.return_value = badge_dict['slug'].encode()
            product_with_price = consumer._build_payload(
                priceless_product,
            )

        main_seller = product_with_price['variations'][1]['sellers'][0]
        badges = main_seller['badges'][0]

        assert badges['name'] == badge_dict['name']
        assert badges['image_url'] == badge_dict['image_url']
        assert mock_redis.called

    def test_build_payload_with_inactive_badges(
        self,
        consumer,
        database,
        badge_dict,
        create_message,
        patch_redis_get,
        priceless_product,
        expected_priced_product,
    ):
        badge_dict['products'] = [{
            'sku': create_message['sku'],
            'seller_id': create_message['seller_id']
        }]
        database.badges.insert_one(badge_dict)

        with patch_redis_get as mock_redis:
            mock_redis.return_value = b'murcho'
            product_with_price = consumer._build_payload(
                priceless_product,
            )

        main_seller = product_with_price['variations'][1]['sellers'][0]

        assert 'badges' not in main_seller
        assert mock_redis.called

    def test_process_message_create_item_with_badges(
        self,
        cache,
        database,
        consumer,
        badge_dict,
        create_message,
        patch_redis_get,
        patch_kinesis_put,
        patch_publish_manager,
        patch_patolino_product_post
    ):
        badge_dict['products'] = [{
            'sku': create_message['sku'],
            'seller_id': create_message['seller_id']
        }]
        database.badges.insert_one(badge_dict)
        _save_badges_cache(cache, badge_dict)

        with patch_patolino_product_post as patolino_mock:
            with patch_publish_manager as mock_pubsub:
                with patch_redis_get as mock_redis:
                    with patch_kinesis_put:
                        mock_redis.return_value = badge_dict['slug'].encode()
                        status = consumer.process_message(create_message)

        assert status is True
        assert patolino_mock.called
        assert 'url' in patolino_mock.call_args[0][0]['payload']
        assert mock_redis.called
        assert mock_pubsub.called

    def test_remove_badge_fields(self, consumer, badge_dict):
        payload = consumer._remove_badge_fields(badge_dict)

        assert not payload.get('products')
        assert not payload.get('start_at')
        assert not payload.get('end_at')
        assert not payload.get('_id')

    def test_process_message_for_product_single_sellers(
        self,
        database,
        matching,
        consumer,
        patch_kinesis_put,
        patch_publish_manager,
        patch_patolino_product_post,
        patch_datetime
    ):
        variation = ProductSamples.magazineluiza_sku_216534900()
        variation['matching_strategy'] = SINGLE_SELLER_STRATEGY

        self._store_variation_media(database, variation)
        database.raw_products.insert_one(variation)

        database.prices.insert_one({
            'sku': variation['sku'],
            'seller_id': variation['seller_id'],
            'list_price': 234.56,
            'price': 123.45,
            'delivery_availability': 'nationwide',
            'stock_count': 82,
            'stock_type': 'on_seller',
            'last_updated_at': datetime.datetime.now()
        })

        categories = [
            {
                'id': 'ED',
                'description': 'Eletrodom',
                'slug': 'eletrodom',
                'parent_id': 'ML'
            },
            {
                'id': 'FORN',
                'description': 'Forno',
                'slug': 'forno',
                'parent_id': 'ED'
            }
        ]

        for category in categories:
            database.categories.insert_one(category)

        message = {
            'sku': variation['sku'],
            'action': 'create',
            'timestamp': 0.1,
            'seller_id': variation['seller_id']
        }

        matching.process_message(message)

        criteria = {
            'sku': variation['sku'],
            'seller_id': variation['seller_id']
        }

        database.id_correlations.update(criteria, {
            '$set': {
                'product_id': '1234567',
                'old_product_ids': ['1234567890']
            }
        })

        datetime_utcnow = datetime.datetime(2022, 1, 24, 0, 0, 0)
        with patch_patolino_product_post as patolino_mock:
            with patch_publish_manager as mock_pubsub:
                with patch_datetime as mock_datetime:
                    with patch_kinesis_put:
                        mock_datetime.utcnow.return_value = datetime_utcnow
                        consumer.process_message(message)

        assert patolino_mock.call_args[0][0] == {
            'sku': '216534900',
            'seller_id': 'magazineluiza',
            'code': PRODUCT_WRITER_PRODUCT_DISABLE_CODE,
            'message': PRODUCT_WRITER_PRODUCT_DISABLE_MESSAGE,
            'payload': {'navigation_id': '216534900'},
            'action': 'update',
            'last_updated_at': '2022-01-24T00:00:00'
        }
        assert mock_pubsub.call_count == 1

    def test_cache_should_be_the_same_redis_instance(
            self, consumer
    ):
        redis_instance = consumer.cache()
        redis_instance_from_same_class = consumer.cache()

        other_record_consumer = consumer

        redis_instance_from_other_record_consumer = (
            other_record_consumer.cache()
        )
        assert isinstance(redis_instance, Redis)
        assert redis_instance is redis_instance_from_same_class
        assert redis_instance_from_other_record_consumer is redis_instance

    def test_process_message_notify_delete_product(
        self,
        database,
        matching,
        consumer,
        patch_kinesis_put,
        patch_publish_manager,
        patch_patolino_product_post
    ):
        variations = [
            ProductSamples.magazineluiza_sku_213445800(),
            ProductSamples.magazineluiza_sku_213445900()
        ]

        for variation in variations:
            variation['matching_strategy'] = SINGLE_SELLER_STRATEGY

            self._store_variation_media(database, variation)
            database.raw_products.insert_one(variation)

            database.prices.insert_one({
                'sku': variation['sku'],
                'seller_id': variation['seller_id'],
                'list_price': 234.56,
                'price': 123.45,
                'delivery_availability': 'nationwide',
                'stock_count': 82,
                'stock_type': 'on_seller',
                'last_updated_at': datetime.datetime.now()
            })

            categories = [
                {
                    'id': 'ED',
                    'description': 'Eletrodom',
                    'slug': 'eletrodom',
                    'parent_id': 'ML'
                },
                {
                    'id': 'LAVA',
                    'description': 'Lava',
                    'slug': 'forno',
                    'parent_id': 'ED'
                }
            ]

            for category in categories:
                database.categories.insert_one(category)

        message = {
            'sku': variation['sku'],
            'action': 'create',
            'timestamp': 0.1,
            'seller_id': variation['seller_id']
        }

        matching.process_message(message)

        variation['disable_on_matching'] = True
        database.raw_products.save(variation)
        with patch_patolino_product_post as patolino_mock:
            with patch_publish_manager as mock_pubsub:
                with patch_kinesis_put:
                    consumer.process_message(message)

        assert patolino_mock.called
        assert mock_pubsub.called

    def test_when_verify_all_skus_have_prices_for_all_variations_without_price_then_return_false( # noqa
        self,
        consumer,
        caplog,
        mock_sku_213445800_price_payload
    ):
        skus_info = [
            (mock_sku_213445800_price_payload['sku'], mock_sku_213445800_price_payload['seller_id']) # noqa
        ]

        response = consumer._verify_all_skus_have_prices(skus_info, [])
        assert not response
        assert 'No SKUs were sent for price verification' in caplog.text

    def test_when_verify_all_skus_have_prices_with_one_or_more_variations_with_price_then_return_true( # noqa
        self,
        consumer,
        caplog,
        mock_sku_213445800_price_payload,
        mock_sku_10621_price_payload
    ):
        skus_info = [
            (mock_sku_213445800_price_payload['sku'], mock_sku_213445800_price_payload['seller_id']), # noqa
            (mock_sku_10621_price_payload['sku'], mock_sku_10621_price_payload['seller_id']) # noqa
        ]

        prices = [mock_sku_213445800_price_payload]
        response = consumer._verify_all_skus_have_prices(skus_info, prices)
        assert response
        assert (
            'Prices are missing for the following skus:{}'.format([
                (mock_sku_10621_price_payload['sku'], mock_sku_10621_price_payload['seller_id']) # noqa
            ])
        ) in caplog.text

    def test_process_message_returns_prices_ordered(
        self,
        database,
        matching,
        consumer,
        patch_kinesis_put,
        patch_publish_manager,
        patch_patolino_product_post
    ):
        product_1 = ProductSamples.magazineluiza_sku_088878800()
        product_1['list_price'] = 359.9
        product_1['price'] = 359.9

        product_2 = ProductSamples.whirlpool_sku_27()
        product_2['list_price'] = 289.9
        product_2['price'] = 289.9

        variations = [product_1, product_2]

        for variation in variations:
            variation['matching_strategy'] = AUTO_BUYBOX_STRATEGY

            self._store_variation_media(database, variation)
            database.raw_products.insert_one(variation)

            database.prices.insert_one({
                'sku': variation['sku'],
                'seller_id': variation['seller_id'],
                'list_price': variation['list_price'],
                'price': variation['price'],
                'delivery_availability': 'nationwide',
                'stock_count': 82,
                'stock_type': 'on_seller',
                'last_updated_at': datetime.datetime.now()
            })

            categories = [
                {
                    'id': 'ED',
                    'description': 'Eletrodom',
                    'slug': 'eletrodom',
                    'parent_id': 'ML'
                },
                {
                    'id': 'LAVA',
                    'description': 'Lava',
                    'slug': 'forno',
                    'parent_id': 'ED'
                },
                {
                    'id': 'OTED',
                    'description': 'Oted',
                    'slug': 'forno',
                    'parent_id': 'ED'
                },
                {
                    'id': 'COFA',
                    'description': 'Cofa',
                    'slug': 'forno',
                    'parent_id': 'ED'
                }
            ]

            for category in categories:
                database.categories.insert_one(category)

        variation = ProductSamples.magazineluiza_sku_088878800()
        message = {
            'sku': variation['sku'],
            'action': 'create',
            'timestamp': 0.1,
            'seller_id': variation['seller_id']
        }

        matching.process_message(message)

        with patch_patolino_product_post:
            with patch_publish_manager as mock_pubsub:
                with patch_kinesis_put:
                    consumer.process_message(message)

        payload = mock_pubsub.call_args_list[0][1]['content']['data']
        main_seller = payload['variations'][0]['sellers'][0]

        assert main_seller['id'] == 'whirlpool'

    def test_process_message_returns_sort_price_with_winning_cheapest_price(
        self,
        database,
        matching,
        consumer,
        patch_kinesis_put,
        patch_publish_manager,
        patch_patolino_product_post
    ):
        variations = [
            ProductSamples.whirlpool_sku_27(),
            ProductSamples.magazineluiza_sku_088878800()
        ]

        for variation in variations:
            variation['matching_strategy'] = AUTO_BUYBOX_STRATEGY

            self._store_variation_media(database, variation)
            database.raw_products.insert_one(variation)

            database.prices.insert_one({
                'sku': variation['sku'],
                'seller_id': variation['seller_id'],
                'list_price': 359.9,
                'price': 359.9,
                'delivery_availability': 'nationwide',
                'stock_count': 82,
                'stock_type': 'on_seller',
                'last_updated_at': datetime.datetime.now()
            })

            categories = [
                {
                    'id': 'ED',
                    'description': 'Eletrodom',
                    'slug': 'eletrodom',
                    'parent_id': 'ML'
                },
                {
                    'id': 'LAVA',
                    'description': 'Lava',
                    'slug': 'forno',
                    'parent_id': 'ED'
                },
                {
                    'id': 'OTED',
                    'description': 'Oted',
                    'slug': 'forno',
                    'parent_id': 'ED'
                },
                {
                    'id': 'COFA',
                    'description': 'Cofa',
                    'slug': 'forno',
                    'parent_id': 'ED'
                }
            ]

            for category in categories:
                database.categories.insert_one(category)

        variation = ProductSamples.magazineluiza_sku_088878800()
        message = {
            'sku': variation['sku'],
            'action': 'create',
            'timestamp': 0.1,
            'seller_id': variation['seller_id']
        }

        matching.process_message(message)

        with patch_patolino_product_post:
            with patch_publish_manager as mock_pubsub:
                with patch_kinesis_put:
                    consumer.process_message(message)

        payload = mock_pubsub.call_args_list[0][1]['content']['data']
        main_seller = payload['variations'][0]['sellers'][0]

        assert main_seller['id'] == 'whirlpool'

    def test_process_message_product_buybox_returns_sort_price_with_winning_ml(
        self,
        database,
        matching,
        consumer,
        patch_kinesis_put,
        patch_publish_manager,
        patch_patolino_product_post
    ):
        variations = [
            ProductSamples.whirlpool_sku_1225(),
            ProductSamples.whirlpool_sku_1224(),
            ProductSamples.magazineluiza_sku_010554000(),
            ProductSamples.whirlpool_sku_1226(),
            ProductSamples.magazineluiza_sku_010554100(),
            ProductSamples.whirlpool_sku_1227()
        ]

        for variation in variations:
            variation['matching_strategy'] = AUTO_BUYBOX_STRATEGY

            self._store_variation_media(database, variation)
            database.raw_products.insert_one(variation)

            database.prices.insert_one({
                'sku': variation['sku'],
                'seller_id': variation['seller_id'],
                'list_price': 2169.0,
                'price': 1879.0,
                'delivery_availability': 'nationwide',
                'stock_count': 50,
                'stock_type': 'on_seller',
                'last_updated_at': datetime.datetime.now()
            })

            categories = [
                {
                    'id': 'ED',
                    'description': 'Eletrodom',
                    'slug': 'eletrodom',
                    'parent_id': 'ML'
                },
                {
                    'id': 'LAVA',
                    'description': 'Lava',
                    'slug': 'forno',
                    'parent_id': 'ED'
                }
            ]

            for category in categories:
                database.categories.insert_one(category)

        message = {
            'sku': variation['sku'],
            'action': 'create',
            'timestamp': 0.1,
            'seller_id': variation['seller_id']
        }

        matching.process_message(message)

        with patch_patolino_product_post:
            with patch_publish_manager as mock_pubsub:
                consumer.process_message(message)

        payload = mock_pubsub.call_args_list[0][1]['content']['data']
        main_seller = payload['variations'][0]['sellers'][0]

        assert main_seller['id'] == 'magazineluiza'

    def test_process_message_create_item_with_short_title_and_description(
        self,
        database,
        matching,
        consumer,
        patch_kinesis_put,
        patch_publish_manager,
        custom_attributes_dict,
        patch_patolino_product_post
    ):
        product_1 = ProductSamples.magazineluiza_sku_088878800()
        product_1['list_price'] = 359.9
        product_1['price'] = 359.9

        product_2 = ProductSamples.whirlpool_sku_27()
        product_2['list_price'] = 289.9
        product_2['price'] = 289.9

        variations = [product_1, product_2]

        for variation in variations:
            variation['matching_strategy'] = AUTO_BUYBOX_STRATEGY

            self._store_variation_media(database, variation)
            database.raw_products.save(variation)

            database.prices.insert_one({
                'sku': variation['sku'],
                'seller_id': variation['seller_id'],
                'list_price': variation['list_price'],
                'price': variation['price'],
                'delivery_availability': 'nationwide',
                'stock_count': 82,
                'stock_type': 'on_seller',
                'last_updated_at': datetime.datetime.now()
            })

            categories = [
                {
                    'id': 'ED',
                    'description': 'Eletrodom',
                    'slug': 'eletrodom',
                    'parent_id': 'ML'
                },
                {
                    'id': 'LAVA',
                    'description': 'Lava',
                    'slug': 'forno',
                    'parent_id': 'ED'
                },
                {
                    'id': 'OTED',
                    'description': 'Oted',
                    'slug': 'forno',
                    'parent_id': 'ED'
                },
                {
                    'id': 'COFA',
                    'description': 'Forno',
                    'slug': 'forno',
                    'parent_id': 'ED'
                }
            ]

            for category in categories:
                database.categories.insert_one(category)

        variation = ProductSamples.magazineluiza_sku_088878800()
        message = {
            'sku': variation['sku'],
            'action': 'create',
            'timestamp': 0.1,
            'seller_id': variation['seller_id']
        }

        matching.process_message(message)

        with patch_publish_manager as mock_pubsub:
            with patch_kinesis_put:
                consumer.process_message(message)

        payload = mock_pubsub.call_args_list[0][1]['content']['data']
        main_seller = payload['variations'][0]['sellers'][0]

        assert main_seller['id'] == 'whirlpool'

        custom_attributes_dict['sku'] = variation['sku']
        custom_attributes_dict['seller_id'] = variation['seller_id']

        database.custom_attributes.insert_one(custom_attributes_dict)

        with patch_patolino_product_post as patolino_mock:
            with patch_publish_manager as mock_pubsub:
                with patch_kinesis_put:
                    status = consumer.process_message(message)

        assert status is True
        assert patolino_mock.called
        assert 'url' in patolino_mock.call_args[0][0]['payload']

        assert mock_pubsub.called

        variation = mock_pubsub.call_args_list[0][1]['content']['data']['variations'][0]  # noqa
        assert variation['short_title'] == 'A short title'
        assert variation['short_description'] == 'A brief description'

    def test_process_message_create_with_invalid_category_send_rc_rcnm(
        self,
        database,
        consumer,
        patch_kinesis_put,
        patch_publish_manager,
        custom_attributes_dict,
        matching,
        patch_patolino_product_post
    ):
        product_1 = ProductSamples.magazineluiza_sku_088878800()
        product_1['list_price'] = 359.9
        product_1['price'] = 359.9

        product_2 = ProductSamples.whirlpool_sku_27()
        product_2['list_price'] = 289.9
        product_2['price'] = 289.9

        variations = [product_1, product_2]

        for variation in variations:
            variation['matching_strategy'] = AUTO_BUYBOX_STRATEGY

            self._store_variation_media(database, variation)
            database.raw_products.insert_one(variation)

            database.prices.insert_one({
                'sku': variation['sku'],
                'seller_id': variation['seller_id'],
                'list_price': variation['list_price'],
                'price': variation['price'],
                'delivery_availability': 'nationwide',
                'stock_count': 82,
                'stock_type': 'on_seller',
                'last_updated_at': datetime.datetime.now()
            })

            categories = [
                {
                    'description': "Recém Chegados",
                    'id': 'RC',
                    'parent_id': 'ML',
                    'slug': 'recem-chegados',
                    'url': 'recem-chegados/l/rc/'
                },
                {
                    'description': 'No Magalu',
                    'id': 'RCNM',
                    'parent_id': 'RC',
                    'slug': 'no-magalu',
                    'url': 'no-magalu/recem-chegados/s/rc/rcnm/'
                }
            ]

            for category in categories:
                database.categories.insert_one(category)

        variation = ProductSamples.magazineluiza_sku_088878800()
        message = {
            'sku': variation['sku'],
            'action': 'create',
            'timestamp': 0.1,
            'seller_id': variation['seller_id']
        }

        matching.process_message(message)

        with patch_patolino_product_post as patolino_mock:
            with patch_publish_manager as mock_pubsub:
                with patch_kinesis_put:
                    consumer.process_message(message)

        assert patolino_mock.called
        assert 'url' in patolino_mock.call_args[0][0]['payload']
        assert mock_pubsub.called
        assert mock_pubsub.call_args_list[0][1]['content']['data']['categories'] == [  # noqa
            {
                'id': 'RC',
                'name': 'Recém Chegados',
                'composite_name': 'RC|Recém Chegados',
                'url': 'recem-chegados/l/rc/',
                'subcategories': [
                    {
                        'id': 'RCNM',
                        'name': 'No Magalu',
                        'composite_name': 'RCNM|No Magalu',
                        'url': 'no-magalu/l/rcnm/'
                    }
                ]
            }
        ]

    def test_process_message_create_with_invalid_category_and_invalid_default(
        self,
        database,
        consumer,
        patch_kinesis_put,
        patch_publish_manager,
        custom_attributes_dict,
        matching
    ):
        product_1 = ProductSamples.magazineluiza_sku_088878800()
        product_1['list_price'] = 359.9
        product_1['price'] = 359.9

        product_2 = ProductSamples.whirlpool_sku_27()
        product_2['list_price'] = 289.9
        product_2['price'] = 289.9

        variations = [product_1, product_2]

        for variation in variations:
            variation['matching_strategy'] = AUTO_BUYBOX_STRATEGY

            self._store_variation_media(database, variation)
            database.raw_products.insert_one(variation)

            database.prices.insert_one({
                'sku': variation['sku'],
                'seller_id': variation['seller_id'],
                'list_price': variation['list_price'],
                'price': variation['price'],
                'delivery_availability': 'nationwide',
                'stock_count': 82,
                'stock_type': 'on_seller',
                'last_updated_at': datetime.datetime.now()
            })

        variation = ProductSamples.magazineluiza_sku_088878800()
        message = {
            'sku': variation['sku'],
            'action': 'create',
            'timestamp': 0.1,
            'seller_id': variation['seller_id']
        }

        matching.process_message(message)

        with patch_kinesis_put as mock_kinesis:
            with patch_publish_manager as mock_pubsub:
                consumer.process_message(message)

        assert not mock_kinesis.called
        assert not mock_pubsub.called
    def test_process_message_should_not_delete_product_out_of_stock_recent_updated(  # noqa
        self,
        consumer,
        database,
        prices,
        patch_kinesis_put,
        patch_publish_manager,
        patch_patolino_product_post
    ):

        product = ProductSamples.variation_a()
        product['sku'] = '10621'
        product['seller_id'] = 'livrariascuritiba'

        database.raw_products.insert_one(product)

        price = {
            'md5': '34a29ac3a49a1b8c546ceaf995e4795f',
            'last_updated_at': datetime.datetime.now().isoformat(),
            'stock_count': 0,
            'delivery_availability': 'nationwide',
            'sku': '10621',
            'seller_id': 'livrariascuritiba',
            'list_price': 165,
            'stock_type': 'on_seller',
            'price': 165
        }

        database.prices.insert_one(price)

        message = {
            'sku': price['sku'],
            'action': 'delete',
            'timestamp': 0.1,
            'seller_id': price['seller_id']
        }

        with patch_kinesis_put as mock_kinesis:
            with patch_publish_manager as mock_pubsub:
                consumer.process_message(message)

        assert not mock_kinesis.called
        assert not mock_pubsub.called

    def test_process_message_should_delete_product_not_price(
        self,
        consumer,
        database,
        patch_publish_manager
    ):
        product = ProductSamples.variation_a()
        database.raw_products.insert_one(product)

        message = {
            'sku': product['sku'],
            'action': 'delete',
            'timestamp': 0.1,
            'seller_id': product['seller_id']
        }

        with patch_publish_manager as mock_pubsub:
            consumer.process_message(message)

        assert mock_pubsub.call_args_list[0][1]['content']['action'] == 'delete'  # noqa
        assert mock_pubsub.called

    def test_process_message_without_variations_bring_no_prices(
        self,
        database,
        matching,
        consumer,
        patch_publish_manager,
        patch_patolino_product_post,
        patch_datetime
    ):
        categories = [{
            'id': 'LI',
            'description': 'Livros',
            'slug': 'livros',
            'parent_id': 'ML'
        }, {
            'id': 'HQLV',
            'description': 'HQ',
            'slug': 'hq',
            'parent_id': 'li'
        }]

        for category in categories:
            database.categories.insert_one(category)

        enriched_products = [
            EnrichedProductSamples._1000store_sku_55316(),
            EnrichedProductSamples._1000store_sku_55313()
        ]

        for enriched_product in enriched_products:
            database.enriched_products.insert_one(enriched_product)

        variations = [
            ProductSamples._1000store_sku_55316(),
            ProductSamples._1000store_sku_55313()
        ]

        for variation in variations:
            database.raw_products.insert_one(variation)

            message = {
                'sku': variation['sku'],
                'action': 'create',
                'timestamp': 0.1,
                'seller_id': variation['seller_id']
            }

            matching.process_message(message)

            for unified_object in list(database.unified_objects.find()):
                unified_object['variations'] = []
                database.unified_objects.save(unified_object)

            datetime_utcnow = datetime.datetime(2022, 1, 24, 0, 0, 0)
            with patch_patolino_product_post as patolino_mock:
                with patch_publish_manager as mock_pubsub:
                    with patch_datetime as mock_datetime:
                        mock_datetime.utcnow.return_value = datetime_utcnow
                        consumer.process_message(message)

        assert patolino_mock.called
        assert patolino_mock.call_args[0][0] == {
            'sku': '55313',
            'seller_id': '1000store',
            'code': PRODUCT_WRITER_PRICE_NOT_FOUND_CODE,
            'message': PRODUCT_WRITER_PRICE_NOT_FOUND_MESSAGE,
            'payload': {'navigation_id': 'bkc899e61c'},
            'action': 'update',
            'last_updated_at': '2022-01-24T00:00:00'
        }

        assert mock_pubsub.call_count == 1
        assert mock_pubsub.call_args_list[0][1]['content']['action'] == 'delete'  # noqa

    def test_process_message_create_kinesis_put_should_successfully_publish(
        self,
        consumer,
        create_message,
        patch_kinesis_put,
        patch_publish_manager,
        patch_patolino_product_post,
        caplog
    ):
        with patch_patolino_product_post, patch_publish_manager:
            with patch_kinesis_put:
                successfully_published = consumer.process_message(
                    create_message
                )

        assert successfully_published

    def test_process_message_create_pubsub_publish_should_thow_error(
        self,
        consumer,
        create_message,
        patch_kinesis_put,
        patch_publish_manager,
        patch_patolino_product_post,
        caplog
    ):
        with patch_patolino_product_post, patch_kinesis_put:
            with patch_publish_manager as mock_pubsub:
                mock_pubsub.side_effect = Exception
                successfully_published = consumer.process_message(
                    create_message
                )

        assert not successfully_published
        assert 'Failed to sent product' in caplog.text

    def test_process_message_should_send_tracking_id(
        self,
        consumer,
        create_message,
        patch_kinesis_put,
        patch_publish_manager,
        patch_patolino_product_post
    ):
        create_message['tracking_id'] = '123456'

        with patch_patolino_product_post as patolino_mock:
            with patch_kinesis_put, patch_publish_manager:
                consumer.process_message(create_message)

        assert patolino_mock.call_args[0][0]['tracking_id']

    def test_build_categories_should_use_cache_to_return_categories(
        self,
        consumer,
        mock_message_categories,
        database
    ):
        self._save_categories(database)
        consumer._build_categories(mock_message_categories)
        database.categories.delete_one({'id': 'UD'})

        result = consumer._build_categories(mock_message_categories)
        assert result[0]['id'] == mock_message_categories['categories'][0]['id'] # noqa

    def test_build_categories_with_expires_cache_should_return_update_categories( # noqa
        self,
        consumer,
        mock_message_categories,
        database
    ):
        self._save_categories(database)
        result = consumer._build_categories(mock_message_categories)
        assert result[0]['id'] == mock_message_categories['categories'][0]['id'] # noqa

        time.sleep(2)
        database.categories.delete_one({'id': 'UD'})

        result = consumer._build_categories(mock_message_categories)
        assert result[0]['id'] == settings.FALLBACK_MISSING_CATEGORY

    @pytest.mark.parametrize('fallback_missing_category', [
        'EP',
        settings.FALLBACK_MISSING_CATEGORY
    ])

    def test_not_found_category_then_return_default_category(  # noqa
        self,
        consumer,
        mock_message_categories,
        database,
        fallback_missing_category
    ):
        self._save_categories(database)
        mock_message_categories['categories'][0]['id'] = 'AA'
        del mock_message_categories['categories'][0]['subcategories']

        result = consumer._build_categories(mock_message_categories)
        assert result[0]['id'] == 'RC'

        with settings_stub(
                FALLBACK_MISSING_CATEGORY=fallback_missing_category
        ):
            result = consumer._build_categories(mock_message_categories)
            assert result[0]['id'] == fallback_missing_category

    def test_when_get_price_of_product_with_one_register_then_return_yourself(
        self,
        consumer,
        database,
        mock_sku_213445800_price_payload
    ):
        database.prices.insert_one(mock_sku_213445800_price_payload)

        result = consumer._get_price(
            mock_sku_213445800_price_payload['sku'],
            mock_sku_213445800_price_payload['seller_id']
        )

        result.pop('_id', None)
        mock_sku_213445800_price_payload.pop('_id', None)
        assert result == mock_sku_213445800_price_payload

    def test_when_get_price_of_product_many_registers_then_return_price_and_stock_merged( # noqa
        self,
        consumer,
        database,
        mock_sku_213445800_price_payload
    ):
        mock_sku_213445800_price_payload_priced = deepcopy(
            mock_sku_213445800_price_payload
        )
        mock_sku_213445800_price_payload_with_stock = deepcopy(
            mock_sku_213445800_price_payload
        )
        mock_sku_213445800_price_payload_priced.pop('stock_count', None)
        mock_sku_213445800_price_payload_with_stock.pop('list_price', None)

        database.prices.insert_many([
            mock_sku_213445800_price_payload_priced,
            mock_sku_213445800_price_payload_with_stock
        ])

        result = consumer._get_price(
            mock_sku_213445800_price_payload['sku'],
            mock_sku_213445800_price_payload['seller_id']
        )

        result.pop('_id', None)
        assert result == mock_sku_213445800_price_payload

    def test_when_get_price_then_return_empty(
        self,
        consumer,
        caplog,
        mock_sku_213445800_price_payload
    ):
        assert consumer._get_price(
            mock_sku_213445800_price_payload['sku'],
            mock_sku_213445800_price_payload['seller_id']
        ) == {}
        assert 'Cannot find price' in caplog.text

    def test_when_get_price_with_records_from_different_dates_and_return_record_with_highest_date( # noqa
        self,
        consumer,
        database,
        mock_sku_213445800_price_payload
    ):
        mock_sku_213445800_price_payload_biggest_date = deepcopy(
            mock_sku_213445800_price_payload
        )
        mock_sku_213445800_price_payload_biggest_date['last_updated_at'] = (
            mock_sku_213445800_price_payload['last_updated_at'] + datetime.timedelta(days=1) # noqa
        )
        database.prices.insert_many([
            mock_sku_213445800_price_payload_biggest_date,
            mock_sku_213445800_price_payload
        ])

        result = consumer._get_price(
            mock_sku_213445800_price_payload['sku'],
            mock_sku_213445800_price_payload['seller_id']
        )

        result.pop('_id', None)
        mock_sku_213445800_price_payload_biggest_date.pop('_id', None)
        assert result == mock_sku_213445800_price_payload_biggest_date

    def test_when_product_has_disable_matching_true_then_should_send_patolino_notification_with_action_delete( # noqa
        self,
        consumer,
        create_message,
        patch_kinesis_put,
        patch_publish_manager,
        database,
        patch_notification_sender_send
    ):
        product = ProductSamples.unmatched_ml_variation_with_parent()
        product['disable_on_matching'] = True
        database.raw_products.update_one(
            {
                'sku': product['sku'],
                'seller_id': product['seller_id']
            },
            {
                '$set': product
            }
        )

        with patch_kinesis_put, patch_publish_manager:
            with patch_notification_sender_send as patolino_mock:
                consumer.process_message(create_message)

        payload = {
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'navigation_id': product['navigation_id'],
            'action': 'delete',
            'url': ''
        }

        patolino_mock.assert_called_once_with(
            sku=product['sku'],
            seller_id=product['seller_id'],
            code=PRODUCT_WRITER_SUCCESS_CODE,
            message=PRODUCT_WRITER_SUCCESS_MESSAGE,
            payload=payload,
            tracking_id=None
        )

    def test_skip_inexistent_product_with_action_update(
        self,
        consumer,
        patch_kinesis_put,
    ):
        message = {
            'sku': 'test-sku',
            'action': 'update',
            'seller_id': 'test-seller'
        }
        with patch_kinesis_put as mock_kinesis:
            assert consumer.process_message(
                message
            )
            assert not mock_kinesis.called

    def test_skip_a_disabled_product(
        self,
        consumer,
        database,
        patch_kinesis_put,
    ):
        product = ProductSamples.variation_a()
        product['disable_on_matching'] = True
        database.raw_products.insert_one(product)

        message = {
            'sku': product['sku'],
            'action': 'update',
            'timestamp': 0.1,
            'seller_id': product['seller_id']
        }
        assert consumer.process_message(message)

    def test_product_writer_return_true_without_correlations(
        self,
        consumer,
        create_message,
        database,
        caplog
    ):
        criteria = {
            'sku': create_message['sku'],
            'seller_id': create_message['seller_id'],
        }
        database.id_correlations.delete_many(criteria)
        create_message['type'] = 'other'
        assert consumer.process_message(create_message) is True
        assert 'Pending matching for variation sku:' in caplog.text
