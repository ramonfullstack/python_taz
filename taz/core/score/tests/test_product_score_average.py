import pytest
from simple_settings import settings

from taz import constants
from taz.core.score.product_score_average import ScoreAverageCalculator


class TestScoreAverageCalculator:

    @pytest.fixture
    def score_average_calculator(self):
        return ScoreAverageCalculator()

    @pytest.fixture
    def entity_name(self):
        return 'Fritadeira'

    @pytest.fixture
    def sources(self):
        return [
            {
                'value': 'Fritadeira Elétrica Air Fryer/Sem Óleo Mondial - AF-14 3,2L Timer',  # noqa
                'points': 50,
                'criteria': 'title::greater_than_60_characters'
            },
            {
                'value': 'O que era inimaginável agora é real, sim, você pode fritar alimentos sem usar óleo, sem deixar cheiro de gordura ou fumaça pela casa, e tem mais, você também pode preparar alimentos de maneira incrivelmente rápida e deixar tudo crocante, gostoso e mais saudável para a sua família!\nCom a incrível Fritadeira Sem Óleo Inox RED Premium da Mondial tudo isso está ao seu alcance.  Painel em aço inox e design sofisticado, lâmpadas-piloto que indicam o funcionamento do produto e do aquecimento, controle de temperatura até 200 ºC para a escolha da temperatura ideal de acordo com diferentes tipos de alimentos, cesta removível segura e prática para facilitar o manuseio dos alimentos, timer de 60 minutos com sinal sonoro e desligamento automático. Com muita praticidade, você pode prepara batatas crocantes em apenas 12 min, e com o livro de receitas você também pode preparar pão de queijo, carnes, aperitivos, peixes, frango a passarinho, pastéis doces e muito mais. \n', # noqa
                'points': 20,
                'criteria': 'description::between_251_and_1000_characters'  # noqa
            }
        ]

    @pytest.fixture
    def save_score_weights(self, mongo_database):
        payload = [
            {
                'entity_name': 'default',
                'criteria_name': 'title',
                'weight': '50',
                'score_version': settings.SCORE_VERSION
            },
            {
                'entity_name': 'default',
                'criteria_name': 'description',
                'weight': '50',
                'score_version': settings.SCORE_VERSION
            }

        ]
        mongo_database.score_weights.insert_many(payload)

    def test_should_calculate_average_score(
        self,
        score_average_calculator,
        save_score_weights,
        entity_name,
        sources
    ):
        payload = score_average_calculator.calculate(
            '023384700',
            constants.MAGAZINE_LUIZA_SELLER_ID,
            entity_name,
            sources
        )

        assert payload['product_total_score'] == 3500.0
        assert payload['product_average_score'] == 35.0
        assert len(payload['sources']) == 2

    def test_should_calculate_zeroed_avg_if_no_score_weights(
        self,
        score_average_calculator,
        sources,
        entity_name
    ):
        payload = score_average_calculator.calculate(
            '023384700',
            constants.MAGAZINE_LUIZA_SELLER_ID,
            entity_name,
            sources
        )

        assert payload['product_total_score'] == 0
        assert payload['product_average_score'] == 0
        assert len(payload['sources']) == 2
