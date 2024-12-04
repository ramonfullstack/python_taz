
from copy import deepcopy
from typing import Dict

from expiring_dict import ExpiringDict
from maaslogger import base_logger
from simple_settings import settings

from taz import constants
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.core.common.media import build_media

logger = base_logger.get_logger(__name__)


class CacheCategories:
    _shared_state = {}

    def __init__(self, **kwargs):
        self.__dict__ = self._shared_state
        if 'categories' not in self._shared_state:
            self.categories = ExpiringDict(**kwargs)


class ScopeHelper(MongodbMixin):

    def __init__(self):
        self.raw_products = self.get_collection('raw_products')
        self.prices = self.get_collection('prices')
        self.medias = self.get_collection('medias')
        self.enriched_products = self.get_collection('enriched_products')
        self.categories = self.get_collection('categories')
        self.sellers = self.get_collection('sellers')
        self.id_correlations = self.get_collection('id_correlations')
        self.unpublished_products = self.get_collection('unpublished_products')
        self.unified_objects = self.get_collection('unified_objects')
        self.cache = CacheCategories(
            ttl=settings.EXPIRES_CACHE_CATEGORIES,
            interval=float(settings.CACHE_CLEANING_INTERVAL)
        )

    def _get_category(
        self, category_id, ttl=settings.EXPIRES_CACHE_CATEGORIES
    ):
        cache_value = self.cache.categories.get(category_id)

        if not cache_value:
            category = self.categories.find_one(
                {'id': category_id}, {'_id': 0}
            )

            if not category:
                logger.warning(f'Category id:{category_id} not found')
                return None

            self.cache.categories.ttl(key=category_id, value=category, ttl=ttl)
            return category

        return cache_value

    def get_categories_detail(self, categories):
        categories_copy = deepcopy(categories)

        for category in categories_copy:
            subcategories = category.get('subcategories') or []

            categories_ids = [category['id']]

            categories_ids.extend([
                subcategory['id'] for subcategory in subcategories
            ])

            stored_categories = []
            for id in categories_ids:
                c = self._get_category(id)
                if c is not None:
                    stored_categories.append(c)

            for stored_category in stored_categories:
                id_ = stored_category.get('id')
                if id_ == category['id']:
                    category.update({
                        'url': stored_category.get('url'),
                        'name': stored_category.get('description')
                    })

                for subcategory in subcategories:
                    if id_ == subcategory['id']:
                        subcategory.update({
                            'url': stored_category.get('url'),
                            'name': stored_category.get('description')
                        })
                        break
        return categories_copy

    def get_seller_name(self, seller_id):
        seller = self.sellers.find_one(
            {'id': seller_id},
            {'_id': 0, 'name': 1}
        )

        if not seller:
            return seller_id

        return seller['name']

    def get_offer_id_and_id_correlations(
        self,
        sku: str,
        seller_id: str
    ) -> dict:
        id_correlation = self.id_correlations.find_one(
            {'seller_id': seller_id, 'sku': sku},
            {'_id': 0, 'product_id': 1}
        ) or {}

        offer_id = id_correlation.get('product_id')
        if not offer_id:
            return {}

        unified_objects = self.unified_objects.find_one(
            {'id': offer_id},
            {'_id': 0, 'canonical_ids': 1}
        ) or {}

        canonical_ids = unified_objects.get('canonical_ids', [])
        return {
            'offer_id': offer_id,
            'id_correlations': canonical_ids
        } if canonical_ids else {}

    def _select_offer_id(self, canonical_ids):
        for navigation_id in canonical_ids:
            raw_product_info = self.raw_products.find_one(
                {
                    'navigation_id': navigation_id
                }
            )

            if not raw_product_info:
                continue

            criteria = {
                'sku': raw_product_info.get('sku'),
                'seller_id': raw_product_info.get('seller_id')
            }

            product_price = self.prices.find_one(criteria)

            if product_price and product_price.get('stock_count', 0) > 0:
                return navigation_id

    def get_medias(self, seller_id: str, sku: str):
        media = self.medias.find_one({
            'sku': sku,
            'seller_id': seller_id
        })
        if not media:
            logger.warning(
                f'Medias not found for sku:{sku} seller_id:{seller_id}'
            )

        return media

    def get_media_urls(self, seller_id, sku, title, reference, media):
        media_result = {}
        media_types = ['audios', 'images', 'podcasts', 'videos']
        for media_type in media_types:
            if not media.get(media_type):
                media_result[media_type] = []
                continue

            media_result[media_type] = build_media(
                sku=sku,
                title=title,
                reference=reference,
                seller_id=seller_id,
                media_type=media_type,
                items=media.get(media_type, []),
                force_path=True
            )
        return media_result

    def get_enriched_products(
        self,
        seller_id: str,
        sku: str,
        fields: Dict = None,
        skip=''
    ):
        fields = fields or {'_id': 0}
        enriched_products = list(
            self.enriched_products.find(
                {
                    'sku': sku,
                    'seller_id': seller_id,
                    'source': {'$nin': skip.split(',')}
                },
                fields
            )
        )

        if not enriched_products:
            logger.warning(
                f'Enriched product not found for sku:{sku} '
                f'seller_id:{seller_id}'
            )

        enriched_products.sort(key=lambda x: x['source'])
        return enriched_products

    def create_unavailable_product_payload(
        self,
        navigation_id: str
    ) -> Dict:
        unpublished_product = self.unpublished_products.find_one(
            {'navigation_id': navigation_id},
            {'navigation_id': 1, '_id': 0}
        )
        if not unpublished_product:
            return {}

        return {
            'active': False,
            'stock_count': 0,
            'availability': constants.AVAILABILITY_OUT_OF_STOCK
        }
