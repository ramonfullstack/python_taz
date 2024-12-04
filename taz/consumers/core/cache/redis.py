from redis import Redis
from simple_settings import settings


class CacheMixin:

    CACHE = None

    def get_cache(self):
        if not self.CACHE:
            self.CACHE = Redis(
                host=settings.REDIS_LOCK_SETTINGS['host'],
                port=settings.REDIS_LOCK_SETTINGS['port'],
                password=settings.REDIS_LOCK_SETTINGS.get('password')
            )
        return self.CACHE
