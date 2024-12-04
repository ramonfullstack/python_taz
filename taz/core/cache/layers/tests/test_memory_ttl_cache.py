import time

import pytest

from taz.core.cache.layers import MemoryTTLCache


class TestMemoryTTLCache:
    @pytest.fixture
    def cache(self):
        return MemoryTTLCache(ttl=1, interval=1)

    @pytest.mark.parametrize(
        'key,value',
        [
            ('test', 1),
            ('test_2', {'test': 1}),
            ('test_3', 'test')
        ]
    )
    def test_cache_save(self, cache, key, value):
        cache.set(key, value)
        assert cache.get(key) == value

    @pytest.mark.parametrize(
        'key,values',
        [
            ('test', [1, 2, 3, 4]),
            ('test_2', [{'test': 1}, {'test': 2}, {'test': 3}, {'test': 4}]),
        ]
    )
    def test_cache_save_many_times(self, cache, key, values):
        for value in values:
            cache.set(key, value)
        assert cache.get(key) == values[-1]

    def test_cache_expires(self, cache):
        cache.set('test', 1)
        time.sleep(2)
        assert cache.get('test') is None
