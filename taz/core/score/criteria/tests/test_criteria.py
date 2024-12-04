import pytest
from simple_settings import settings
from simple_settings.utils import settings_stub

from taz import constants
from taz.core.score.criteria import ScoreCriteria


class TestScoreCriteria:

    @pytest.fixture
    def score_criteria(self):
        return ScoreCriteria()

    @settings_stub(SCORE_VERSION='0.3.0')
    @pytest.mark.parametrize('entity, criteria_name, value, expected_points, expected_name', [  # noqa
        (
            'default',
            'None',
            1,
            0,
            None
        ),
        (
            'Guarda-Roupa',
            constants.SCORE_TITLE_CRITERIA,
            'Guarda-roupa Casal 3 Portas Madesa - City 1056-1E com Espelho',
            50,
            'title::greater_than_60_characters'
        ),
        (
            'Guarda-Roupa',
            constants.SCORE_TITLE_CRITERIA,
            'Guarda-roupa Casal 3 Portas Madesa - City',
            30,
            'title::between_31_and_60_characters'
        ),
        (
            'Guarda-Roupa',
            constants.SCORE_TITLE_CRITERIA,
            'Guarda-roupa Casal 3 Portas',
            20,
            'title::between_1_and_30_characters'
        ),
        (
            'Murcho',
            constants.SCORE_TITLE_CRITERIA,
            'Guarda-roupa Casal 3 Portas',
            100,
            'title::greater_than_1_characters'
        ),
        (
            'Guarda-Roupa',
            constants.SCORE_DESCRIPTION_CRITERIA,
            'Com os móveis da Madesa sua casa vai ficar mais bonita e organizada. Isso porque ele tem beleza e qualidade em só produto.',  # noqa
            20,
            'description::between_1_and_250_characters'
        ),
        (
            'Guarda-Roupa',
            constants.SCORE_DESCRIPTION_CRITERIA,
            'Com os móveis da Madesa sua casa vai ficar mais bonita e organizada. Isso porque ele tem beleza e qualidade em só produto. Com sistema de montagem de parafusos, cavilha e minifix, possui material em MDP e três portas de correr. Que são ideais para quem precisa de organização porém não tem muito espaço. Tem acabamento fosco e espelho na porta do meio. E tudo isso com material ecologicamente correto que garantem a beleza e qualidade do produto. Leve agora esse guarda-roupa e tenha o melhor da Madesa na sua casa.',  # noqa
            20,
            'description::between_251_and_1000_characters'
        ),
        (
            'Guarda-Roupa',
            constants.SCORE_DESCRIPTION_CRITERIA,
            'Com os móveis da Madesa sua casa vai ficar mais bonita e organizada. Isso porque ele tem beleza e qualidade em só produto. Com sistema de montagem de parafusos, cavilha e minifix, possui material em MDP e três portas de correr. Que são ideais para quem precisa de organização porém não tem muito espaço. Tem acabamento fosco e espelho na porta do meio. E tudo isso com material ecologicamente correto que garantem a beleza e qualidade do produto. Leve agora esse guarda-roupa e tenha o melhor da Madesa na sua casa. Com os móveis da Madesa sua casa vai ficar mais bonita e organizada. Isso porque ele tem beleza e qualidade em só produto. Com sistema de montagem de parafusos, cavilha e minifix, possui material em MDP e três portas de correr. Que são ideais para quem precisa de organização porém não tem muito espaço. Tem acabamento fosco e espelho na porta do meio. E tudo isso com material ecologicamente correto que garantem a beleza e qualidade do produto. Leve agora esse guarda-roupa e tenha o melhor da Madesa na sua casa.',  # noqa
            60,
            'description::greater_than_1000_characters'
        ),
        (
            'Murcho',
            constants.SCORE_DESCRIPTION_CRITERIA,
            'Com os móveis da Madesa sua casa vai ficar mais bonita e organizada. ',  # noqa
            100,
            'description::greater_than_1000_characters'
        ),
        (
            'Guarda-Roupa',
            constants.SCORE_IMAGES_CRITERIA,
            1,
            20,
            'images::equals_1'
        ),
        (
            'Guarda-Roupa',
            constants.SCORE_IMAGES_CRITERIA,
            3,
            30,
            'images::between_2_and_3_images'
        ),
        (
            'Guarda-Roupa',
            constants.SCORE_IMAGES_CRITERIA,
            5,
            50,
            'images::greater_than_3_images'
        ),
        (
            'Murcho',
            constants.SCORE_IMAGES_CRITERIA,
            1,
            100,
            'images::greater_than_1_image'
        ),
        (
            'Guarda-Roupa',
            constants.SCORE_REVIEW_COUNT_CRITERIA,
            1,
            20,
            'review_count::between_1_and_2_reviews_count'
        ),
        (
            'Guarda-Roupa',
            constants.SCORE_REVIEW_COUNT_CRITERIA,
            3,
            30,
            'review_count::between_3_and_6_reviews_count'
        ),
        (
            'Guarda-Roupa',
            constants.SCORE_REVIEW_COUNT_CRITERIA,
            7,
            50,
            'review_count::greater_than_6_reviews_count'
        ),
        (
            'Murcho',
            constants.SCORE_REVIEW_COUNT_CRITERIA,
            1,
            100,
            'review_count::greater_than_1_reviews_count'
        ),
        (
            'Guarda-Roupa',
            constants.SCORE_REVIEW_RATING_CRITERIA,
            1,
            20,
            'review_rating::between_1_and_2_reviews_rating'
        ),
        (
            'Guarda-Roupa',
            constants.SCORE_REVIEW_RATING_CRITERIA,
            3,
            30,
            'review_rating::equals_3_reviews_rating'
        ),
        (
            'Guarda-Roupa',
            constants.SCORE_REVIEW_RATING_CRITERIA,
            4,
            50,
            'review_rating::greater_than_4_reviews_rating'
        ),
        (
            'Murcho',
            constants.SCORE_REVIEW_RATING_CRITERIA,
            2,
            100,
            'review_rating::greater_than_1_reviews_rating'
        ),
        (
            'Guarda-Roupa',
            constants.SCORE_FACTSHEET_CRITERIA,
            7,
            30,
            'factsheet::between_1_and_7_attributes'
        ),
        (
            'Guarda-Roupa',
            constants.SCORE_FACTSHEET_CRITERIA,
            10,
            60,
            'factsheet::between_8_and_10_attributes'
        ),
        (
            'Guarda-Roupa',
            constants.SCORE_FACTSHEET_CRITERIA,
            11,
            100,
            'factsheet::greater_than_10_attributes'
        )
    ])
    def test_get_score_criteria(
        self,
        score_criteria,
        save_score_criteria,
        entity,
        criteria_name,
        value,
        expected_points,
        expected_name
    ):
        points, name = score_criteria.get(entity, criteria_name, value)

        assert points == expected_points
        assert name == expected_name

    @pytest.mark.parametrize('entity_name, expected_count', [
        ('livro', 6),
        ('default', 6),
    ])
    def test_should_get_entity(
        self,
        score_criteria,
        save_score_criteria,
        entity_name,
        expected_count,
        mongo_database
    ):

        book = {
            'entity_name': 'livro',
            'elements': [
                {
                    'name': 'images',
                    'type': 'range',
                    'criteria': [
                        {
                            'name': 'greater_than_1_images',
                            'min': 1,
                            'points': 100
                        }
                    ]
                }
            ],
            'score_version': settings.SCORE_VERSION
        }

        mongo_database.score_criterias.save(book)

        entity = score_criteria._get_entity(entity_name)
        assert len(entity['elements']) == expected_count
