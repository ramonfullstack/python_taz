import pytest

from taz import constants


@pytest.fixture
def save_score_weights(mongo_database):
    payloads = [
        {
            'entity_name': constants.SCORE_DEFAULT_ENTITY,
            'criteria_name': constants.SCORE_TITLE_CRITERIA,
            'weight': 30,
            'score_version': '0.2.0'
        },
        {
            'entity_name': constants.SCORE_DEFAULT_ENTITY,
            'criteria_name': constants.SCORE_DESCRIPTION_CRITERIA,
            'weight': 30,
            'score_version': '0.2.0'
        },
        {
            'entity_name': 'livros',
            'criteria_name': constants.SCORE_TITLE_CRITERIA,
            'weight': 100,
            'score_version': '0.2.0'
        },
        {
            'entity_name': constants.SCORE_DEFAULT_ENTITY,
            'criteria_name': constants.SCORE_TITLE_CRITERIA,
            'weight': 20,
            'score_version': '0.3.0'
        },
        {
            'entity_name': constants.SCORE_DEFAULT_ENTITY,
            'criteria_name': constants.SCORE_FACTSHEET_CRITERIA,
            'weight': 20,
            'score_version': '0.3.0'
        },
    ]

    for payload in payloads:
        mongo_database.score_weights.save(payload)
