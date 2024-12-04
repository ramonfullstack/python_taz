from datetime import datetime, timedelta
from unittest.mock import patch

import pytest
from redis import Redis

from taz.api.badges.models import BadgeModel
from taz.consumers.core.aws.sqs import SQSManager


@pytest.fixture
def badge_dict():
    end_now = (datetime.utcnow() + timedelta(days=-1)).isoformat()
    start_now = (datetime.utcnow() + timedelta(days=-3)).isoformat()

    return {
        'image_url': 'https://a-static.mlcdn.com.br/{w}x{h}/black_fraude.jpg',
        'position': 'bottom',
        'container': 'information',
        'text': 'Melhores oferta é na BLACK FRAUDE da Magazine Luiza - Procure este selo e compre tranquilo que garantimos o melhor preço.',  # noqa
        'tooltip': 'Black Fraude',
        'start_at': start_now,
        'end_at': end_now,
        'products': [
            {'sku': '123456789', 'seller_id': 'magazineluiza'},
            {'sku': 'JHU-9876', 'seller_id': 'murcho'}
        ],
        'name': 'Black Fraude',
        'slug': 'black-fraude',
        'active': True,
        'priority': 7
    }


@pytest.fixture
def save_badges_without_name(badge_dict_without_name):
    badge_dict_without_name['start_at'] = (
        datetime.utcnow() + timedelta(days=-1)
    ).isoformat()
    badge_dict_without_name['end_at'] = (
        (datetime.utcnow() + timedelta(days=5)).isoformat()
    )

    BadgeModel(**badge_dict_without_name).save()


@pytest.fixture
def save_badges(badge_dict):
    badge_dict['start_at'] = (
        datetime.utcnow() + timedelta(days=-1)
    ).isoformat()
    badge_dict['end_at'] = (datetime.utcnow() + timedelta(days=5)).isoformat()

    BadgeModel(**badge_dict).save()

    for _ in range(3):
        badge_dict['active'] = False
        BadgeModel(**badge_dict).save()


@pytest.fixture
def save_invalid_badges(badge_dict):
    badge_dict['start_at'] = (
        datetime.utcnow() + timedelta(days=-1)
    ).isoformat()
    badge_dict['end_at'] = (datetime.utcnow() + timedelta(days=5)).isoformat()

    BadgeModel(**badge_dict).save()

    for i in range(3):
        if i > 1:
            del badge_dict['name']
            del badge_dict['products']
            del badge_dict['position']
            del badge_dict['container']

        badge_dict['active'] = False
        BadgeModel(**badge_dict).save()


@pytest.fixture
def patch_redis():
    return patch.object(Redis, 'delete')


@pytest.fixture
def patch_sqs_put():
    return patch.object(SQSManager, 'put')
