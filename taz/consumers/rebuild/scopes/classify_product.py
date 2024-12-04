import logging

from marshmallow import Schema, fields

from taz import constants
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.notification_enrichment import NotificationEnrichment
from taz.consumers.rebuild.scopes.base import BaseRebuild

logger = logging.getLogger(__name__)


class ClassifyProductSchema(Schema):
    navigation_id = fields.String(required=True)
    seller_id = fields.String(required=True)
    sku = fields.String(required=True)


class RebuildClassifyProduct(MongodbMixin, BaseRebuild):
    schema_class = ClassifyProductSchema
    poller_scope = 'classify_product'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notification_classify = NotificationEnrichment()
        self.raw_products = self.get_collection('raw_products')

    def _rebuild(self, action, data):
        logger.info(
            'Starting classify product rebuild with action:{action} '
            'request:{data}'.format(
                data=data,
                action=action
            )
        )

        product = self._get_product_by_sku_and_seller_id(
            data['sku'],
            data['seller_id']
        )

        if not product:
            logger.warning(
                'Product with sku:{} seller_id:{} navigation_id:{} '
                'not found in scope:{}'.format(
                    data['sku'],
                    data['seller_id'],
                    data['navigation_id'],
                    self.poller_scope
                )
            )
            return True

        self.notification_classify.notify(
            product=product,
            attributes={
                'event_type': constants.EnrichmentEventType.CLASSIFY.value
            }
        )
        return True

    def _get_product_by_sku_and_seller_id(self, sku, seller_id):
        return self.raw_products.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0}
        )
