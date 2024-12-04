from unittest import mock

import pytest


class TestCategoryScoreHandler:

    @pytest.fixture
    def mock_url(self):
        return '/score/category/ed'

    @pytest.fixture
    def save_category(self, mongo_database):
        mongo_database.get_collection('categories').save({
            'id': 'BR',
            'description': 'Brinquedos'
        })

    @mock.patch('time.time', mock.MagicMock(return_value=0))
    def test_get_should_return_category_score(
        self,
        client,
        mock_url,
        save_scores,
        save_category
    ):
        mock.return_value = 0
        response = client.get(mock_url)

        assert response.status_code == 200
        assert response.json == {
            'data': {
                'catalog_average_score': 76.0,
                'catalog_score_count': 2,
                'category_id': 'ED',
                'category_description': '',
                'timestamp': 0
            }
        }

    @mock.patch('time.time', mock.MagicMock(return_value=0))
    def test_get_should_return_category_score_count(
        self,
        client,
        mock_url,
        save_scores,
        save_category
    ):
        mock.return_value = 0
        response = client.get(mock_url)

        assert response.status_code == 200
        assert response.json == {
            'data': {
                'catalog_average_score': 76.0,
                'catalog_score_count': 2,
                'category_id': 'ED',
                'category_description': '',
                'timestamp': 0
            }
        }

    @mock.patch('time.time', mock.MagicMock(return_value=0))
    def test_get_should_consider_only_active_scores(
        self,
        client,
        mock_url,
        save_scores,
        save_inactive_score,
        save_category
    ):
        response = client.get(mock_url)
        assert response.status_code == 200
        assert response.json == {
            'data': {
                'catalog_average_score': 76.0,
                'catalog_score_count': 2,
                'category_id': 'ED',
                'category_description': '',
                'timestamp': 0
            }
        }

    @mock.patch('time.time', mock.MagicMock(return_value=0))
    def test_get_should_consider_only_scores_from_category(
        self,
        client,
        mock_url,
        save_scores,
        save_other_seller_score,
        save_category
    ):
        response = client.get(mock_url)
        assert response.status_code == 200
        assert response.json == {
            'data': {
                'catalog_average_score': 76.0,
                'catalog_score_count': 2,
                'category_id': 'ED',
                'category_description': '',
                'timestamp': 0
            }
        }

    def test_should_return_not_found_if_no_scores_for_category(
        self,
        mock_url,
        client
    ):
        response = client.get(mock_url)
        assert response.status_code == 404
