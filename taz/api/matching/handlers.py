import logging
import uuid
from functools import cached_property

import falcon
from simple_settings import settings

from taz.api.common.exceptions import NotFound
from taz.api.common.handlers.base import BaseHandler
from taz.api.medias.models import MediaModel
from taz.api.prices.models import PriceModel
from taz.api.products.models import RawProductModel
from taz.constants import AUTO_BUYBOX_STRATEGY, SINGLE_SELLER_STRATEGY
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.google.stream import StreamPublisherManager
from taz.consumers.matching.consumer import MatchingRecordProcessor

logger = logging.getLogger(__name__)


class MatchingHandler(BaseHandler):
    def on_get(self, request, response, seller_id, sku):
        message = {
            'action': 'update',
            'sku': sku,
            'seller_id': seller_id,
            'task_id': uuid.uuid4(),
            'origin': __name__
        }

        processor = MatchingRecordProcessor(
            persist_changes=False,
            exclusive_strategy=False,
            strategy=AUTO_BUYBOX_STRATEGY,
        )
        payload = processor.process_message(message)

        if not payload or payload is True:
            raise NotFound('Matching for sku:{} seller:{} not found'.format(
                sku, seller_id
            ))

        for variation in payload['variations']:
            for seller in variation['sellers']:
                product = RawProductModel.get_product(
                    seller['id'], seller['sku']
                )

                seller.update({
                    'title': product['title'],
                    'reference': product['reference'],
                    'brand': product['brand'],
                    'ean': product.get('ean') or '',
                    'navigation_id': product['navigation_id'],
                    'attributes': product.get('attributes') or {}
                })

                seller['media'] = MediaModel.get_media(
                    seller['id'], seller['sku'], product
                )

                seller['price'] = PriceModel.get_price(
                    seller['id'], seller['sku']
                )

        self.write_response(response, falcon.HTTP_200, {'data': payload})


class RemoveMatchingHandler(BaseHandler, MongodbMixin):

    @cached_property
    def id_correlations(self):
        return self.get_collection('id_correlations')

    @cached_property
    def raw_products(self):
        return self.get_collection('raw_products')

    @cached_property
    def pubsub(self):
        return StreamPublisherManager()

    def on_delete(self, request, response, variation_id):
        id_correlation = self.id_correlations.find_one(
            {'variation_id': variation_id},
            {'_id': 0, 'product_id': 1}
        )

        if not id_correlation:
            raise NotFound(f'Variation {variation_id} not found')

        product_id = id_correlation['product_id']
        id_correlations = self.id_correlations.find(
            {'product_id': product_id},
            {'_id': 0, 'sku': 1, 'seller_id': 1}
        )

        for id_correlation in id_correlations:
            sku = id_correlation['sku']
            seller_id = id_correlation['seller_id']

            criteria = {
                'sku': sku,
                'seller_id': seller_id
            }

            raw_product = self.raw_products.find_one(
                criteria,
                {'_id': 0}
            )

            raw_product['matching_strategy'] = SINGLE_SELLER_STRATEGY
            self.raw_products.update(criteria, raw_product, upsert=True)

            self.id_correlations.remove(criteria)
            self.pubsub.publish(
                content={
                    **criteria,
                    'action': 'update',
                    'task_id': uuid.uuid4().hex
                },
                attributes={
                    'sku': sku,
                    'seller_id': seller_id,
                },
                topic_name=settings.PUBSUB_MATCHING_PRODUCT_TOPIC_NAME,
                project_id=settings.GOOGLE_PROJECT_ID
            )

            logger.info(
                f'Remove matching for id:{variation_id} '
                f'sku:{sku} seller:{seller_id}'
            )

        self.write_response(response, falcon.HTTP_200)
