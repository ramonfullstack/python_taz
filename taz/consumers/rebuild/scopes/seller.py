import logging
from functools import cached_property

from marshmallow import Schema, fields, validate
from simple_settings import settings

from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.rebuild.scopes.base import BaseRebuild
from taz.pollers.core.brokers.pubsub import StreamPublisherManager

logger = logging.getLogger(__name__)


class ProductSchema(Schema):
    seller_id = fields.String(
        validate=[validate.Length(min=1, max=50)], required=True
    )


class RebuildProductSeller(MongodbMixin, BaseRebuild):

    schema_class = ProductSchema
    poller_scope = 'product'

    @cached_property
    def raw_products(self):
        return self.get_collection('raw_products')

    @cached_property
    def pubsub(self):
        return StreamPublisherManager()

    def _rebuild(self, action, data):
        logger.info(
            'Starting product seller rebuild with request:{}'.format(data)
        )

        criteria = {
            'disable_on_matching': False,
            'seller_id': data['seller_id']
        }

        raw_products = self.raw_products.find(
            criteria,
            no_cursor_timeout=True
        )
        for product in raw_products:
            self.pubsub.publish(
                content={
                    'data': product,
                    'action': action
                },
                topic_name=settings.PUBSUB_PRODUCT_TOPIC_NAME,
                project_id=settings.GOOGLE_PROJECT_ID,
            )
        logger.info('Product seller rebuild successfully finished')

        return True
