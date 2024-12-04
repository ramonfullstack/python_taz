import logging
import time
from concurrent.futures import ThreadPoolExecutor, wait

import falcon

from taz.api.common.exceptions import NotFound
from taz.api.common.handlers.base import BaseHandler
from taz.consumers.core.database.mongodb import MongodbMixin

logger = logging.getLogger(__name__)


class CatalogScoreHandler(BaseHandler, MongodbMixin):

    @property
    def scores(self):
        return self.get_collection('scores')

    def on_get(self, request, response):
        aggregation = [
            {
                '$match': {'active': True},
            },
            {
                '$group': {
                    '_id': None,
                    'count': {'$sum': 1},
                    'average': {
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
        ]

        category_aggregation = [
            {
                '$match': {'active': True},
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

        with ThreadPoolExecutor(max_workers=2) as executor:
            catalog_average_score = executor.submit(
                self.retrieve_aggregate_score,
                aggregation
            )
            category_average_score = executor.submit(
                self.retrieve_aggregate_score,
                category_aggregation
            )

        wait([catalog_average_score, category_average_score])

        try:
            catalog_average_score = catalog_average_score.result().next()
            category_average_score = list(category_average_score.result())
            categories_description = self.get_collection('categories').find({
                '$or': [
                    {'id': category['category_id']}
                    for category in category_average_score
                ]
            }, {'description': 1, 'id': 1, '_id': 0})
            categories_description = list(categories_description)

            for category in category_average_score:
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
            raise NotFound('Score not found for catalog')

        res = {
            'catalog_average_score': catalog_average_score['average'],
            'catalog_score_count': catalog_average_score['count'],
            'timestamp': time.time(),
            'categories': category_average_score
        }

        self.write_response(response, falcon.HTTP_200, {'data': res})

    def retrieve_aggregate_score(self, aggregation):
        start_time = time.time()
        score = self.scores.aggregate(aggregation)

        logger.info(
            'Time elapsed to retrieve score aggregation:{time_spent}s '
            'with query:{query}'.format(
                time_spent='{0:.3f}'.format(time.time() - start_time),
                query=aggregation
            )
        )

        return score
