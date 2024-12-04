import pytest
from pagination_adelpha import Pagination as PaginationOpenApi


class TestPaginationOpenApi:

    @pytest.fixture
    def collection(self, mongo_database):
        return mongo_database.get_collection('pagination')

    @pytest.fixture
    def mock_save_data(self, collection):
        collection.insert_many([
            {'id': i + 1}
            for i in reversed(range(10))
        ])

    @pytest.fixture
    def pagination(self, collection):
        return PaginationOpenApi(collection, '')

    @pytest.mark.parametrize('params,expected', [
        (
            {
                'criteria': {},
                'fields': {'_id': 0},
                'offset': 0,
                'limit': 10
            },
            {
                'meta': {
                    'page': {
                        'limit': 10,
                        'offset': 0,
                        'count': 10
                    },
                    'links': {
                        'previous_page': '',
                        'next_page': '?_offset=10&_limit=10'
                    }
                },
                'results': [{'id': 10}, {'id': 9}, {'id': 8}, {'id': 7}, {'id': 6}, {'id': 5}, {'id': 4}, {'id': 3}, {'id': 2}, {'id': 1}]  # noqa
            }
        ),
        (
            {
                'criteria': {},
                'fields': {'_id': 0},
                'offset': 0,
                'limit': 2
            },
            {
                'meta': {
                    'page': {
                        'limit': 2,
                        'offset': 0,
                        'count': 2
                    },
                    'links': {
                        'previous_page': '',
                        'next_page': '?_offset=2&_limit=2'
                    }
                },
                'results': [{'id': 10}, {'id': 9}]
            }
        ),
        (
            {
                'criteria': {},
                'fields': {'_id': 0},
                'offset': 1,
                'limit': 2
            },
            {
                'meta': {
                    'page': {
                        'limit': 2,
                        'offset': 1,
                        'count': 2
                    },
                    'links': {
                        'previous_page': '?_offset=0&_limit=2',
                        'next_page': '?_offset=3&_limit=2'
                    }
                },
                'results': [{'id': 9}, {'id': 8}]
            }
        ),
        (
            {
                'criteria': {'id': 1},
                'fields': {'_id': 0},
                'offset': 0,
                'limit': 10
            },
            {
                'meta': {
                    'page': {
                        'limit': 10,
                        'offset': 0,
                        'count': 1
                    },
                    'links': {
                        'previous_page': '',
                        'next_page': ''
                    }
                },
                'results': [{'id': 1}]
            }
        ),
        (
            {
                'criteria': {'filter': None},
                'fields': {'_id': 0},
                'offset': 0,
                'limit': 10
            },
            {
                'meta': {
                    'page': {
                        'limit': 10,
                        'offset': 0,
                        'count': 10
                    },
                    'links': {
                        'previous_page': '',
                        'next_page': '?_offset=10&_limit=10'
                    }
                },
                'results': [{'id': 10}, {'id': 9}, {'id': 8}, {'id': 7}, {'id': 6}, {'id': 5}, {'id': 4}, {'id': 3}, {'id': 2}, {'id': 1}]  # noqa
            }
        ),
        (
            {
                'criteria': {'filter': None},
                'fields': None,
                'offset': 0,
                'limit': 10
            },
            {
                'meta': {
                    'page': {
                        'limit': 10,
                        'offset': 0,
                        'count': 10
                    },
                    'links': {
                        'previous_page': '',
                        'next_page': '?_offset=10&_limit=10'
                    }
                },
                'results': [{'id': 10}, {'id': 9}, {'id': 8}, {'id': 7}, {'id': 6}, {'id': 5}, {'id': 4}, {'id': 3}, {'id': 2}, {'id': 1}]  # noqa
            }
        ),
    ])
    def test_when_paginate_then_return_pagination_with_success(
        self,
        mock_save_data,
        pagination,
        params,
        expected
    ):
        assert pagination.paginate(**params) == expected

    def test_build_next_return_empty(
        self,
        pagination,
    ):
        assert pagination._Pagination__build_next({
            '_count': 1,
            '_limit': 2
        }) == ''

    def test_build_previous_return_empty(
        self,
        pagination,
    ):

        assert pagination._Pagination__build_previous({
            '_offset': 0,
        }) == ''
