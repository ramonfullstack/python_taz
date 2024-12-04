import json

import pytest
from simple_settings import settings

from taz.core.forbidden_terms.forbidden_terms import ForbiddenTerms
from taz.utils import diacriticless


class TestForbiddenTermsHandler:

    @pytest.fixture
    def forbidden_terms_payload(self):
        return {
            'sku': '123456789',
            'seller_id': 'luizalabs',
            'navigation_id': '987654321',
            'forbidden_terms': [
                {
                    'term': 'velcro',
                    'field': 'title',
                    'scope': 'product',
                    'replace': 'Tiras autocolantes',
                    'replace_at': ''
                }
            ]
        }

    @pytest.fixture
    def mock_url(self):
        return '/v1/products/forbidden_terms'

    @pytest.fixture
    def save_forbidden_terms(self, mongo_database, forbidden_terms_payload):
        mongo_database.forbidden_terms.insert_one(
            forbidden_terms_payload
        )

    def test_when_get_forbidden_terms_then_should_return_data_with_success( # noqa
        self,
        client,
        mock_url,
        forbidden_terms_payload,
        save_forbidden_terms
    ):
        sku = forbidden_terms_payload['sku']
        seller_id = forbidden_terms_payload['seller_id']
        response = client.get(
            mock_url,
            query_string=f'sku={sku}&seller_id={seller_id}'
        )

        del forbidden_terms_payload['_id']
        assert response.status_code == 200
        assert response.json == forbidden_terms_payload

    def test_when_get_forbidden_terms_but_record_not_exists_then_should_return_404( # noqa
        self,
        client,
        mock_url,
        forbidden_terms_payload
    ):
        sku = forbidden_terms_payload['sku']
        seller_id = forbidden_terms_payload['seller_id']
        response = client.get(
            mock_url,
            query_string=f'sku={sku}&seller_id={seller_id}'
        )

        assert response.status_code == 404

    def test_when_get_forbidden_terms_not_has_sku_query_string_then_should_return_bad_request( # noqa
        self,
        client,
        mock_url,
        forbidden_terms_payload
    ):
        seller_id = forbidden_terms_payload['seller_id']
        response = client.get(
            mock_url,
            query_string=f'sku=&seller_id={seller_id}'
        )

        assert response.status_code == 400

    def test_when_get_forbidden_terms_not_has_seller_id_query_string_then_should_return_bad_request( # noqa
        self,
        client,
        mock_url,
        forbidden_terms_payload
    ):
        sku = forbidden_terms_payload['sku']
        response = client.get(mock_url, query_string=f'sku={sku}')
        assert response.status_code == 400


class TestForbiddenTermsRedisHandler:

    @pytest.fixture
    def save_terms_redis(self, mock_de_para_forbidden_terms):
        ForbiddenTerms().save_redis_terms(mock_de_para_forbidden_terms)

    @pytest.fixture
    def mock_keys_input(self):
        return {
            'v.e.l.c.r.o': 'Tiras Autocolantes',
            'test': 'test'
        }

    @pytest.fixture
    def mock_url(self):
        return '/forbidden_terms/'

    def test_when_get_terms_then_should_return_with_success(
        self,
        client,
        mock_url,
        save_terms_redis,
        mock_de_para_forbidden_terms
    ):
        response = client.get(mock_url)
        assert response.status_code == 200
        assert response.json == mock_de_para_forbidden_terms

    def test_when_get_terms_but_key_not_exists_yet_then_should_return_default_dict( # noqa
        self,
        client,
        mock_url
    ):
        response = client.get(mock_url)
        assert response.status_code == 200
        assert response.json == settings.FORBIDDEN_TERMS

    def test_when_save_forbidden_terms_then_should_return_created_with_success(
        self,
        client,
        mock_url,
        save_terms_redis,
        mock_de_para_forbidden_terms
    ):
        response = client.post(
            mock_url,
            body=json.dumps(mock_de_para_forbidden_terms)
        )

        result = client.get(mock_url)

        assert response.status_code == 201
        assert result.json == mock_de_para_forbidden_terms

    def test_when_update_forbidden_terms_then_should_return_updated_key_with_success( # noqa
        self,
        client,
        mock_url,
        save_terms_redis,
        mock_de_para_forbidden_terms
    ):
        mock_de_para_forbidden_terms.update({'DE': 'PARA'})
        response = client.post(
            mock_url,
            body=json.dumps(mock_de_para_forbidden_terms)
        )

        result = client.get(mock_url)

        expected = {
            diacriticless(key): value
            for (key, value) in mock_de_para_forbidden_terms.items()
        }

        assert response.status_code == 201
        assert result.json == expected

    def test_when_delete_forbidden_terms_key_then_should_delete_with_success(
        self,
        client,
        mock_url,
        save_terms_redis,
        mock_de_para_forbidden_terms
    ):
        response = client.delete(
            mock_url,
            body=json.dumps({'v.e.l.c.r.o': 'Tiras Autocolantes'})
        )

        del mock_de_para_forbidden_terms['v.e.l.c.r.o']

        result = client.get(mock_url)
        assert result.json == mock_de_para_forbidden_terms
        assert response.status_code == 204

    def test_when_delete_keys_forbidden_terms_but_some_key_not_found_then_should_return_success_and_key_name_not_found( # noqa
        self,
        client,
        mock_url,
        save_terms_redis,
        mock_de_para_forbidden_terms,
        mock_keys_input
    ):
        response = client.delete(
            mock_url,
            body=json.dumps(mock_keys_input)
        )

        del mock_de_para_forbidden_terms['v.e.l.c.r.o']

        result = client.get(mock_url)
        assert result.json == mock_de_para_forbidden_terms
        assert response.status_code == 200
        assert response.json == {
            'message': "keys not found to delete:['test']"
        }

    def test_when_delete_keys_forbidden_terms_but_all_keys_not_found_then_should_return_message_error( # noqa
        self,
        client,
        mock_url,
        mock_de_para_forbidden_terms,
        save_terms_redis,
        mock_keys_input
    ):
        del mock_keys_input['v.e.l.c.r.o']

        response = client.delete(
            mock_url,
            body=json.dumps(mock_keys_input)
        )

        result = client.get(mock_url)
        assert result.json == mock_de_para_forbidden_terms
        assert response.status_code == 404
        assert response.json == {
            'error_message': 'All keys not found to delete'
        }

    def test_when_delete_keys_forbidden_terms_but_cache_key_not_found_then_should_return_exception( # noqa
        self,
        client,
        mock_url,
        mock_de_para_forbidden_terms,
        mock_keys_input
    ):
        response = client.delete(
            mock_url,
            body=json.dumps(mock_keys_input)
        )

        assert response.status_code == 500
        assert response.json == {
            'error_message': 'Redis key forbidden_terms not exist'
        }
