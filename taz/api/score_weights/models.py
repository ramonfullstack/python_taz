import logging

from mongoengine import DynamicDocument

logger = logging.getLogger(__name__)


class ScoreWeightModel(DynamicDocument):
    meta = {
        'collection': 'score_weights'
    }
