from expiring_dict import ExpiringDict

from taz.core.cache.layers import BaseLayer


class MemoryTTLCache(BaseLayer):
    def __init__(self, ttl, interval):
        self.ttl = ttl
        self.__cache = ExpiringDict(ttl=ttl, interval=interval)

    def get(self, key):
        return self.__cache.get(key)

    def set(self, key, value):
        self.__cache.ttl(key, value, self.ttl)
