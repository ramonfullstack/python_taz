import pytest
from simple_settings.utils import settings_stub

from taz.core.matching.common.enriched_products import EnrichedProductSamples
from taz.core.matching.common.samples import ProductSamples
from taz.core.score import Score
from taz.core.score.helpers import create_payload


class TestScore:

    @pytest.fixture
    def product(self, factsheet_product_227718300):
        product = ProductSamples.magazineluiza_sku_0233847()
        enriched = EnrichedProductSamples.magazineluiza_sku_0233847()

        return create_payload(
            product,
            enriched,
            {},
            {},
            factsheet_product_227718300
        )

    @pytest.fixture
    def score_data(self):
        return {
            'sku': '200238300',
            'seller_id': 'magazineluiza',
            'version': 'v0_2_0',
            'sources': [
                {
                    'weight': 0.0,
                    'points': 20.0,
                    'criteria': 'description::between_251_and_1000_characters',
                    'value': 'Passadeira que higieniza as roupas, eliminando odore em poucos minutos e evitando a proliferação de ácaros e outros microorganismos. Muito prática, ela é ideal para qualquer tipo de tecido, roupas ou cortinas. É portátil e fácil de levar nas viagens. Possui escovas especiais para retirar fiapos e pelos.' # noqa
                },
                {
                    'weight': 0.0,
                    'points': 50.0,
                    'criteria': 'images::greater_than_3_images',
                    'value': 7
                },
                {
                    'weight': 0.0,
                    'points': 50.0,
                    'criteria': 'offer_title::greater_than_60_characters',
                    'value': 'Passadeira a Vapor Portátil Cadence Lisser VAP901 - 200ml 700W Branco' # noqa
                },
                {
                    'weight': 0.0,
                    'points': 50.0,
                    'criteria': 'review_count::greater_than_6_reviews_count',
                    'value': 10
                },
                {
                    'weight': 0.0,
                    'points': 20.0,
                    'criteria': 'review_rating::between_1_and_2_reviews_rating', # noqa
                    'value': 2.9
                },
                {
                    'weight': 0.0,
                    'points': 50.0,
                    'criteria': 'title::greater_than_60_characters',
                    'value': 'Passadeira a Vapor Portátil Cadence Lisser VAP901 - 200ml 700W Branco' # noqa
                }
            ],
            'entity_name': 'Passadeira a Vapor',
            'category_id': 'EP',
            'final_score': 0,
            'active': True,
            'md5': '0ac056e19399bde86b42e838ab2831c4'
        }

    @pytest.fixture
    def score(self):
        return Score()

    @settings_stub(SCORE_VERSION='0.3.0')
    def test_should_score_calculate(
        self,
        product,
        score,
        save_score_criteria,
        mongo_database
    ):
        score.calculate(product)
        payload = mongo_database.scores.find_one({'active': True})

        del payload['_id']
        del payload['timestamp']

        assert payload == {
            'seller_id': 'magazineluiza',
            'entity_name': 'Fritadeira Elétrica',
            'active': True,
            'md5': '6564a402d9549324a3ab0b798e5f59ab',
            'final_score': 0,
            'sources': [
                {
                    'criteria': 'description::between_251_and_1000_characters',
                    'value': 'O que era inimaginável agora é real, sim, você pode fritar alimentos sem usar óleo, sem deixar cheiro de gordura ou fumaça pela casa, e tem mais, você também pode preparar alimentos de maneira incrivelmente rápida e deixar tudo crocante, gostoso e mais saudável para a sua família!Com a incrível Fritadeira Sem Óleo Inox RED Premium da Mondial tudo isso está ao seu alcance. Painel em aço inox e design sofisticado, lâmpadas-piloto que indicam o funcionamento do produto e do aquecimento, controle de temperatura até 200 ºC para a escolha da temperatura ideal de acordo com diferentes tipos de alimentos, cesta removível segura e prática para facilitar o manuseio dos alimentos, timer de 60 minutos com sinal sonoro e desligamento automático. Com muita praticidade, você pode prepara batatas crocantes em apenas 12 min, e com o livro de receitas você também pode preparar pão de queijo, carnes, aperitivos, peixes, frango a passarinho, pastéis doces e muito mais.',  # noqa
                    'weight': 0.0,
                    'points': 20.0
                },
                {
                    'criteria': 'factsheet::greater_than_10_attributes',
                    'value': 14,
                    'weight': 0.0,
                    'points': 100.0
                },
                {
                    'criteria': 'title::greater_than_60_characters',
                    'value': 'Fritadeira Elétrica Air Fryer/Sem Óleo Mondial - AF-14 3,2L Timer',  # noqa
                    'weight': 0.0,
                    'points': 50.0
                }
            ],
            'category_id': 'EP',
            'version': 'v0_2_0',
            'sku': '023384700'
        }

    def test_should_score_calculate_fix_none_and_same_reviews(
        self,
        score,
        save_score_criteria,
        mongo_database,
        score_data,
        product_200238300
    ):
        score.calculate(product_200238300)
        payload = mongo_database.scores.find_one({'active': True})

        del payload['_id']
        del payload['timestamp']

        assert payload == score_data

    def test_should_disable_previous_records(
        self,
        score,
        score_data,
        mongo_database,
        product_200238300,
        save_score_criteria
    ):
        mongo_database.scores.save(score_data)
        assert mongo_database.scores.count({'active': True}) == 1

        product_200238300['reviews_count'] = 0
        score.calculate(product_200238300)

        assert mongo_database.scores.count() == 2
        assert mongo_database.scores.count({'active': True}) == 1

    def test_should_skip_existing_md5(
        self,
        score,
        score_data,
        mongo_database,
        product_200238300,
        save_score_criteria
    ):
        mongo_database.scores.save(score_data)
        assert mongo_database.scores.count() == 1

        score.calculate(product_200238300)

        assert mongo_database.scores.count() == 1

    @settings_stub(SCORE_VERSION='0.3.0')
    def test_should_update_product_score_to_active_false_only_products_score_actives( # noqa
        self,
        product,
        score,
        save_score_criteria,
        mongo_database
    ):
        mongo_database.scores.insert_many([
            {
                'seller_id': 'magazineluiza',
                'sku': '023384700',
                'entity_name': 'Fritadeira Elétrica',
                'final_score': 45,
                'sources': [],
                'category_id': 'EP',
                'version': 'v0_3_0'
            },
            {
                'seller_id': 'magazineluiza',
                'sku': '023384700',
                'entity_name': 'Fritadeira Elétrica',
                'final_score': 25,
                'sources': [],
                'category_id': 'EP',
                'version': 'v0_3_0',
                'active': True
            }
        ])

        score.calculate(product)
        score_all = mongo_database.scores.find().count()
        score_false = mongo_database.scores.find({'active': False}).count()
        score_active = mongo_database.scores.find({'active': True}).count()

        assert score_false == 1
        assert score_active == 1
        assert score_all == 3
