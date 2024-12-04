from functools import cached_property
from time import perf_counter
from typing import Dict, List, Optional, Tuple

from maaslogger import base_logger
from simple_settings import settings

from taz.constants import (
    CREATE_ACTION,
    MAGAZINE_LUIZA_SELLER_ID,
    SOURCE_DATASHEET,
    SOURCE_METABOOKS,
    SOURCE_METADATA_VERIFY,
    SOURCE_SMARTCONTENT,
    UPDATE_ACTION,
    EnrichmentEventType
)
from taz.consumers.core.brokers.stream import (
    PubSubBroker,
    PubSubRecordProcessor
)
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.exceptions import InvalidScope
from taz.consumers.core.frajola import FrajolaRequest
from taz.consumers.core.google.stream import StreamPublisherManager
from taz.consumers.core.notification import Notification
from taz.consumers.core.notification_enrichment import NotificationEnrichment
from taz.consumers.metadata_verify import SCOPE
from taz.consumers.metadata_verify.scopes.base import BaseScope
from taz.consumers.metadata_verify.scopes.datasheet.scope import (
    Scope as DatasheetScope
)
from taz.consumers.metadata_verify.scopes.metabooks.scope import (
    Scope as MetabooksScope
)
from taz.consumers.metadata_verify.scopes.smartcontent.scope import (
    Scope as SmartContentScope
)
from taz.core.merge.merger import Merger
from taz.utils import get_identifier

logger = base_logger.get_logger(__name__)


