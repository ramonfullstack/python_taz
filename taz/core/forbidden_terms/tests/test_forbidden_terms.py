from datetime import datetime
from unittest.mock import Mock

import pytest
from simple_settings import settings

from taz.core.forbidden_terms.forbidden_terms import ForbiddenTerms
from taz.utils import diacriticless


class TestForbiddenTerms:

    @pytest.fixture
    def forbidden_terms(self):
        return ForbiddenTerms()

    @pytest.fixture
    def mock_payload_forbidden_terms(self):
        return {
            'sku': '0123456789',
            'seller_id': 'luizalabs',
            'navigation_id': '987654321',
            'forbidden_terms': [
                {
                    'term': 'criado mudo',
                    'replace': 'Mesa de Cabeceira',
                    'field': 'title',
                    'scope': 'product',
                    'replaced_at': '2023-05-17T15:16:09.683255'
                }
            ]
        }

    def test_when_add_term_and_key_not_exists_then_should_create_key_and_save_with_success( # noqa
        self,
        forbidden_terms,
        mock_de_para_forbidden_terms
    ):
        forbidden_terms.save_redis_terms(mock_de_para_forbidden_terms)
        assert forbidden_terms.get_redis_terms() == mock_de_para_forbidden_terms # noqa

    def test_when_add_term_and_key_already_exists_then_should_update_key_with_new_values( # noqa
        self,
        forbidden_terms,
        mock_de_para_forbidden_terms
    ):
        forbidden_terms.save_redis_terms(mock_de_para_forbidden_terms)
        new_value = {'DE': 'PARA'}

        forbidden_terms.save_redis_terms(new_value)

        mock_de_para_forbidden_terms.update(new_value)
        assert forbidden_terms.get_redis_terms() == {
            diacriticless(key): value
            for (key, value) in mock_de_para_forbidden_terms.items()
        }

    def test_when_get_terms_then_should_return_values_with_success(
        self,
        forbidden_terms,
        mock_de_para_forbidden_terms
    ):
        forbidden_terms.save_redis_terms(mock_de_para_forbidden_terms)
        assert forbidden_terms.get_redis_terms() == {
            diacriticless(key): value
            for (key, value) in mock_de_para_forbidden_terms.items()
        }

    def test_when_get_forbidden_terms_but_not_exist_then_should_return_default_values( # noqa
        self,
        forbidden_terms
    ):
        assert forbidden_terms.get_redis_terms() == settings.FORBIDDEN_TERMS

    def test_when_send_payload_forbidden_terms_then_insert_with_success(
        self,
        forbidden_terms,
        mock_payload_forbidden_terms,
        mongo_database
    ):
        sku = mock_payload_forbidden_terms['sku']
        seller_id = mock_payload_forbidden_terms['seller_id']

        forbidden_terms.save_forbidden_terms(
            sku=sku,
            seller_id=seller_id,
            navigation_id=mock_payload_forbidden_terms['navigation_id'],
            new_terms=mock_payload_forbidden_terms['forbidden_terms']
        )

        result = mongo_database.forbidden_terms.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0}
        )

        assert result == mock_payload_forbidden_terms

    def test_when_send_payload_forbidden_terms_and_record_already_exists_then_should_update_with_success( # noqa
        self,
        forbidden_terms,
        mock_payload_forbidden_terms,
        mongo_database
    ):
        sku = mock_payload_forbidden_terms['sku']
        seller_id = mock_payload_forbidden_terms['seller_id']

        forbidden_terms.save_forbidden_terms(
            sku=sku,
            seller_id=seller_id,
            navigation_id=mock_payload_forbidden_terms['navigation_id'],
            new_terms=mock_payload_forbidden_terms['forbidden_terms']
        )

        result = mongo_database.forbidden_terms.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0}
        )

        assert result == mock_payload_forbidden_terms

        terms = {
            'term': 'criado mudo',
            'replace': 'Mesa de cabeceira',
            'field': 'description',
            'scope': 'product',
            'replaced_at': datetime(2023, 1, 1, 0, 0, 0)
        }

        forbidden_terms.save_forbidden_terms(
            sku=sku,
            seller_id=seller_id,
            navigation_id=mock_payload_forbidden_terms['navigation_id'],
            new_terms=[terms]
        )

        result = mongo_database.forbidden_terms.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0}
        )

        mock_payload_forbidden_terms['forbidden_terms'].insert(0, dict(terms))
        assert result == mock_payload_forbidden_terms

    def test_when_send_payload_forbidden_terms_empty_then_should_return_none(
        self,
        forbidden_terms,
        mock_payload_forbidden_terms,
        patch_mongo_collection
    ):

        with patch_mongo_collection as mock_collection:
            mock = Mock()
            mock_collection.return_value = mock

            forbidden_terms.save_forbidden_terms(
                sku=mock_payload_forbidden_terms['sku'],
                seller_id=mock_payload_forbidden_terms['seller_id'],
                navigation_id=mock_payload_forbidden_terms['navigation_id'],
                new_terms=[]
            )

        assert mock.find_one.call_count == 0

    def test_when_send_payload_forbidden_terms_with_field_and_term_equals_to_database_data_then_should_ignore_this_term_in_update( # noqa
        self,
        forbidden_terms,
        mock_payload_forbidden_terms,
        mongo_database
    ):
        sku = mock_payload_forbidden_terms['sku']
        seller_id = mock_payload_forbidden_terms['seller_id']

        forbidden_terms.save_forbidden_terms(
            sku=sku,
            seller_id=seller_id,
            navigation_id=mock_payload_forbidden_terms['navigation_id'],
            new_terms=mock_payload_forbidden_terms['forbidden_terms']
        )

        result = mongo_database.forbidden_terms.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0}
        )
        assert result == mock_payload_forbidden_terms

        mock_payload_forbidden_terms['forbidden_terms'].append(
            {
                'term': 'Velcro',
                'replace': 'Tiras Autocolantes',
                'field': 'description',
                'scope': 'product',
                'replaced_at': datetime(2023, 1, 1, 0, 0, 0).isoformat()
            }
        )

        forbidden_terms.save_forbidden_terms(
            sku=sku,
            seller_id=seller_id,
            navigation_id=mock_payload_forbidden_terms['navigation_id'],
            new_terms=mock_payload_forbidden_terms['forbidden_terms']
        )

        result = mongo_database.forbidden_terms.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0}
        )

        assert len(result['forbidden_terms']) == 2
        assert result == mock_payload_forbidden_terms

    def test_when_send_payload_forbidden_terms_with_all_fields_and_terms_equals_to_database_then_should_ignore_event( # noqa
        self,
        forbidden_terms,
        mock_payload_forbidden_terms,
        mongo_database,
        patch_mongo_collection
    ):
        mongo_database.forbidden_terms.insert_one(mock_payload_forbidden_terms)
        with patch_mongo_collection as mock_collection:
            mock = Mock()
            mock_collection.return_value = mock
            mock.find_one.return_value = {
                'forbidden_terms': mock_payload_forbidden_terms[
                    'forbidden_terms'
                ]
            }

            forbidden_terms.save_forbidden_terms(
                sku=mock_payload_forbidden_terms['sku'],
                seller_id=mock_payload_forbidden_terms['seller_id'],
                navigation_id=mock_payload_forbidden_terms['navigation_id'],
                new_terms=mock_payload_forbidden_terms['forbidden_terms']
            )

        assert mock.find_one.call_count == 1
        assert mock.update_one.call_count == 0

    @pytest.mark.parametrize('text,pattern,expected', [
        (
            'velcro, Velcron, Velcro, velcron.',
            'velcro',
            'tiras autoadesivas, tiras autoadesivas, tiras autoadesivas, tiras autoadesivas.'  # noqa
        ),
        (
            'Jaqueta com velcro.',
            'velcro',
            'Jaqueta com tiras autoadesivas.'
        ),
        (
            'Jaqueta com velcron',
            'velcro',
            'Jaqueta com tiras autoadesivas'
        ),
        (
            'Jaqueta com velcro, couro e algodão',
            'velcro',
            'Jaqueta com tiras autoadesivas, couro e algodão'
        ),
        (
            'Jaqueta com velcron, couro e algodão',
            'velcro',
            'Jaqueta com tiras autoadesivas, couro e algodão'
        ),
        (
            'Jaqueta com velcron, couro e velcro.',
            'velcro',
            'Jaqueta com tiras autoadesivas, couro e tiras autoadesivas.'
        )
    ])
    def test_replace_terms_with_one_word(
        self,
        text,
        pattern,
        expected,
        forbidden_terms
    ):
        text, _ = forbidden_terms.replace_term(
            text,
            pattern,
            'tiras autoadesivas'
        )

        assert text == expected

    @pytest.mark.parametrize('text,pattern,expected', [
        (
            'Jaqueta de couro sintético',
            'couro sintetico',
            'Jaqueta de material sintético'
        ),
        (
            'Jaqueta de couro sintético.',
            'couro sintetico',
            'Jaqueta de material sintético.'
        ),
        (
            'Jaqueta de couro sintéticom.',
            'couro sintetico',
            'Jaqueta de material sintético.'
        ),
    ])
    def test_replace_terms_with_two_words(
        self,
        text,
        pattern,
        expected,
        forbidden_terms
    ):
        text, _ = forbidden_terms.replace_term(
            text,
            pattern,
            'material sintético'
        )
        assert text == expected

    @pytest.mark.parametrize('text,pattern,expected', [
        (
            'Jaqueta de couro ecológico com Velcro. Com couro original e '
            'velcro top, você não se arrependerá de comprar essa linda '
            'jaqueta de couro com velcro',
            'couro ecologico',
            'Jaqueta de material ecológico com Velcro. Com couro original e '
            'velcro top, você não se arrependerá de comprar essa linda '
            'jaqueta de couro com velcro',
        ),
    ])
    def test_replace_terms_in_text(
        self,
        text,
        pattern,
        expected,
        forbidden_terms
    ):
        text, _ = forbidden_terms.replace_term(
            text,
            pattern,
            'material ecológico'
        )

        assert text == expected
