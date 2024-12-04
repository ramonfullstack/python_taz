import logging
from concurrent.futures import ThreadPoolExecutor, wait
from datetime import datetime, timedelta

from simple_settings import settings

from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.google.stream import (
    DeadlineManager,
    StreamPublisherManager
)
from taz.consumers.rebuild.scopes.base import BaseRebuildWithRawMessage

logger = logging.getLogger(__name__)


ENVS = {
    'MAX_THREAD': settings.MAX_PUBSUB_SEND_THREADS_MARVIN_SELLER_REBUILD,
    'ACK_DEADLINE_SECONDS': settings.ACK_DEADLINE_SECONDS_MARVIN_SELLER_REBUILD, # noqa
    'ITERATION_SECONDS': settings.MAX_ITERATION_SECONDS_MARVIN_SELLER_REBUILD,
    'LIMIT_MARVIN_SELLER_REBUILD': settings.LIMIT_MARVIN_SELLER_REBUILD
}


class RebuildMarvinSellerPaginator(MongodbMixin, BaseRebuildWithRawMessage):
    poller_scope = 'rebuild_marvin_seller_paginator'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._next_ack_refresh = None
        self.raw_products = self.get_collection('raw_products')
        self.pubsub_manager = StreamPublisherManager()
        self.deadline_manager = DeadlineManager(
            subscription_name=settings.PUBSUB_REBUILD_SUB_NAME,
            project_id=settings.GOOGLE_PROJECT_ID
        )

    @staticmethod
    def get_env_value(env_name, default_value):
        env_string_value = ENVS.get(env_name, default_value)

        try:
            return int(env_string_value)
        except ValueError as e:
            logger.warning(f'cant load: {env_name}: {e}')
            return default_value

    @staticmethod
    def get_aggregation(seller_id, sku=None):
        match = {
            'seller_id': seller_id,
            'disable_on_matching': False,
            'sku': {
                '$gt': sku
            }
        } if sku else {
            'seller_id': seller_id,
            'disable_on_matching': False,
        }

        return [{
            '$match': match
        }, {
            '$sort': {
                'sku': 1
            }
        }, {
            '$limit': RebuildMarvinSellerPaginator.get_env_value(
                'LIMIT_MARVIN_SELLER_REBUILD', 10000
            )
        }, {
            '$project': {
                '_id': 0,
                'sku': 1,
            }
        }, {
            '$group': {
                '_id': None,
                'min_sku': {
                    '$min': '$sku'
                },
                'max_sku': {
                    '$max': '$sku'
                }
            }
        }]

    def must_refresh_ack_deadline(self):
        return datetime.now() >= self.next_ack_refresh

    @property
    def next_ack_refresh(self):
        if self._next_ack_refresh is None:
            self._next_ack_refresh = (
                datetime.now() + timedelta(
                    seconds=RebuildMarvinSellerPaginator.get_env_value(
                        'ITERATION_SECONDS',
                        60
                    )
                )
            )

        return self._next_ack_refresh

    def reload_ack_refresh(self):
        self._next_ack_refresh = (
            datetime.now() + timedelta(
                seconds=RebuildMarvinSellerPaginator.get_env_value(
                    'ITERATION_SECONDS',
                    60
                )
            )
        )

    def _rebuild(self, message, action, data):
        logger.info(
            f'Starting marvin seller rebuild paginator with action:{action} '
            f'request:{data}'
        )

        if action not in ['update', 'delete']:
            logger.warning(
                f'Invalid action [{action}] on marvin seller rebuild paginator'
            )
            return True

        sku = None
        payloads = []
        seller_id = data.get('seller_id')
        if not seller_id:
            logger.warning(
                f'Invalid seller_id [{seller_id}] on marvin seller rebuild paginator' # noqa
            )
            return True

        while True:
            aggregation = RebuildMarvinSellerPaginator.get_aggregation(
                seller_id=seller_id,
                sku=sku
            )
            agg_result = list(self.raw_products.aggregate(aggregation))
            if not agg_result or str(sku) == str(agg_result[-1]['max_sku']):
                logger.info(
                    f'Finishing marvin seller rebuild paginator for {seller_id}' # noqa
                )
                break

            payloads.extend([
                {
                    'scope': data.get('scope', 'marvin_seller'),
                    'action': action,
                    'data': {
                        'seller_id': seller_id,
                        'min_sku': result.get('min_sku'),
                        'max_sku': result.get('max_sku')
                    }
                }
                for result in agg_result if result
            ])
            sku = agg_result[-1]['max_sku']
            logger.debug(f'updated payloads size: {len(payloads)}')
            if self.must_refresh_ack_deadline():
                ack_id = message.ack_id
                self.deadline_manager.try_modify_ack_deadline(
                    ack_id,
                    RebuildMarvinSellerPaginator.get_env_value(
                        'ACK_DEADLINE_SECONDS',
                        600
                    )
                )
                self.reload_ack_refresh()

        with ThreadPoolExecutor(
            max_workers=RebuildMarvinSellerPaginator.get_env_value(
                'MAX_THREAD',
                3
            )
        ) as executor:
            futures = [
                executor.submit(self.publish_message, payload)
                for payload in payloads
            ]

        wait(futures)
        return True

    def publish_message(self, payload):
        self.pubsub_manager.publish(
            content=payload,
            topic_name=settings.PUBSUB_REBUILD_TOPIC_NAME,
            project_id=settings.GOOGLE_PROJECT_ID
        )
