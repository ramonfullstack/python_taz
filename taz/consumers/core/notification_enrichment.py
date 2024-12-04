from functools import cached_property
from typing import Dict, List, Optional

from maaslogger import base_logger
from simple_settings import settings

from taz.constants import SOURCE_OMNILOGIC, EnrichmentEventType
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.google.stream import StreamPublisherManager
from taz.consumers.product_exporter.helpers import _generate_factsheet_url
from taz.core.common.media import _build_images
from taz.utils import generate_uuid, get_identifier

logger = base_logger.get_logger(__name__)


class NotificationEnrichment(MongodbMixin):

    @cached_property
    def enriched_products(self):
        return self.get_collection('enriched_products')

    @cached_property
    def medias(self):
        return self.get_collection('medias')

    @cached_property
    def pubsub(self):
        return StreamPublisherManager()

    def notify(
        self,
        product: Dict,
        attributes: Dict = None,
        trace_id: Optional[str] = None
    ) -> None:
        title = product.get('title')
        identifier = get_identifier(product)
        seller_id = product['seller_id']
        sku = product['sku']
        navigation_id = product['navigation_id']

        try:
            attributes = attributes or {}
            event_type = attributes.get('event_type')
            event_type = EnrichmentEventType(event_type).value
        except (KeyError, ValueError):
            logger.error(
                f'Failed send product with sku:{sku} seller_id:{seller_id} '
                f'navigation_id:{navigation_id} to '
                f'{settings.PRODUCT_METADATA_TOPIC_NAME} invalid '
                f'attribute event_type:{event_type}'
            )
            return

        product_type = self._find_product_type(product)
        if self._is_enabled_notify(product_type, title):
            medias = _build_images(product, self.medias)
            if not medias:
                logger.warning(
                    f'Images not found for product sku:{sku} '
                    f'seller_id:{seller_id} navigation_id:{navigation_id}'
                )

            content = self.__format_product_metadata_payload(
                product,
                medias,
                product_type,
                trace_id
            )

            result_trace_id: str = content.get('trace_id')
            self.pubsub.publish(
                content=content,
                topic_name=settings.PRODUCT_METADATA_TOPIC_NAME,
                project_id=settings.GOOGLE_PROJECT_ID,
                attributes=attributes,
            )
            logger.info(
                f'Product with sku:{sku} seller_id:{seller_id} '
                f'navigation_id:{navigation_id} identifier:{identifier} '
                f'sent to {settings.PRODUCT_METADATA_TOPIC_NAME} '
                f'event_type:{event_type} trace_id:{result_trace_id}'
            )

    def _find_product_type(self, product: Dict) -> Optional[str]:
        entity = self.enriched_products.find_one({
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'source': SOURCE_OMNILOGIC
        }, {'entity': 1, '_id': 0}) or {}

        return entity.get('entity')

    def __format_product_metadata_payload(
        self,
        product: Dict,
        media: List,
        product_type: str,
        trace_id: Optional[str]
    ) -> Dict:
        payload = {
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'navigation_id': product['navigation_id'],
            'identifiers': self.__format_identifiers(product),
            'parent_sku': product['parent_sku'],
            'metadata': {
                'title': product['title'],
                'description': product.get('description'),
                'factsheet': _generate_factsheet_url(
                    product['sku'],
                    product['seller_id']
                ),
                'medias': media,
                'product_type': product_type
            },
            'trace_id': trace_id or generate_uuid()
        }

        logger.debug(
            'Payload for product_metadata sku:{sku} seller_id:{seller_id} '
            'navigation_id:{navigation_id} topic:{topic} '
            'payload:{payload}'.format(
                sku=product['sku'],
                seller_id=product['seller_id'],
                navigation_id=product['navigation_id'],
                topic=settings.PRODUCT_METADATA_TOPIC_NAME,
                payload=payload
            )
        )

        return payload

    def __format_identifiers(self, product: Dict) -> List[Dict]:
        return [
            {'type': identifier, 'value': product[identifier]}
            for identifier in ['isbn', 'ean']
            if product.get(identifier)
        ]

    def _is_enabled_notify(self, product_type: str, title: str) -> bool:
        if (
            title is None or
            title == '' or
            (
                '*' not in settings.ALLOW_PUBLISH_PRODUCT_METADATA and
                product_type not in settings.ALLOW_PUBLISH_PRODUCT_METADATA
            )
        ):
            return False

        return True
