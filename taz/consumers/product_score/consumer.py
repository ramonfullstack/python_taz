
from maaslogger import base_logger
from simple_settings import settings

from taz import constants
from taz.consumers.core.brokers.stream import (
    PubSubBroker,
    PubSubRecordProcessor
)
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.notification import Notification
from taz.core.score import Score
from taz.core.score.helpers import create_payload
from taz.core.storage.factsheet_storage import FactsheetStorage
from taz.utils import convert_id_to_nine_digits, cut_product_id

logger = base_logger.get_logger(__name__)
PRODUCT_SCORE_CONSUMER_SCOPE = 'product_score'


class ProductScoreProcessor(MongodbMixin, PubSubRecordProcessor):

    scope = PRODUCT_SCORE_CONSUMER_SCOPE
    max_process_workers = settings.PRODUCT_SCORE_PROCESS_WORKERS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.raw_products = self.get_collection('raw_products')
        self.enriched_products = self.get_collection('enriched_products')
        self.medias = self.get_collection('medias')
        self.customer_behaviors = self.get_collection('customer_behaviors')
        self.scores = self.get_collection('scores')
        self.score = Score()
        self.notification = Notification()
        self.factsheet_storage = FactsheetStorage()

    def process_message(self, message):
        criteria = {'sku': message['sku'], 'seller_id': message['seller_id']}
        raw_product = self.raw_products.find_one(criteria, {'_id': 0})

        if not raw_product:
            logger.warning(
                'Product not found for sku:{sku} seller_id:{seller_id}'.format(
                    **criteria
                )
            )
            return True

        if not raw_product.get('navigation_id'):
            self.scores.update_many(
                {
                    'sku': raw_product['sku'],
                    'seller_id': raw_product['seller_id'],
                    'active': True
                },
                {
                    '$set': {'active': False}
                }
            )

            logger.warning(
                'Product does not have a navigation_id, saving to disabled '
                'score from sku:{sku} seller_id:{seller_id}'.format(
                    **criteria
                )
            )
            return True

        enriched_product = self.enriched_products.find_one({
            'sku': criteria['sku'],
            'seller_id': criteria['seller_id'],
            '$or': [
                {'source': constants.SOURCE_METABOOKS},
                {'source': constants.SOURCE_OMNILOGIC}
            ]
        })

        if not enriched_product:
            logger.debug(
                'Enriched product not found for sku:{sku} '
                'seller_id:{seller_id}'.format(
                    **criteria
                )
            )

            category_id = 'RC'
            categories = raw_product.get('categories') or []
            if categories:
                category_id = categories[0]['id']

            enriched_product = {
                'entity': constants.SCORE_DEFAULT_ENTITY,
                'category_id': category_id
            }

        media = self.medias.find_one(criteria) or {}
        if not media:
            logger.debug(
                'Medias not found for sku:{sku} seller_id:{seller_id}'.format(
                    **criteria
                )
            )

        navigation_id = raw_product['navigation_id']

        customer_behaviors = list(self.customer_behaviors.find(
            {
                '$or': [
                    {'product_id': convert_id_to_nine_digits(navigation_id)},
                    {'product_id': cut_product_id(navigation_id)}
                ]
            }
        ))

        if not customer_behaviors:
            logger.debug(
                'Customer behavior not found for navigation_id:{}'.format(
                    navigation_id
                )
            )

        product = create_payload(
            raw_product,
            enriched_product,
            media,
            customer_behaviors,
            self._get_factsheet(
                criteria['sku'],
                criteria['seller_id']
            )
        )

        self.score.calculate(product)

        self.catalog_notification(
            constants.UPDATE_ACTION,
            message['seller_id'],
            message['sku'],
            raw_product['navigation_id']
        )

        logger.info(
            'Saving score for product sku:{sku} seller_id:{seller_id}'.format(
                **criteria
            )
        )

        return True

    def catalog_notification(self, action, seller_id, sku, navigation_id):
        payload = {
            'sku': sku,
            'seller_id': seller_id,
            'navigation_id': navigation_id
        }

        self.notification.put(payload, self.scope, action)

        logger.debug(
            'Send product notification for sku:{sku} seller_id:{seller_id} '
            'navigation_id:{navigation_id} scope:{scope} '
            'action:{action}'.format(
                action=action,
                scope=self.scope,
                **payload
            )
        )

    def _get_factsheet(self, sku, seller_id):
        if self.score.version.VERSION == constants.SCORE_V3:
            try:
                return self.factsheet_storage.get_bucket_data(
                    sku=sku,
                    seller_id=seller_id
                )
            except Exception as e:
                logger.info(
                    'Error to get factsheet from bucket:{}'.format(e)
                )


class ProductScoreConsumer(PubSubBroker):
    scope = PRODUCT_SCORE_CONSUMER_SCOPE
    record_processor_class = ProductScoreProcessor
    project_name = settings.GOOGLE_PROJECT_ID
