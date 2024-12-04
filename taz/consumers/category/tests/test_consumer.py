from unittest import mock

import pytest
from simple_settings import settings

from taz.consumers.category.consumer import CategoryRecordProcessor
from taz.consumers.core.exceptions import InvalidAcmeResponseException


class TestCategoryRecordProcessor:

    @pytest.fixture
    def record_processor(self):
        return CategoryRecordProcessor('category')

    @pytest.fixture
    def mongo_collection(self, record_processor):
        return record_processor.get_collection('categories')

    @pytest.fixture
    def category_dict(self):
        return {
            'id': 'MO',
            'description': 'Móveis e Decoração',
            'slug': 'moveis-decoracao',
            'parent_id': 'ML',
            'active': True
        }

    @pytest.fixture
    def subcategory_dict(self):
        return {
            'id': 'MOCH',
            'description': 'Guarda Roupa',
            'slug': 'guarda-roupa',
            'parent_id': 'MO',
            'active': True
        }

    @pytest.fixture
    def patch_requests_post(self):
        return mock.patch('requests.post')

    @pytest.fixture
    def patch_requests_put(self):
        return mock.patch('requests.put')

    @pytest.fixture
    def mock_create(
        self, record_processor, category_dict, patch_requests_post
    ):
        mock_response = mock.Mock()
        mock_response.status_code = 201

        with patch_requests_post as mock_requests:
            mock_requests.return_value = mock_response
            record_processor.create(category_dict)

    def test_record_processor_create_a_category(
        self, record_processor, category_dict, mongo_collection,
        patch_requests_post
    ):
        mock_response = mock.Mock()
        mock_response.status_code = 201

        with patch_requests_post as mock_requests:
            mock_requests.return_value = mock_response
            record_processor.create(category_dict)

        assert mongo_collection.count_documents(
            {'id': category_dict['id']}
        ) == 1
        assert mock_requests.called

    def test_record_processor_create_a_category_inactive(
        self, record_processor, category_dict, mongo_collection,
        patch_requests_post
    ):
        mock_response = mock.Mock()
        mock_response.status_code = 201

        category_dict['active'] = False

        with patch_requests_post as mock_requests:
            mock_requests.return_value = mock_response
            record_processor.create(category_dict)

        assert mongo_collection.count_documents(
            {'id': category_dict['id']}
        ) == 1
        assert mock_requests.called

    def test_record_processor_create_a_subcategory_returns_urls(
        self, record_processor, category_dict, subcategory_dict,
        mongo_collection, mock_create, patch_requests_post
    ):
        mock_response = mock.Mock()
        mock_response.status_code = 201

        with patch_requests_post as mock_requests:
            mock_requests.return_value = mock_response
            record_processor.create(subcategory_dict)

        cursor = mongo_collection.find_one({'id': subcategory_dict['id']})
        excepted = settings.SUBCATEGORY_PATH.format(
            subcategory_dict['slug'],
            category_dict['slug'],
            category_dict['id'],
            subcategory_dict['id']
        ).lower()

        assert cursor['url'] == excepted
        assert mock_requests.called

    def test_record_processor_update_a_category(
        self, record_processor, category_dict, mongo_collection,
        mock_create, patch_requests_post, patch_requests_put
    ):
        mock_response = mock.Mock()
        mock_response.status_code = 200

        slug_updated = 'murchos'
        category_dict['slug'] = slug_updated

        with patch_requests_put as mock_requests:
            with patch_requests_post:
                mock_requests.return_value = mock_response
                record_processor.update(category_dict)

        cursor = mongo_collection.find({'id': category_dict['id']})

        assert cursor[0]['slug'] == slug_updated
        assert mock_requests.called

    def test_record_processor_update_returns_not_found_and_create_category(
        self, record_processor, category_dict, mongo_collection,
        mock_create, patch_requests_post, patch_requests_put
    ):
        mock_put_response = mock.Mock()
        mock_put_response.status_code = 404

        mock_post_response = mock.Mock()
        mock_post_response.status_code = 201

        with patch_requests_put as mock_put:
            mock_put.return_value = mock_put_response

            with patch_requests_post as mock_post:
                mock_post.return_value = mock_post_response
                record_processor.update(category_dict)

        cursor = mongo_collection.find_one(
            {'id': category_dict['id']},
            {'_id': 0}
        )

        assert mock_put.called
        assert mock_post.called

        assert cursor == {
            'id': 'MO',
            'description': 'Móveis e Decoração',
            'slug': 'moveis-decoracao',
            'parent_id': 'ML',
            'active': True,
            'url': 'moveis-decoracao/l/mo/'
        }

    def test_record_processor_delete_a_category(
        self, record_processor, category_dict,
        mongo_collection, mock_create, patch_requests_post
    ):
        mock_response = mock.Mock()
        mock_response.status_code = 204

        with mock.patch('requests.delete') as mock_requests:
            with patch_requests_post:
                mock_requests.return_value = mock_response
                record_processor.delete(category_dict)

        assert mongo_collection.count_documents(
            {'id': category_dict['id']}
        ) == 0
        assert mock_requests.called

    def test_record_delete_acme_returns_404_should_continue_process(
        self,
        record_processor,
        category_dict,
        mongo_collection,
        caplog
    ):
        mock_response = mock.Mock()
        mock_response.status_code = 404

        mongo_collection.update_one(
            {'id': category_dict['id']}, {'$set': category_dict}, upsert=True
        )

        with mock.patch('requests.delete') as mock_requests:
            mock_requests.return_value = mock_response
            mock_requests.return_value.url = 'url'
            record_processor.delete(category_dict)

        assert mock_requests.called
        assert (
            'Error deleting category in url '
            'category MO not found'
        ) in caplog.text
        assert 'Successfully deleted category:MO' in caplog.text

    @pytest.mark.parametrize('processor_method, patch_method', [
        ('create', 'requests.post'),
        ('update', 'requests.put'),
        ('delete', 'requests.delete')
    ])
    def test_record_processor_raise_error_in_category_actions(
        self, record_processor, category_dict, processor_method, patch_method
    ):
        mock_response = mock.Mock()
        mock_response.status_code = 400

        with mock.patch(patch_method) as mock_requests_put:
            mock_requests_put.return_value = mock_response

            with pytest.raises(InvalidAcmeResponseException):
                getattr(record_processor, processor_method)(category_dict)
