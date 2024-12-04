import json
import logging

from mongoengine import DynamicDocument
from mongoengine.queryset import DoesNotExist

logger = logging.getLogger(__name__)


class UnifiedObjectModel(DynamicDocument):
    meta = {
        'collection': 'unified_objects',
    }

    @classmethod
    def get(cls, product_id):
        logger.info(
            'Get unified_objects from product_id:{}'.format(product_id)
        )

        try:
            payload = UnifiedObjectModel.objects(
                __raw__={'id': product_id}
            )

            if not payload:
                logger.warning(
                    'Unified Object product_id:{} not found'.format(product_id)
                )

                return {}

            return json.loads(payload.to_json())[0]
        except DoesNotExist:
            logger.warning(
                'Unified Object product_id:{} not found'.format(product_id)
            )

            return {}
