import pytest

from taz import constants
from taz.core.matching.common.enriched_products import EnrichedProductSamples
from taz.core.matching.common.samples import ProductSamples
from taz.core.score.helpers import create_payload
from taz.core.score.versions.v0_2_0 import Score


class TestScoreV2:

    @pytest.fixture
    def score(self):
        return Score()

    @pytest.fixture
    def product(self):
        product = ProductSamples.magazineluiza_sku_0233847()
        enriched = EnrichedProductSamples.magazineluiza_sku_0233847()

        media = {
            'images': [
                'd2e14e48997a911745931e6a2991b2cf.jpg'
            ],
            'seller_id': product['seller_id'],
            'sku': product['sku']
        }

        customer_behaviors = [{
            'product_id': product['navigation_id'],
            'type': constants.META_TYPE_PRODUCT_TOTAL_REVIEW_COUNT,
            'value': 658
        }, {
            'product_id': product['navigation_id'],
            'type': constants.META_TYPE_PRODUCT_AVERAGE_RATING,
            'value': 4.730769230769231
        }]

        return create_payload(product, enriched, media, customer_behaviors)

    def test_when_entity_is_empty_then_should_skip_process(
        self,
        score,
        product,
        caplog
    ):
        del product['entity']
        response = score.calculate(product)

        message = 'Entity not found for sku:{} seller_id:{}'.format(
            product['sku'],
            product['seller_id']
        )

        assert not response
        assert message in caplog.text

    def test_should_calculate_without_full_title(
        self,
        score,
        product,
        save_score_criteria,
        mongo_database
    ):
        del product['full_title']
        payload = score.calculate(product)

        assert payload['sources'] == [{
            'value': 'O que era inimaginável agora é real, sim, você pode fritar alimentos sem usar óleo, sem deixar cheiro de gordura ou fumaça pela casa, e tem mais, você também pode preparar alimentos de maneira incrivelmente rápida e deixar tudo crocante, gostoso e mais saudável para a sua família!Com a incrível Fritadeira Sem Óleo Inox RED Premium da Mondial tudo isso está ao seu alcance. Painel em aço inox e design sofisticado, lâmpadas-piloto que indicam o funcionamento do produto e do aquecimento, controle de temperatura até 200 ºC para a escolha da temperatura ideal de acordo com diferentes tipos de alimentos, cesta removível segura e prática para facilitar o manuseio dos alimentos, timer de 60 minutos com sinal sonoro e desligamento automático. Com muita praticidade, você pode prepara batatas crocantes em apenas 12 min, e com o livro de receitas você também pode preparar pão de queijo, carnes, aperitivos, peixes, frango a passarinho, pastéis doces e muito mais.',  # noqa
            'criteria': 'description::between_251_and_1000_characters',
            'points': 20
        }, {
            'value': 1,
            'criteria': 'images::equals_1',
            'points': 20
        }, {
            'value': 658,
            'criteria': 'review_count::greater_than_6_reviews_count',
            'points': 50
        }, {
            'value': 4.730769230769231,
            'criteria': 'review_rating::greater_than_4_reviews_rating',
            'points': 50
        }]

    def test_calculate_score(
        self,
        score,
        product,
        save_score_criteria,
        mongo_database
    ):
        payload = score.calculate(product)

        assert payload['sources'] == [{
            'points': 50,
            'value': 'Fritadeira Elétrica Air Fryer/Sem Óleo Mondial - AF-14 3,2L Timer',  # noqa
            'criteria': 'title::greater_than_60_characters'
        }, {
            'points': 20,
            'value': 'O que era inimaginável agora é real, sim, você pode fritar alimentos sem usar óleo, sem deixar cheiro de gordura ou fumaça pela casa, e tem mais, você também pode preparar alimentos de maneira incrivelmente rápida e deixar tudo crocante, gostoso e mais saudável para a sua família!Com a incrível Fritadeira Sem Óleo Inox RED Premium da Mondial tudo isso está ao seu alcance. Painel em aço inox e design sofisticado, lâmpadas-piloto que indicam o funcionamento do produto e do aquecimento, controle de temperatura até 200 ºC para a escolha da temperatura ideal de acordo com diferentes tipos de alimentos, cesta removível segura e prática para facilitar o manuseio dos alimentos, timer de 60 minutos com sinal sonoro e desligamento automático. Com muita praticidade, você pode prepara batatas crocantes em apenas 12 min, e com o livro de receitas você também pode preparar pão de queijo, carnes, aperitivos, peixes, frango a passarinho, pastéis doces e muito mais.',  # noqa
            'criteria': 'description::between_251_and_1000_characters'
        }, {
            'points': 20,
            'value': 1,
            'criteria': 'images::equals_1'
        }, {
            'points': 50,
            'value': 658,
            'criteria': 'review_count::greater_than_6_reviews_count'
        }, {
            'points': 50,
            'value': 4.730769230769231,
            'criteria': 'review_rating::greater_than_4_reviews_rating'
        }]
