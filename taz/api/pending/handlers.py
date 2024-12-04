import json
import logging
import uuid
from functools import cached_property

import falcon
from mongoengine.queryset import DoesNotExist
from simple_settings import settings

from taz import constants
from taz.api.common.exceptions import BadRequest, NotFound
from taz.api.common.handlers.base import BaseHandler
from taz.api.pending.models import PendingProductModel
from taz.consumers.core.google.stream import StreamPublisherManager

from .helpers import PendingProductHelper

logger = logging.getLogger(__name__)


class ListPendingHandler(BaseHandler):
    def on_get(self, request, response):
        seller_id = request.get_param('seller')

        if seller_id:
            pending_products = PendingProductModel.objects(seller_id=seller_id)
        else:
            pending_products = PendingProductModel.objects

        payload = json.loads(pending_products.to_json())

        self.write_response(response, falcon.HTTP_200, {'data': payload})


class PendingHandler(BaseHandler):
    @cached_property
    def pubsub(self):
        return StreamPublisherManager()

    def on_get(self, request, response, seller_id, sku):
        pending_product = PendingProductHelper.get_pending_product(
            seller_id, sku
        )
        payload = json.loads(pending_product.to_json())

        self.write_response(response, falcon.HTTP_200, payload)

    def on_delete(self, request, response, seller_id, sku):
        PendingProductHelper.save_raw_products(
            seller_id=seller_id,
            sku=sku,
            matching_strategy=constants.SINGLE_SELLER_STRATEGY
        )

        try:
            PendingProductModel.objects.get(
                seller_id=seller_id,
                sku=sku,
            ).delete()

            logger.info(
                'Product successfully deleted sku:{} seller:{}'.format(
                    sku, seller_id
                )
            )
        except DoesNotExist:
            logger.warning(
                'Remove product sku:{} seller:{} not found'.format(
                    sku, seller_id
                )
            )

        self.write_response(response, falcon.HTTP_204)

    def on_put(self, request, response, seller_id, sku):
        if 'sellers' not in request.context:
            raise BadRequest(message='Invalid parameter: sellers')

        PendingProductHelper.get_pending_product(seller_id, sku)

        sellers = request.context['sellers']
        sellers.append({'sku': sku, 'seller_id': seller_id})

        logger.debug(
            'Send request PUT for pending_product sku:{} seller:{} '
            'payload:{}'.format(sku, seller_id, sellers)
        )

        sellers_comparison = PendingProductHelper.get_sellers(seller_id, sku)

        if not PendingProductHelper.validate_sellers(
            seller_id, sku, sellers, sellers_comparison
        ):
            exception_message = (
                'Comparison of sellers is not the same for product '
                'sku:{} seller:{} with payload:{} and '
                'sellers_comparison:{}'.format(
                    sku, seller_id, sellers, sellers_comparison
                )
            )

            logger.warning(exception_message)
            raise BadRequest(message=exception_message)

        for seller in sellers:
            try:
                PendingProductHelper.save_raw_products(
                    seller['seller_id'],
                    seller['sku'],
                    constants.AUTO_BUYBOX_STRATEGY
                )
            except NotFound:
                continue
            except Exception as e:
                logger.error(
                    'Error for saved in raw_products with sku:{sku} '
                    'seller:{seller_id} error:{error}'.format(
                        sku=sku,
                        seller_id=seller_id,
                        error=e
                    )
                )

                self.write_response(response, falcon.HTTP_500)
                return

            PendingProductHelper.delete_pending_products(
                seller['seller_id'], seller['sku']
            )

            logger.debug(
                'Product saved in raw_products and removed from '
                'pending_products to sku:{} seller:{}'.format(
                    seller['sku'], seller['seller_id']
                )
            )

        logger.debug(
            'Call notify matcher for queue:{} sku:{} seller:{}'.format(
                settings.PUBSUB_MATCHING_PRODUCT_TOPIC_NAME,
                sku,
                seller_id
            )
        )

        attributes = {
            'action': 'update',
            'sku': sku,
            'seller_id': seller_id,
        }
        self.pubsub.publish(
            content={
                **attributes,
                'task_id': uuid.uuid4().hex,
                'origin': __name__
            },
            attributes=attributes,
            topic_name=settings.PUBSUB_MATCHING_PRODUCT_TOPIC_NAME,
            project_id=settings.GOOGLE_PROJECT_ID
        )

        logger.info(
            'Product successfully approved sku:{} seller:{}'.format(
                sku, seller_id
            )
        )

        self.write_response(response, falcon.HTTP_200)


class PendingSellerHandler(BaseHandler):

    def on_get(self, request, response):
        sellers = PendingProductModel.objects.distinct('seller_id')
        self.write_response(response, falcon.HTTP_200, {'data': sellers})
