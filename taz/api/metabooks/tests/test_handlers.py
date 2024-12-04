import json

import pytest

from taz.api.metabooks.models import MetabooksCategoryModel


class TestMetabooksCategoryHandler:

    @pytest.fixture
    def mock_categories_url(self):
        return '/metabooks/categories'

    @pytest.fixture
    def categories(self):
        return [
            {
                'category_id': 'LI',
                'subcategory_ids': [
                    'PETS'
                ],
                'metabook_id': 'PET012000'
            }, {
                'category_id': 'LI',
                'subcategory_ids': [
                    'PETS',
                    'ADEP'
                ],
                'metabook_id': 'PET004020'
            }, {
                'category_id': 'LI',
                'subcategory_ids': [
                    'PETS'
                ],
                'metabook_id': 'PET013000'
            }, {
                'category_id': 'LI',
                'subcategory_ids': [
                    'PETS',
                    'PEIO'
                ],
                'metabook_id': 'PET005000'
            }, {
                'category_id': 'LI',
                'subcategory_ids': [
                    'LDAR'
                ],
                'metabook_id': 'ANT042010'
            }, {
                'category_id': 'LI',
                'subcategory_ids': [
                    'LDAR'
                ],
                'metabook_id': 'ANT042000'
            }, {
                'category_id': 'LI',
                'subcategory_ids': [
                    'LDAR'
                ],
                'metabook_id': 'ANT008000'
            }
        ]

    def test_post_categories(
        self, client, categories, mock_categories_url
    ):
        response = client.post(
            mock_categories_url,
            body=json.dumps(categories)
        )

        payload = MetabooksCategoryModel.objects()

        assert len(payload) == 7
        assert response.status_code == 201

    def test_post_categories_already_exists(
        self, client, categories, mock_categories_url
    ):
        client.post(mock_categories_url, body=json.dumps(categories))
        client.post(mock_categories_url, body=json.dumps(categories))

        payload = MetabooksCategoryModel.objects()

        assert len(payload) == 7
