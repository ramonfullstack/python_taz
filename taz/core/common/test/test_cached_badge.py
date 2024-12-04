from copy import deepcopy
from unittest.mock import patch

import pytest
from redis import Redis

from taz.core.common.cached_badge import CachedBadge


class TestCachedBadge:

    @pytest.fixture
    def cached_badge(self):
        return CachedBadge()

    @pytest.fixture
    def patch_redis_get(self):
        return patch.object(Redis, 'get')

    @pytest.fixture
    def saved_badge_dict_mongo(
        self,
        badge_dict,
        mongo_database
    ):
        mongo_database.badges.insert_one(badge_dict)

    def test_when_get_badge_by_seller_id_sku_and_not_cached_then_return_empty(
        self,
        cached_badge,
        patch_redis_get
    ):
        with patch_redis_get as mock_redis_get:
            mock_redis_get.return_value = None
            badges = cached_badge.get_badges_by_seller_id_sku(
                seller_id='magazineluiza',
                sku='123456789'
            )
        assert badges == []

    def test_when_get_badge_by_seller_id_sku_then_return_list(
        self,
        cached_badge,
        patch_redis_get,
        saved_badge_dict_mongo,
        badge_dict
    ):
        badge_slug = badge_dict['slug']
        with patch_redis_get as mock_redis_get:
            mock_redis_get.return_value = badge_slug.encode('utf-8')
            badges = cached_badge.get_badges_by_seller_id_sku(
                seller_id='magazineluiza',
                sku='123456789'
            )

        assert len(badges) == 1
        assert badges[0]['slug'] == badge_slug

    @pytest.mark.parametrize('field', [
        ('slug'),
        ('tooltip'),
        ('priority')
    ])
    def test_when_get_badge_by_seller_id_sku_filtered_fields_then_return_badges_filtered( # noqa
        self,
        cached_badge,
        patch_redis_get,
        saved_badge_dict_mongo,
        badge_dict,
        field
    ):
        badge_slug = badge_dict['slug']
        with patch_redis_get as mock_redis_get:
            mock_redis_get.return_value = badge_slug.encode('utf-8')
            badges = cached_badge.get_badges_by_seller_id_sku(
                seller_id='magazineluiza',
                sku='123456789',
                fields={field: 1}
            )

        assert len(badges[0].keys()) == 1
        assert field in badges[0]

    def test_when_get_badge_by_seller_id_sku_ordered_by_priority_then_return_badges_ordered( # noqa
        self,
        cached_badge,
        patch_redis_get,
        badge_dict,
        mongo_database
    ):
        badge_dict2 = deepcopy(badge_dict)
        badge_dict2['priority'] = 2
        badge_dict2['name'] = 'Black Fraude 2'
        mongo_database.badges.insert_many([badge_dict2, badge_dict])

        badge_slug = badge_dict['slug']
        with patch_redis_get as mock_redis_get:
            mock_redis_get.return_value = badge_slug.encode('utf-8')
            badges = cached_badge.get_badges_by_seller_id_sku(
                seller_id='magazineluiza',
                sku='123456789',
                fields={'name': 1, 'priority': 1},
                sort_by='priority'
            )
        assert badges == [
            {'name': 'Black Fraude', 'priority': 1},
            {'name': 'Black Fraude 2', 'priority': 2}
        ]
