import logging

from mongoengine import DynamicDocument

logger = logging.getLogger(__name__)


class ScoreCriteriaModel(DynamicDocument):
    meta = {
        'collection': 'score_criterias'
    }
