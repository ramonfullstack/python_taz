from simple_settings import settings

from taz import constants
from taz.consumers.core.database.mongodb import MongodbMixin


class ScoreWeight(MongodbMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.score_weights = self.get_collection('score_weights')

    def get(self, entity_name, criteria_name):
        default = self.score_weights.find_one(
            {
                'entity_name': constants.SCORE_DEFAULT_ENTITY,
                'criteria_name': criteria_name,
                'score_version': settings.SCORE_VERSION
            },
            {'_id': 0}
        )

        if not default:
            return 0

        if entity_name != constants.SCORE_DEFAULT_ENTITY:
            entity = self.score_weights.find_one(
                {
                    'entity_name': entity_name,
                    'criteria_name': criteria_name,
                    'score_version': settings.SCORE_VERSION
                },
                {'_id': 0}
            )

            if entity:
                default.update(entity)

        return default.get('weight') or 0
