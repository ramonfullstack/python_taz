import logging

import falcon
from pymongo import DESCENDING

from taz.api.common.exceptions import NotFound
from taz.api.common.handlers.base import BaseHandler
from taz.consumers.core.database.mongodb import MongodbMixin

logger = logging.getLogger(__name__)


class ProductScoreHandler(BaseHandler, MongodbMixin):

    @property
    def scores(self):
        return self.get_collection('scores')

    def on_get(self, request, response, sku, seller_id):
        show_history = request.params.get('show_history', '') == 'true'
        debug = request.params.get('debug', '') == 'true'

        product_score = self.scores.find_one({
            'sku': sku,
            'seller_id': seller_id,
            'active': True
        })

        if not product_score:
            raise NotFound(
                'Product score not found sku:{sku} '
                'seller_id:{seller_id}'.format(
                    sku=sku,
                    seller_id=seller_id
                )
            )

        data = self._create_score_payload(
            score=product_score['final_score'],
            version=product_score['version'],
            sku=sku,
            seller_id=seller_id
        )

        if debug:
            data['debug'] = product_score

        if show_history:
            data['histories'] = list(self.scores.find({
                'sku': sku,
                'seller_id': seller_id,
                'active': False
            }).sort('timestamp', DESCENDING))

        self.write_response(response, falcon.HTTP_200, {'data': data})

    def _create_score_payload(self, score, version, sku, seller_id):
        payload = {
            'sku': sku,
            'seller_id': seller_id,
            'catalog_average_score': score,
            'version': version
        }

        return payload
