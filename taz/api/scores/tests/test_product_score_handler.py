import pytest

from taz.tests.helpers import product_score


class TestProductScoreHandler:

    @pytest.fixture
    def mock_url(self):
        return '/score/seller/magazineluiza/sku/181160400'

    @pytest.fixture
    def save_score(self, mongo_database):
        mongo_database.get_collection('scores').save(product_score(
            active=True,
            sku='181160400'
        ))

    @pytest.fixture
    def save_inactive_score(self, mongo_database):
        mongo_database.get_collection('scores').save(product_score(
            active=False,
            sku='181160400'
        ))

    @pytest.fixture
    def expected_payload(self):
        return {
            'data': {
                'catalog_average_score': 100.0,
                'sku': '181160400',
                'seller_id': 'magazineluiza',
                'version': 'v0_0_1'
            }
        }

    def test_get_should_return_product_score(
        self,
        client,
        mock_url,
        save_score,
        expected_payload
    ):
        response = client.get(mock_url)

        assert response.status_code == 200
        assert response.json == expected_payload

    def test_get_should_return_active_product_score(
        self,
        client,
        mock_url,
        save_score,
        save_inactive_score,
        expected_payload
    ):
        response = client.get(mock_url)
        assert response.status_code == 200
        assert response.json == expected_payload

    def test_get_should_return_not_found_if_there_is_no_score_for_product(
        self,
        mock_url,
        client
    ):
        response = client.get(mock_url)
        assert response.status_code == 404

    def test_get_should_return_all_data_if_debug_true_on_query_string(
        self,
        client,
        mock_url,
        save_score
    ):
        response = client.get(
            mock_url,
            query_string='debug=true'
        )
        assert response.json == {
            'data': {
                'sku': '181160400',
                'seller_id': 'magazineluiza',
                'catalog_average_score': 100.0,
                'version': 'v0_0_1',
                'debug': {
                    'md5': '40a70a00979631dac768a14369601712',
                    'sku': '181160400',
                    'seller_id': 'magazineluiza',
                    'entity_name': 'brinquedo',
                    'active': True,
                    'timestamp': 1555476519.4684415,
                    'version': 'v0_0_1',
                    'final_score': 100.0,
                    'category_id': 'BR',
                    'sources': [{
                        'value': 'Playset Imaginext DTM81 Fisher-Price - 6 Peças',  # noqa
                        'points': 100.0,
                        'weight': 0.3,
                        'criteria': 'title::between_31_and_60_characters'
                    }, {
                        'value': 'Para estimular a imaginação e garantir a brincadeira da criançada, a Fisher Price lançou o divertido Playset Teen Titans Tower Imaginext DTM81!\n6 peças compõe a torre protegida por Robin que é atacado pelo Mamute. \nDurante a brincadeira pequenos heróis poderão impedir o ataque colocando Robin no elevador para o alto da torre, onde ele vira a plataforma e transforma os sofás em lançadores. \nO brinquedo é certificado pelo INMETRO e é indicado para crianças de 6 a 7 anos. \n\n\n\n\n',  # noqa
                        'points': 100.0,
                        'weight': 0.2,
                        'criteria': 'description::between_251_and_1000_characters'  # noqa
                    }, {
                        'value': 5,
                        'points': 100.0,
                        'weight': 0.5,
                        'criteria': 'images::greater_than_3_images'
                    }]
                }
            }
        }

    def test_get_should_return_all_scores_if_show_history(
        self,
        client,
        mock_url,
        save_score,
        save_inactive_score
    ):
        response = client.get(
            mock_url,
            query_string='show_history=true'
        )
        assert response.json == {
            'data': {
                'sku': '181160400',
                'seller_id': 'magazineluiza',
                'catalog_average_score': 100.0,
                'version': 'v0_0_1',
                'histories': [{
                    'md5': '40a70a00979631dac768a14369601712',
                    'sku': '181160400',
                    'seller_id': 'magazineluiza',
                    'entity_name': 'brinquedo',
                    'active': False,
                    'timestamp': 1555476519.4684415,
                    'version': 'v0_0_1',
                    'final_score': 100.0,
                    'category_id': 'BR',
                    'sources': [{
                        'value': 'Playset Imaginext DTM81 Fisher-Price - 6 Peças',  # noqa
                        'points': 100.0,
                        'weight': 0.3,
                        'criteria': 'title::between_31_and_60_characters'
                    }, {
                        'value': 'Para estimular a imaginação e garantir a brincadeira da criançada, a Fisher Price lançou o divertido Playset Teen Titans Tower Imaginext DTM81!\n6 peças compõe a torre protegida por Robin que é atacado pelo Mamute. \nDurante a brincadeira pequenos heróis poderão impedir o ataque colocando Robin no elevador para o alto da torre, onde ele vira a plataforma e transforma os sofás em lançadores. \nO brinquedo é certificado pelo INMETRO e é indicado para crianças de 6 a 7 anos. \n\n\n\n\n',  # noqa
                        'points': 100.0,
                        'weight': 0.2,
                        'criteria': 'description::between_251_and_1000_characters'  # noqa
                    }, {
                        'value': 5,
                        'points': 100.0,
                        'weight': 0.5,
                        'criteria': 'images::greater_than_3_images'  # noqa
                    }]
                }]
            }
        }
