import json
import logging

from mongoengine import DynamicDocument

logger = logging.getLogger(__name__)


class PriceModel(DynamicDocument):
    meta = {
        'collection': 'prices',
        'shard_key': ('sku', 'seller_id',)
    }

    @classmethod
    def get_price(cls, seller_id, sku):
        payload = PriceModel.objects(seller_id=seller_id, sku=sku).first()
        if not payload:
            logger.debug(
                'Price sku:{} seller:{} not found'.format(sku, seller_id)
            )
            return {}

        return json.loads(payload.to_json())
