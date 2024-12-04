import json
import logging
import uuid

from mongoengine.queryset import DoesNotExist

from taz import constants
from taz.api.common.exceptions import HttpError, NotFound
from taz.api.pending.models import PendingProductModel
from taz.api.products.models import RawProductModel
from taz.consumers.matching.consumer import MatchingRecordProcessor

logger = logging.getLogger(__name__)


class PendingProductHelper:

    @classmethod
    def delete_pending_products(cls, seller_id, sku):
        try:
            cls.get_pending_product(seller_id, sku).delete()

            logger.info(
                'Product removed from pending_products to sku:{} '
                'seller:{}'.format(sku, seller_id)
            )
        except NotFound:
            logger.debug('Pending product sku:{} seller:{} not found'.format(
                sku, seller_id
            ))

    @classmethod
    def save_raw_products(cls, seller_id, sku, matching_strategy):

        raw_product = RawProductModel.objects.get(
            seller_id=seller_id, sku=sku
        )

        try:
            raw_product['matching_strategy'] = matching_strategy

            product = json.loads(raw_product.to_json())
            del product['_id']

            logger.debug(
                'Send payload to raw_products sku:{} seller:{} with '
                'payload:{}'.format(sku, seller_id, raw_product)
            )

            raw_product.delete()
            RawProductModel(**product).save()

            logger.info(
                'Product saved in raw_products to sku:{} '
                'seller:{}'.format(sku, seller_id)
            )
        except Exception:
            message = 'Could not save product sku:{} seller:{}'.format(
                sku, seller_id
            )

            logger.exception(message)
            raise HttpError(message=message)

    @classmethod
    def get_pending_product(cls, seller_id, sku):
        try:
            return PendingProductModel.objects.get(
                seller_id=seller_id, sku=sku
            )
        except DoesNotExist:
            exception_message = (
                'Pending product sku:{} seller:{} not '
                'found'.format(sku, seller_id)
            )
            logger.warning(exception_message)
            raise NotFound(message=exception_message)

    @classmethod
    def validate_sellers(cls, seller_id, sku, sellers, sellers_comparison):
        pairs = zip(
            sorted(sellers, key=lambda x: x['sku']),
            sorted(sellers_comparison, key=lambda x: x['sku'])
        )
        return any(x == y for x, y in pairs)

    @classmethod
    def get_sellers(cls, seller_id, sku):
        message = {
            'action': 'update',
            'sku': sku,
            'seller_id': seller_id,
            'task_id': str(uuid.uuid4()),
            'origin': __name__
        }

        consumer = MatchingRecordProcessor(
            persist_changes=False,
            exclusive_strategy=False,
            strategy=constants.AUTO_BUYBOX_STRATEGY
        )
        unified_objects = consumer.process_message(message)

        sellers = []
        if not unified_objects:
            return sellers

        for variation in unified_objects['variations']:
            for seller in variation['sellers']:
                sellers.append({
                    'sku': seller['sku'], 'seller_id': seller['id']
                })

        return sellers
