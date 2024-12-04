from datetime import datetime, timedelta

import pytest
from mongoengine import DynamicDocument

from taz.api.common.pagination import Pagination


class BadgeModel(DynamicDocument):
    meta = {
        'collection': 'badges'
    }


class TestPagination:

    @pytest.fixture
    def badge_dict(self):
        return {
            'tooltip': 'Black Fraude',
            'text': 'Melhores oferta é na BLACK FRAUDE da Magazine Luiza - Procure este selo e compre tranquilo que garantimos o melhor preço.', # noqa
            'image_url': 'https://a-static.mlcdn.com.br/{w}x{h}/black_fraude.jpg',  # noqa
            'products': [
                {
                    'sku': '123456789',
                    'seller_id': 'magazineluiza'
                },
                {
                    'sku': 'JDLK765G',
                    'seller_id': 'murcho'
                }
            ],
            'position': 'bottom',
            'container': 'information',
            'name': 'Black Fraude',
            'active': True,
            'priority': 1,
            'start_at': '2017-08-17T06:17:03.503000',
            'end_at': '2018-08-17T06:17:03.503000',
            'slug': 'black-fraude',
        }

    @pytest.fixture
    def save_badges(self, badge_dict):
        badge_dict['start_at'] = (
            datetime.utcnow() + timedelta(days=-1)
        ).isoformat()
        badge_dict['end_at'] = (
            datetime.utcnow() + timedelta(days=5)
        ).isoformat()

        BadgeModel(**badge_dict).save()

        for _ in range(3):
            badge_dict['active'] = False
            BadgeModel(**badge_dict).save()

    def test_paginate_badges(self, save_badges):
        pagination = Pagination(BadgeModel)

        response = pagination.paginate(
            criteria={'name': {'$exists': True}},
            page_number=1,
            offset=2,
            sort_by='name'
        )

        assert len(response['records']) == 2
        assert response['offset'] == 2
        assert response['page_number'] == 1
        assert response['total_documents'] == 4
        assert response['total_pages'] == 2
        assert 'products' in response['records'][0]

    def test_paginate_badges_without_field_products(self, save_badges):
        pagination = Pagination(BadgeModel)

        response = pagination.paginate(
            criteria={'name': {'$exists': True}},
            page_number=1,
            offset=2,
            sort_by='name',
            fields={'products': 0}
        )

        assert len(response['records']) == 2
        assert response['offset'] == 2
        assert response['page_number'] == 1
        assert response['total_documents'] == 4
        assert response['total_pages'] == 2
        assert 'products' not in response['records'][0]

    def test_paginate_without_badges(self):
        pagination = Pagination(BadgeModel)

        response = pagination.paginate(
            criteria={'name': {'$exists': True}},
            page_number=1,
            offset=2,
            sort_by='name'
        )

        assert len(response['records']) == 0
        assert response['offset'] == 2
        assert response['page_number'] == 1
        assert response['total_documents'] == 0
        assert response['total_pages'] == 0
