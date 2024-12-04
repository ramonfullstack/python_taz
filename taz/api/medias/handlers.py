import logging

import falcon

from taz.api.common.exceptions import NotFound
from taz.api.common.handlers.base import BaseHandler
from taz.api.products.models import RawProductModel
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.core.common.media import _build_images

logger = logging.getLogger(__name__)


class ProductMediasSkuSellerHandler(BaseHandler, MongodbMixin):

    def on_get(self, request, response, sku, seller):

        product = RawProductModel.get_product(
            sku=sku,
            seller_id=seller
        )

        if not product:
            logger.warning(
                'Product not found in raw products '
                'sku:{sku} seller_id:{seller_id}'
            ).format(
                sku=sku,
                seller_id=seller
            )
            raise NotFound('Product not found')

        payload = {}

        images = _build_images(product, self.get_collection('medias'))

        if not images:
            logger.warning(
                'Images not found for sku:{sku} seller_id:{seller_id}'
                .format(
                    sku=product['sku'],
                    seller_id=product['seller_id']
                )
            )
            raise NotFound('Images not found')

        payload['images'] = images

        self.write_response(
            response,
            falcon.HTTP_200,
            {
                'data': payload
            }
        )


class ProductMediasNavigationIdHandler(BaseHandler, MongodbMixin):

    def on_get(self, request, response, navigation_id):

        product = RawProductModel.get_product_by_navigation_id(
            navigation_id=navigation_id
        )

        if not product:
            logger.warning(
                'Product not found '
                'in raw products navigation_id:{navigation_id}'
            ).format(
                navigation_id=navigation_id
            )
            raise NotFound('Product not found')

        payload = {}

        images = _build_images(product, self.get_collection('medias'))

        if not images:
            logger.warning(
                'Images not found for sku:{sku} seller_id:{seller_id}'
                .format(
                    sku=product['sku'],
                    seller_id=product['seller_id']
                )
            )
            raise NotFound('Images not found')

        payload['images'] = images

        self.write_response(
            response,
            falcon.HTTP_200,
            {
                'data': payload
            }
        )
