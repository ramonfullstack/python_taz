import json

import pytest

from taz.api.blacklist.models import BlacklistModel


class TestBlacklistHandler:

    @pytest.fixture
    def mock_url(self):
        return '/blacklist'

    @pytest.mark.parametrize('payload', [
        ({}),
        ({'term': '', 'field': 'brand'}),
        ({'term': 'apple', 'field': ''}),
    ])
    def test_create_new_term_in_blacklist_returns_bad_request(
        self, client, payload, mock_url
    ):
        response = client.post(mock_url, body=json.dumps(payload))
        assert response.status_code == 400

    def test_save_blacklist(self, client, blacklist_dict, mock_url):
        response = client.post(mock_url, body=json.dumps(blacklist_dict))
        assert response.status_code == 200

        blacklist = BlacklistModel.objects().first()
        assert blacklist.term == blacklist_dict['term']
        assert blacklist.field == blacklist_dict['field']

    @pytest.mark.parametrize('payload', [
        ({}),
        ({'term': '', 'field': 'brand'}),
        ({'term': 'apple', 'field': ''}),
    ])
    def test_delete_blacklist_returns_bad_request(
        self, client, payload, mock_url
    ):
        response = client.delete(mock_url, body=json.dumps(payload))
        assert response.status_code == 400

    def test_delete_blacklist(self, client, blacklist_dict, mock_url):
        response = client.delete(mock_url, body=json.dumps(blacklist_dict))

        assert response.status_code == 204

        blacklist = BlacklistModel.objects().first()
        assert not blacklist


class TestBlacklistListHandler:

    def test_blacklist_list(self, client, blacklist_dict):
        BlacklistModel(**blacklist_dict).save()

        response = client.get('/blacklist/list')

        assert response.status_code == 200
        assert len(response.json) == 1
