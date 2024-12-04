import copy
import json
from unittest.mock import call, patch

import pytest

from taz.constants import (
    ENRICHED_PRODUCT_ORIGIN,
    SOURCE_OMNILOGIC,
    SOURCE_WAKKO,
    UPDATE_ACTION
)
from taz.consumers.enriched_product.consumer import (
    SCOPE,
    EnrichedProductProcessor
)
from taz.core.matching.common.enriched_products import EnrichedProductSamples
from taz.utils import md5


class TestEnrichProductConsumer:

    @pytest.fixture
    def enriched_product(self):
        return EnrichedProductProcessor(scope=SCOPE)

    @pytest.fixture
    def message(self, product):
        enriched = EnrichedProductSamples.magazineluiza_sku_0233847()
        enriched.update({
            'sku': product['sku'],
            'navigation_id': product['navigation_id'],
            'md5': '1500f08a6a7f4e486533a7c66129de50'
        })
        return enriched

    @pytest.fixture
    def save_product(self, product, mongo_database):
        mongo_database.raw_products.insert_one(product)

    @pytest.fixture
    def save_enriched_product(self, message, mongo_database):
        mongo_database.enriched_products.insert_one(copy.copy(message))

    @pytest.fixture
    def patch_raw_products(self, enriched_product):
        return patch.object(enriched_product, 'raw_products')

    @pytest.fixture
    def patch_enriched_products(self, enriched_product):
        return patch.object(enriched_product, 'enriched_products')

    def test_when_receiving_enriched_product_event_coming_from_price_consumer(
        self,
        enriched_product,
        save_product,
        message,
        patch_notification,
        caplog,
        mongo_database
    ):
        sku = message['sku']
        seller_id = message['seller_id']
        navigation_id = message['navigation_id']

        message['price'] = 4003.1

        original_message = copy.copy(message)
        original_message['md5'] = md5(message)

        with patch_notification as mock_notification:
            result = enriched_product.process_message(message)

        enriched_product_db = mongo_database.enriched_products.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0}
        )

        assert result
        assert original_message == enriched_product_db

        mock_notification.assert_called_once_with(
            data={
                'sku': sku,
                'seller_id': seller_id,
                'navigation_id': message['navigation_id'],
                'source': SOURCE_OMNILOGIC
            },
            scope='enriched_product',
            action=UPDATE_ACTION,
            origin=ENRICHED_PRODUCT_ORIGIN
        )

        assert (
            'Successfully created enriched product '
            f'sku:{sku} seller_id:{seller_id} navigation_id:{navigation_id} '
            f'source:{SOURCE_OMNILOGIC}'
        ) in caplog.text

    def test_when_receive_enriched_product_event_then_should_process_with_success( # noqa
        self,
        enriched_product,
        save_product,
        message,
        patch_notification,
        caplog,
        mongo_database
    ):
        sku = message['sku']
        seller_id = message['seller_id']
        navigation_id = message['navigation_id']
        original_message = copy.copy(message)

        with patch_notification as mock_notification:
            result = enriched_product.process_message(message)

        enriched_product_db = mongo_database.enriched_products.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0}
        )

        assert result
        assert json.dumps(
            original_message, sort_keys=True
        ) == json.dumps(enriched_product_db, sort_keys=True)

        mock_notification.assert_called_once_with(
            data={
                'sku': sku,
                'seller_id': seller_id,
                'navigation_id': message['navigation_id'],
                'source': SOURCE_OMNILOGIC
            },
            scope='enriched_product',
            action=UPDATE_ACTION,
            origin=ENRICHED_PRODUCT_ORIGIN
        )

        assert (
            'Successfully created enriched product '
            f'sku:{sku} seller_id:{seller_id} navigation_id:{navigation_id} '
            f'source:{SOURCE_OMNILOGIC}'
        ) in caplog.text

    def test_when_receive_event_with_different_data_then_should_process_with_success(  # noqa
        self,
        enriched_product,
        save_product,
        save_enriched_product,
        message,
        patch_notification,
        caplog,
        mongo_database
    ):
        sku = message['sku']
        seller_id = message['seller_id']
        navigation_id = message['navigation_id']
        source = message['source']

        message['entity'] = 'Pijama'
        original_message = copy.copy(message)
        original_message['md5'] = md5(message)

        with patch_notification as mock_notification:
            result = enriched_product.process_message(message)

        enriched_product_db = mongo_database.enriched_products.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0}
        )

        assert result
        assert original_message == enriched_product_db
        mock_notification.assert_called_once()
        assert (
            'Successfully created enriched product '
            f'sku:{sku} seller_id:{seller_id} navigation_id:{navigation_id} '
            f'source:{source}'
        ) in caplog.text

    def test_when_receive_event_with_same_data_then_should_skip_process(
        self,
        enriched_product,
        save_product,
        save_enriched_product,
        message,
        patch_notification,
        caplog
    ):
        sku = message['sku']
        seller_id = message['seller_id']
        navigation_id = message['navigation_id']
        md5 = message['md5']

        with patch_notification as mock_notification:
            result = enriched_product.process_message(message)

        assert result
        mock_notification.assert_not_called()

        assert (
            f'Skip enriched product update for sku:{sku} '
            f'seller_id:{seller_id} navigation_id:{navigation_id} '
            f'source:{SOURCE_OMNILOGIC} income payload:{message} '
            f'database md5:{md5} income md5:{md5}'
        ) in caplog.text

    def test_when_not_found_product_in_raw_product_collection_then_should_skip_process( # noqa
        self,
        enriched_product,
        message,
        patch_notification,
        mongo_database,
        caplog
    ):
        sku = message['sku']
        seller_id = message['seller_id']
        navigation_id = message['navigation_id']

        with patch_notification as mock_notification:
            result = enriched_product.process_message(message)

        assert result
        mock_notification.assert_not_called()
        assert mongo_database.enriched_products.count_documents({}) == 0
        assert (
            f'Product sku:{sku} seller_id:{seller_id} '
            f'navigation_id:{navigation_id} not found '
            'in raw_products'
        ) in caplog.text

    def test_when_find_product_by_sku_and_seller_id_then_not_should_search_by_navigation_id( # noqa
        self,
        enriched_product,
        patch_raw_products,
        product
    ):
        with patch_raw_products as mock_raw_products:
            mock_raw_products.find_one.return_value = product
            result = enriched_product._get_product_data(
                sku=product['sku'],
                seller_id=product['seller_id'],
                navigation_id=product['navigation_id']
            )

            assert result == product
            mock_raw_products.find_one.assert_called_once_with(
                {
                    'sku': product['sku'],
                    'seller_id': product['seller_id']
                },
                {
                    '_id': 0,
                    'sku': 1,
                    'seller_id': 1,
                    'navigation_id': 1,
                    'parent_sku': 1
                }
            )

    def test_when_not_find_product_by_sku_and_seller_id_then_should_search_by_navigation_id( # noqa
        self,
        enriched_product,
        patch_raw_products,
        product
    ):
        with patch_raw_products as mock_raw_products:
            mock_raw_products.find_one.side_effect = [None, product]
            result = enriched_product._get_product_data(
                sku=product['sku'],
                seller_id=product['seller_id'],
                navigation_id=product['navigation_id']
            )

            fields = {
                '_id': 0,
                'sku': 1,
                'seller_id': 1,
                'navigation_id': 1,
                'parent_sku': 1
            }

            expected_calls = [
                call(
                    {'sku': product['sku'], 'seller_id': product['seller_id']},
                    fields
                ),
                call(
                    {'navigation_id': product['navigation_id']},
                    fields
                ),
            ]

            assert result == product
            mock_raw_products.find_one.assert_has_calls(expected_calls)

    def test_when_message_is_omnilogic_source_and_not_has_product_hash_then_should_generate_product_hash( # noqa
        self,
        enriched_product,
        message,
        save_product,
        product,
        patch_notification,
        mongo_database
    ):
        del message['product_hash']

        sku = message['sku']
        seller_id = message['seller_id']

        with patch_notification as mock_notification:
            result = enriched_product.process_message(message)

        message['product_hash'] = md5({
            'seller_id': message['seller_id'],
            'parent_sku': product['parent_sku']
        })

        enriched_product_db = mongo_database.enriched_products.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0}
        )

        assert result
        assert message == enriched_product_db
        mock_notification.assert_called_once()

    @pytest.mark.parametrize('source,product_hash', [
        (SOURCE_WAKKO, None),
        (SOURCE_OMNILOGIC, '123')
    ])
    def test_when_format_product_hash_should_not_generate_a_new_product_hash(
        self,
        enriched_product,
        message,
        product,
        source,
        product_hash
    ):
        message['source'] = source
        message['product_hash'] = product_hash

        enriched_product._format_product_hash(
            message=message,
            sku=product['sku'],
            seller_id=product['seller_id'],
            navigation_id=product['navigation_id'],
            parent_sku=product['parent_sku']
        )

        assert message['product_hash'] == product_hash

    def test_when_update_enriched_products_throw_exception_then_should_save_log_and_return_false( # noqa
        self,
        enriched_product,
        message,
        save_product,
        patch_notification,
        patch_enriched_products,
        caplog
    ):
        sku = message['sku']
        seller_id = message['seller_id']
        navigation_id = message['navigation_id']

        with patch_notification as mock_notification:
            with patch_enriched_products as mock_enriched_products:
                mock_enriched_products.find_one.return_value = None
                mock_enriched_products.update.side_effect = Exception
                result = enriched_product.process_message(message)

        assert not result
        mock_notification.assert_not_called()
        assert (
            f'Could not save enriched product sku:{sku} '
            f'seller_id:{seller_id} navigation_id:{navigation_id} '
            f'source:{SOURCE_OMNILOGIC} error:'
        ) in caplog.text
