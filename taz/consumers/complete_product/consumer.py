from functools import cached_property
from typing import Dict, List

import requests
from maaslogger import base_logger
from simple_settings import settings
from slugify import slugify

from taz import constants
from taz.constants import OMNILOGIC
from taz.consumers.complete_product import SCOPE
from taz.consumers.complete_product.schema import CompleteProductSchema
from taz.consumers.core.brokers.stream import (
    PubSubBroker,
    PubSubRecordProcessor
)
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.core.common.media import build_media
from taz.core.storage.raw_products_storage import RawProductsStorage
from taz.helpers.json import strip_decimals
from taz.helpers.url import generate_product_url

logger = base_logger.get_logger(__name__)


class CompleteProductProcessor(MongodbMixin, PubSubRecordProcessor):

    scope = SCOPE
    max_process_workers = settings.COMPLETE_PRODUCT_PROCESS_WORKERS
    schema_class = CompleteProductSchema
    disable_cache_lock = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @cached_property
    def raw_products(self):
        return self.get_collection('raw_products')

    @cached_property
    def medias(self):
        return self.get_collection('medias')

    @cached_property
    def prices(self):
        return self.get_collection('prices')

    @cached_property
    def storage(self):
        return RawProductsStorage()

    def process_message(self, message: Dict) -> bool:
        sku = message['sku']
        seller_id = message['seller_id']
        action = message['action']

        if action == constants.DELETE_ACTION:
            action = constants.UPDATE_ACTION

        product = self._get_product_data(sku, seller_id)

        if not product:
            logger.warning(
                f'Product not found in for sku:{sku} '
                f'seller_id:{seller_id}',
                detail={
                    "sku": sku,
                    "seller_id": seller_id
                }
            )
            return True

        categories = product.get('categories')
        navigation_id = product.get('navigation_id')

        if self._should_skip_process(
            sku=sku,
            seller_id=seller_id,
            navigation_id=navigation_id,
            category=categories
        ):
            return True

        path = self._get_product_url(
            navigation_id=navigation_id,
            title=product.get('title'),
            reference=product.get('reference'),
            categories=categories
        )

        if not path:
            logger.info(
                f'Discarding the product sku:{sku} seller_id:{seller_id} '
                f'{navigation_id} because it was not possible '
                f'to generate the url',
                detail={
                    "sku": sku,
                    "navigation_id": navigation_id,
                    "seller_id": seller_id
                }
            )
            return True

        price = self.prices.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0, 'list_price': 1, 'price': 1, 'stock_count': 1}
        ) or {}

        if not price:
            logger.debug(
                f'Price not found for sku:{sku} seller_id:{seller_id}'
                f'navigation_id:{navigation_id}',
                detail={
                    "sku": sku,
                    "navigation_id": navigation_id,
                    "seller_id": seller_id
                }
            )

        images = self._build_images(
            sku,
            seller_id,
            product['title'],
            product.get('reference') or ''
        )

        payload = self._create_payload(
            product=product,
            price=price,
            images=images,
            action=action,
            path=path
        )

        notification_success = self._notify_omnilogic(payload)

        if not notification_success:
            logger.warning(
                f'Could not send Message sku:{sku} '
                f'seller:{seller_id} navigation_id:'
                f'{navigation_id} action:{action} ',
                detail={
                    "sku": sku,
                    "navigation_id": navigation_id,
                    "seller_id": seller_id
                }
            )
            return False

        logger.info(
            f'Message sent successfully for sku:{sku} '
            f'seller_id:{seller_id} navigation_id:'
            f'{navigation_id} action:{action} ',
            detail={
                "sku": sku,
                "navigation_id": navigation_id,
                "seller_id": seller_id
            }
        )
        return True

    def _create_payload(
        self,
        product: Dict,
        price: Dict,
        images: List,
        action: str,
        path: str
    ):
        return {
            'action': action,
            'sku': product['sku'],
            'sku_slug': slugify(product['sku']),
            'seller_id': product['seller_id'],
            'type': product['type'],
            'dimensions': product.get('dimensions') or {},
            'ean': product.get('ean') or product.get('isbn') or '',
            'brand': product['brand'],
            'title': product['title'],
            'description': product['description'],
            'categories': product['categories'],
            'reference': product['reference'],
            'active': not product['disable_on_matching'],
            'attributes': product.get('attributes') or [],
            'medias': images,
            'factsheet_url': self._generate_factsheet_url(
                sku=product['sku'],
                seller_id=product['seller_id']
            ),
            'created_at': product['created_at'],
            'parent_sku': product['parent_sku'],
            'navigation_id': product['navigation_id'],
            'price': price.get('price') or '0.00',
            'list_price': price.get('list_price') or '0.00',
            'stock_count': price.get('stock_count') or 0,
            'path': path,
            'offer_title': product.get('offer_title') or product.get('title'),
            'product_hash': product.get('product_hash')
        }

    @staticmethod
    def _should_skip_process(
        sku: str,
        seller_id: str,
        navigation_id: str,
        category: List
    ) -> bool:
        try:
            category_id = category[0]['id']
        except Exception:
            logger.warning(
                f'Skip process category not found for '
                f'product sku:{sku} seller_id:{seller_id} '
                f'navigation_id:{navigation_id}',
                detail={
                    "sku": sku,
                    "navigation_id": navigation_id,
                    "seller_id": seller_id
                }
            )
            return True

        if (
            category_id in settings.CATEGORY_SKIP_EXTERNAL_OMNILOGIC or
            '*' in settings.CATEGORY_SKIP_EXTERNAL_OMNILOGIC
        ):
            logger.info(
                f'Skip process for product sku:{sku} '
                f'seller_id:{seller_id} navigation_id:'
                f'{navigation_id} category_id:{category_id}',
                detail={
                    "sku": sku,
                    "navigation_id": navigation_id,
                    "seller_id": seller_id,
                    "category_id": category_id
                }
            )
            return True

        return False

    def _notify_omnilogic(self, payload: Dict) -> bool:
        payload = strip_decimals(payload)
        content_plain = ''
        url = settings.APIS[OMNILOGIC]['url']

        try:
            response = requests.post(
                url,
                json=payload,
                headers=settings.APIS[OMNILOGIC]['headers'],
                timeout=(
                    int(settings.CONNECTION_TIMEOUT_REQUEST_OMNILOGIC),
                    int(settings.READ_TIMEOUT_REQUEST_OMNILOGIC)
                )
            )

            if not str(response.status_code).startswith('2'):
                return False

            content_plain = response.text
            content = response.json()

            return content.get('status') != 'error'
        except Exception as e:
            logger.error(
                'Error in send request to Omnilogic endpoint:{url} '
                'for product sku:{sku} seller_id:{seller_id} '
                'navigation_id:{navigation_id} with response:{content}, '
                'error:{error}'.format(
                    url=url,
                    sku=payload['sku'],
                    seller_id=payload['seller_id'],
                    navigation_id=payload['navigation_id'],
                    content=content_plain,
                    error=e
                ),
                detail={
                    "url": url,
                    "sku": payload['sku'],
                    "seller_id": payload['seller_id'],
                    "navigation_id": payload['navigation_id'],
                    "content": content_plain,
                    "error": e
                }
            )
            raise e

    @staticmethod
    def _generate_factsheet_url(
        sku: str,
        seller_id: str
    ) -> str:
        return f'{settings.FACTSHEET_DOMAIN}/{seller_id}/factsheet/{sku}.json'

    def _build_images(
        self,
        sku: str,
        seller_id: str,
        title: str,
        reference: str
    ) -> List:
        medias = self.medias.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0, 'images': 1}
        ) or {}

        if not medias:
            return []

        return build_media(
            sku=sku,
            title=title,
            reference=reference,
            seller_id=seller_id,
            media_type='images',
            items=medias['images'],
            force_path=True
        )

    @staticmethod
    def _get_product_url(
        navigation_id: str,
        title: str,
        reference: str,
        categories: List
    ) -> str:
        try:
            return generate_product_url(
                navigation_id,
                {
                    'title': title,
                    'reference': reference
                },
                categories
            )
        except Exception as e:
            logger.error(
                'Error in generate product URL for navigation_id:'
                f'{navigation_id} and error:{e}'
            )

    def _get_product_data(
        self,
        sku: str,
        seller_id: str
    ) -> Dict:
        product = self.raw_products.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0}
        )

        category_id = None
        original_product = None

        if product:
            category_id = product['categories'][0]['id']

        if category_id not in settings.COMPLETE_PRODUCT_CATEGORY_SKIP:
            original_product = self.storage.get_bucket_data(
                sku=sku,
                seller_id=seller_id
            )

        return original_product or product


class CompleteProductConsumer(PubSubBroker):
    scope = SCOPE
    record_processor_class = CompleteProductProcessor
    project_name = settings.GOOGLE_PROJECT_ID
