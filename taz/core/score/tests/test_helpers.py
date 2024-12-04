import copy

import pytest
from simple_settings import settings

from taz.core.score.helpers import (
    _delete_fields,
    create_payload,
    get_weights_and_scores_by_criteria_and_entity
)


class TestHelpers:

    @pytest.fixture
    def save_enrich_product(self, mongo_database):
        mongo_database.enriched_products.save(
            {
                'source': 'magalu',
                'sku': '023384700',
                'seller_id': 'magazineluiza',
                'entity': 'Fritadeira'
            }
        )

    @pytest.fixture
    def criteria_values(self):
        return [
            {
                'value': 'Fritadeira Elétrica Air Fryer/Sem Óleo Mondial - AF-14 3,2L Timer',  # noqa
                'points': 50,
                'criteria': 'title::greater_than_60_characters'
            },
            {
                'value': 'O que era inimaginável agora é real, sim, você pode fritar alimentos sem usar óleo, sem deixar cheiro de gordura ou fumaça pela casa, e tem mais, você também pode preparar alimentos de maneira incrivelmente rápida e deixar tudo crocante, gostoso e mais saudável para a sua família!\nCom a incrível Fritadeira Sem Óleo Inox RED Premium da Mondial tudo isso está ao seu alcance.  Painel em aço inox e design sofisticado, lâmpadas-piloto que indicam o funcionamento do produto e do aquecimento, controle de temperatura até 200 ºC para a escolha da temperatura ideal de acordo com diferentes tipos de alimentos, cesta removível segura e prática para facilitar o manuseio dos alimentos, timer de 60 minutos com sinal sonoro e desligamento automático. Com muita praticidade, você pode prepara batatas crocantes em apenas 12 min, e com o livro de receitas você também pode preparar pão de queijo, carnes, aperitivos, peixes, frango a passarinho, pastéis doces e muito mais. \n',  # noqa
                'points': 20,
                'criteria': 'description::between_251_and_1000_characters'
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

    @pytest.fixture
    def save_weights_for_fritadeira_entity(self, mongo_database):
        payload = [
            {
                'entity_name': 'Fritadeira',
                'criteria_name': 'title',
                'weight': '60',
                'score_version': settings.SCORE_VERSION
            },
            {
                'entity_name': 'Fritadeira',
                'criteria_name': 'description',
                'weight': '40',
                'score_version': settings.SCORE_VERSION
            }
        ]

        mongo_database.score_weights.insert_many(payload)

    def test_should_get_criterias_with_success(
        self,
        criteria_values,
        save_score_weights
    ):
        score_weights = get_weights_and_scores_by_criteria_and_entity(
            criteria_values=criteria_values,
            entity='default'
        )

        assert score_weights == {
            'title': {
                'points': 50.0,
                'value': 'Fritadeira Elétrica Air Fryer/Sem Óleo Mondial - AF-14 3,2L Timer',  # noqa
                'weight': 50.0,
                'criteria': 'title::greater_than_60_characters'
            },
            'description': {
                'points': 20.0,
                'value': 'O que era inimaginável agora é real, sim, você pode fritar alimentos sem usar óleo, sem deixar cheiro de gordura ou fumaça pela casa, e tem mais, você também pode preparar alimentos de maneira incrivelmente rápida e deixar tudo crocante, gostoso e mais saudável para a sua família!\nCom a incrível Fritadeira Sem Óleo Inox RED Premium da Mondial tudo isso está ao seu alcance.  Painel em aço inox e design sofisticado, lâmpadas-piloto que indicam o funcionamento do produto e do aquecimento, controle de temperatura até 200 ºC para a escolha da temperatura ideal de acordo com diferentes tipos de alimentos, cesta removível segura e prática para facilitar o manuseio dos alimentos, timer de 60 minutos com sinal sonoro e desligamento automático. Com muita praticidade, você pode prepara batatas crocantes em apenas 12 min, e com o livro de receitas você também pode preparar pão de queijo, carnes, aperitivos, peixes, frango a passarinho, pastéis doces e muito mais. \n',  # noqa
                'weight': 50.0,
                'criteria': 'description::between_251_and_1000_characters'
            }
        }

    def test_should_get_entity_fritadeira_criterias_with_success(
        self,
        criteria_values,
        save_score_weights,
        save_weights_for_fritadeira_entity
    ):
        score_weights = get_weights_and_scores_by_criteria_and_entity(
            criteria_values=criteria_values,
            entity='Fritadeira'
        )
        assert score_weights == {
            'description': {
                'value': 'O que era inimaginável agora é real, sim, você pode fritar alimentos sem usar óleo, sem deixar cheiro de gordura ou fumaça pela casa, e tem mais, você também pode preparar alimentos de maneira incrivelmente rápida e deixar tudo crocante, gostoso e mais saudável para a sua família!\nCom a incrível Fritadeira Sem Óleo Inox RED Premium da Mondial tudo isso está ao seu alcance.  Painel em aço inox e design sofisticado, lâmpadas-piloto que indicam o funcionamento do produto e do aquecimento, controle de temperatura até 200 ºC para a escolha da temperatura ideal de acordo com diferentes tipos de alimentos, cesta removível segura e prática para facilitar o manuseio dos alimentos, timer de 60 minutos com sinal sonoro e desligamento automático. Com muita praticidade, você pode prepara batatas crocantes em apenas 12 min, e com o livro de receitas você também pode preparar pão de queijo, carnes, aperitivos, peixes, frango a passarinho, pastéis doces e muito mais. \n',  # noqa
                'criteria': 'description::between_251_and_1000_characters',
                'weight': 40.0,
                'points': 20.0
            },
            'title': {
                'value': 'Fritadeira Elétrica Air Fryer/Sem Óleo Mondial - AF-14 3,2L Timer',  # noqa
                'criteria': 'title::greater_than_60_characters',
                'weight': 60.0,
                'points': 50.0
            }
        }


class TestHelperCreatePayload:

    @pytest.mark.parametrize(
        'enriched_product,medias,customer_behaviors,factsheet,attr_count', [
            (
                'enriched_product_200238300',
                'media_product_200238300',
                'customer_behavior_200238300',
                'factsheet_product_010015900',
                40
            ),
            (
                'enriched_product_200238300',
                'media_product_200238300',
                'customer_behavior_200238300',
                'factsheet_product_227718300',
                14
            ),
            (
                'enriched_product_200238300',
                'media_product_200238300',
                'customer_behavior_200238300',
                'factsheet_product_227747300',
                11
            )
        ]
    )
    def test_should_create_payload_with_success(
        self,
        product_200238300,
        enriched_product,
        medias,
        customer_behaviors,
        factsheet,
        attr_count,
        request
    ):
        enriched_product = request.getfixturevalue(enriched_product)
        medias = request.getfixturevalue(medias)
        customer_behaviors = request.getfixturevalue(customer_behaviors)
        factsheet = request.getfixturevalue(factsheet)

        expected_payload = copy.deepcopy(product_200238300)

        payload = create_payload(
            product_200238300,
            enriched_product,
            medias,
            customer_behaviors,
            factsheet
        )

        expected_payload['factsheet_attributes_count'] = attr_count
        assert payload == expected_payload

    def test_when_factsheet_param_is_empty_then_should_return_payload_without_factsheet_attributes_fields( # noqa
        self,
        product_200238300,
        enriched_product_200238300,
        media_product_200238300,
        customer_behavior_200238300
    ):
        expected_payload = copy.deepcopy(product_200238300)

        payload = create_payload(
            product_200238300,
            enriched_product_200238300,
            media_product_200238300,
            customer_behavior_200238300,
            None
        )

        assert payload == expected_payload


class TestHelperDeleteFields:

    @pytest.mark.parametrize('product, expected', [
        ({'id': '123', 'title': 'mrucho'}, {'id': '123', 'title': 'mrucho'}),
        ({'id': '123', 'review_count': 10}, {'id': '123'}),
        ({'id': '123', 'review_score': 2.3}, {'id': '123'}),
    ])
    def test_delete_fields(self, product, expected):
        _delete_fields(product)
        assert product == expected
