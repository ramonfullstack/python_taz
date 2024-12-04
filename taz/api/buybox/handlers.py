import logging

import falcon

from taz import constants
from taz.api.common.exceptions import NotFound
from taz.api.common.handlers.base import BaseHandler
from taz.api.correlations.models import CorrelationModel
from taz.api.prices.models import PriceModel
from taz.api.products.models import RawProductModel
from taz.api.unified_objects.models import UnifiedObjectModel

logger = logging.getLogger(__name__)


class BuyBoxHandler(BaseHandler):
    def on_get(self, request, response, seller_id, sku):
        logger.info(
            'Get buybox detail from sku:{sku} seller_id:{seller_id}'.format(
                sku=sku,
                seller_id=seller_id
            )
        )

        id_correlation = CorrelationModel.get(seller_id, sku)
        if not id_correlation:
            raise NotFound(
                'Correlation not found for sku:{sku} '
                'seller_id:{seller_id}'.format(
                    sku=sku,
                    seller_id=seller_id
                )
            )

        product_id = id_correlation['product_id']

        unified_object = UnifiedObjectModel.get(product_id)
        if not unified_object:
            raise NotFound(
                'Unified objects not found for sku:{sku} '
                'seller_id:{seller_id} product_id:{product_id}'.format(
                    sku=sku,
                    seller_id=seller_id,
                    product_id=product_id
                )
            )

        for variation in unified_object['variations']:
            for seller in variation['sellers']:
                price = PriceModel.get_price(seller['id'], seller['sku'])
                seller.update(**price)

        self.write_response(
            response,
            falcon.HTTP_200,
            {'data': unified_object}
        )


class BuyBoxSellerHandler(BaseHandler):
    def on_get(self, request, response):
        sellers = RawProductModel.get_sellers_by_strategy(
            constants.AUTO_BUYBOX_STRATEGY
        )

        self.write_response(response, falcon.HTTP_200, {'data': sellers})


class BuyBoxProductListHandler(BaseHandler):
    def on_get(self, request, response, seller_id):
        products = RawProductModel.product_list_by_strategy_and_seller(
            constants.AUTO_BUYBOX_STRATEGY,
            seller_id
        )

        self.write_response(response, falcon.HTTP_200, {'data': products})
