import datetime
from functools import cached_property
from typing import Dict, List, Union

from maaslogger import base_logger
from simple_settings import settings

from taz.constants import (
    CREATE_ACTION,
    DELETE_ACTION,
    MAGAZINE_LUIZA_SELLER_DESCRIPTION,
    MAGAZINE_LUIZA_SELLER_ID,
    PRODUCT_ALREADY_DISABLED_CODE,
    PRODUCT_ALREADY_DISABLED_MESSAGE,
    PRODUCT_ERROR_CODE,
    PRODUCT_ERROR_MESSAGE,
    PRODUCT_ORIGIN,
    PRODUCT_SKIP_PROCESS,
    PRODUCT_SUCCESS_CODE,
    PRODUCT_SUCCESS_MESSAGE,
    PRODUCT_UNFINISHED_PROCESS_CODE,
    REBUILD_ORIGIN,
    SINGLE_SELLER_STRATEGY,
    UPDATE_ACTION
)
from taz.consumers.core.brokers.stream import (
    PubSubBroker,
    PubSubRecordProcessorWithRequiredFields
)
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.exceptions import NavigationIdNotFound
from taz.consumers.core.generators import id_generator
from taz.consumers.core.notification import Notification
from taz.consumers.product.helpers import ProductHelpers
from taz.consumers.product.rank_generator import RankGenerator
from taz.core.forbidden_terms.forbidden_terms import ForbiddenTerms
from taz.core.notification.notification_sender import NotificationSender
from taz.core.storage.raw_products_storage import RawProductsStorage
from taz.helpers.isbn import validate_isbn
from taz.helpers.json import json_dumps
from taz.utils import (
    clean_invalid_characters,
    decode_body,
    format_ean,
    md5,
    valid_ean
)

logger = base_logger.get_logger(__name__)

SCOPE = 'product'


