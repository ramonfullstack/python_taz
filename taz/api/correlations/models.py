import json
import logging

from mongoengine import DynamicDocument
from mongoengine.queryset import DoesNotExist

logger = logging.getLogger(__name__)


class CorrelationModel(DynamicDocument):
    meta = {
        'collection': 'id_correlations',
    }

    @classmethod
    def get(cls, seller_id, sku):
        logger.info(
            'Get id_correlations from sku:{sku} seller_id:{seller_id}'.format(
                sku=sku,
                seller_id=seller_id
            )
        )

        try:
            payload = CorrelationModel.objects.get(
                sku=sku,
                seller_id=seller_id
            )

            return json.loads(payload.to_json())
        except DoesNotExist:
            logger.warning(
                'Correlation sku:{sku} seller_id:{seller_id} '
                'not found'.format(
                    sku=sku,
                    seller_id=seller_id
                )
            )

            return {}
