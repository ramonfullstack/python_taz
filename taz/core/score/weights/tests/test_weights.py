import pytest
from simple_settings.utils import settings_stub

from taz import constants
from taz.core.score.weights import ScoreWeight


class TestScoreWeight:

    @pytest.fixture
    def score_weight(self):
        return ScoreWeight()

    @pytest.mark.parametrize('entity, criteria_name, expected', [
        (
            'murcho',
            constants.SCORE_TITLE_CRITERIA,
            30
        ),
        (
            'livros',
            constants.SCORE_TITLE_CRITERIA,
            100
        ),
        (
            constants.SCORE_DEFAULT_ENTITY,
            'criteria_name_not_exists',
            0
        ),
        (
            constants.SCORE_DEFAULT_ENTITY,
            constants.SCORE_TITLE_CRITERIA,
            30
        ),
        (
            constants.SCORE_DEFAULT_ENTITY,
            constants.SCORE_DESCRIPTION_CRITERIA,
            30
        ),
        (
            constants.SCORE_DEFAULT_ENTITY,
            constants.SCORE_IMAGES_CRITERIA,
            30
        ),
        (
            constants.SCORE_DEFAULT_ENTITY,
            constants.SCORE_REVIEW_COUNT_CRITERIA,
            5
        ),
        (
            constants.SCORE_DEFAULT_ENTITY,
            constants.SCORE_REVIEW_RATING_CRITERIA,
            5
        )
    ])
    def test_get_weights_with_score_v2(
        self,
        save_weights,
        score_weight,
        entity,
        criteria_name,
        expected
    ):
        payload = score_weight.get(entity, criteria_name)
        assert payload == expected

    @pytest.mark.parametrize('entity, criteria_name, expected', [
        (
            'murcho',
            constants.SCORE_TITLE_CRITERIA,
            20
        ),
        (
            'livros',
            constants.SCORE_TITLE_CRITERIA,
            100
        ),
        (
            constants.SCORE_DEFAULT_ENTITY,
            'criteria_name_not_exists',
            0
        ),
        (
            constants.SCORE_DEFAULT_ENTITY,
            constants.SCORE_TITLE_CRITERIA,
            20
        ),
        (
            constants.SCORE_DEFAULT_ENTITY,
            constants.SCORE_DESCRIPTION_CRITERIA,
            20
        ),
        (
            constants.SCORE_DEFAULT_ENTITY,
            constants.SCORE_IMAGES_CRITERIA,
            20
        ),
        (
            constants.SCORE_DEFAULT_ENTITY,
            constants.SCORE_FACTSHEET_CRITERIA,
            20
        ),
        (
            constants.SCORE_DEFAULT_ENTITY,
            constants.SCORE_REVIEW_COUNT_CRITERIA,
            10
        ),
        (
            constants.SCORE_DEFAULT_ENTITY,
            constants.SCORE_REVIEW_RATING_CRITERIA,
            10
        )
    ])
    @settings_stub(SCORE_VERSION='0.3.0')
    def test_get_weights_with_score_v3(
        self,
        save_weights,
        score_weight,
        entity,
        criteria_name,
        expected
    ):
        payload = score_weight.get(entity, criteria_name)
        assert payload == expected

    def test_default_entity_not_exists_returns_zero(
        self,
        score_weight
    ):
        payload = score_weight.get(
            constants.SCORE_DEFAULT_ENTITY,
            constants.SCORE_TITLE_CRITERIA
        )

        assert payload == 0
