from unittest import mock

import pytest


class TestSellerScoreHandler:

    @pytest.fixture
    def mock_url(self):
        return '/score/seller/magazineluiza'

    @pytest.fixture
    def save_categories(self, mongo_database):
        mongo_database.get_collection('categories').save(
            {
                'id': 'ED',
                'active': True,
                'slug': 'eletrodomesticos',
                'parent_id': 'ML',
                'description': 'Eletrodomésticos',
                'url': 'eletrodomesticos/l/ed/'
            }
        )

        mongo_database.get_collection('categories').save(
            {
                'id': 'BR',
                'active': True,
                'slug': 'brinquedos',
                'parent_id': 'ML',
                'description': 'brinquedos',
                'url': 'brinquedos/l/br/'
            }
        )

        mongo_database.get_collection('categories').save(
            {
                'id': 'FS',
                'active': True,
                'slug': 'ferramentas-e-seguranca',
                'parent_id': 'ML',
                'description': 'Ferramentas e Segurança',
                'url': 'ferramentas-e-seguranca/l/fs/'
            }
        )

    @pytest.fixture
    def save_categories_without_description(self, mongo_database):
        mongo_database.get_collection('categories').save(
            {
                'id': 'ED',
                'active': True,
                'slug': 'eletrodomesticos',
                'parent_id': 'ML',
                'description': 'Eletrodomésticos',
                'url': 'eletrodomesticos/l/ed/'
            }
        )

        mongo_database.get_collection('categories').save(
            {
                'id': 'FS',
                'active': True,
                'slug': 'ferramentas-e-seguranca',
                'parent_id': 'ML',
                'url': 'ferramentas-e-seguranca/l/fs/'
            }
        )

    @pytest.fixture
    def expected_payload(self):
        return {
            'data': {
                'seller_id': 'magazineluiza',
                'catalog_average_score': 65.6,
                'catalog_score_count': 5,
                'categories': [
                    {
                        'category_id': 'BR',
                        'catalog_average_score': 100.0,
                        'catalog_score_count': 1,
                        'category_description': 'brinquedos'
                    },
                    {
                        'category_id': 'ED',
                        'catalog_average_score': 76.0,
                        'catalog_score_count': 2,
                        'category_description': 'Eletrodomésticos'
                    },
                    {
                        'category_id': 'FS',
                        'catalog_average_score': 38.0,
                        'catalog_score_count': 2,
                        'category_description': 'Ferramentas e Segurança'
                    }
                ],
                'timestamp': 0
            }
        }

    @mock.patch('time.time', mock.MagicMock(return_value=0))
    def test_get_should_return_seller_score(
        self,
        client,
        mock_url,
        save_scores,
        save_categories,
        expected_payload
    ):
        mock.return_value = 0
        response = client.get(mock_url)

        assert response.status_code == 200
        assert response.json == expected_payload

    @mock.patch('time.time', mock.MagicMock(return_value=0))
    def test_get_should_return_consider_only_active_scores(
        self,
        client,
        mock_url,
        save_scores,
        save_inactive_score,
        save_categories,
        expected_payload
    ):
        response = client.get(mock_url)
        assert response.status_code == 200
        assert response.json == expected_payload

    @mock.patch('time.time', mock.MagicMock(return_value=0))
    def test_get_should_consider_only_scores_from_seller(
        self,
        client,
        mock_url,
        save_scores,
        save_other_seller_score,
        save_categories,
        expected_payload
    ):
        response = client.get(mock_url)
        assert response.status_code == 200
        assert response.json == expected_payload

    def test_should_return_not_found_if_no_scores_for_seller(
        self,
        mock_url,
        client
    ):
        response = client.get(mock_url)
        assert response.status_code == 404

    @mock.patch('time.time', mock.MagicMock(return_value=0))
    def test_should_use_hyphen_in_category_description_if_does_not_find_description_or_category( # noqa
        self,
        client,
        mock_url,
        save_scores,
        save_categories_without_description
    ):
        response = client.get(mock_url)

        assert response.status_code == 200
        assert response.json == {
            'data': {
                'seller_id': 'magazineluiza',
                'catalog_average_score': 65.6,
                'catalog_score_count': 5,
                'categories': [
                    {
                        'category_id': 'BR',
                        'catalog_average_score': 100.0,
                        'catalog_score_count': 1,
                        'category_description': '-'
                    },
                    {
                        'category_id': 'ED',
                        'catalog_average_score': 76.0,
                        'catalog_score_count': 2,
                        'category_description': 'Eletrodomésticos'
                    },
                    {
                        'category_id': 'FS',
                        'catalog_average_score': 38.0,
                        'catalog_score_count': 2,
                        'category_description': '-'
                    }
                ],
                'timestamp': 0
            }
        }
