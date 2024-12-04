import importlib
from functools import cached_property
from typing import Dict

from maaslogger import base_logger
from simple_settings import settings

from taz.constants import DELETE_ACTION
from taz.consumers.core.brokers.stream import (
    PubSubBroker,
    PubSubRecordProcessorValidateSchema
)
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.notification import Notification

from . import SCOPE
from .processor import MatchingProcessor
from .schema import MatchingSchema

logger = base_logger.get_logger(__name__)


class MatchingRecordProcessor(
    MongodbMixin,
    PubSubRecordProcessorValidateSchema
):
    schema_class = MatchingSchema

    def __init__(self, *args, **kwargs):
        self.persist_changes = kwargs.get('persist_changes', True)
        self.exclusive_strategy = kwargs.get('exclusive_strategy', True)
        self.strategy = kwargs.get('strategy')
        super().__init__(scope=SCOPE)

    @cached_property
    def raw_products(self):
        return self.get_collection('raw_products')

    @cached_property
    def notification(self):
        return Notification()

    def process_message(self, message: Dict):
        """
        This method decides (based on settings) which matching strategy must
        be used for each seller and delegates the execution to the
        strategy's consumer
        """
        tracking_id = message.get('tracking_id')

        if not self._valid_message(message):
            logger.error(
                f'Received invalid message from matching queue "{message}"'
            )
            return True

        sku, seller_id = message['sku'], message['seller_id']
        product = self.raw_products.find_one(
            {
                'sku': sku,
                'seller_id': seller_id
            },
            {
                '_id': 0,
                'matching_strategy': 1,
                'navigation_id': 1
            }
        ) or {}
        if not product:
            logger.warning(
                f'product not found sku:{sku} seller_id:{seller_id}',
                detail={
                    "sku": sku,
                    "seller_id": seller_id,
                }
            )
            return True

        item_strategy = self._get_strategy_for_item(
            product.get('matching_strategy')
        )

        processor = MatchingProcessor(
            persist_changes=self.persist_changes,
            exclusive_strategy=self.exclusive_strategy,
            strategy=item_strategy
        )

        logger.debug(
            'Start matching for sku:{sku} seller:{seller_id} '
            'with strategy:{strategy}'.format(
                sku=message['sku'],
                seller_id=message['seller_id'],
                strategy=item_strategy.__name__
            ),
            detail={
                "sku": sku,
                "seller_id": seller_id,
                "strategy": item_strategy.__name__,
            }
        )

        matched_product, discarded = processor.process_message(message)

        if self.persist_changes and matched_product:
            self._notify(
                message['action'],
                message['seller_id'],
                message['sku'],
                product.get('navigation_id'),
                tracking_id
            )

        if self.persist_changes and discarded:
            for discarded_info in discarded:
                self._notify(
                    DELETE_ACTION,
                    discarded_info['seller_id'],
                    discarded_info['sku'],
                    product.get('navigation_id'),
                    tracking_id
                )

        return matched_product

    def _notify(
        self,
        action: str,
        seller_id: str,
        sku: str,
        navigation_id: str,
        tracking_id: str
    ) -> None:
        payload = {
            'seller_id': seller_id,
            'sku': sku,
            'navigation_id': navigation_id,
            'tracking_id': tracking_id
        }

        self.notification.put(payload, self.scope, action)

        logger.info(
            f'Send matching notification for sku:{sku} seller_id:{seller_id} '
            f'scope:{self.scope} action:{action}',
            detail={
                "sku": sku,
                "seller_id": seller_id,
                "scope": self.scope,
                "action": action
            }
        )

    @staticmethod
    def _valid_message(message: Dict) -> bool:
        return all(
            field in message
            for field in ('sku', 'seller_id', 'action')
        )

    def _get_strategy_for_item(self, product_matching_strategy: str):
        strategy = self.strategy or (
            product_matching_strategy or
            settings.DEFAULT_MATCHING_STRATEGY
        )

        module_name = settings.STRATEGIES[strategy]
        module = importlib.import_module(module_name)

        for submodule in ['assembler', 'matcher']:
            importlib.import_module(f'{module_name}.{submodule}')

        return module


class MatchingConsumer(PubSubBroker):
    scope = SCOPE
    record_processor_class = MatchingRecordProcessor
    project_name = settings.GOOGLE_PROJECT_ID
    subscription_name = settings.PUBSUB_MATCHING_PRODUCT_SUB_NAME
