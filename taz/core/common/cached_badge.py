from copy import copy

from taz import constants
from taz.consumers.core.cache.redis import CacheMixin
from taz.consumers.core.database.mongodb import MongodbMixin


class CachedBadge(MongodbMixin, CacheMixin):

    @property
    def badges(self):
        return self.get_collection('badges')

    def get_badges_by_seller_id_sku(
        self,
        seller_id,
        sku,
        fields=None,
        sort_by=None
    ):
        cache_key = constants.BADGE_CACHE_KEY.format(
            sku=sku,
            seller_id=seller_id
        )

        cache_value = self.get_cache().get(cache_key)
        if not cache_value:
            return []

        cache_value = cache_value.decode()
        fields_selected = self.__generate_fields(fields)
        badges = self.badges.find(
            {
                'products.sku': sku,
                'products.seller_id': seller_id,
                'slug': cache_value
            },
            fields_selected
        )

        badges = list(badges)
        if sort_by and badges:
            badges = sorted(badges, key=lambda k: k.get(sort_by))

        return badges

    def __generate_fields(self, fields=None):
        if not fields:
            return {'_id': 0}

        returned_fields = copy(fields)
        returned_fields['_id'] = 0
        return returned_fields
