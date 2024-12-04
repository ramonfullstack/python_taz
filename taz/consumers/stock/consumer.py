from datetime import datetime

from maaslogger import base_logger
from simple_settings import settings

from taz import constants
from taz.consumers.core.brokers.stream import (
    PubSubBroker,
    PubSubRecordProcessor
)
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.google.stream import StreamPublisherManager
from taz.consumers.core.notification import Notification
from taz.consumers.core.stock import StockHelper

from .helpers import get_availability, get_type

logger = base_logger.get_logger(__name__)


class StockRecordProcessor(MongodbMixin, PubSubRecordProcessor):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stocks = self.get_collection('stocks')
        self.raw_products = self.get_collection('raw_products')
        self.prices = self.get_collection('prices')
        self.pubsub = StreamPublisherManager()
        self.notification = Notification()
        self.stock_helper = StockHelper()

    def process_message(self, message):
        logger.debug('Processing message:{}'.format(message))
        entity_type = message['entity_type']
        if entity_type != constants.ENTITY_TYPE:
            return True

        entity = message['entity']
        sku = entity['product']['sku']
        seller_id = constants.MAGAZINE_LUIZA_SELLER_ID

        criteria = {'sku': sku, 'seller_id': seller_id}

        navigation_id = self._get_navigation_id(**criteria)
        if not navigation_id:
            logger.warning(
                'Product of sku:{} seller_id:{} without navigation_id'.format(
                    sku,
                    seller_id
                )
            )
            return True

        stock_type, branch_id = self._save(
            sku,
            seller_id,
            navigation_id,
            entity
        )

        payload = self.stock_helper.mount(
            sku,
            seller_id,
            navigation_id,
            stock_type,
            branch_id
        )

        if not settings.STOCK_NOTIFICATION.get(stock_type):
            logger.info(
                'Failed to process message of sku:{} '
                'seller_id:{} because the stock type {} not found'.format(
                    sku,
                    seller_id,
                    stock_type
                )
            )
            return True

        try:
            attributes = {'seller_id': seller_id}
            self.pubsub.publish(
                content=payload,
                topic_name=settings.STOCK_NOTIFICATION[stock_type]['topic_name'],  # noqa
                project_id=settings.STOCK_NOTIFICATION[stock_type]['project_id'],  # noqa
                attributes=attributes
            )
        except Exception as e:
            logger.error(
                'An error occurred while sending data on pubsub '
                'with error:{error} payload:{payload}'.format(
                    error=e,
                    payload=payload
                )
            )
            raise

        if (
            stock_type == constants.STOCK_TYPE_DC and
            self._must_notify(sku, seller_id, payload['stock_count'])
        ):
            self._catalog_notification(seller_id, sku, navigation_id)
            self._save_price(seller_id=seller_id, sku=sku, payload=payload)

        logger.info(
            'Successfully processed the message for sku:{sku} '
            'seller_id:{seller_id} navigation_id:{navigation_id} '
            'with stock count {stock_count} and '
            'branch_id:{branch_id}'.format(

                sku=sku,
                seller_id=seller_id,
                navigation_id=navigation_id,
                stock_count=payload.get('stock_count'),
                branch_id=branch_id
            )
        )
        return True

    def _set_stock_count_for_magalu_rule(self, seller_id, stock_count):
        if seller_id == constants.MAGAZINE_LUIZA_SELLER_ID:
            stock_count = 1 if stock_count > 0 else 0

        return stock_count

    def _must_notify(self, sku, seller_id, stock_count):
        criteria = {'sku': sku, 'seller_id': seller_id}

        price = (
            self.prices.find_one(criteria, {'_id': 0, 'stock_count': 1})
        )

        if price is None or 'stock_count' not in price:
            logger.warning(
                'No stock found for product with '
                'sku:{sku} seller_id:{seller_id} in prices collection'.format(
                    sku=criteria['sku'],
                    seller_id=criteria['seller_id']
                ))

            return True

        original_stock_count = price.get('stock_count') or 0

        stock_count = self._set_stock_count_for_magalu_rule(
            seller_id=seller_id,
            stock_count=stock_count
        )

        return original_stock_count != stock_count

    def _save_price(self, seller_id, sku, payload):
        stock_count = payload['stock_count']

        stock_count = self._set_stock_count_for_magalu_rule(
            seller_id=seller_id,
            stock_count=stock_count
        )

        data = {
            'sku': sku,
            'seller_id': seller_id,
            'delivery_availability': payload['delivery_availability'],
            'stock_type': payload['stock_type'],
            'stock_count': stock_count,
            'last_updated_at': datetime.utcnow().isoformat()
        }

        self.prices.update_many(
            {'sku': sku, 'seller_id': seller_id},
            {'$set': data},
            upsert=True
        )

    def _save(self, sku, seller_id, navigation_id, entity):
        position = {}
        for level in entity['position']['new']['levels']:
            position.update(level)

        branch_id = entity['branch']['id']

        payload = {
            'seller_id': seller_id,
            'sku': sku,
            'branch_id': branch_id,
            'latitude': entity['branch']['latitude'],
            'longitude': entity['branch']['longitude'],
            'type': get_type(entity['branch']['type']['description']),
            'position': position,
            'delivery_availability': get_availability(branch_id),
            'navigation_id': navigation_id,
            'last_updated_at': datetime.utcnow().isoformat()
        }

        self.stocks.update_many(
            {'sku': sku, 'seller_id': seller_id, 'branch_id': branch_id},
            {'$set': payload},
            upsert=True
        )

        return payload['type'], payload['branch_id']

    def _get_navigation_id(self, sku, seller_id):
        product = self.raw_products.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'navigation_id': 1, '_id': 0}
        )

        if not product:
            return

        return product['navigation_id']

    def _catalog_notification(self, seller_id, sku, navigation_id):
        payload = {
            'sku': sku,
            'seller_id': seller_id,
            'navigation_id': navigation_id
        }

        action = constants.UPDATE_ACTION

        self.notification.put(payload, self.scope, action)

        logger.debug(
            'Send price notification for sku:{sku} seller_id:{seller_id} '
            'navigation_id:{navigation_id} scope:{scope} '
            'action:{action}'.format(
                action=action,
                scope=self.scope,
                **payload
            )
        )


class StockConsumer(PubSubBroker):
    project_name = settings.GOOGLE_PROJECT_ID
    scope = 'stock'
    record_processor_class = StockRecordProcessor
