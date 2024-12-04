import pytest
from simple_settings import settings

from taz import constants
from taz.api.score_criterias.models import ScoreCriteriaModel


@pytest.fixture
def criterias(
    score_criteria_title,
    score_criteria_description
):
    return [
        {
            'entity_name': 'default',
            'elements': [
                score_criteria_title,
                score_criteria_description
            ],
            'score_version': settings.SCORE_VERSION
        },
        {
            'entity_name': 'murcho',
            'elements': [
                {
                    'name': 'title',
                    'type': constants.RANGE_TYPE,
                    'criteria': [
                        {
                            'name': 'greater_than_1_characters',
                            'min': 1,
                            'max': 99999,
                            'points': 100
                        }
                    ]
                }
            ],
            'score_version': settings.SCORE_VERSION
        }
    ]


@pytest.fixture
def save_score_criteria(criterias):
    for criteria in criterias:
        ScoreCriteriaModel(**criteria).save()
