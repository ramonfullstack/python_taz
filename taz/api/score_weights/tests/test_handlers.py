import json

import pytest

from taz import constants
from taz.api.score_weights.models import ScoreWeightModel


class TestScoreWeightHandler:

    @pytest.fixture
    def mock_url(self):
        return '/score/weight'

    @pytest.fixture
    def mock_url_with_criteria(self, mock_url):
        return mock_url + '/{entity_name}/{criteria_name}'

    def test_get_score_weight(
        self,
        client,
        save_score_weights,
        mock_url_with_criteria
    ):
        response = client.get(
            mock_url_with_criteria.format(
                entity_name=constants.SCORE_DEFAULT_ENTITY,
                criteria_name=constants.SCORE_TITLE_CRITERIA
            )
        )

        assert response.status_code == 200
        assert response.json['criteria_name'] == constants.SCORE_TITLE_CRITERIA
        assert response.json['entity_name'] == constants.SCORE_DEFAULT_ENTITY
        assert response.json['weight'] == 30

    def test_get_score_weight_returns_not_found(
        self,
        client,
        mock_url_with_criteria
    ):
        response = client.get(
            mock_url_with_criteria.format(
                entity_name=constants.SCORE_DEFAULT_ENTITY,
                criteria_name=constants.SCORE_TITLE_CRITERIA
            )
        )
        assert response.status_code == 404

    def test_post_score_weight_returns_bad_request(
        self,
        client,
        mock_url
    ):
        response = client.post(mock_url)
        assert response.status_code == 400

    def test_post_score_weight(
        self,
        client,
        mock_url
    ):
        payload = {
            'entity_name': constants.SCORE_DEFAULT_ENTITY,
            'criteria_name': constants.SCORE_TITLE_CRITERIA,
            'weight': 30
        }

        response = client.post(mock_url, body=json.dumps(payload))
        assert response.status_code == 200

        score_weight = ScoreWeightModel.objects().first()
        assert score_weight['entity_name'] == payload['entity_name']
        assert score_weight['entity_name'] == payload['entity_name']

    def test_delete_score_weight(
        self,
        client,
        save_score_weights,
        mock_url_with_criteria
    ):
        response = client.delete(
            mock_url_with_criteria.format(
                entity_name=constants.SCORE_DEFAULT_ENTITY,
                criteria_name=constants.SCORE_TITLE_CRITERIA
            )
        )

        assert response.status_code == 204
        score_weight = ScoreWeightModel.objects()
        assert len(score_weight) == 4

    def test_delete_with_invalid_payload_returns_not_found(
        self,
        client,
        mock_url_with_criteria
    ):
        response = client.delete(
            mock_url_with_criteria.format(
                entity_name=0,
                criteria_name=0
            )
        )
        assert response.status_code == 404


class TestScoreWeightListHandler:

    def test_list_score_weights(
        self,
        client,
        save_score_weights
    ):
        response = client.get('/score/weight/list')

        assert response.status_code == 200
        assert len(response.json) == 5
