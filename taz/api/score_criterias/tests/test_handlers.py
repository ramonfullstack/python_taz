import json

import pytest

from taz.api.score_criterias.models import ScoreCriteriaModel


class TestCriteriaHandler:

    @pytest.fixture
    def mock_url(self):
        return '/score/criteria'

    def test_get_criteria(
        self,
        client,
        save_score_criteria
    ):
        response = client.get('/score/criteria/default')
        assert response.status_code == 200

        payload = response.json
        del payload['_id']

        assert payload == {
            'entity_name': 'default',
            'elements': [
                {
                    'name': 'title',
                    'criteria': [
                        {
                            'min': 1,
                            'points': 20,
                            'name': 'between_1_and_30_characters',
                            'max': 30
                        }, {
                            'min': 31,
                            'points': 30,
                            'name': 'between_31_and_60_characters',
                            'max': 60
                        }, {
                            'min': 60,
                            'points': 50,
                            'name': 'greater_than_60_characters'
                        }
                    ],
                    'type': 'range'
                },
                {
                    'name': 'description',
                    'criteria': [
                        {
                            'min': 1,
                            'points': 20,
                            'name': 'between_1_and_250_characters',
                            'max': 250
                        }, {
                            'min': 251,
                            'points': 20,
                            'name': 'between_251_and_1000_characters',
                            'max': 1000
                        }, {
                            'min': 1000,
                            'points': 60,
                            'name': 'greater_than_1000_characters'
                        }
                    ],
                    'type': 'range'
                }
            ],
            'score_version': '0.2.0'
        }

    def test_get_criteria_return_not_found(
        self,
        client,
        save_score_criteria
    ):
        response = client.get('/score/criteria/xpto')
        assert response.status_code == 404

        payload = response.json
        assert payload == {
            'error_message': 'Criteria entity_name:xpto not found'
        }

    def test_post_criteria(
        self,
        client,
        criterias,
        mock_url
    ):
        response = client.post(
            mock_url,
            body=json.dumps(criterias[0])
        )

        assert response.status_code == 200

        criteria = ScoreCriteriaModel.objects().first()
        assert criteria.entity_name == criterias[0]['entity_name']
        assert criteria.elements == [
            {
                'type': 'range',
                'name': 'title',
                'criteria': [
                    {
                        'points': 20,
                        'min': 1,
                        'max': 30,
                        'name': 'between_1_and_30_characters'
                    },
                    {
                        'points': 30,
                        'min': 31,
                        'max': 60,
                        'name': 'between_31_and_60_characters'
                    },
                    {
                        'points': 50,
                        'min': 60,
                        'name': 'greater_than_60_characters'
                    }
                ]
            },
            {
                'type': 'range',
                'name': 'description',
                'criteria': [
                    {
                        'points': 20,
                        'min': 1,
                        'max': 250,
                        'name': 'between_1_and_250_characters'
                    }, {
                        'points': 20,
                        'min': 251,
                        'max': 1000,
                        'name': 'between_251_and_1000_characters'
                    }, {
                        'points': 60,
                        'min': 1000,
                        'name': 'greater_than_1000_characters'
                    }
                ]
            }
        ]

    def test_update_criteria(
        self,
        client,
        criterias,
        mock_url
    ):
        client.post(mock_url, body=json.dumps(criterias[0]))

        criterias[0]['elements'] = [criterias[0]['elements'][0]]
        response = client.post(
            mock_url,
            body=json.dumps(criterias[0])
        )

        assert response.status_code == 200
        criteria = ScoreCriteriaModel.objects().first()
        assert len(criteria.elements) == 1

    def test_post_criteria_returns_bad_requests(
        self,
        client,
        criterias,
        mock_url
    ):
        response = client.post(mock_url)
        assert response.status_code == 400

    def test_delete_criteria_returns_not_found(
        self,
        client
    ):
        response = client.delete('/score/criteria/murcho')
        assert response.status_code == 404

    def test_delete_criteria(
        self,
        client,
        save_score_criteria,
        criterias
    ):
        for criteria in criterias:
            response = client.delete('/score/criteria/{}'.format(
                criteria['entity_name']
            ))
            assert response.status_code == 204


class TestCriteriaListHandler:

    def test_get_criteria_list_returns_empty_list(self, client):
        response = client.get('/score/criteria/list')

        assert response.status_code == 200
        assert response.json == []

    def test_get_criteria_list(self, client, save_score_criteria):
        response = client.get('/score/criteria/list')

        assert response.status_code == 200
        assert len(response.json) == 2
