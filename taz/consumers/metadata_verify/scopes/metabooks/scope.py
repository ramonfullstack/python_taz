import logging
from functools import cached_property
from typing import Optional, Tuple

from simple_settings import settings

from taz.constants import SOURCE_METABOOKS
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.exceptions import NotFound
from taz.consumers.metadata_verify.scopes.base import BaseScope
from taz.consumers.metadata_verify.scopes.metabooks.helpers import (
    create_enriched_product_payload,
    create_factsheet_payload,
    create_media_payload,
    get_subject_codes
)
from taz.utils import get_identifier

logger = logging.getLogger(__name__)


class Scope(MongodbMixin, BaseScope):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @cached_property
    def enriched_products(self):
        return self.get_collection('enriched_products')

    @cached_property
    def metabooks_categories(self):
        return self.get_collection('metabooks_categories')

    def is_allowed(self, product: dict) -> Tuple[bool, str]:
        identifier = get_identifier(product)
        return identifier is not None and identifier != '', identifier

    def _process(
        self,
        identifier: str,
        sku: str,
        seller_id: str,
        navigation_id: str
    ) -> Optional[dict]:
        try:
            metadata = self.get_metadata(SOURCE_METABOOKS, identifier)
        except NotFound:
            self.__remove_old_metabooks_enrichment(sku, seller_id)
            raise

        try:
            media_payload = self.get_media(SOURCE_METABOOKS, identifier)
        except NotFound:
            media_payload = None

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
            media_payload=media_payload
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
            sku,
            seller_id,
            navigation_id,
            metadata
        )

        self.__category_process(sku, seller_id, metadata, payload)

        logger.debug(
            f'Create enriched products payload from sku:{sku} '
            f'seller_id:{seller_id} navigation_id:{navigation_id} '
            f'payload:{payload}'
        )

        criteria = {
            'sku': sku,
            'seller_id': seller_id,
            'source': SOURCE_METABOOKS
        }
        self.enriched_products.update_one(
            criteria,
            {'$set': payload},
            upsert=True
        )

        logger.info(
            f'Enriched product sku:{sku} seller_id:{seller_id} '
            f'navigation_id:{navigation_id} source:{SOURCE_METABOOKS} '
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
        if not media_payload:
            logger.warning(
                f'Media not found for sku:{sku} seller_id:{seller_id} '
                f'navigation_id:{navigation_id}'
            )
            return None

        media = create_media_payload(sku, seller_id, media_payload)
        logger.debug(
            f'Create media payload from sku:{sku} seller_id:{seller_id} '
            f'navigation_id:{navigation_id} payload:{media}'
        )
        return media

    def __category_process(
        self,
        sku: str,
        seller_id: str,
        metadata: dict,
        enriched_product: dict
    ) -> None:
        codes = get_subject_codes(metadata)

        category_id = None
        subcategory_ids = []
        for code in codes:
            response = self.metabooks_categories.find_one({
                'metabook_id': code
            })

            if not response:
                logger.warning(
                    f'Metabooks categories not found for code:{code} '
                    f'sku:{sku} seller_id:{seller_id}'
                )
                continue

            category_id = response['category_id']

            for subcategory_id in response['subcategory_ids']:
                if subcategory_id in subcategory_ids:
                    continue

                subcategory_ids.append(subcategory_id)

        if not category_id:
            category_id = settings.FALLBACK_MISSING_CATEGORY
            subcategory_ids = [
                settings.FALLBACK_MISSING_SUBCATEGORY
            ]
            logger.warning(
                f'category not found for sku:{sku} '
                f'seller_id:{seller_id} source:metabooks codes:{codes}'
            )

        enriched_product['category_id'] = category_id
        enriched_product['subcategory_ids'] = subcategory_ids

        logger.debug(
            f'Applying categorization to sku:{sku} seller_id:{seller_id} '
            f'codes:{codes} category_id:{category_id} '
            f'subcategory_ids:{subcategory_ids}'
        )

    def __remove_old_metabooks_enrichment(
        self,
        sku: str,
        seller_id: str
    ) -> None:
        try:
            criteria = {
                'sku': sku,
                'seller_id': seller_id,
                'source': SOURCE_METABOOKS
            }
            self.enriched_products.delete_one(criteria)
        except Exception as e:
            raise Exception(
                f'Error for delete metabooks enrichment for sku:{sku} '
                f'seller_id:{seller_id} error:{e}'
            )
