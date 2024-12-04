import logging

from redis import Redis

from taz.core.cache.layers import BaseLayer

logger = logging.getLogger(__name__)


class RedisCache(BaseLayer):
    def __init__(self, host, port, password, key_pattern='', ttl=None):
        self.__db = Redis(
            host=host,
            port=port,
            password=password
        )
        self.key_pattern = key_pattern
        self.ttl = int(ttl) if ttl is not None else None

    def _get_key(self, key):
        return f'{self.key_pattern}{key}'

    def set(self, key, value):
        self.__db.set(name=self._get_key(key), value=value, ex=self.ttl)

    def get(self, key):
        return self.__db.get(name=self._get_key(key))

    def delete(self, key):
        try:
            self.__db.delete(self._get_key(key))
        except Exception as e:
            logger.debug(f'error on delete cache: {str(e)}')
            return
