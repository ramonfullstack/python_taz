import copy
from datetime import datetime
from functools import cached_property
from typing import Dict, Union

from maaslogger import base_logger
from simple_settings import settings

from taz.constants import (
    CREATE_ACTION,
    DELETE_ACTION,
    PRICE_ERROR_CODE,
    PRICE_ERROR_MESSAGE,
    PRICE_SUCCESS_CODE,
    PRICE_SUCCESS_MESSAGE,
    PRICE_UNFINISHED_PROCESS,
    UPDATE_ACTION
)
from taz.consumers.core.brokers.stream import (
    PubSubBroker,
    PubSubRecordProcessor
)
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.locks import CacheLock
from taz.consumers.core.notification import Notification
from taz.core.notification.notification_sender import NotificationSender
from taz.helpers.format import generate_sku_seller_id_key
from taz.helpers.json import strip_decimals
from taz.utils import decode_body, md5

logger = base_logger.get_logger(__name__)


class Price3pRecordProcessor(MongodbMixin, PubSubRecordProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @cached_property
    def raw_products(self):
        return self.get_collection('raw_products')

    @cached_property
    def prices(self):
        return self.get_collection('prices')

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

        self.__check_price_vs_cubage(message)
        self.__update(message)

    def __create(self, message: Dict):
        logger.debug(f'Request created price with payload:{message}')

        decoded_price = decode_body(strip_decimals(message))

        sku = message['sku']
        seller_id = message['seller_id']

        key = generate_sku_seller_id_key(sku, seller_id)
        lock_key = f'prices-{key}'

        with CacheLock(key=lock_key):
            decoded_price.update({
                'last_updated_at': datetime.utcnow().isoformat(),
                'md5': self.__prepare_md5(decoded_price)
            })

            self.__save(decoded_price, CREATE_ACTION)
            self._catalog_notification(
                action=CREATE_ACTION,
                sku=sku,
                seller_id=seller_id,
                navigation_id=message.get('navigation_id'),
                tracking_id=message.get('tracking_id')
            )

            logger.info(
                'Successfully created price for sku:{sku} seller_id:'
                '{seller_id} price:{price} list_price:{list_price}'.format(
                    sku=sku,
                    seller_id=seller_id,
                    price=decoded_price.get('price'),
                    list_price=decoded_price.get('list_price')
                )
            )

    def __update(self, message: Dict):
        logger.debug(f'Request updated price with payload:{message}')

        criteria = {
            'sku': message['sku'],
            'seller_id': message['seller_id']
        }

        document = self.prices.find_one(criteria, {'_id': 0}) or {}

        if not document:
            self.__create(message)
            return

        decoded_price = decode_body(strip_decimals(message))
        payload = self._merge(document, decoded_price)
        new_md5 = self.__prepare_md5(payload)

        if document.get('md5') == new_md5:
            logger.info(
                'Skip price update for sku:{sku} seller_id:{seller_id} '
                'price:{price} list_price:{list_price}'.format(
                    sku=payload['sku'],
                    seller_id=payload['seller_id'],
                    price=payload.get('price'),
                    list_price=payload.get('list_price')
                )
            )
            self.patolino.notify_patolino_about_unfinished_process(
                payload,
                UPDATE_ACTION,
                'Values did not change',
                code=PRICE_UNFINISHED_PROCESS
            )
            return

        blocked_reason = self.__block_product(document, message)

        if blocked_reason:
            self.patolino.notify_patolino_about_error(
                payload,
                UPDATE_ACTION,
                blocked_reason,
                PRICE_ERROR_CODE
            )
            return

        info_fields = {
            'last_updated_at': datetime.utcnow().isoformat(),
            'md5': new_md5
        }

        decoded_price.update(info_fields)
        payload.update(info_fields)

        self.__save(decoded_price, UPDATE_ACTION)
        self._catalog_notification(
            action=UPDATE_ACTION,
            sku=criteria['sku'],
            seller_id=criteria['seller_id'],
            navigation_id=message.get('navigation_id'),
            tracking_id=message.get('tracking_id')
        )

        logger.info(
            'Successfully updated price sku:{sku} seller_id:{seller_id} '
            'price:{price} list_price:{list_price}'.format(
                sku=criteria['sku'],
                seller_id=criteria['seller_id'],
                price=payload.get('price'),
                list_price=payload.get('list_price')
            )
        )

    def __save(self, data: Dict, action: str) -> None:
        data['source'] = self.scope

        sku = data['sku']
        seller_id = data['seller_id']

        criteria = {
            'sku': sku,
            'seller_id': seller_id
        }

        notification_payload = {
            'action': action,
            'sku': sku,
            'seller_id': seller_id
        }

        try:
            self.prices.update_many(criteria, {'$set': data}, upsert=True)
            self.patolino.send(
                sku=sku,
                seller_id=seller_id,
                code=PRICE_SUCCESS_CODE,
                message=PRICE_SUCCESS_MESSAGE,
                tracking_id=data.get('tracking_id'),
                payload=notification_payload
            )
        except Exception as e:
            logger.error(
                f'Could not save price sku:{sku} seller_id:{seller_id} '
                f'payload:{data} error:{e}'
            )
            self.patolino.send(
                sku=sku,
                seller_id=seller_id,
                code=PRICE_ERROR_CODE,
                message=PRICE_ERROR_MESSAGE,
                tracking_id=data.get('tracking_id'),
                payload=notification_payload
            )
            raise

    def __block_product(
        self,
        current_price: Dict,
        new_price: Dict
    ) -> Union[bool, str]:

        if not settings.ENABLE_PRICE_LOCK_PERCENT:
            return False

        if (
            'price' not in current_price or
            'price' not in new_price
        ):
            return False

        sku = new_price['sku']
        seller_id = new_price['seller_id']

        price_lock = self.price_lock.find_one({'seller_id': seller_id})

        max_percent = float(
            price_lock.get('percent')
            if price_lock else settings.DEFAULT_PRICE_LOCK_PERCENT
        ) / 100

        lowest_price_accepted = current_price['price'] * max_percent
        if new_price['price'] < lowest_price_accepted:
            reason = (
                'Blocking product because lowest price accepted violated '
                'price update for sku:{sku} seller_id:{seller_id} '
                'current_price: {current_price} new price:{new_price} '
                'max_percent:{max_percent} '
                'lowest price accepted:{lowest_price_accepted}'.format(
                    sku=new_price['sku'],
                    seller_id=new_price['seller_id'],
                    current_price=current_price['price'],
                    new_price=new_price['price'],
                    max_percent=max_percent,
                    lowest_price_accepted=lowest_price_accepted
                )
            )
            logger.info(reason)

            new_price['disable_on_matching'] = True
            self.raw_products.update_many(
                {
                    'sku': sku,
                    'seller_id': seller_id
                },
                {
                    '$set': {
                        'disable_on_matching': True
                    }
                }
            )

            self._catalog_notification(
                action=DELETE_ACTION,
                sku=sku,
                seller_id=seller_id,
                navigation_id=new_price.get('navigation_id'),
                tracking_id=current_price.get('tracking_id')
            )
            return reason

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

    @staticmethod
    def _merge(price: Dict, new_price: Dict) -> Dict:
        price_merged = copy.deepcopy(price)
        price_merged.update(new_price)
        return price_merged

    @staticmethod
    def __is_valid_message(data: Dict) -> bool:
        if 'price' not in data or 'list_price' not in data:
            logger.warning(
                'Discarding price for sku:{sku} seller_id:{seller} because '
                'price is NULL. payload:{payload}'.format(
                    sku=data['sku'],
                    seller=data['seller_id'],
                    payload=data
                )
            )
            return False

        price = data['price']
        list_price = data['list_price']

        if (
            not price or price <= 0 or
            not list_price or list_price <= 0
        ):
            logger.warning(
                'Discarding price for sku:{sku} seller_id:{seller} because '
                'is a invalid price. payload:{payload}'.format(
                    sku=data['sku'],
                    seller=data['seller_id'],
                    payload=data
                )
            )
            return False
        return True

    @staticmethod
    def __prepare_md5(new_price: Dict) -> str:
        payload = new_price.copy()

        payload.pop('source', None)
        old_md5 = payload.pop('md5', None)

        return md5(payload, old_md5)

    def __check_price_vs_cubage(self, data: Dict):
        if data['price'] <= 0.05 and data['list_price'] <= 1:

            sku = data['sku']
            seller_id = data['seller_id']

            product = self.raw_products.find_one(
                {
                    'sku': sku,
                    'seller_id': seller_id
                },
                {
                    'dimensions': 1,
                    'disable_on_matching': 1,
                    '_id': 0
                }
            )

            if product['disable_on_matching']:
                return False

            dimensions = product['dimensions']

            if int(
                dimensions['width'] *
                dimensions['depth'] *
                dimensions['height'] *
                (100 ** 3)
            ) > 1000:
                logger.warning(
                    f'Wrong Price X Cubage for sku:{sku} seller_id:{seller_id}'
                )


class Price3pConsumer(PubSubBroker):
    scope = 'price'
    project_name = settings.GOOGLE_PROJECT_ID
    record_processor_class = Price3pRecordProcessor
