from functools import cached_property
from time import perf_counter
from typing import Dict, Optional

from maaslogger import base_logger
from simple_settings import settings

from taz.constants import (
    ENRICHED_PRODUCT_ORIGIN,
    SOURCE_OMNILOGIC,
    UPDATE_ACTION
)
from taz.consumers.core.brokers.stream import (
    PubSubBroker,
    PubSubRecordProcessor
)
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.notification import Notification
from taz.helpers.json import strip_decimals
from taz.utils import decode_body, md5

SCOPE = 'enriched_product'

logger = base_logger.get_logger(__name__)


class EnrichedProductProcessor(MongodbMixin, PubSubRecordProcessor):
    scope = SCOPE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @cached_property
    def raw_products(self):
        return self.get_collection('raw_products')

    @cached_property
    def enriched_products(self):
        return self.get_collection('enriched_products')

    @cached_property
    def notification(self):
        return Notification()

    def get_metadata(self, source: str, identifier: str) -> Optional[dict]:
        file_name = f'{source}/{identifier}.json'
        return self.data_storage.get_json(file_name)

    def process_message(self, message: Dict) -> bool:
        elapsed_time = perf_counter()
        sku = message['sku']
        seller_id = message['seller_id']
        navigation_id = message['navigation_id']
        source = message['source']

        logger.info(
            f'Request enriched product sku:{sku} seller_id:{seller_id} '
            f'navigation_id:{navigation_id} source:{source}',
            detail={
                "sku": sku,
                "seller_id": seller_id,
                "navigation_id": navigation_id,
                "source": source
            }
        )

        message.update(decode_body(strip_decimals(message)))

        raw_product = self._get_product_data(
            sku=sku,
            seller_id=seller_id,
            navigation_id=navigation_id
        )

        if not raw_product:
            logger.warning(
                f'Product not found sku:{sku} seller_id:{seller_id} '
                f'navigation_id:{navigation_id}',
                detail={
                    "sku": sku,
                    "seller_id": seller_id,
                    "navigation_id": navigation_id,
                }
            )
            return True

        self._format_product_hash(
            message=message,
            sku=raw_product['sku'],
            seller_id=raw_product['seller_id'],
            navigation_id=raw_product['navigation_id'],
            parent_sku=raw_product['parent_sku']
        )
        new_md5 = md5(message)

        enriched_product = self.enriched_products.find_one(
            {'sku': sku, 'seller_id': seller_id, 'source': source},
            {'md5': 1, '_id': 0}
        ) or {}

        old_md5 = enriched_product.get('md5')

        if old_md5 == new_md5:
            logger.info(
                f'Skip enriched product update for sku:{sku} '
                f'seller_id:{seller_id} navigation_id:{navigation_id} '
                f'source:{source} income payload:{message} '
                f'database md5:{old_md5} income md5:{new_md5}',
                detail={
                    "sku": sku,
                    "seller_id": seller_id,
                    "navigation_id": navigation_id,
                    "source": source,
                    "old_md5": old_md5,
                    "new_md5": new_md5
                }
            )
            return True

        try:
            message.update(md5=new_md5)
            self.enriched_products.update(
                {'sku': sku, 'seller_id': seller_id, 'source': source},
                message,
                upsert=True
            )
        except Exception as e:
            logger.error(
                f'Could not save enriched product sku:{sku} '
                f'seller_id:{seller_id} navigation_id:{navigation_id} '
                f'source:{source} error:{e}',
                detail={
                    "sku": sku,
                    "seller_id": seller_id,
                    "navigation_id": navigation_id,
                    "source": source,
                    "old_md5": old_md5,
                    "new_md5": new_md5
                }
            )
            return False

        self.catalog_notification(
            action=UPDATE_ACTION,
            sku=raw_product['sku'],
            seller_id=raw_product['seller_id'],
            navigation_id=raw_product['navigation_id'],
            source=source
        )

        elapsed_time = perf_counter() - elapsed_time
        logger.info(
            'Successfully created enriched product '
            f'sku:{sku} seller_id:{seller_id} navigation_id:{navigation_id} '
            f'source:{source} in {elapsed_time:.3f}s',
            detail={
                "sku": sku,
                "seller_id": seller_id,
                "navigation_id": navigation_id,
                "source": source
            }
        )

        return True

    def catalog_notification(
        self,
        action: str,
        seller_id: str,
        sku: str,
        navigation_id: str,
        source: str
    ) -> None:
        payload = {
            'sku': sku,
            'seller_id': seller_id,
            'navigation_id': navigation_id,
            'source': source
        }

        self.notification.put(
            data=payload,
            scope=self.scope,
            action=action,
            origin=ENRICHED_PRODUCT_ORIGIN
        )

        logger.info(
            f'Send enriched product notification for sku:{sku} '
            f'seller_id:{seller_id} navigation_id:{navigation_id} '
            f'scope:{self.scope} action:{action}',
            detail={
                "sku": sku,
                "seller_id": seller_id,
                "navigation_id": navigation_id,
                "action": action
            }
        )

    @staticmethod
    def _format_product_hash(
        message: Dict,
        sku: str,
        seller_id: str,
        navigation_id: str,
        parent_sku: str
    ) -> None:
        if (
            message.get('source') == SOURCE_OMNILOGIC and
            not message.get('product_hash')
        ):
            product_hash = md5({
                'seller_id': seller_id,
                'parent_sku': parent_sku
            })

            message.update(product_hash=product_hash)

            logger.debug(
                f'product_hash generated:{product_hash} sku:{sku} '
                f'seller_id:{seller_id} navigation_id:{navigation_id}',
                detail={
                    "sku": sku,
                    "seller_id": seller_id,
                    "navigation_id": navigation_id,
                }
            )

    def _get_product_data(
        self,
        sku: str,
        seller_id: str,
        navigation_id: str
    ) -> Optional[Dict]:
        fields = {
            '_id': 0,
            'sku': 1,
            'seller_id': 1,
            'navigation_id': 1,
            'parent_sku': 1
        }

        raw_product = self.raw_products.find_one(
            {'sku': sku, 'seller_id': seller_id},
            fields
        )

        if not raw_product:
            raw_product = self.raw_products.find_one(
                {'navigation_id': navigation_id},
                fields
            )

            if not raw_product:
                logger.warning(
                    f'Product sku:{sku} seller_id:{seller_id} '
                    f'navigation_id:{navigation_id} not found '
                    'in raw_products',
                    detail={
                        "sku": sku,
                        "seller_id": seller_id,
                        "navigation_id": navigation_id,
                    }
                )

        return raw_product


class EnrichedProductConsumer(PubSubBroker):
    scope = SCOPE
    record_processor_class = EnrichedProductProcessor
    project_name = settings.GOOGLE_PROJECT_ID
    subscription_name = settings.PUBSUB_NOTIFICATION_SUB_NAME
