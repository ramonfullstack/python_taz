import pytest
from pymongo.database import Database

from taz.constants import MAGAZINE_LUIZA_SELLER_ID
from taz.consumers.datalake.scopes.product_score import Scope
from taz.tests.helpers import product_score


class TestProductScoreScope:

    @pytest.fixture
    def product_score_scope(self, mock_sku: str):
        return Scope(sku=mock_sku, seller_id=MAGAZINE_LUIZA_SELLER_ID)

    @pytest.fixture
    def save_score(self, mongo_database: Database, mock_sku: str):
        mongo_database.scores.insert_one(
            product_score(active=True, sku=mock_sku)
        )

    @pytest.fixture
    def save_inactive_score(self, mongo_database: Database, mock_sku: str):
        mongo_database.scores.insert_one(
            product_score(active=False, sku=mock_sku)
        )

    def test_get_data_should_return_active_score(
        self,
        product_score_scope: Scope,
        save_score,
        save_inactive_score,
        mock_sku: str
    ):
        assert product_score_scope.get_data() == {
            'sku': mock_sku,
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'final_score': 100.0,
            'sources': [
                {
                    'value': 'Playset Imaginext DTM81 Fisher-Price - 6 Peças',
                    'points': 100.0,
                    'weight': 0.3,
                    'criteria': 'title::between_31_and_60_characters'
                },
                {
                    'value': 'Para estimular a imaginação e garantir a brincadeira da criançada, a Fisher Price lançou o divertido Playset Teen Titans Tower Imaginext DTM81!\n6 peças compõe a torre protegida por Robin que é atacado pelo Mamute. \nDurante a brincadeira pequenos heróis poderão impedir o ataque colocando Robin no elevador para o alto da torre, onde ele vira a plataforma e transforma os sofás em lançadores. \nO brinquedo é certificado pelo INMETRO e é indicado para crianças de 6 a 7 anos. \n\n\n\n\n',  # noqa
                    'points': 100.0,
                    'weight': 0.2,
                    'criteria': 'description::between_251_and_1000_characters'
                },
                {
                    'value': '5',
                    'points': 100.0,
                    'weight': 0.5,
                    'criteria': 'images::greater_than_3_images'
                }
            ]
        }

    def test_get_data_should_empty_result(
        self,
        product_score_scope: Scope,
        mock_sku: str
    ):
        assert not product_score_scope.get_data()
