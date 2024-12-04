from datetime import datetime

from maaslogger import base_logger
from simple_settings import settings

from taz.constants import (
    DEFAULT_CAMPAIGN_CODE,
    MAGAZINE_LUIZA_SELLER_ID,
    UPDATE_ACTION
)
from taz.consumers.core.brokers.stream import (
    PubSubBroker,
    PubSubRecordProcessor
)
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.notification import Notification
from taz.utils import md5

logger = base_logger.get_logger(__name__)


class PricingRecordProcessor(MongodbMixin, PubSubRecordProcessor):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prices = self.get_collection('prices')
        self.notification = Notification()

    def process_message(self, message):
        campaign_code = message['data']['campaign_code']
        channel_id = message['data']['channel_id']
        seller_id = message['data']['seller_id']
        sku = message['data']['sku']
        price = message['data']['price']
        base_price = message['data']['base_price']

        if (
            campaign_code != DEFAULT_CAMPAIGN_CODE or
            channel_id != '*' or
            seller_id != MAGAZINE_LUIZA_SELLER_ID
        ):
            return

        logger.info(
            'Payload received for sku:{sku} seller_id:{seller_id} '
            'payload:{payload}'.format(
                sku=sku,
                seller_id=seller_id,
                payload=message
            )
        )

        self._save(sku, seller_id, price, base_price)
        self._catalog_notification(sku, seller_id)

        logger.info(
            'Processing message for sku:{sku} seller_id:{seller_id} '
            'scope:{scope} action:{action}, price:{price} '
            'list_price:{list_price}'.format(
                sku=sku,
                seller_id=seller_id,
                scope=self.scope,
                action=UPDATE_ACTION,
                price=price,
                list_price=base_price
            )
        )

        return True

    def _save(self, sku, seller_id, price, base_price):
        criteria = {'sku': sku, 'seller_id': seller_id}

        payload = self.prices.find_one(criteria, {'_id': 0}) or criteria

        payload.update({
            'price': price,
            'list_price': base_price,
            'source': self.scope,
            'last_updated_at': datetime.utcnow().isoformat()
        })

        payload['md5'] = md5(payload)

        self.prices.update_many(criteria, {'$set': payload}, upsert=True)

        return True

    def _catalog_notification(self, sku, seller_id):
        payload = {'sku': sku, 'seller_id': seller_id}

        self.notification.put(payload, 'price', UPDATE_ACTION)

        logger.debug(
            'Sent pricing notification for sku:{sku} seller_id:{seller_id} '
            'scope:{scope} action:{action}'.format(
                sku=sku,
                seller_id=seller_id,
                action=UPDATE_ACTION,
                scope=self.scope,
            )
        )


class PricingConsumer(PubSubBroker):
    project_name = settings.GOOGLE_PROJECT_ID
    scope = 'pricing'
    record_processor_class = PricingRecordProcessor