class MetadataVerifyProcessor(PubSubRecordProcessor, MongodbMixin):
    max_process_workers = settings.METADATA_VERIFY_PROCESS_WORKERS
    scope = SCOPE
    disable_cache_lock = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SCOPES = {
            SOURCE_METABOOKS: MetabooksScope(),
            SOURCE_DATASHEET: DatasheetScope(),
            SOURCE_SMARTCONTENT: SmartContentScope()
        }

    @cached_property
    def raw_products(self):
        return self.get_collection('raw_products')

    @cached_property
    def pubsub(self):
        return StreamPublisherManager()

    @cached_property
    def frajola_request(self):
        return FrajolaRequest()

    @cached_property
    def notification(self):
        return Notification()

    @cached_property
    def notification_enrichment(self):
        return NotificationEnrichment()

    def process_message(self, message: dict) -> bool:
        elapsed_time = perf_counter()
        sku = message.get('sku')
        seller_id = message.get('seller_id')
        action = message.get('action', CREATE_ACTION)
        tracking_id = message.get('tracking_id')

        if not sku or not seller_id:
            logger.warning(f'Invalid message with payload:{message}')
            return True

        product = self.raw_products.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0}
        )

        if not product:
            logger.warning(
                f'Product sku:{sku} seller_id:{seller_id} not found'
            )
            return True

        navigation_id = product['navigation_id']
        identifier = get_identifier(product)

        scopes = self._get_scopes(product)
        payload_info = {}
        if scopes:
            payload_info = self._evaluate_scopes(
                sku,
                seller_id,
                navigation_id,
                product,
                scopes
            )

            self._put_factsheet(
                sku=sku,
                seller_id=seller_id,
                navigation_id=navigation_id,
                payload=payload_info.get('factsheet')
            )

            self._put_media(
                sku=sku,
                seller_id=seller_id,
                navigation_id=navigation_id,
                payload=payload_info.get('media')
            )

        self._execute_merger(
            product,
            payload_info.get('enriched_product'),
            action
        )

        self._send_notification(
            product=product,
            sku=sku,
            seller_id=seller_id,
            navigation_id=navigation_id,
            tracking_id=tracking_id
        )

        elapsed_time = perf_counter() - elapsed_time
        logger.info(
            f'Successfully processed sku:{sku} seller_id:{seller_id} '
            f'navigation_id:{navigation_id} identifier:{identifier} '
            f'in {elapsed_time:.3f}s'
        )

        return True

    def _put_factsheet(
        self,
        sku: str,
        seller_id: str,
        navigation_id: str,
        payload: dict
    ) -> None:
        if not payload:
            return

        payload.update({'source': SOURCE_METADATA_VERIFY})
        message = {
            'action': CREATE_ACTION,
            'data': payload
        }
        self.pubsub.publish(
            content=message,
            topic_name=settings.PUBSUB_FACTSHEET_TOPIC_NAME,
            project_id=settings.GOOGLE_PROJECT_ID,
        )
        logger.info(
            f'Factsheet sku:{sku} seller_id:{seller_id} '
            f'navigation_id:{navigation_id} sent to the stream successfully'
        )

    def _put_media(
        self,
        sku: str,
        seller_id: str,
        navigation_id: str,
        payload: dict
    ) -> None:
        if not payload:
            return

        payload.update({'source': SOURCE_METADATA_VERIFY})
        message = {
            'action': CREATE_ACTION,
            'data': payload
        }
        self.pubsub.publish(
            topic_name=settings.PUBSUB_MEDIA_TOPIC_NAME,
            project_id=settings.GOOGLE_PROJECT_ID,
            content=message
        )
        logger.info(
            f'Media sku:{sku} seller_id:{seller_id} '
            f'navigation_id:{navigation_id} sent to the '
            f'pubsub stream successfully'
        )

    def _frajola_process(
        self,
        sku: str,
        seller_id: str,
        navigation_id: str,
        product: dict
    ):
        if seller_id != MAGAZINE_LUIZA_SELLER_ID:
            return

        category_id = product['categories'][0]['id']
        subcategory_id = product['categories'][0]['subcategories'][0]['id']

        payload = {
            'category_id': category_id,
            'subcategory_id': subcategory_id,
            'title': product['title'],
            'reference': product.get('reference') or '',
            'brand': product['brand'],
            'active': True
        }

        self.frajola_request.put(sku[:7], payload)

        logger.info(
            f'Send to Frajola with sku:{sku} seller_id:{seller_id} '
            f'navigation_id:{navigation_id} payload:{payload}'
        )

    def _get_scopes(
        self,
        product: dict
    ) -> List[Tuple[str, str]]:
        scopes = []
        for source in [
            SOURCE_METABOOKS,
            SOURCE_SMARTCONTENT,
            SOURCE_DATASHEET
        ]:
            is_allowed, identifier = self._get_scope(
                source
            ).is_allowed(product)
            if is_allowed:
                scopes.append((source, identifier))
        return scopes

    def _get_scope(
        self,
        scope_name: str
    ) -> BaseScope:
        try:
            return self.SCOPES[scope_name]
        except Exception:
            raise InvalidScope(scope_name=scope_name)

    def _evaluate_scopes(
        self,
        sku: str,
        seller_id: str,
        navigation_id: str,
        product: dict,
        scopes: list
    ) -> dict:
        media = {}
        factsheet = {}
        enriched_product = {}
        for scope_name, identifier in scopes:
            scope = self._get_scope(scope_name)
            payload = scope.process(identifier, product)

            if not payload:
                continue

            if (
                scope_name in settings.SCOPES_ALLOWED_SEND_IMAGES_TO_MEDIA and
                payload['media']
            ):
                media = payload['media']

            factsheet = payload['factsheet']
            enriched_product = payload['enriched_product']

            logger.info(
                f'Successfully processed identifier:{identifier} '
                f'source:{scope_name} for sku:{sku} seller_id:{seller_id} '
                f'navigation_id:{navigation_id}'
            )

            if (
                product['categories'][0]['id'] == 'TM' and
                scope_name == SOURCE_METABOOKS
            ):
                self._frajola_process(
                    sku=sku,
                    seller_id=seller_id,
                    navigation_id=navigation_id,
                    product=product
                )

        return {
            'media': media,
            'factsheet': factsheet,
            'enriched_product': enriched_product,
        }

    def _send_notification(
        self,
        product: Dict,
        sku: str,
        seller_id: str,
        navigation_id: str,
        tracking_id: str = None
    ) -> None:
        self.notification_enrichment.notify(
            product=product,
            attributes={'event_type': EnrichmentEventType.ALL.value},
            trace_id=tracking_id
        )

        self.notification.put(
            data={
                'sku': sku,
                'seller_id': seller_id,
                'navigation_id': navigation_id,
                'tracking_id': tracking_id
            },
            scope=self.scope,
            action=UPDATE_ACTION
        )

    def _execute_merger(
        self,
        raw_product: Dict,
        enriched_product: Optional[Dict],
        action: str
    ) -> None:
        try:
            Merger(
                raw_product=raw_product,
                enriched_product=enriched_product,
                action=action
            ).merge()
        except Exception as e:
            logger.exception(
                'An error occurred merging data for sku:{sku} '
                'seller_id:{seller_id} navigation_id:{navigation_id} '
                'with action:{action}, error:{error}'.format(
                    sku=raw_product['sku'],
                    seller_id=raw_product['seller_id'],
                    navigation_id=raw_product['navigation_id'],
                    action=action,
                    error=e
                )
            )
            raise


class MetadataVerifyConsumer(PubSubBroker):
    scope = SCOPE
    record_processor_class = MetadataVerifyProcessor
    project_name = settings.GOOGLE_PROJECT_ID
