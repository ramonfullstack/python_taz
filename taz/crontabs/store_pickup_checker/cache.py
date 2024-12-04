import datetime

from taz.consumers.core.cache.redis import CacheMixin


class APICacheController(CacheMixin):

    CACHE_KEY = 'apiluiza-pickup_stores'
    TOKEN_TTL = datetime.timedelta(days=29)

    def __init__(self):
        self.cache = self.get_cache()

    def get_token(self) -> str:
        return self.cache.get(self.CACHE_KEY) or ''

    def update_token(self, token) -> bool:
        changed_token = self.cache.set(self.CACHE_KEY, token)
        changed_expire = self.cache.expire(self.CACHE_KEY, self.TOKEN_TTL)
        return changed_token and changed_expire
