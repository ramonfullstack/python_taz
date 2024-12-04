import logging

from simple_settings import settings

from taz.consumers.core.database.mongodb import MongodbMixin
from taz.core.score.helpers import (
    get_weights_and_scores_by_criteria_and_entity
)
from taz.core.score.weights import ScoreWeight

logger = logging.getLogger(__name__)


class ScoreAverageCalculator(MongodbMixin):

    def __init__(self):
        self.score_weight = ScoreWeight()

    @property
    def score_points(self):  # pragma: no cover
        return self.get_collection('score_points')

    @property
    def enriched_products(self):  # pragma: no cover
        return self.get_collection('enriched_products')

    def calculate(
        self,
        sku,
        seller_id,
        entity_name,
        sources,
        score_version=None
    ):
        score_version = score_version or settings.SCORE_VERSION

        logger.debug(
            'Starting calculating score for sku:{sku} '
            'seller_id:{seller_id} '
            'score_version:{score_version}'.format(
                sku=sku,
                seller_id=seller_id,
                score_version=score_version
            )
        )

        sources = get_weights_and_scores_by_criteria_and_entity(
            criteria_values=sources,
            entity=entity_name
        )

        total_and_average = self._calculate_average_and_total_score(sources)

        average_score = total_and_average
        average_score['sources'] = list(sources.values())

        return average_score

    def _calculate_average_and_total_score(self, sources):
        total_score = 0
        average = 0

        for weight_and_score in sources.values():
            score = weight_and_score['points']
            weight = weight_and_score['weight']

            total_score += score * weight

        if total_score > 0:
            average = round(total_score / 100, 2)

        return {
            'product_total_score': total_score,
            'product_average_score': average
        }

    def _get_weights_by_criteria(self, sources, entity):
        weight_criterias = {}

        for source in sources:
            criteria = source['criteria'].split('::')[0]

            score = self.score_weight.get(
                entity_name=entity,
                criteria_name=criteria
            )

            weight_criterias[criteria] = float(score)

        return weight_criterias

    def _format_score_version(self, version):
        return 'v' + version.replace('.', '_')
