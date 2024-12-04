import datetime

from maaslogger import base_logger
from simple_settings import settings

from taz import constants
from taz.constants import (
    META_TYPE_PRODUCT_AVERAGE_RATING,
    META_TYPE_PRODUCT_TOTAL_REVIEW_COUNT
)
from taz.consumers.core.brokers.stream import (
    PubSubBroker,
    PubSubRecordProcessor
)
from taz.consumers.core.cache.redis import CacheMixin
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.notification import Notification
from taz.utils import convert_id_to_nine_digits, md5

logger = base_logger.get_logger(__name__)


class UserReviewRecordProcessor(
    MongodbMixin,
    CacheMixin,
    PubSubRecordProcessor,
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.customer_behaviors = self.get_collection('customer_behaviors')
        self.raw_products = self.get_collection('raw_products')
        self.notification = Notification()
        self.cache_key_prefix = constants.USER_REVIEW_CACHE_KEY_PREFIX
        self.cache_expire_ttl = datetime.timedelta(
            minutes=settings.USER_REVIEW_CACHE_TTL
        )
        self.cache = self.get_cache()

    def get_user_review_cache_key(self, payload: dict) -> str:
        return self.cache_key_prefix.format(
            seller_id=payload.get('seller_id'), sku=payload.get('sku')
        )

    def set_user_review_cache(self, payload: dict):
        cache_key = self.get_user_review_cache_key(payload)
        payload_md5 = md5(payload)

        self.cache.set(cache_key, payload_md5)
        self.cache.expire(cache_key, self.cache_expire_ttl)

    def has_skip_user_review(self, payload: dict) -> bool:
        cache_key = self.get_user_review_cache_key(payload)
        logger.debug(f'Verify skip user review cache key:{cache_key}')
        review = self.cache.get(cache_key)

        if not review:
            logger.debug(f'Cache not exits for cache_key:{cache_key}')
            return False

        review = review.decode()
        payload_md5 = md5(payload)
        logger.debug(f'Verify md5 user review cached:{review}'
                     f' payload:{payload_md5}')
        has_skip = payload_md5 == review

        if has_skip:
            self.cache.expire(cache_key, self.cache_expire_ttl)
        return has_skip

    def process_message(self, message):
        navigation_id = None
        avg_rating = None
        review_count = None

        try:
            navigation_id = message['ExternalId']
            seller_id = message['seller_id']
            sku = message['sku']
            avg_rating = message['AverageRating']
            review_count = message['TotalReviewCount']
        except KeyError:
            logger.warning(
                'Invalid incoming message for user review '
                'with payload:{payload}'.format(payload=message)
            )
            return True
        review_payload = {
            'seller_id': seller_id,
            'sku': sku,
            'avg_rating': avg_rating,
            'review_count': review_count,
        }
        if self.has_skip_user_review(review_payload):
            logger.warning(
                'Review with sku:{sku} seller_id: {seller_id}'
                ' skipped'.format(sku=sku, seller_id=seller_id)
            )
            return True

        product = self.raw_products.find_one({
            'sku': sku,
            'seller_id': seller_id
        })

        if not product:
            logger.warning(
                'Product with sku:{sku} seller_id {seller_id}'
                ' not found in raw_products'.format(
                    sku=sku,
                    seller_id=seller_id
                )
            )

            return True

        self._remove_history(navigation_id)

        self._save_user_reviews(navigation_id, review_count, avg_rating)

        self._catalog_notification(
            seller_id=product['seller_id'],
            sku=product['sku'],
            navigation_id=navigation_id,
        )

        self.set_user_review_cache(review_payload)
        logger.info(
            'Successfully processed the message for sku:{sku} '
            'seller_id:{seller_id} navigation_id:{navigation_id} '
            'review_count:{review_count} avg_rating:{avg_rating}'.format(
                sku=product['sku'],
                seller_id=product['seller_id'],
                navigation_id=navigation_id,
                review_count=review_count,
                avg_rating=avg_rating,
            )
        )

        return True

    def _remove_history(self, navigation_id):
        criteria = {
            '$and': [
                {'product_id': navigation_id},
                {
                    'type': {
                        '$in': [
                            META_TYPE_PRODUCT_TOTAL_REVIEW_COUNT,
                            META_TYPE_PRODUCT_AVERAGE_RATING,
                        ]
                    }
                },
            ],
        }
        self.customer_behaviors.remove(criteria)

    def _save_user_reviews(self, navigation_id, review_count, avg_rating):
        self.customer_behaviors.insert_many(
            [
                {
                    'product_id': navigation_id,
                    'type': META_TYPE_PRODUCT_TOTAL_REVIEW_COUNT,
                    'value': review_count,
                },
                {
                    'product_id': navigation_id,
                    'type': META_TYPE_PRODUCT_AVERAGE_RATING,
                    'value': avg_rating,
                },
            ]
        )

    def _catalog_notification(self, seller_id, sku, navigation_id):
        payload = {
            'sku': sku,
            'seller_id': seller_id,
            'navigation_id': convert_id_to_nine_digits(navigation_id),
        }

        self.notification.put(payload, 'reviews', constants.UPDATE_ACTION)

        logger.debug(
            'Send user review notification for sku:{sku} '
            'seller_id:{seller_id} navigation_id:{navigation_id} '
            'scope:{scope} action:{action}'.format(
                action=constants.UPDATE_ACTION, scope=self.scope, **payload
            )
        )


class UserReviewConsumer(PubSubBroker):
    project_name = settings.GOOGLE_PROJECT_ID
    scope = 'user_review'
    record_processor_class = UserReviewRecordProcessor
