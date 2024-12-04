import datetime
import re
from collections.abc import Sequence
from functools import cached_property
from typing import Dict, List, Optional, Tuple

import bleach
from maaslogger import base_logger
from simple_settings import settings

from taz.constants import (
    CREATE_ACTION,
    DELETE_ACTION,
    FACTSHEET_SKIP_MESSAGE,
    FACTSHEET_UNFINISHED_PROCESS,
    MAGAZINE_LUIZA_SELLER_ID,
    NOT_SORTING_FACTSHEET,
    PRODUCT_PRESENTATION,
    SOURCE_DATASHEET,
    SOURCE_METADATA_VERIFY,
    UPDATE_ACTION
)
from taz.consumers.core.brokers.stream import (
    PubSubBroker,
    PubSubRecordProcessorWithRequiredFields
)
from taz.consumers.core.cache.redis import CacheMixin
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.google.stream import StreamPublisherManager
from taz.consumers.core.notification import Notification
from taz.core.forbidden_terms.forbidden_terms import ForbiddenTerms
from taz.core.merge.factsheet import FactsheetMerger
from taz.core.notification.acme_notification import AcmeNotificationSender
from taz.core.notification.notification_sender import NotificationSender
from taz.core.storage.factsheet_storage import FactsheetStorage
from taz.core.storage.raw_factsheet_storage import RawFactsheetStorage
from taz.helpers.json import json_dumps
from taz.utils import md5

logger = base_logger.get_logger(__name__)

CACHE_KEY = 'factsheet_invalidate_{sku}_{seller_id}'
CACHE_EXPIRES = 600
SCOPE = 'factsheet'


