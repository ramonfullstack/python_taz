import logging
import time

import falcon

from taz.api.common.exceptions import NotFound
from taz.api.common.handlers.base import BaseHandler
from taz.consumers.core.database.mongodb import MongodbMixin

logger = logging.getLogger(__name__)


class CategoryScoreHandler(BaseHandler, MongodbMixin):

    @property
    def scores(self):
        return self.get_collection('scores')

    @property
    def categories(self):
        return self.get_collection('categories')

    def on_get(self, request, response, category_id):
        category_id = category_id.upper()

        category_average_score = self.scores.aggregate([
            {
                '$match': {'active': True, 'category_id': category_id},
            },
            {
                '$group': {
                    '_id': None,
                    'count': {'$sum': 1},
                    'avg_score': {'$avg': '$final_score'}
                }
            }
        ])

        try:
            category_average_score = category_average_score.next()
        except StopIteration:
            raise NotFound('Score not found for category:{category_id}'.format(
                category_id=category_id
            ))

        data = {
            'category_id': category_id,
            'catalog_average_score': category_average_score['avg_score'],
            'catalog_score_count': category_average_score['count'],
            'category_description': self._get_category_description(
                category_id
            ),
            'timestamp': time.time()
        }

        self.write_response(response, falcon.HTTP_200, {'data': data})

    def _get_category_description(self, category_id):
        description = ''
        category = self.categories.find_one({'id': category_id})
        if category:
            description = category['description']

        return description
