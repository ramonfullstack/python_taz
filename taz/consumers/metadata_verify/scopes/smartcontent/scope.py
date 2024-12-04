import logging
from functools import cached_property
from typing import Optional, Tuple

from simple_settings import settings

from taz.constants import SOURCE_SMARTCONTENT
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.metadata_verify.scopes.base import BaseScope
from taz.consumers.metadata_verify.scopes.smartcontent.helpers import (
    create_enriched_product_payload,
    create_factsheet_payload,
    create_media_payload
)
from taz.utils import get_identifier

logger = logging.getLogger(__name__)


class Scope(MongodbMixin, BaseScope):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @cached_property
    def enriched_products(self):
        return self.get_collection('enriched_products')

    @staticmethod
    def get_category(product):
        category_id = settings.FALLBACK_MISSING_CATEGORY
        sku, seller_id, navigation_id = (
            product['sku'],
            product['seller_id'],
            product['navigation_id']
        )
        try:
            category_id = (
                product['categories'][0]['id']
            ) or settings.FALLBACK_MISSING_CATEGORY
        except Exception as e:
            logger.warning(
                f'Cannot find category sku:{sku} seller_id:{seller_id} '
                f' navigation_id:{navigation_id} error:{e}'
            )

        return category_id

    def is_allowed(self, product: dict) -> Tuple[bool, str]:
        seller_id = product['seller_id']
        category_id = Scope.get_category(product)
        identifier = get_identifier(product)
        allowed = (
            category_id in settings.ALLOWED_SMARTCONTENT_CATEGORY or
            '*' in settings.ALLOWED_SMARTCONTENT_CATEGORY
        ) and (
            seller_id in settings.ALLOWED_SMARTCONTENT_SELLER or
            '*' in settings.ALLOWED_SMARTCONTENT_SELLER or
            category_id in settings.CATEGORY_DISABLE_SMARTCONTENT_VERIFY_SELLER or  # noqa
            '*' in settings.CATEGORY_DISABLE_SMARTCONTENT_VERIFY_SELLER
        ) and (
            identifier is not None and identifier != ''
        )
        return (allowed, identifier)

    def _process(
        self,
        identifier: str,
        sku: str,
        seller_id: str,
        navigation_id: str
    ) -> Optional[dict]:
        metadata = self.get_metadata(SOURCE_SMARTCONTENT, identifier)

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

        logger.debug(
            f'Create enriched products payload from sku:{sku} '
            f'seller_id:{seller_id} navigation_id:{navigation_id} '
            f'payload:{payload}'
        )

        criteria = {
            'sku': sku,
            'seller_id': seller_id,
            'source': SOURCE_SMARTCONTENT
        }
        self.enriched_products.update_one(
            criteria,
            {'$set': payload},
            upsert=True
        )

        logger.info(
            f'Enriched product sku:{sku} seller_id:{seller_id} '
            f'navigation_id:{navigation_id} source:{SOURCE_SMARTCONTENT} '
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
        media = create_media_payload(
            sku=sku,
            seller_id=seller_id,
            metadata=media_payload
        )

        logger.debug(
            f'Create media payload from sku:{sku} seller_id:{seller_id} '
            f'navigation_id:{navigation_id} payload:{media}'
        )

        return media