class FactsheetRecordProcessor(
    CacheMixin,
    PubSubRecordProcessorWithRequiredFields,
    MongodbMixin
):
    required_fields = ['seller_id', 'sku', 'items']
    required_fields_delete = ['seller_id', 'sku']
    bleach.ALLOWED_TAGS = settings.ALLOWED_HTML_TAGS.split(',')
    max_process_workers = settings.FACTSHEET_CONSUMER_MAX_WORKERS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @cached_property
    def pubsub(self):
        return StreamPublisherManager()

    @cached_property
    def notification_sender(self):
        return NotificationSender()

    @cached_property
    def notification(self):
        return Notification()

    @cached_property
    def factsheet_merger(self):
        return FactsheetMerger()

    @cached_property
    def factsheet_storage(self):
        return FactsheetStorage()

    @cached_property
    def acme_notification(self):
        return AcmeNotificationSender()

    @cached_property
    def forbidden_terms(self):
        return ForbiddenTerms()

    @cached_property
    def raw_factsheet_storage(self):
        return RawFactsheetStorage()

    @cached_property
    def raw_products(self):
        return self.get_collection('raw_products')

    @cached_property
    def enriched_products(self):
        return self.get_collection('enriched_products')

    @cached_property
    def factsheets(self):
        return self.get_collection('factsheets')

    def _create(self, data: Dict):
        self.__process_factsheet(CREATE_ACTION, data)

    def _update(self, data: Dict):
        self.__process_factsheet(UPDATE_ACTION, data)

    def _delete(self, data: Dict):
        seller_id = data['seller_id']
        sku = data['sku']
        navigation_id = self._get_navigation_id(sku, seller_id)
        send_to_datalake = True if navigation_id else False

        self.factsheet_storage.delete_bucket_data(
            sku=sku,
            seller_id=seller_id
        )

        self.raw_factsheet_storage.delete_bucket_data(
            sku=sku,
            seller_id=seller_id
        )

        self._notify(
            action=DELETE_ACTION,
            seller_id=seller_id,
            sku=sku,
            navigation_id=navigation_id,
            send_to_datalake=send_to_datalake
        )

    @classmethod
    def cache(cls):
        return cls.get_cache(cls)

    @staticmethod
    def _is_html(value: str) -> bool:
        regex_html = re.compile('<[^<]+?>')
        return bool(regex_html.search(value, re.MULTILINE))

    def _create_attribute(
        self,
        item: Dict
    ) -> None:
        if item.get('value'):
            item.update({
                'is_html': self._is_html(item['value'])
            })

    def _sort_elements(
        self,
        items: List,
        attribute_amount: int = 0
    ) -> [List, int]:  # type: ignore
        for item in items:
            self._create_attribute(item)

            if (
                item.get('value') and
                item.get('key_name') and
                item['key_name'] != PRODUCT_PRESENTATION
            ):
                attribute_amount += 1

            if 'elements' not in item:
                continue

            item['elements'], attribute_amount = self._sort_elements(sorted(
                item['elements'], key=lambda o: o.get(
                    'position', NOT_SORTING_FACTSHEET
                )
            ), attribute_amount)

        return sorted(
            items, key=lambda o: o.get('position', NOT_SORTING_FACTSHEET)
        ), attribute_amount

    def validate_factsheet_to_process(
        self,
        sku: str,
        seller_id: str,
        source: str
    ) -> Tuple[bool, bool]:
        criteria = {
            'sku': sku,
            'seller_id': seller_id,
            'source': {
                '$in': settings.SKIP_ENRICHED_SOURCES_WHEN_NOT_METADATA_VERIFY
            }
        }

        enriched_product = {
            enriched.get('source'): enriched
            for enriched in list(self.enriched_products.find(criteria))
        }

        enabled_process = (
            not enriched_product or
            source == SOURCE_METADATA_VERIFY
        )

        enabled_clean_html = (
            seller_id != MAGAZINE_LUIZA_SELLER_ID and
            enriched_product.get(SOURCE_DATASHEET) is None
        )

        return enabled_process, enabled_clean_html

    def _notify(
        self,
        action: str,
        seller_id: str,
        sku: str,
        navigation_id: str,
        send_to_datalake: bool = False
    ) -> None:
        self.pubsub.publish(
            content={
                'action': action,
                'seller_id': seller_id,
                'sku': sku,
                'origin': __name__
            },
            topic_name=settings.PUBSUB_COMPLETE_PRODUCT_TOPIC_NAME,
            project_id=settings.GOOGLE_PROJECT_ID
        )

        if send_to_datalake:
            logger.info(
                f'Send factsheet to datalake seller_id:{seller_id} '
                f'sku:{sku} navigation_id:{navigation_id} '
                f'action:{action}',
                detail={
                    "sku": sku,
                    "seller_id": seller_id,
                    "navigation_id": navigation_id,
                    "action": action
                }
            )

            data = {
                'seller_id': seller_id,
                'sku': sku,
                'navigation_id': navigation_id,
                'action': action
            }
            self.notification.put(data, self.scope, action)

        logger.info(
            f'Send factsheet message on complete product for sku: {sku} '
            f'seller_id: {seller_id} action: {action}',
            detail={
                "sku": sku,
                "seller_id": seller_id,
                "action": action
            }
        )

    @staticmethod
    def _clean_invalid_characters(
        text: str
    ) -> str:
        return bleach.clean(text, strip=True)

    def _clean_invalid_characters_from_dict(
        self,
        d: Dict
    ) -> Dict:
        for key, value in d.items():
            if isinstance(value, str):
                d[key] = self._clean_invalid_characters(value)
            elif isinstance(value, dict):
                d[key] = self._clean_invalid_characters_from_dict(value)
            elif isinstance(value, Sequence):
                d[key] = self._clean_invalid_characters_from_sequence(value)
        return d

    def _clean_invalid_characters_from_sequence(
        self,
        sequence: Sequence
    ) -> List:
        result = []
        for i in sequence:
            if isinstance(i, str):
                result.append(self._clean_invalid_characters(i))
            elif isinstance(i, dict):
                result.append(self._clean_invalid_characters_from_dict(i))
            elif isinstance(i, Sequence):
                result.append(self._clean_invalid_characters_from_sequence(i))
            else:
                result.append(i)
        return result

    def _get_navigation_id(
        self,
        sku: str,
        seller_id: str
    ) -> Optional[str]:

        product = self.raw_products.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0, 'navigation_id': 1}
        )

        if not product:
            return

        return product['navigation_id']

    def _exists_term(
        self,
        term: str,
        field: str,
        replace_terms: List[Dict]
    ) -> bool:
        for replacement in replace_terms:
            if replacement['field'] == field and replacement['term'] == term:
                return True
        return False

    def _search_terms(
        self,
        elements: List[dict],
        element_key: str
    ) -> List[dict]:
        replace_terms = []
        for element in elements:
            if element.get('elements'):
                element_key = element['key_name']
                replace_terms += self._search_terms(
                    element.get('elements'),
                    element_key
                )
            else:
                terms_from_cache = self.forbidden_terms.get_redis_terms()
                for forbidden_term, new_term in terms_from_cache.items():
                    element_key = self.__validate_and_save_parent_key_name(
                        replace_terms=replace_terms,
                        parent_element_key_name=element_key,
                        forbidden_term=forbidden_term,
                        new_term=new_term
                    )

                    self.__validate_and_save_element_key(
                        replace_terms=replace_terms,
                        element=element,
                        forbidden_term=forbidden_term,
                        new_term=new_term,
                        element_key=element_key
                    )

                    self.__validate_and_save_element_value(
                        replace_terms=replace_terms,
                        element=element,
                        forbidden_term=forbidden_term,
                        new_term=new_term,
                        element_key=element_key
                    )

        return replace_terms

    def _handler_forbidden_terms(
        self,
        factsheet: List[dict]
    ) -> List[dict]:
        replace_terms = []
        for item in factsheet['items']:
            if not item.get('elements'):
                continue
            elif self.__is_hierarchical(item['elements']):
                for elements in item['elements']:
                    element_key = elements['key_name']
                    replace_terms += self._search_terms(
                        elements['elements'],
                        element_key
                    )
            else:
                element_key = item['display_name']
                replace_terms += self._search_terms(
                    item['elements'],
                    element_key
                )

        return replace_terms

    @staticmethod
    def __is_hierarchical(elements: List[Dict]) -> int:
        for element in elements:
            for element_item in element.get('elements') or []:
                if element_item.get('elements'):
                    return True
        return False

    def __process_factsheet(
        self,
        action: str,
        data: Dict
    ):
        seller_id: str = data['seller_id']
        sku: str = data['sku']
        source: str = data.get('source')
        items: List[Dict] = data['items']

        enabled_to_process, enabled_to_clean_html = (
            self.validate_factsheet_to_process(
                sku=sku,
                seller_id=seller_id,
                source=source
            )
        )

        if not enabled_to_process:
            reason = (
                'Message skips because product was enriched by one of the '
                f'sources:{settings.SKIP_ENRICHED_SOURCES_WHEN_NOT_METADATA_VERIFY} ' # noqa
                f'from sku:{sku} seller_id:{seller_id} and source '
                'not is metadata_verify'
            )
            source = settings.SKIP_ENRICHED_SOURCES_WHEN_NOT_METADATA_VERIFY
            logger.warning(
                reason,
                detail={
                    "sku": sku,
                    "seller_id": seller_id,
                    "sources": source,
                })

            self.notification_sender.notify_patolino_about_unfinished_process( # noqa
                data,
                UPDATE_ACTION,
                reason,
                FACTSHEET_UNFINISHED_PROCESS
            )
            return False

        new_md5 = md5(data)
        if not self.__is_different_data(data, new_md5, action):
            return False

        send_to_datalake = False
        navigation_id = self._get_navigation_id(sku, seller_id)
        if navigation_id:
            send_to_datalake = True
            data.update({'navigation_id': navigation_id})

        last_updated_at = datetime.datetime.utcnow().isoformat()
        data.update({'md5': new_md5, 'last_updated_at': last_updated_at})
        if source != SOURCE_METADATA_VERIFY:
            self.raw_factsheet_storage.upload_bucket_data(
                sku=sku,
                seller_id=seller_id,
                payload=json_dumps(data, ensure_ascii=False)
            )

        items, attribute_amount = self._sort_elements(items)

        if enabled_to_clean_html:
            items = self._clean_invalid_characters_from_sequence(items)

        factsheet = {'items': list(filter(lambda x: bool(x), items))}

        terms = self._handler_forbidden_terms(factsheet)

        if navigation_id:
            factsheet.update({'navigation_id': navigation_id})

        self.forbidden_terms.save_forbidden_terms(
            sku=sku,
            seller_id=seller_id,
            navigation_id=navigation_id,
            new_terms=terms
        )

        self.factsheet_merger.merge(
            sku,
            seller_id,
            factsheet=factsheet
        )

        self.factsheet_storage.upload_bucket_data(
            sku=sku,
            seller_id=seller_id,
            payload=json_dumps(factsheet, ensure_ascii=False)
        )

        self._notify(
            action=action,
            seller_id=seller_id,
            sku=sku,
            navigation_id=navigation_id,
            send_to_datalake=send_to_datalake
        )

        self.acme_notification.send_factsheet(
            action=CREATE_ACTION,
            seller_id=seller_id,
            sku=sku,
            payload=factsheet
        )

        self.factsheets.update_one(
            {'sku': sku, 'seller_id': seller_id},
            {
                '$set': {
                    'sku': sku,
                    'seller_id': seller_id,
                    'last_updated_at': last_updated_at,
                    'md5': new_md5,
                    **factsheet
                }
            },
            upsert=True
        )

    def __is_different_data(
        self,
        payload: Dict,
        new_md5: str,
        action: str
    ):
        sku = payload['sku']
        seller_id = payload['seller_id']

        factsheet = self.factsheets.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0, 'md5': 1}
        ) or {}

        if factsheet.get('md5') == new_md5:
            logger.info(
                f'Skip process factsheet to sku:{sku} '
                f'seller_id:{seller_id} payload are the same',
                detail={
                    "sku": sku,
                    "seller_id": seller_id
                }
            )
            self.notification_sender.notify_patolino_about_unfinished_process(  # noqa
                product=payload,
                action=action,
                reason=FACTSHEET_SKIP_MESSAGE,
                code=FACTSHEET_UNFINISHED_PROCESS
            )
            return False
        return True

    def __validate_and_save_parent_key_name(
        self,
        replace_terms: List,
        parent_element_key_name: str,
        forbidden_term: str,
        new_term: str
    ) -> str:
        text, should_save = self.forbidden_terms.replace_term(
            text=parent_element_key_name,
            pattern=forbidden_term,
            replacement=new_term
        )

        if should_save:
            replace_terms.append({
                'term': forbidden_term,
                'replace': new_term,
                'field': parent_element_key_name,
                'scope': SCOPE,
                'replace_at': datetime.datetime.now().isoformat()
            })

        return text

    def __validate_and_save_element_key(
        self,
        replace_terms: List,
        element: Dict,
        forbidden_term: str,
        new_term: str,
        element_key: str
    ) -> None:
        key_name = element.get('key_name', element_key)
        text, should_save = self.forbidden_terms.replace_term(
            text=key_name,
            pattern=forbidden_term,
            replacement=new_term
        )

        if should_save:
            element['key_name'] = text
            replace_terms.append({
                'term': forbidden_term,
                'replace': new_term,
                'field': key_name,
                'scope': SCOPE,
                'replace_at': datetime.datetime.now().isoformat()
            })

    def __validate_and_save_element_value(
        self,
        replace_terms: List,
        element: Dict,
        forbidden_term: str,
        new_term: str,
        element_key: str
    ) -> None:
        text, should_save = self.forbidden_terms.replace_term(
            text=element.get('value'),
            pattern=forbidden_term,
            replacement=new_term
        )

        if should_save:
            default_info = {
                'scope': SCOPE,
                'replace_at': datetime.datetime.now().isoformat()
            }

            element['value'] = text
            field = element.get('key_name')

            if field:
                replace_terms.append(
                    {
                        'term': forbidden_term,
                        'replace': new_term,
                        'field': field,
                        **default_info
                    }
                )
            elif not self._exists_term(
                forbidden_term,
                element_key,
                replace_terms
            ):
                replace_terms.append({
                    'term': forbidden_term,
                    'replace': new_term,
                    'field': field,
                    **default_info
                })


class FactsheetConsumer(PubSubBroker):
    scope = SCOPE
    project_name = settings.GOOGLE_PROJECT_ID
    subscription_name = settings.PUBSUB_FACTSHEET_SUB_NAME
    record_processor_class = FactsheetRecordProcessor
