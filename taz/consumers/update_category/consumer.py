from datetime import datetime

from maaslogger import base_logger
from simple_settings import settings

from taz import constants
from taz.consumers.core.brokers.stream import (
    PubSubBroker,
    PubSubRecordProcessor
)
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.frajola import FrajolaRequest
from taz.consumers.update_category import SCOPE

logger = base_logger.get_logger(__name__)


class UpdateCategoryProcessor(PubSubRecordProcessor, MongodbMixin):
    scope = SCOPE
    max_process_workers = settings.UPDATE_CATEGORY_PROCESS_WORKERS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frajola = FrajolaRequest()
        self.category_history = self.get_collection('category_history')
        self.raw_products = self.get_collection('raw_products')

    def process_message(self, message):
        sku = message['sku']
        seller_id = message['seller_id']

        if seller_id != constants.MAGAZINE_LUIZA_SELLER_ID:
            logger.warn(
                'Discarting message sku:{sku} seller_id:{seller_id} from '
                'update category because not seller_id "magazineluiza"'.format(
                    sku=sku,
                    seller_id=seller_id
                )
            )

            return True

        product = self.raw_products.find_one({
            'sku': sku, 'seller_id': seller_id
        })
        if not product:
            logger.warn(
                'Product sku:{sku} seller_id:{seller_id} not found'.format(
                    sku=sku, seller_id=seller_id
                )
            )

            return True

        category = product['categories'][0]
        category_id = category['id']

        subcategory = category['subcategories'][0]
        subcategory_id = subcategory['id']

        product_id = sku[:7]
        original_product = self.frajola.get(product_id)
        if not original_product:
            logger.warn('Product {} not found from Frajola'.format(product_id))
            return

        if (
            category_id == original_product['category_id'] and
            subcategory_id == original_product['subcategory_id']
        ):
            logger.warn(
                'Discarting message because product {product_id} same '
                'categories {category_id}-{subcategory_id} '
                '{orignal_category_id}-{orignal_subcategory_id}'.format(
                    product_id=product_id,
                    category_id=category_id,
                    subcategory_id=subcategory_id,
                    orignal_category_id=original_product['category_id'],
                    orignal_subcategory_id=original_product['subcategory_id']
                )
            )

            return True

        self._save_category_history(
            sku,
            seller_id,
            category_id,
            subcategory_id,
            original_product
        )

        self._update_category(
            product_id,
            original_product,
            category_id,
            subcategory_id
        )

        logger.info(
            'Update category sku:{sku} seller_id:{seller_id} '
            'from Frajola'.format(
                sku=sku,
                seller_id=seller_id
            )
        )

        return True

    def _update_category(
        self,
        product_id,
        original_product,
        category_id,
        subcategory_id
    ):
        payload = original_product
        payload.update({
            'category_id': category_id,
            'subcategory_id': subcategory_id
        })

        self.frajola.put(product_id, payload)

    def _save_category_history(
        self,
        sku,
        seller_id,
        category_id,
        subcategory_id,
        original_product
    ):
        payload = {
            'sku': sku,
            'seller_id': seller_id,
            'original': {
                'category_id': original_product['category_id'],
                'subcategory_id': original_product['subcategory_id']
            },
            'category_id': category_id,
            'subcategory_id': subcategory_id,
            'date': datetime.utcnow().isoformat()
        }

        self.category_history.insert(payload)


class UpdateCategoryConsumer(PubSubBroker):
    scope = SCOPE
    record_processor_class = UpdateCategoryProcessor
    project_name = settings.GOOGLE_PROJECT_ID
