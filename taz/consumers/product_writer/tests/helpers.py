from taz.constants import BADGE_CACHE_KEY


def _save_badges_cache(cache, badge_dict):
    for product in badge_dict['products']:
        cache_key = BADGE_CACHE_KEY.format(
            sku=product['sku'],
            seller_id=product['seller_id']
        )
        cache.set(cache_key, badge_dict['slug'])
