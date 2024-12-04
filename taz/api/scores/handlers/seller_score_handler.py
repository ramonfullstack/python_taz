import logging
import time

import falcon

from taz.api.common.exceptions import NotFound
from taz.api.common.handlers.base import BaseHandler
from taz.consumers.core.database.mongodb import MongodbMixin

logger = logging.getLogger(__name__)


class SellerScoreHandler(BaseHandler, MongodbMixin):

    @property
    def scores(self):
        return self.get_collection('scores')

    def on_get(self, request, response, seller_id):

        seller_average_score = self.scores.aggregate([
            {
                '$match': {'active': True, 'seller_id': seller_id},
            },
            {
                '$group': {
                    '_id': None,
                    'count': {'$sum': 1},
                    'avg_score': {
                        '$avg': {
                            '$divide': [
                                {
                                    '$trunc': {
                                        '$multiply': ['$final_score', 100]
                                    }
                                }, 100]
                        }
                    }
                }
            }
        ])

        seller_category_aggregation = [
            {
                '$match': {'active': True, 'seller_id': seller_id},
            },
            {
                '$group': {
                    '_id': {'category_id': '$category_id'},
                    'count': {'$sum': 1},
                    'average': {
                        '$avg': {
                            '$divide': [{
                                '$trunc': {
                                    '$multiply': [
                                        '$final_score', 100
                                    ]}
                            }, 100]
                        }
                    }
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'category_id': '$_id.category_id',
                    'catalog_average_score': '$average',
                    'catalog_score_count': '$count'
                }
            },
            {
                '$sort': {
                    'catalog_average_score': -1
                }
            }
        ]

        seller_category_average_score = self.scores.aggregate(
            seller_category_aggregation
        )
        try:
            seller_average_score = seller_average_score.next()
            seller_category_average_score = list(seller_category_average_score)
            categories_description = self.get_collection('categories').find({
                '$or': [
                    {'id': category['category_id']}
                    for category in seller_category_average_score
                ]
            }, {'description': 1, 'id': 1, '_id': 0})
            categories_description = list(categories_description)

            for category in seller_category_average_score:
                category_description = next(
                    (
                        description for description in categories_description
                        if description['id'] == category['category_id']
                    ), {}
                )
                category['category_description'] = (
                    category_description.get('description') or
                    '-'
                )
        except StopIteration:
            raise NotFound('Score not found for seller:{seller_id}'.format(
                seller_id=seller_id
            ))

        data = {
            'seller_id': seller_id,
            'catalog_average_score': seller_average_score['avg_score'],
            'catalog_score_count': seller_average_score['count'],
            'categories': seller_category_average_score,
            'timestamp': time.time()
        }

        self.write_response(response, falcon.HTTP_200, {'data': data})
