import pytest
from redis import Redis
from simple_settings import settings


class TestRedisPollerHandler:

    @pytest.fixture
    def key(self):
        return 'test-poller-key'

    @pytest.fixture
    def cache(self):
        return Redis(
            host=settings.REDIS_SETTINGS['host'],
            port=settings.REDIS_SETTINGS['port'],
            password=settings.REDIS_SETTINGS.get('password')
        )

    @pytest.fixture
    def mock_url(self):
        return '/redis/poller/key/{}'

    def test_get_key_returns_empty(self, client, key, mock_url):
        result = client.get(mock_url.format(key))

        assert result.json == {}

    def test_get_key_returns_ok(self, client, key, cache, mock_url):
        cache.set(key, '{"product": "1234"}')

        result = client.get(mock_url.format(key))

        assert result.json == {'product': '1234'}

    def test_delete_key_returns_ok(self, client, key, cache, mock_url):
        result = client.delete(mock_url.format(key))

        assert result.status_code == 204
        assert cache.get(key) is None

    def test_delete_key_not_exists_returns_ok(
        self,
        client,
        key,
        cache,
        mock_url
    ):
        assert cache.get(key) is None

        result = client.delete(mock_url.format(key))

        assert result.status_code == 204
        assert cache.get(key) is None
