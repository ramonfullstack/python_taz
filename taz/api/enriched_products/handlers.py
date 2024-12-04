import logging
from functools import cached_property

import falcon
from simple_settings import settings

from taz.api.common.exceptions import NotFound
from taz.api.common.handlers.base import BaseHandler
from taz.api.middlewares.authorization_owner import AuthOwner
from taz.constants import (
    DELETE_ACTION,
    SOURCE_DATASHEET,
    SOURCE_GENERIC_CONTENT,
    SOURCE_METABOOKS,
    SOURCE_RECLASSIFICATION_PRICE_RULE,
    UPDATE_ACTION
)
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.google.stream import StreamPublisherManager
from taz.consumers.core.notification import Notification
from taz.utils import cut_product_id, md5

logger = logging.getLogger(__name__)


class EnrichedProductsHandler(BaseHandler, MongodbMixin):

    def on_get(self, request, response, navigation_id):

        criteria = {
            '$or': [
                {'navigation_id': navigation_id},
                {'navigation_id': cut_product_id(navigation_id)}
            ]
        }

        results = self.get_collection('enriched_products').find(criteria)
        results = list(results)

        if not results:
            logger.warning(
                'Could not find enriched product for '
                'navigation id:{nav}'.format(
                    nav=navigation_id
                )
            )
            self.write_response(response, falcon.HTTP_404)
            return

        self.write_response(response, falcon.HTTP_200, {'data': results})


class EnrichedSellerProductsHandler(BaseHandler, MongodbMixin):

    def on_get(self, request, response, sku, seller_id):
        criteria = {'sku': sku, 'seller_id': seller_id}

        results = self.get_collection('enriched_products').find(criteria)
        results = list(results)

        if not results:
            logger.warning(
                'Could not find enriched product for '
                'sku:{sku} and seller:{seller}'.format(
                    sku=sku,
                    seller=seller_id
                )
            )
            self.write_response(response, falcon.HTTP_404)
            return

        self.write_response(response, falcon.HTTP_200, {'data': results})


class EnrichedSourceHandler(BaseHandler, MongodbMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @cached_property
    def enriched_products(self):
        return self.get_collection('enriched_products')

    @cached_property
    def raw_products(self):
        return self.get_collection('raw_products')

    @cached_property
    def notification(self):
        return Notification()

    @cached_property
    def pubsub_manager(self):
        return StreamPublisherManager()

    def on_get(self, request, response, navigation_id, source):
        product = self.raw_products.find_one(
            {'navigation_id': navigation_id},
            {'_id': 0, 'sku': 1, 'seller_id': 1}
        )

        if not product:
            logger.warning(
                f'Product with navigation_id:{navigation_id}'
                'not found in raw products'
            )
            raise NotFound()

        enriched_product = self.enriched_products.find_one(
            {
                'sku': product['sku'],
                'seller_id': product['seller_id'],
                'source': source
            },
            {'_id': 0}
        )

        if not enriched_product:
            logger.warning(
                'Product with sku:{sku} and seller_id:{seller_id}'
                'not found in enriched products'.format(
                    sku=product['sku'],
                    seller_id=product['seller_id']
                )
            )
            raise NotFound()

        self.write_response(response, falcon.HTTP_200, enriched_product)

    @AuthOwner(
        allowed_owners=settings.ALLOWED_OWNERS_TO_DELETE_ENRICHED_SOURCE
    )
    def on_delete(self, request, response, seller_id, sku, source):
        criteria = {'sku': sku, 'seller_id': seller_id, 'source': source}

        if source == SOURCE_GENERIC_CONTENT:
            enriched = self.enriched_products.find_one(
                criteria,
                {'_id': 0, 'timestamp': 0, 'md5': 0}
            )

            if not enriched:
                logger.error(
                    f'enriched product with sku:{sku} seller_id:{seller_id} '
                    f'and source:{source} not found'
                )
                raise NotFound()

            enriched.update({'active': False})
            new_md5 = md5(enriched)

            result = self.enriched_products.update_one(
                criteria,
                {'$set': {'active': False, 'md5': new_md5}}
            )
            success = result.modified_count > 0
        else:
            result = self.enriched_products.delete_one(criteria)
            success = result.deleted_count > 0

        if not success:
            logger.error(
                'Could not delete enriched_products '
                f'source:{source} for seller_id:{seller_id} sku:{sku}'
            )
            raise NotFound()

        logger.info(
            'Successfully deleted enriched_products '
            f'source:{source} for seller_id:{seller_id} sku:{sku}'
        )
        self._notify(seller_id, sku, source)
        self.write_response(response, falcon.HTTP_204)

    def _notify(self, seller_id: str, sku: str, source: str) -> None:
        data = {
            'seller_id': seller_id,
            'sku': sku,
            'source': source
        }

        if source in [SOURCE_DATASHEET, SOURCE_METABOOKS]:
            payload = {
                'scope': 'maas_product_reprocess',
                'action': UPDATE_ACTION,
                'data': data
            }

            self.pubsub_manager.publish(
                content=payload,
                topic_name=settings.PUBSUB_REBUILD_TOPIC_NAME,
                project_id=settings.GOOGLE_PROJECT_ID,
                attributes=payload.get('data')
            )
        elif source in [
            SOURCE_GENERIC_CONTENT,
            SOURCE_RECLASSIFICATION_PRICE_RULE
        ]:
            self.notification.put(
                data=data,
                scope='enriched_product',
                action=DELETE_ACTION
            )
