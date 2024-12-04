import pytest
from redis import Redis
from simple_settings import settings

from taz.tasks.delete_redis_key import RedisDeleteKey


class TestDeleteRedisKey:

    @pytest.fixture
    def redis(self):
        return Redis(
            host=settings.REDIS_LOCK_SETTINGS['host'],
            port=settings.REDIS_LOCK_SETTINGS['port']
        )

    def test_should_not_delete_key_asterisk(self, redis, logger_stream):
        task = RedisDeleteKey()
        assert task.execute('*') is False

        log = logger_stream.getvalue()
        assert 'Error while deleting key:*' in log

    def test_should_not_delete_key_not_found(self, redis, logger_stream):
        task = RedisDeleteKey()
        assert task.execute('mock_key') is False

        log = logger_stream.getvalue()
        assert 'Error while deleting key not found keys with:mock_key' in log

    def test_should_delete_key_one(self, redis, logger_stream):
        redis.set('mock_key', True)
        redis.set('mock_keyA', True)

        task = RedisDeleteKey()
        assert task.execute('mock_key') is True

        log = logger_stream.getvalue()
        assert 'Deleted keys [b\'mock_key\'] from Redis' in log
        assert len(redis.keys()) == 1

    def test_should_delete_keys(self, redis, logger_stream):
        redis.set('mock_key', True)
        redis.set('mock_keyA', True)
        redis.set('mock_keyB', True)
        redis.set('mock_keyC', True)

        task = RedisDeleteKey()

        assert task.execute('mock_key*') is True

        log = logger_stream.getvalue()
        assert ('Deleted keys [b') in log
        assert len(redis.keys()) == 0
