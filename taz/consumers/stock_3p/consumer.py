from datetime import datetime
from functools import cached_property
from typing import Dict, Optional

from maaslogger import base_logger
from simple_settings import settings

from taz.constants import (
    CREATE_ACTION,
    MAGAZINE_LUIZA_SELLER_ID,
    STOCK_ERROR_CODE,
    STOCK_ERROR_MESSAGE,
    STOCK_SUCCESS_CODE,
    STOCK_SUCCESS_MESSAGE,
    STOCK_UNFINISHED_PROCESS,
    UPDATE_ACTION
)
from taz.consumers.core.brokers.stream import (
    PubSubBroker,
    PubSubRecordProcessor
)
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.locks import CacheLock
from taz.consumers.core.notification import Notification
from taz.consumers.stock_3p.helpers import Stock3pHelper
from taz.core.notification.notification_sender import NotificationSender
from taz.helpers.format import generate_sku_seller_id_key
from taz.helpers.json import strip_decimals
from taz.utils import decode_body

logger = base_logger.get_logger(__name__)


class Stock3pRecordProcessor(MongodbMixin, PubSubRecordProcessor):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @cached_property
    def prices(self):
        return self.get_collection('prices')

    @cached_property
    def stocks(self):
        return self.get_collection('stocks')

    @cached_property
    def raw_products(self):
        return self.get_collection('raw_products')

    @cached_property
    def price_lock(self):
        return self.get_collection('price_lock')

    @cached_property
    def sns(self):
        return Notification()

    @cached_property
    def patolino(self):
        return NotificationSender()

    def process_message(self, message: Dict) -> None:
        if not self.__is_valid_message(message):
            return

        self.__update(message)

    def __create(self, message: Dict):
        logger.debug(f'Request created stock 3P with payload:{message}')

        decoded_payload = decode_body(strip_decimals(message))

        key = generate_sku_seller_id_key(
            sku=message['sku'],
            seller_id=message['seller_id']
        )
        lock_key = f'prices-{key}'

        with CacheLock(key=lock_key):
            decoded_payload.update({
                'last_updated_at': datetime.utcnow().isoformat(),
                'md5': Stock3pHelper.prepare_md5(decoded_payload)
            })

            navigation_id = self.__get_navigation_id(message)

            self.__save(
                data=decoded_payload,
                navigation_id=navigation_id,
                action=CREATE_ACTION
            )

            self._catalog_notification(
                action=CREATE_ACTION,
                sku=message['sku'],
                seller_id=message['seller_id'],
                navigation_id=navigation_id,
                tracking_id=message.get('tracking_id')
            )

            logger.info(
                'Successfully created stock 3P for sku:{sku} '
                'seller_id:{seller_id} with '
                'stock_count:{stock_count}'.format(
                    sku=decoded_payload.get('sku'),
                    seller_id=decoded_payload.get('seller_id'),
                    stock_count=decoded_payload.get('stock_count')
                )
            )

    def __update(self, message: Dict):
        logger.debug(f'Request updated stock 3P with payload:{message}')

        criteria = {
            'sku': message['sku'],
            'seller_id': message['seller_id']
        }

        document = self.prices.find_one(criteria, {'_id': 0}) or {}

        if not document:
            self.__create(message)
            return

        decoded_payload = decode_body(strip_decimals(message))
        payload = Stock3pHelper.merge(document, decoded_payload)
        new_md5 = Stock3pHelper.prepare_md5(payload)

        if document.get('md5') == new_md5:
            logger.info(
                'Skip stock 3p update for sku:{sku} seller_id:{seller_id} '
                'with stock_count:{stock_count}'.format(
                    sku=payload['sku'],
                    seller_id=payload['seller_id'],
                    stock_count=payload.get('stock_count')
                )
            )

            self.patolino.notify_patolino_about_unfinished_process( # noqa
                product=payload,
                action=UPDATE_ACTION,
                reason='Values did not change',
                code=STOCK_UNFINISHED_PROCESS
            )
            return

        payload.update({
            'last_updated_at': datetime.utcnow().isoformat(),
            'md5': new_md5
        })

        navigation_id = self.__get_navigation_id(message)

        self.__save(
            data=payload,
            navigation_id=navigation_id,
            action=UPDATE_ACTION
        )

        self._catalog_notification(
            action=UPDATE_ACTION,
            sku=message['sku'],
            seller_id=message['seller_id'],
            navigation_id=navigation_id,
            tracking_id=message.get('tracking_id')
        )

        logger.info(
            'Successfully updated stock 3P for sku:{sku} '
            'seller_id:{seller_id} stock_count:{stock_count} '.format(
                sku=message['sku'],
                seller_id=message['seller_id'],
                stock_count=payload.get('stock_count')
            )
        )

    def __save(self, data: Dict, navigation_id: str, action: str) -> None:
        data['source'] = self.scope

        criteria = {
            'sku': data['sku'],
            'seller_id': data['seller_id']
        }

        notification_payload = {
            'action': action,
            **criteria
        }

        try:
            payload_stocks = Stock3pHelper.mount_payload_stocks(
                sku=criteria['sku'],
                seller_id=criteria['seller_id'],
                navigation_id=navigation_id,
                stock_count=data['stock_count']
            )

            payload_stocks['branch_id'] = 0

            self.stocks.update_many(
                {**criteria, 'branch_id': 0},
                {'$set': payload_stocks},
                upsert=True
            )

            self.prices.update_many(
                criteria,
                {'$set': data},
                upsert=True
            )

            self.patolino.send(
                sku=data['sku'],
                seller_id=data['seller_id'],
                code=STOCK_SUCCESS_CODE,
                message=STOCK_SUCCESS_MESSAGE,
                tracking_id=data.get('tracking_id'),
                payload=notification_payload
            )
        except Exception as e:
            logger.error(
                'Could not save stock 3P for sku:{sku} seller_id:{seller_id} '
                'with payload:{payload} and error:{error}'.format(
                    sku=criteria['sku'],
                    seller_id=criteria['seller_id'],
                    error=e,
                    payload=data
                )
            )
            self.patolino.send(
                sku=data['sku'],
                seller_id=data['seller_id'],
                code=STOCK_ERROR_CODE,
                message=STOCK_ERROR_MESSAGE,
                tracking_id=data.get('tracking_id'),
                payload=notification_payload
            )
            raise

    @staticmethod
    def __is_valid_message(data: Dict) -> bool:
        if data['seller_id'] == MAGAZINE_LUIZA_SELLER_ID:
            return False

        if Stock3pHelper.is_missing_stock(data):
            logger.warning(
                'Discarding stock for sku:{sku} '
                'seller_id:{seller_id} because stock '
                'is null. payload:{payload}'.format(
                    sku=data['sku'],
                    seller_id=data['seller_id'],
                    payload=data
                )
            )
            return False
        return True

    def __get_navigation_id(self, message: Dict) -> Optional[str]:
        if message.get('navigation_id'):
            return message['navigation_id']

        product = self.raw_products.find_one(
            {'sku': message['sku'], 'seller_id': message['seller_id']},
            {'navigation_id': 1, '_id': 0}
        )

        if not product:
            return None

        return product['navigation_id']

    def _catalog_notification(
        self,
        action: str,
        sku: str,
        seller_id: str,
        tracking_id: str,
        navigation_id: str = None
    ) -> None:
        payload = {
            'sku': sku,
            'seller_id': seller_id,
            'tracking_id': tracking_id
        }

        if navigation_id:
            payload.update({'navigation_id': navigation_id})

        self.sns.put(
            data=payload,
            scope=self.scope,
            action=action
        )

        logger.debug(
            f'Send stock 3P notification for sku:{sku} seller_id:{seller_id} '
            f'with scope:{self.scope} and action:{action}'
        )


class Stock3pConsumer(PubSubBroker):
    scope = 'stock'
    project_name = settings.GOOGLE_PROJECT_ID
    record_processor_class = Stock3pRecordProcessor
