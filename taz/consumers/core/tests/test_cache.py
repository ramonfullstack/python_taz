import pytest
from redis import Redis

from taz.consumers.core.cache.redis import CacheMixin


class TestCache:

    @pytest.fixture
    def cache(self):
        return CacheMixin()

    def test_redis_is_same_instance(self, cache):
        first_instance = cache.get_cache()
        second_instance = cache.get_cache()

        assert isinstance(first_instance, Redis)
        assert first_instance is second_instance
