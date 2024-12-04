from typing import Dict
from unittest.mock import call, patch

import pytest

from taz.helpers.pagination import Pagination


class TestPagination:

    @pytest.fixture
    def pagination(self, mongo_database):
        return Pagination(mongo_database.raw_products)

    @pytest.fixture
    def products(self):
        products = [
            {
                'seller_id': 'magazineluiza',
                'navigation_id': '123456789',
                'sku': '092380941'
            },
            {
                'seller_id': 'magazineluiza',
                'navigation_id': '987654321',
                'sku': '432349823'
            },
            {
                'seller_id': 'magazineluiza',
                'navigation_id': '123987456',
                'sku': '198898432'
            },
            {
                'seller_id': 'magazineluiza',
                'navigation_id': '432321231',
                'sku': '321321412'
            },
            {
                'seller_id': 'magazineluiza',
                'navigation_id': '656785856',
                'sku': '190293090'
            },
            {
                'seller_id': 'magazineluiza',
                'navigation_id': '312321123',
                'sku': '111111111'
            }
        ]

        return products

    @pytest.fixture
    def save_products(self, mongo_database, products):
        mongo_database.raw_products.insert_many(products)

    def test_pagination_with_offset_should_process_with_success(
        self,
        pagination,
        save_products,
        products
    ):

        products_sorted = sorted(products, key=lambda x: x['sku'])

        data = pagination._paginate_keyset(
            criteria={'seller_id': 'magazineluiza'},
            fields={'sku': 1},
            sort=[('sku', 1)],
            limit_size=3,
            offset=products_sorted[2]['sku'],
            field_offset='sku'
        )

        assert data.count(with_limit_and_skip=True) == 3
        for index, value in enumerate(data):
            assert value['sku'] == products_sorted[index + 3]['sku']

    def test_pagination_without_offset(
        self,
        pagination,
        save_products,
        products
    ):
        products_sorted = sorted(products, key=lambda x: x['sku'])

        data = pagination._paginate_keyset(
            criteria={'seller_id': 'magazineluiza'},
            fields={'sku': 1},
            sort=[('sku', 1)],
            limit_size=4,
        )

        assert data.count(with_limit_and_skip=True) == 4
        for index, value in enumerate(data):
            assert value['sku'] == products_sorted[index]['sku']

    def test_finish_pagination_process_with_success(
        self,
        pagination,
        save_products,
        products
    ):
        products_sorted = sorted(products, key=lambda x: x['sku'])

        data = pagination._paginate_keyset(
            criteria={'seller_id': 'magazineluiza'},
            fields={'sku': 1},
            sort=[('sku', 1)],
            limit_size=2,
            offset=products_sorted[-1]['sku'],
            field_offset='sku'
        )

        assert data.count(with_limit_and_skip=True) == 0

    def test_when_unset_no_cursor_timeout_then_stay_with_cursor(
        self,
        pagination
    ):
        criteria: Dict = {'seller_id': 'magazineluiza'}
        fields: Dict = {'sku': 1}
        with patch.object(pagination, 'collection') as mock_collection:
            pagination._paginate_keyset(
                criteria=criteria,
                fields=fields,
                sort=[('sku', 1)],
                limit_size=2,
                offset=None,
                field_offset='sku'
            )

            assert mock_collection.find.call_args == call(
                criteria, fields, no_cursor_timeout=True
            )

    @pytest.mark.parametrize('no_cursor_timeout,expected_not_cursor_timeout', [
        (True, True),
        (False, False),
        (None, True)
    ])
    def test_when_set_no_cursor_timeout_then_stay_with_cursor(
        self,
        pagination,
        no_cursor_timeout,
        expected_not_cursor_timeout
    ):
        criteria: Dict = {'seller_id': 'magazineluiza'}
        fields: Dict = {'sku': 1}
        with patch.object(pagination, 'collection') as mock_collection:
            pagination._paginate_keyset(
                criteria=criteria,
                fields=fields,
                sort=[('sku', 1)],
                limit_size=2,
                offset=None,
                field_offset='sku',
                no_cursor_timeout=no_cursor_timeout
            )

            assert mock_collection.find.call_args == call(
                criteria, fields, no_cursor_timeout=expected_not_cursor_timeout
            )
