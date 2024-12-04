import json
import time

import pytest
from simple_settings import settings

from taz.core.cache.layers import RedisCache


class TestRedisCache:
    @pytest.fixture
    def cache(self):
        return RedisCache(
            key_pattern='TestRedisCache::',
            ttl=int(settings.EXPIRES_REDIS_CACHE_CATEGORIES),
            host=settings.REDIS_LOCK_SETTINGS['host'],
            port=settings.REDIS_LOCK_SETTINGS['port'],
            password=settings.REDIS_LOCK_SETTINGS.get('password')
        )

    @pytest.mark.parametrize(
        'key,value',
        [
            ('test', 1),
            ('test_2', {'test': 1}),
            ('test_3', 'test')
        ]
    )
    def test_cache_save(self, cache, key, value):
        cache.set(key, json.dumps(value))
        assert json.loads(cache.get(key).decode()) == value

    @pytest.mark.parametrize(
        'key,values',
        [
            ('test', [1, 2, 3, 4]),
            ('test_2', [{'test': 1}, {'test': 2}, {'test': 3}, {'test': 4}]),
        ]
    )
    def test_cache_save_many_times(self, cache, key, values):
        for value in values:
            cache.set(key, json.dumps(value))
        assert json.loads(cache.get(key).decode()) == values[-1]

    def test_cache_expires(self, cache):
        cache.set('test', json.dumps(1))
        time.sleep(1.1)
        assert cache.get('test') is None

    def test_delete_key(self, cache):
        cache.set('test_delete', json.dumps(1))
        cache.delete('test_delete')
        assert cache.get('test') != 1
