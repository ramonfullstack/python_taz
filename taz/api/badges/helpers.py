import json
import logging
from datetime import datetime

from redis import Redis
from simple_settings import settings

from taz import constants
from taz.api.common.models.validations import convert_str_to_datetime
from taz.consumers.core.google.stream import StreamPublisherManager

logger = logging.getLogger(__name__)


def validate(data):
    required_fields = (
        'image_url', 'position', 'container', 'start_at',
        'end_at', 'products', 'name', 'slug',
    )

    return all(f in data for f in required_fields)


def create_interval_payload(payload):
    payload['start_at'] = convert_str_to_datetime(
        datetime.fromtimestamp(
            payload['start_at']['$date'] / 1000
        )
    )

    payload['end_at'] = convert_str_to_datetime(
        datetime.fromtimestamp(
            payload['end_at']['$date'] / 1000
        )
    )

    return payload


def create_payload(payload, data):
    badge = json.loads(payload.to_json())

    del badge['_id']

    badge['name'] = data['name']
    badge['position'] = data['position']
    badge['container'] = data['container']
    badge['text'] = data['text']
    badge['tooltip'] = data['tooltip']
    badge['start_at'] = convert_str_to_datetime(data['start_at'])
    badge['end_at'] = convert_str_to_datetime(data['end_at'])
    badge['products'] = data['products']
    badge['priority'] = data['priority']
    badge['image_url'] = data['image_url']

    return badge


def validate_product_list(product, list_to_compare):
    product_dict = {
        'sku': product['sku'],
        'seller_id': product['seller_id']
    }
    return product_dict in list_to_compare


class BadgeProductCache:

    def __init__(self):
        self.cache = Redis(
            host=settings.REDIS_LOCK_SETTINGS['host'],
            port=settings.REDIS_LOCK_SETTINGS['port'],
            password=settings.REDIS_LOCK_SETTINGS.get('password')
        )

    def remove(self, product):
        cache_key = constants.BADGE_CACHE_KEY.format(
            sku=product['sku'],
            seller_id=product['seller_id']
        )

        self.cache.delete(cache_key)

        logger.info(
            'Removed cache from product badge '
            'sku:{sku} seller:{seller} successfully.'.format(
                sku=product['sku'],
                seller=product['seller_id'],
            )
        )


class BadgeProductQueue:

    def __init__(self):
        self.pubsub = StreamPublisherManager()

    def send_update(self, product):
        action = constants.UPDATE_ACTION
        payload = {
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'action': action,
            'force': True,
            'origin': __name__
        }

        self.pubsub.publish(
            content=payload,
            topic_name=settings.PUBSUB_PRODUCT_WRITER_TOPIC_NAME,
            project_id=settings.GOOGLE_PROJECT_ID

        )

        logger.info(
            'Notifying the product sku:{sku} seller:{seller_id} '
            'action:{action} in the product writer queue through '
            'badge product API'.format(
                sku=product['sku'],
                seller_id=product['seller_id'],
                action=action
            )
        )
