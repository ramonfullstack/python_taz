import logging
from functools import cached_property
from typing import Dict, Optional, Tuple

from slugify import slugify

from taz.constants import (
    CREATE_ACTION,
    MAGAZINE_LUIZA_SELLER_ID,
    SOURCE_DATASHEET,
    SOURCE_GENERIC_CONTENT,
    SOURCE_OMNILOGIC,
    GenericContentName
)
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.core.notification.acme_notification import AcmeNotificationSender
from taz.core.storage.factsheet_storage import FactsheetStorage
from taz.helpers.json import json_dumps

logger = logging.getLogger(__name__)


class FactsheetMerger(MongodbMixin):

    def __init__(self):
        self.display_name = 'Informações complementares'
        self.slug = slugify('{}-magazineluiza'.format(self.display_name))

    @cached_property
    def factsheet_storage(self):
        return FactsheetStorage()

    @cached_property
    def acme_notification(self):
        return AcmeNotificationSender()

    @cached_property
    def enriched_products(self):
        return self.get_collection('enriched_products')

    def merge(
        self,
        sku: str,
        seller_id: str,
        factsheet: Dict = None
    ):
        logger.debug(
            'Factsheet Merger received to merge '
            f'sku:{sku} seller_id:{seller_id}'
        )

        should_process, enriched_product = self.validate_if_should_process(
            sku=sku,
            seller_id=seller_id
        )

        if not should_process:
            return

        factsheet_exists = factsheet is not None
        if not factsheet_exists:
            factsheet = self._get_factsheet(sku, seller_id)

        self._add_metadata_to_factsheet(factsheet, enriched_product)

        if not factsheet_exists:
            self.factsheet_storage.upload_bucket_data(
                sku=sku,
                seller_id=seller_id,
                payload=json_dumps(factsheet, ensure_ascii=False)
            )

            self.acme_notification.send_factsheet(
                CREATE_ACTION,
                seller_id,
                sku,
                factsheet
            )

    def _add_metadata_to_factsheet(
        self,
        factsheet: Dict,
        enriched_product_indexed: Dict
    ) -> None:
        if 'items' not in factsheet:
            factsheet['items'] = []

        enriched_product = enriched_product_indexed.get(SOURCE_OMNILOGIC) or {}
        specifications = self._get_technical_specification_from_metadata(
            enriched_product
        )
        specifications.update(
            self._get_technical_specification_from_generic_content(
                enriched_product_indexed.get(SOURCE_GENERIC_CONTENT) or {}
            )
        )
        elements = []
        for i, key in enumerate(sorted(specifications.keys()), start=1):
            value = specifications.get(key)
            value = value if not isinstance(value, list) else ', '.join(value)
            elements.append(
                dict(
                    key_name=key,
                    slug=slugify(key),
                    position=i,
                    value=value,
                    is_html=False
                )
            )

        technical_info = dict(
            slug=self.slug,
            position=1,
            key_name=self.display_name,
            elements=elements
        )

        data_sheet = self._get_data_sheet(factsheet)
        self._remove_technical_info(data_sheet)

        if elements:
            data_sheet['elements'].append(technical_info)

        self._remove_data_sheet(factsheet)
        factsheet['items'].append(data_sheet)

    @staticmethod
    def _get_technical_specification_from_metadata(
        enriched_product: Dict
    ) -> Dict:
        metadata = enriched_product.get('metadata') or {}
        technical_specification_attributes_name = enriched_product.get(
            'technical_specification'
        ) or []

        attributes = {
            name: metadata.get(name)
            for name in technical_specification_attributes_name
            if metadata.get(name)
        }

        return attributes or metadata

    @staticmethod
    def _get_technical_specification_from_generic_content(
        enriched_product: Dict
    ) -> Dict:
        attributes: Dict = {}
        navigation_id: str = enriched_product.get('navigation_id')
        if enriched_product.get('active', True):
            for key, value in enriched_product.get('metadata', {}).items():
                try:
                    attributes[GenericContentName[key].value] = value
                except KeyError as error:
                    logger.exception(
                        'Failed include {key}:{value} on product with '
                        'sku:{sku} seller_id:{seller_id} '
                        'navigation_id:{navigation_id} error:{error}'.format(
                            key=key,
                            value=value,
                            seller_id=enriched_product['seller_id'],
                            sku=enriched_product['sku'],
                            navigation_id=navigation_id,
                            error=error
                        )
                    )

        return attributes

    @staticmethod
    def _get_data_sheet(factsheet: Dict) -> Dict:
        data_sheet = None
        for factsheet_item in factsheet['items']:
            if factsheet_item['slug'] == 'ficha-tecnica':
                data_sheet = factsheet_item
        if not data_sheet:
            data_sheet = dict(
                display_name='Ficha Técnica',
                slug='ficha-tecnica',
                position=len(factsheet['items']) + 1,
                elements=[]
            )
        return data_sheet

    def _remove_technical_info(self, data_sheet: Dict) -> None:
        index = None
        for i, element in enumerate(data_sheet['elements']):
            if element.get('slug') == self.slug:
                index = i

        if index is not None:
            del data_sheet['elements'][index]

    @staticmethod
    def _remove_data_sheet(factsheet: Dict) -> None:
        index = None
        for i, item in enumerate(factsheet['items']):
            if item.get('slug') == 'ficha-tecnica':
                index = i

        if index is not None:
            del factsheet['items'][index]

    def _get_factsheet(self, sku: str, seller_id: str) -> Dict:
        try:
            return self.factsheet_storage.get_bucket_data(
                sku=sku,
                seller_id=seller_id
            ) or dict(items=[])

        except Exception as e:
            logger.debug(
                'An error occurred to get the factsheet with '
                f'sku:{sku} seller_id:{seller_id} error:{e}'
            )
            return dict(items=[])

    def _get_enriched_products(
        self,
        sku: str,
        seller_id: str
    ) -> Optional[Dict]:
        enriched_products = list(
            self.enriched_products.find(
                {
                    'sku': sku,
                    'seller_id': seller_id,
                    'source': {
                        '$in': [
                            SOURCE_OMNILOGIC,
                            SOURCE_DATASHEET,
                            SOURCE_GENERIC_CONTENT
                        ]
                    }
                },
                {'_id': 0}
            )
        )
        return {enriched['source']: enriched for enriched in enriched_products}

    def validate_if_should_process(
        self,
        sku: str,
        seller_id: str
    ) -> Tuple[bool, Optional[Dict]]:
        if seller_id == MAGAZINE_LUIZA_SELLER_ID:
            logger.debug(
                'Factsheet merge disabled for '
                f'sku:{sku} seller_id:{seller_id}'
            )
            return False, None

        enriched_products = self._get_enriched_products(
            sku=sku,
            seller_id=seller_id
        )

        if not enriched_products or (
            SOURCE_OMNILOGIC not in enriched_products and
            SOURCE_GENERIC_CONTENT not in enriched_products
        ):
            logger.info(
                'Product dont have enriched product '
                f'sku:{sku} seller_id:{seller_id}'
            )
            return False, None

        if SOURCE_DATASHEET in enriched_products:
            logger.info(
                f'Ignore product with sku:{sku} seller_id:{seller_id} '
                f'because it has {SOURCE_DATASHEET} on enriched products'
            )
            return False, None

        return True, enriched_products
