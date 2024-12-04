import json
import logging

import falcon
from simple_settings import settings

from taz.api.common.exceptions import BadRequest, NotFound
from taz.api.common.handlers.base import BaseHandler
from taz.api.common.utils import parse_base64_to_dict
from taz.api.products.models import RawProductModel
from taz.api.sellers.helpers import (
    create_message,
    generate_task_id_with_seller_id_and_scope,
    parse_seller
)
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.google.stream import StreamPublisherManager

logger = logging.getLogger(__name__)


class ListSellerHandler(BaseHandler):
    def on_get(self, request, response):
        seller = RawProductModel.get_sellers()

        self.write_response(response, falcon.HTTP_200, {'data': seller})


class SellerHandler(BaseHandler, MongodbMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pubsub_manager = StreamPublisherManager()

    @property
    def sellers(self):
        return self.get_collection('sellers')

    def on_post(self, request, response):
        payload = request.context.get('message', {}).get('data')

        if not payload:
            raise BadRequest('Invalid payload')

        seller = self._decode_base64_or_raise_bad_request(
            payload
        )

        logger.info(
            'Received seller id:{seller_id}'.format(
                seller_id=seller['id']
            )
        )

        self._notify_rebuilds(seller)
        self._publish(seller)

        criteria = {'id': seller['id']}
        self.sellers.update(criteria, seller, upsert=True)

        self.write_response(response, falcon.HTTP_200)

    def on_get(self, request, response, seller_id):
        seller = self.sellers.find_one(
            {'id': seller_id},
            {'_id': 0, 'api_signature_secret': 0}
        )

        if not seller:
            raise NotFound('Seller {} not found'.format(seller_id))

        content = json.dumps({'data': seller})

        self.write_response(response, falcon.HTTP_200, content)

    def _decode_base64_or_raise_bad_request(self, base64_payload):

        try:
            return parse_base64_to_dict(base64_payload)

        except Exception as e:
            logger.error(
                'Could not parse seller base64 payload to dict '
                'error:{error} payload:{payload}'.format(
                    error=e,
                    payload=base64_payload
                )
            )

            raise BadRequest('Invalid payload')

    def _notify_rebuilds(self, seller):
        seller_id = seller['id']

        saved_seller = self.sellers.find_one(
            {'id': seller_id},
            {'_id': 0, 'is_active': 1, 'sells_to_company': 1}
        )

        if saved_seller:
            task_id_marvin = generate_task_id_with_seller_id_and_scope(
                seller_id=seller_id,
                scope='marvin_seller_ipdv'
            )

            self.pubsub_manager.publish(
                content=create_message(
                    scope='marvin_seller_ipdv',
                    data=seller,
                    task_id=task_id_marvin
                ),
                topic_name=settings.PUBSUB_REBUILD_TOPIC_NAME,
                project_id=settings.GOOGLE_PROJECT_ID
            )

            logger.info(
                'Request to rebuild marvin seller ipdv '
                'for seller:{seller}'.format(
                    seller=seller_id
                )
            )

            if (
                settings.INACTIVATE_SELLER_SKUS_FLOW_ENABLED and
                seller['is_active'] is False
            ):
                task_id = generate_task_id_with_seller_id_and_scope(
                    seller_id=seller_id,
                    scope='inactivate_seller_products'
                )

                data = {'seller_id': seller_id}
                inactive_reason = seller.get('inactive_reason')

                if inactive_reason:
                    data.update({
                        'inactive_reason': inactive_reason
                    })

                self.pubsub_manager.publish(
                    content=create_message(
                        scope='inactivate_seller_products',
                        data=data,
                        task_id=task_id
                    ),
                    topic_name=settings.PUBSUB_REBUILD_TOPIC_NAME,
                    project_id=settings.GOOGLE_PROJECT_ID
                )

                logger.info(
                    'Request to rebuild inactive seller products '
                    'for seller:{seller}'.format(
                        seller=seller_id
                    )
                )

            old_sells_to_company = saved_seller.get('sells_to_company', False)
            new_sells_to_company = seller.get('sells_to_company')

            if old_sells_to_company != new_sells_to_company:
                task_id_company = generate_task_id_with_seller_id_and_scope(
                    seller_id=seller_id,
                    scope='seller_sells_to_company'
                )

                self.pubsub_manager.publish(
                    content=create_message(
                        scope='seller_sells_to_company',
                        data=seller,
                        task_id=task_id_company
                    ),
                    topic_name=settings.PUBSUB_REBUILD_TOPIC_NAME,
                    project_id=settings.GOOGLE_PROJECT_ID
                )

                logger.info(
                    'Request to rebuild products of seller:{seller} because '
                    'the sells_to_company information has changed'.format(
                        seller=seller_id
                    )
                )

    def _publish(self, seller):
        try:
            payload = parse_seller(seller)

            self.pubsub_manager.publish(
                content=payload,
                topic_name=settings.PUBSUB_TOPIC_TAZ_SELLERS
            )
        except KeyError as e:
            logger.error(
                'Error in publish message in {topic} '
                'because exception:{error}'.format(
                    topic=settings.PUBSUB_TOPIC_TAZ_SELLERS,
                    error=e
                )
            )