class ProductRecordProcessor(
    MongodbMixin,
    PubSubRecordProcessorWithRequiredFields
):

    required_fields = [
        'ean', 'seller_id', 'sku', 'type',
        'main_variation', 'title', 'description', 'reference',
        'brand', 'sold_count', 'categories', 'dimensions', 'created_at'
    ]
    required_non_empty_fields = ['categories']

    required_fields_delete = ['seller_id', 'sku']
    required_non_empty_fields_delete = ['seller_id', 'sku']

    max_process_workers = settings.PRODUCT_CONSUMER_MAX_WORKERS

    FIELDS_TO_CLEAN = ('title', 'reference', 'brand')

    FORBIDDEN_TERMS_FIELDS_TO_CLEAN = ['title', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__rank_generator = RankGenerator()
        self.__notification = Notification()
        self.__notification_sender = NotificationSender()
        self.__forbidden_terms = ForbiddenTerms()

    @cached_property
    def raw_products(self):
        return self.get_collection('raw_products')

    @cached_property
    def sellers(self):
        return self.get_collection('sellers')

    @cached_property
    def raw_products_storage(self):
        return RawProductsStorage()

    def _create(self, product: Dict):
        seller_id = product['seller_id']
        sku = product['sku']

        if seller_id in settings.ENABLE_SELLER_PAYLOAD_LOG:
            logger.info(f'Request created item with payload:{product}')

        seller_info = self.get_seller_info(
            product=product,
            action=CREATE_ACTION
        )

        if not seller_info:
            return

        stored_product = self.raw_products.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0}
        )

        if stored_product:
            self._update(product)
            return

        decoded_product = decode_body(product)
        hash_md5 = md5(decoded_product)

        navigation_id = (
            id_generator.generate_id() if
            seller_id != MAGAZINE_LUIZA_SELLER_ID else
            product['sku']
        )

        terms = self._handler_forbidden_terms(decoded_product)
        self.__forbidden_terms.save_forbidden_terms(
            sku=sku,
            seller_id=seller_id,
            navigation_id=navigation_id,
            new_terms=terms
        )
        self.normalize_product_payload(decoded_product)

        decoded_product.update(
            ProductHelpers.format_payload_product(
                decoded_product=decoded_product,
                seller_info=seller_info,
                grade=self.__rank_generator.compute_grade(decoded_product),
                navigation_id=navigation_id,
                matching_strategy=SINGLE_SELLER_STRATEGY,
                md5=hash_md5
            )
        )

        self.__save(
            product=decoded_product,
            seller_info=seller_info,
            action=CREATE_ACTION
        )

        self.__catalog_notification(
            action=CREATE_ACTION,
            sku=sku,
            seller_id=seller_id,
            navigation_id=navigation_id,
            tracking_id=product.get('tracking_id')
        )

        logger.info(
            f'Successfully created item sku:{sku} seller_id:{seller_id} '
            f'navigation_id:{navigation_id}'
        )

    def _update(self, product: Dict):
        seller_id = product['seller_id']
        sku = product['sku']
        tracking_id = product.get('tracking_id')

        if seller_id == MAGAZINE_LUIZA_SELLER_ID:
            logger.info(f'Request updated item with payload:{product}')

        seller_info = self.get_seller_info(
            product=product,
            action=UPDATE_ACTION
        )

        if not seller_info:
            return

        stored_product = self.raw_products.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0}
        )

        if not stored_product:
            self._create(product)
            return

        decoded_product = decode_body(product)
        new_md5 = md5(decoded_product, stored_product.get('md5'))

        if (
            not settings.SKIP_MD5_VALIDATION and
            stored_product.get('md5') == new_md5 and
            not stored_product.get('disable_on_matching')
        ):
            logger.info(
                f'Skip product update for sku:{sku} seller_id:{seller_id}'
            )
            self.__notification_sender.notify_patolino_about_unfinished_process( # noqa
                product,
                UPDATE_ACTION,
                PRODUCT_SKIP_PROCESS,
                PRODUCT_UNFINISHED_PROCESS_CODE
            )
            return

        if (
            stored_product.get('gift_product') and
            not decoded_product.get('gift_product')
        ):
            self.raw_products.update_many(
                {'sku': sku, 'seller_id': seller_id},
                {'$unset': {'gift_product': ''}}
            )

        navigation_id = stored_product.get('navigation_id')

        terms = self._handler_forbidden_terms(decoded_product)
        self.__forbidden_terms.save_forbidden_terms(
            sku=sku,
            seller_id=seller_id,
            navigation_id=navigation_id,
            new_terms=terms
        )
        self.normalize_product_payload(decoded_product, stored_product)

        payload = ProductHelpers.format_payload_product(
            decoded_product=decoded_product,
            seller_info=seller_info,
            grade=(
                stored_product.get('grade') or
                self.__rank_generator.compute_grade(decoded_product)
            ),
            navigation_id=navigation_id,
            matching_strategy=(
                stored_product.get('matching_strategy') or
                product.get('matching_strategy', SINGLE_SELLER_STRATEGY)
            ),
            md5=new_md5
        )

        decoded_product.update(payload)

        if stored_product.get('product_hash'):
            decoded_product['product'] = stored_product.get('product_hash')

        if decoded_product.get('origin') == REBUILD_ORIGIN:
            self.__catalog_notification(
                action=UPDATE_ACTION,
                sku=sku,
                seller_id=seller_id,
                navigation_id=navigation_id,
                tracking_id=tracking_id
            )
            return

        self.__save(
            product=decoded_product,
            seller_info=seller_info,
            action=UPDATE_ACTION
        )

        self.__catalog_notification(
            action=UPDATE_ACTION,
            sku=sku,
            seller_id=seller_id,
            navigation_id=navigation_id,
            tracking_id=tracking_id
        )

        logger.info(
            f'Successfully updated item sku:{sku} seller:{seller_id} '
            f'navigation_id:{navigation_id}'
        )

    def _delete(self, product: Dict):
        sku = product['sku']
        seller_id = product['seller_id']
        tracking_id = product.get('tracking_id')

        if seller_id in settings.ENABLE_SELLER_PAYLOAD_LOG:
            logger.info(f'Request delete item with payload:{product}')

        seller_info = self.get_seller_info(
            product=product,
            action=DELETE_ACTION
        )

        if not seller_info:
            return

        stored_product = self.raw_products.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0}
        )

        if not stored_product:
            self.__notification_sender.notify_patolino_about_unfinished_process( # noqa
                product,
                DELETE_ACTION,
                'Product not found.',
                PRODUCT_UNFINISHED_PROCESS_CODE
            )
            return

        if (
            seller_id == MAGAZINE_LUIZA_SELLER_ID and
            product['active']
        ):
            logger.warning(
                f'Ignoring product delete from sku:{sku} '
                f'seller_id:{seller_id} because it is active'
            )
            self._update(product)
            return

        if stored_product['disable_on_matching']:
            self.__notification_sender.send(
                sku=stored_product['sku'],
                seller_id=stored_product['seller_id'],
                code=PRODUCT_ALREADY_DISABLED_CODE,
                message=PRODUCT_ALREADY_DISABLED_MESSAGE,
                tracking_id=product.get('tracking_id'),
                payload={
                    'navigation_id': stored_product['navigation_id'],
                    'action': DELETE_ACTION
                }
            )

            logger.info(
                f'Product sku:{sku} seller_id:{seller_id} already disabled '
                'on catalog, send event notification to Patolino'
            )
            return

        self._save_original_product_bucket(
            sku=stored_product['sku'],
            seller_id=stored_product['seller_id'],
            tracking_id=tracking_id,
            product={**stored_product},
        )

        stored_product['disable_on_matching'] = True
        stored_product['tracking_id'] = tracking_id
        self._save_raw_product(stored_product, DELETE_ACTION)

        self.__catalog_notification(
            action=DELETE_ACTION,
            sku=sku,
            seller_id=seller_id,
            navigation_id=stored_product['navigation_id'],
            tracking_id=tracking_id
        )

        logger.info(
            f'Successfully disabled item sku:{sku} '
            f'seller_id:{seller_id} from raw_products'
        )

    def _handler_forbidden_terms(
        self,
        product: Dict
    ) -> List:
        terms = self.__forbidden_terms.get_redis_terms()

        if not terms:
            logger.warning(
                'Error to retrieve forbidden terms, value is empty'
            )
            return []

        terms_replace = []
        for term in terms.keys():
            for field in self.FORBIDDEN_TERMS_FIELDS_TO_CLEAN:
                data, should_save = self.__forbidden_terms.replace_term(
                    product[field],
                    term,
                    terms.get(term)
                )

                if should_save:
                    product[field] = data
                    terms_replace.append(
                        {
                            'term': term,
                            'replace': terms.get(term),
                            'field': field,
                            'scope': self.scope,
                            'replaced_at': datetime.datetime.now().isoformat()
                        }
                    )

        return terms_replace

    def _save_raw_product(
        self,
        product: Dict,
        action: str
    ) -> None:
        sku = product['sku']
        seller_id = product['seller_id']

        categories = ProductHelpers.extract_categorization(product, action)
        try:
            result = self.raw_products.update_many(
                {'sku': sku, 'seller_id': seller_id},
                {'$set': product},
                upsert=True
            )
            count_update = result.matched_count

            if count_update != 1:
                logger.warning(
                    f'Updated {count_update} documents in raw_products '
                    f'for sku:{sku} seller_id:{seller_id}'
                )

            self.__notification_sender.send(
                sku=sku,
                seller_id=seller_id,
                code=PRODUCT_SUCCESS_CODE,
                message=PRODUCT_SUCCESS_MESSAGE,
                tracking_id=product.get('tracking_id'),
                payload={
                    'navigation_id': product['navigation_id'],
                    'action': action
                }
            )

            if categories:
                product.update(categories)

        except Exception as e:
            logger.error(
                f'Could not save product sku:{sku} seller:{seller_id} '
                f'error:{e}'
            )
            self.__notification_sender.notify_patolino_about_error(
                product=product,
                action=action,
                reason=PRODUCT_ERROR_MESSAGE,
                code=PRODUCT_ERROR_CODE
            )
            raise

    def _save_original_product_bucket(
        self,
        sku: str,
        seller_id: str,
        tracking_id: str,
        product: dict = None
    ) -> None:
        original_product = self.raw_products_storage.get_bucket_data(
            sku=sku,
            seller_id=seller_id
        )

        if not original_product:
            original_product = product
            logger.warning(
                f'Product with sku:{sku} seller_id:{seller_id}'
                'not found in raw products storage'
            )

        original_product['disable_on_matching'] = True
        original_product['tracking_id'] = tracking_id

        self.__upload(
            payload=original_product,
            seller_id=seller_id,
            sku=sku
        )

    def __save(
        self,
        product: Dict,
        seller_info: Dict,
        action: str
    ) -> None:
        sku = product['sku']
        seller_id = product['seller_id']
        navigation_id = product.get('navigation_id')

        if not navigation_id:
            message = (
                f'Navigation ID for sku:{sku} '
                f'seller_id:{seller_id} not generated'
            )
            logger.warning(message)

            self.__notification_sender.notify_patolino_about_error(
                product=product,
                action=action,
                reason=PRODUCT_ERROR_MESSAGE,
                code=PRODUCT_ERROR_CODE
            )
            raise NavigationIdNotFound(message)

        self.__upload(
            payload=product,
            sku=sku,
            seller_id=seller_id
        )

        self.clean_html_from_product(product)

        sells_to_company = seller_info.get('sells_to_company') or False
        product['sells_to_company'] = sells_to_company

        self._save_raw_product(product, action)

    def __upload(
        self,
        payload: Dict,
        sku: str,
        seller_id: str
    ) -> None:
        if '_id' in payload:
            del payload['_id']

        raw_product = json_dumps(payload, ensure_ascii=False)

        self.raw_products_storage.upload_bucket_data(
            sku=sku,
            seller_id=seller_id,
            payload=raw_product
        )

    def get_seller_info(
        self,
        product: Dict,
        action: str
    ) -> Union[Dict, None]:
        sku = product['sku']
        seller_id = product['seller_id']

        if seller_id == MAGAZINE_LUIZA_SELLER_ID:
            seller_info = {
                'is_active': True,
                'sells_to_company': True,
                'name': MAGAZINE_LUIZA_SELLER_DESCRIPTION
            }
        else:
            seller_info = self.sellers.find_one(
                {'id': seller_id},
                {'_id': 0, 'is_active': 1, 'sells_to_company': 1, 'name': 1}
            )

        if not seller_info:
            logger.warning(
                f'Skip product {action} of sku:{sku} seller_id:{seller_id} '
                f'because could not find seller information'
            )
            self.__notification_sender.notify_patolino_about_error(
                product=product,
                action=action,
                reason=PRODUCT_ERROR_MESSAGE,
                code=PRODUCT_ERROR_CODE
            )

        return seller_info

    @staticmethod
    def clean_html_from_product(product: Dict) -> None:
        attributes = product.get('attributes', [])

        for attribute in attributes:
            value = attribute.get('value')
            if not value:
                continue

            value = ProductHelpers.clear_html(value, {'clean'}, {})
            value = value.strip()
            attribute['value'] = value

        description = ProductHelpers.clear_html(product['description'])
        product['description'] = description

    def normalize_product_payload(
        self,
        product: Dict,
        stored_product: Dict = {}
    ) -> None:
        ProductHelpers.capitalize_fields(product)
        ProductHelpers.format_reference(product)
        ProductHelpers.clean_ean_whitespace(product)
        ProductHelpers.normalize_voltage(product)

        for field in self.FIELDS_TO_CLEAN:
            product[field] = clean_invalid_characters(product[field])

        identifiers = self._normalize_identifiers(
            product,
            stored_product or {}
        )
        product.update(identifiers)

    def _normalize_identifiers(
        self,
        decoded_product: Dict,
        stored_product: Dict,
    ) -> Dict:
        ean = format_ean(decoded_product.get('ean', ''))
        identifiers = {'ean': ean} if valid_ean(ean) else {'ean': ''}

        if validate_isbn(identifiers['ean']):
            identifiers.update({'isbn': identifiers['ean']})
        elif stored_product.get('isbn'):
            identifiers.update({'isbn': ''})

        return identifiers

    def __catalog_notification(
        self,
        action: str,
        seller_id: str,
        sku: str,
        navigation_id: str,
        tracking_id: str
    ) -> None:
        payload = {
            'sku': sku,
            'seller_id': seller_id,
            'navigation_id': navigation_id,
            'tracking_id': tracking_id
        }

        self.__notification.put(
            data=payload,
            scope=self.scope,
            action=action,
            origin=PRODUCT_ORIGIN
        )

        logger.debug(
            f'Send product notification for sku:{sku} seller_id:{seller_id} '
            f'navigation_id:{navigation_id} scope:{self.scope} '
            f'action:{action}'
        )


class ProductConsumer(PubSubBroker):
    scope = SCOPE
    project_name = settings.GOOGLE_PROJECT_ID
    subscription_name = settings.PUBSUB_PRODUCT_SUB_NAME
    record_processor_class = ProductRecordProcessor
