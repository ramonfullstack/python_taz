import importlib
import logging

from simple_settings import settings

from taz.consumers.core.database.mongodb import MongodbMixin

from .helpers import generate_md5
from .product_score_average import ScoreAverageCalculator

logger = logging.getLogger(__name__)


class Score(MongodbMixin):

    def __init__(self):
        self.version = self._get_version().Score()
        self.score_average_calculator = ScoreAverageCalculator()
        self.scores = self.get_collection('scores')

    def calculate(self, product):
        product = self.version.calculate(product)

        sku = product['sku']
        seller_id = product['seller_id']

        score_average = self.score_average_calculator.calculate(
            sku,
            seller_id,
            product['entity_name'],
            product['sources']
        )

        final_score = score_average['product_average_score']

        sources = sorted(
            score_average['sources'],
            key=lambda s: s['criteria']
        )

        product.update({
            'final_score': final_score,
            'sources': sources,
            'active': True,
            'md5': generate_md5(sources)
        })

        product_score = self.scores.find_one({
            'sku': sku,
            'seller_id': seller_id,
            'active': True
        })

        if product_score and product_score.get('md5') == product['md5']:
            logger.info(
                'Discarding product sku:{sku} seller_id:{seller_id} '
                'because it already exists in the database'.format(
                    sku=sku,
                    seller_id=seller_id
                )
            )

            return

        self.scores.update_many(
            {
                'sku': sku,
                'seller_id': seller_id,
                'active': True
            },
            {
                '$set': {'active': False}
            }
        )

        self.scores.insert(product)

        logger.info(
            'Product scored successfully from sku:{sku} '
            'seller_id:{seller_id} '
            'final_score:{final_score}'.format(
                sku=sku,
                seller_id=seller_id,
                final_score=final_score
            )
        )

    def _get_version(self):
        version = 'taz.core.score.versions.v{}.score'.format(
            settings.SCORE_VERSION.replace('.', '_')
        )

        return importlib.import_module(version)
