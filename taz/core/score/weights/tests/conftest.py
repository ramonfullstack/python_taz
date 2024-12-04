import copy

import pytest

from taz import constants


@pytest.fixture
def save_weights(mongo_database):
    weight = [
        {
            'entity_name': constants.SCORE_DEFAULT_ENTITY,
            'criteria_name': constants.SCORE_TITLE_CRITERIA
        },
        {
            'entity_name': constants.SCORE_DEFAULT_ENTITY,
            'criteria_name': constants.SCORE_DESCRIPTION_CRITERIA
        },
        {
            'entity_name': constants.SCORE_DEFAULT_ENTITY,
            'criteria_name': constants.SCORE_IMAGES_CRITERIA
        },
        {
            'entity_name': constants.SCORE_DEFAULT_ENTITY,
            'criteria_name': constants.SCORE_REVIEW_COUNT_CRITERIA
        },
        {
            'entity_name': constants.SCORE_DEFAULT_ENTITY,
            'criteria_name': constants.SCORE_REVIEW_RATING_CRITERIA
        },
        {
            'entity_name': 'livros',
            'criteria_name': constants.SCORE_TITLE_CRITERIA
        }
    ]

    weight_score_v2 = [30, 30, 30, 5, 5, 100]
    weight_score_v3 = [20, 20, 20, 10, 10, 100, 20]

    weight_v3 = copy.deepcopy(weight)
    weight_v3.append({
        'entity_name': constants.SCORE_DEFAULT_ENTITY,
        'criteria_name': constants.SCORE_FACTSHEET_CRITERIA
    })

    for index, value in enumerate(weight):
        value['score_version'] = '0.2.0'
        value['weight'] = weight_score_v2[index]
        mongo_database.score_weights.save(value)

    for index, value in enumerate(weight_v3):
        value['score_version'] = '0.3.0'
        value['weight'] = weight_score_v3[index]
        mongo_database.score_weights.save(value)
