import logging
from functools import cached_property
from typing import Optional, Tuple

from taz.constants import SOURCE_DATASHEET
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.exceptions import NotFound
from taz.consumers.metadata_verify.scopes.base import BaseScope
from taz.consumers.metadata_verify.scopes.smartcontent.helpers import (
    create_enriched_product_payload,
    create_factsheet_payload
)

logger = logging.getLogger(__name__)


class Scope(MongodbMixin, BaseScope):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @cached_property
    def enriched_products(self):
        return self.get_collection('enriched_products')

    def is_allowed(self, product: dict) -> Tuple[bool, str]:
        enriched_product = self.enriched_products.find_one(
            {
                'seller_id': product['seller_id'],
                'sku': product['sku'],
                'source': SOURCE_DATASHEET
            },
            {'_id': 0, 'identifier': 1}
        ) or {}
        identifier = enriched_product.get('identifier')
        return identifier is not None, identifier

    def _process(
        self,
        identifier: str,
        sku: str,
        seller_id: str,
        navigation_id: str
    ) -> Optional[dict]:
        metadata = self.get_metadata(SOURCE_DATASHEET, identifier)

        factsheet = self._factsheet_process(
            sku=sku,
            seller_id=seller_id,
            navigation_id=navigation_id,
            metadata=metadata
        )

        media = self._media_process(
            sku=sku,
            seller_id=seller_id,
            navigation_id=navigation_id,
            media_payload=metadata
        )

        enriched_product = self._enriched_product_process(
            sku=sku,
            seller_id=seller_id,
            navigation_id=navigation_id,
            metadata=metadata
        )

        return {
            'factsheet': factsheet,
            'media': media,
            'enriched_product': enriched_product
        }

    def _factsheet_process(
        self,
        sku: str,
        seller_id: str,
        navigation_id: str,
        metadata: dict
    ) -> Optional[dict]:
        factsheet = create_factsheet_payload(
            sku=sku,
            seller_id=seller_id,
            metadata=metadata
        )

        logger.debug(
            f'Create factsheet payload from sku:{sku} '
            f'seller_id:{seller_id} navigation_id:{navigation_id} '
            f'payload:{factsheet}'
        )

        return factsheet

    def _enriched_product_process(
        self,
        sku: str,
        seller_id: str,
        navigation_id: str,
        metadata: dict
    ) -> dict:
        payload = create_enriched_product_payload(
            sku=sku,
            seller_id=seller_id,
            navigation_id=navigation_id,
            metadata=metadata
        )

        payload.update({'source': SOURCE_DATASHEET})

        logger.debug(
            f'Create enriched products payload from sku:{sku} '
            f'seller_id:{seller_id} navigation_id:{navigation_id} '
            f'payload:{payload}'
        )

        criteria = {
            'sku': sku,
            'seller_id': seller_id,
            'source': SOURCE_DATASHEET
        }
        result = self.enriched_products.update_one(criteria, {'$set': payload})
        if result.matched_count == 0:
            raise NotFound('Datasheet is not linked')

        logger.info(
            f'Enriched product sku:{sku} seller_id:{seller_id} '
            f'navigation_id:{navigation_id} source:{SOURCE_DATASHEET} '
            'successfully saved in database'
        )

        return payload

    def _media_process(
        self,
        sku: str,
        seller_id: str,
        navigation_id: str,
        media_payload: dict
    ) -> Optional[dict]:
        logger.debug(
            f'Media disabled for sku:{sku} seller_id:{seller_id} '
            f'navigation_id:{navigation_id}'
        )
        return None
