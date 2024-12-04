from unittest.mock import Mock, call

import pytest

from taz.core.cache.layered_cache import LayeredCache


class TestLayeredCache:
    @pytest.fixture
    def memory_cache(self):
        return Mock()

    @pytest.fixture
    def redis_cache(self):
        return Mock()

    def test_save_value(self, memory_cache, redis_cache):
        cache = LayeredCache()
        memory_cache.get.side_effect = [None, 10]
        redis_cache.get.side_effect = [None, 10]
        cache.set_layers([memory_cache, redis_cache])
        cache.set('test', 10)
        cache.get('test')

        assert memory_cache.set.call_args_list == [call('test', '10')]
        assert memory_cache.get.call_args_list == [call('test'), call('test')]
