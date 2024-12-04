from redis import Redis
from simple_settings import settings


class LockActiveError(Exception):
    pass


class Lock(object):

    def __init__(self):
        self.active = False


class CacheLock(Lock):
    def __init__(self, key, expire=60):
        super(CacheLock, self).__init__()
        self._key = key
        self._expire = expire
        self._cache = Redis(
            host=settings.REDIS_LOCK_SETTINGS['host'],
            port=settings.REDIS_LOCK_SETTINGS['port'],
            password=settings.REDIS_LOCK_SETTINGS.get('password'),
            socket_connect_timeout=int(
                settings.REDIS_LOCK_SETTINGS['socket_connect_timeout']
            ),
            socket_timeout=int(settings.REDIS_LOCK_SETTINGS['socket_timeout'])
        )

    def __enter__(self):
        if not self._cache.get(self._key):
            self.active = self._cache.set(self._key, True, self._expire)

        if not self.active:
            raise LockActiveError(f'For key {self._key}')

        return self

    def __exit__(self, *args, **kwargs):
        self.active = False
        self._cache.delete(self._key)
