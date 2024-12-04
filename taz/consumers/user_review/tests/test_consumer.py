from unittest.mock import patch

import pytest
from redis import Redis

from taz.constants import (
    META_TYPE_PRODUCT_AVERAGE_RATING,
    META_TYPE_PRODUCT_TOTAL_REVIEW_COUNT
)
from taz.consumers.user_review.consumer import UserReviewRecordProcessor
from taz.core.matching.common.samples import ProductSamples
from taz.utils import md5


class TestUserReviewConsumer:

    @pytest.fixture
    def consumer(self):
        return UserReviewRecordProcessor('user_review')

    @pytest.fixture
    def save_raw_product(self, mongo_database):
        variation = ProductSamples.cookeletroraro_sku_2000160()
        mongo_database.raw_products.save(variation)

    @pytest.fixture
    def patch_redis_get(self):
        return patch.object(Redis, 'get')

    @pytest.fixture
    def message(self):
        return {
            'ExternalId': '857710100',
            'AverageRating': 4.6,
            'TotalReviewCount': 15,
            'seller_id': 'cookeletroraro',
            'sku': '2000160'
        }

    @pytest.fixture
    def invalid_data(self):
        return [
            {
                'product_id': '857710100',
                'type': META_TYPE_PRODUCT_TOTAL_REVIEW_COUNT,
                'value': 1
            },
            {
                'product_id': '857710100',
                'type': META_TYPE_PRODUCT_TOTAL_REVIEW_COUNT,
                'value': 1
            }
        ]

    def test_should_save_and_notify_user_reviews(
        self,
        consumer,
        message,
        mongo_database,
        patch_publish_manager,
        save_raw_product
    ):
        with patch_publish_manager as mock_pubsub:
            response = consumer.process_message(message)

        assert response is True

        review_count = mongo_database.customer_behaviors.find_one(
            {
                'product_id': '857710100',
                'type': META_TYPE_PRODUCT_TOTAL_REVIEW_COUNT
            },
            {
                '_id': 0
            }
        )
        product_avg_rating = mongo_database.customer_behaviors.find_one(
            {
                'product_id': '857710100',
                'type': META_TYPE_PRODUCT_AVERAGE_RATING
            },
            {
                '_id': 0
            }
        )

        assert review_count == {
            'product_id': '857710100',
            'type': 'product_total_review_count',
            'value': 15
        }

        assert product_avg_rating == {
            'product_id': '857710100',
            'type': 'product_average_rating',
            'value': 4.6
        }

        assert mock_pubsub.call_count == 1

        content = mock_pubsub.call_args_list[0][1]['content']
        assert content['sku'] == '2000160'
        assert content['seller_id'] == 'cookeletroraro'
        assert content['navigation_id'] == '857710100'
        assert content['action'] == 'update'
        assert content['type'] == 'reviews'

    def test_should_not_generate_duplicity(
        self,
        consumer,
        message,
        mongo_database,
        patch_publish_manager,
        save_raw_product,
        invalid_data
    ):
        mongo_database.customer_behaviors.insert_many(invalid_data)

        with patch_publish_manager:
            response = consumer.process_message(message)

        assert response is True

        review_count = mongo_database.customer_behaviors.count(
            {
                'product_id': '857710100',
                'type': META_TYPE_PRODUCT_TOTAL_REVIEW_COUNT
            }
        )

        assert review_count == 1

    def test_should_not_delete_other_data(
        self,
        consumer,
        message,
        mongo_database,
        patch_publish_manager,
        save_raw_product
    ):
        mongo_database.customer_behaviors.insert({
            'product_id': '0116017',
            'type': 'other_custom_attribute',
            'value': 10
        })

        with patch_publish_manager:
            response = consumer.process_message(message)

        assert response is True

        review_count = mongo_database.customer_behaviors.count(
            {
                'product_id': '0116017',
                'type': 'other_custom_attribute'
            }
        )

        assert review_count == 1

    @pytest.mark.parametrize('field_name', [
        ('ExternalId'),
        ('AverageRating'),
        ('TotalReviewCount'),
    ])
    def test_should_not_notify_if_invalid_message(
        self,
        field_name,
        consumer,
        message,
        patch_publish_manager
    ):
        with patch_publish_manager as mock_pubsub:
            del message[field_name]

            response = consumer.process_message(message)

        assert response is True
        assert mock_pubsub.call_count == 0

    def test_should_not_notify_if_product_not_in_raw_product(
        self,
        consumer,
        message,
        patch_publish_manager
    ):
        with patch_publish_manager as mock_pubsub:
            response = consumer.process_message(message)

        assert response is True
        assert mock_pubsub.call_count == 0

    def test_should_process_skip_user_reviews(
        self,
        consumer,
        message,
        mongo_database,
        patch_publish_manager,
        save_raw_product,
        patch_redis_get
    ):
        with patch_redis_get as mock_redis_get:
            review_payload = {
                'seller_id': message.get('seller_id'),
                'sku': message.get('sku'),
                'avg_rating': message.get('AverageRating'),
                'review_count': message.get('TotalReviewCount'),
            }
            mock_redis_get.return_value = md5(review_payload).encode()

            with patch_publish_manager as mock_pubsub:
                response = consumer.process_message(message)

        assert response is True

        review_count = mongo_database.customer_behaviors.find_one(
            {
                'product_id': '857710100',
                'type': META_TYPE_PRODUCT_TOTAL_REVIEW_COUNT
            },
            {
                '_id': 0
            }
        )
        product_avg_rating = mongo_database.customer_behaviors.find_one(
            {
                'product_id': '857710100',
                'type': META_TYPE_PRODUCT_AVERAGE_RATING
            },
            {
                '_id': 0
            }
        )

        assert review_count is None

        assert product_avg_rating is None

        assert mock_pubsub.call_count == 0
