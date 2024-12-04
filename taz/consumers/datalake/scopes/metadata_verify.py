import logging
from functools import cached_property
from typing import Dict, List, Optional

from simple_settings import settings

from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.reviews import Reviews
from taz.utils import convert_id_to_nine_digits

logger = logging.getLogger(__name__)


class Scope(MongodbMixin):
    name = 'product'

    def __init__(
        self,
        sku: str,
        seller_id: str,
        navigation_id: str = None,
        **kwargs
    ) -> None:
        self.__sku = sku
        self.__seller_id = seller_id
        self.__navigation_id = navigation_id

    @cached_property
    def raw_products(self):
        return self.get_collection('raw_products')

    @cached_property
    def prices(self):
        return self.get_collection('prices')

    @cached_property
    def categories(self):
        return self.get_collection('categories')

    @cached_property
    def reviews(self):
        return Reviews()

    def get_data(self):
        product = self._get_product()
        if not product:
            return None

        price = self._get_prices()
        categories = self._get_categories(product['categories'])

        rating = self.reviews.get_customer_behavior(
            navigation_id=product['navigation_id'],
            behavior_type='product_average_rating'
        )

        review = self.reviews.get_customer_behavior(
            navigation_id=product['navigation_id'],
            behavior_type='product_total_review_count'
        )

        return self._create_product_payload(
            product=product,
            price=price,
            categories=categories,
            rating=rating,
            review=review
        )

    def _create_product_payload(
        self,
        product: Dict,
        price: Dict,
        categories: List,
        rating: int,
        review: int
    ) -> Dict:

        product.update(
            {
                'active': not product['disable_on_matching'],
                'stock': (price.get('stock_count') or 0) > 0,
                'categories': categories,
                'product_average_rating': rating,
                'product_total_review_count': review,
                'extra_data': product.get('extra_data'),
                'fulfillment': product.get('fulfillment'),
                'matching_uuid': product.get('matching_uuid'),
                'parent_matching_uuid': product.get('parent_matching_uuid'),
                'scope_name': self.name
            }
        )

        bundles = self._get_bundles(product)

        if bundles:
            product['bundles'] = bundles

        return product

    def _get_product(self) -> Optional[Dict]:
        fields = {
            '_id': 0,
            'selections': 0
        }

        product = self.raw_products.find_one(
            {'sku': self.__sku, 'seller_id': self.__seller_id},
            fields
        )

        if not product:
            product = self.raw_products.find_one(
                {'navigation_id': self.__navigation_id},
                fields
            )

            if not product:
                logger.warning(
                    f'Product no found with scope:{self.name} '
                    f'with sku:{self.__sku} seller_id:{self.__seller_id} '
                    f'navigation_id:{self.__navigation_id}'
                )
                return None

        product['navigation_id'] = convert_id_to_nine_digits(
            product['navigation_id']
        )
        return product

    def _get_prices(self) -> Dict:
        price = self.prices.find_one(
            {'sku': self.__sku, 'seller_id': self.__seller_id},
            {'_id': 0, 'stock_count': 1}
        )

        if not price:
            logger.warning(
                f'Price not found with scope:{self.name} '
                f'sku:{self.__sku} seller_id:{self.__seller_id}'
            )
            return {'stock_count': 0}

        return price

    def _get_categories(self, product_categories: List) -> List:
        categories = []

        for product_category in product_categories:

            if not product_category.get('subcategories'):
                category = self._get_fallback_category()
                categories.append(category)

                category_id = product_category.get('id')
                logger.info(
                    f'Product with sku:{self.__sku} seller_id:'
                    f'{self.__seller_id} and category:{category_id} '
                    f'without subcategories set default values to '
                    'category and subcategories'
                )
                continue

            category = self.categories.find_one(
                {'id': product_category['id']},
                {'_id': 0}
            ) or {}

            if not category:
                logger.warning(
                    'Category {category} not found'.format(
                        category=category.get('id')
                    )
                )
                continue

            category['subcategories'] = self._get_sorted_subcategories(
                category=product_category
            )

            category_id = category.get('id')
            if not category['subcategories']:
                category = self._get_fallback_category()
                logger.info(
                    f'Product with sku:{self.__sku}, seller_id:'
                    f'{self.__seller_id} and category:{category_id} '
                    'not found subcategories in categories collection '
                    'set default values to category and subcategories'
                )
            categories.append(category)

        if not categories:
            logger.warning(
                f'Categories not found with scope:{self.name} '
                f'sku:{self.__sku} seller_id:{self.__seller_id} '
                f'categories:{product_categories}'
            )
            return product_categories

        return categories

    def _get_fallback_category(self):
        category = self.categories.find_one(
            {'id': settings.FALLBACK_MISSING_CATEGORY},
            {'_id': 0}
        )

        subcategories = self.categories.find(
            {'id': settings.FALLBACK_MISSING_SUBCATEGORY},
            {'_id': 0}
        )

        category['subcategories'] = list(subcategories)
        return category

    def _get_sorted_subcategories(self, category: Dict):
        subcategories = self.categories.find(
            {'$or': [{'id': sc['id']} for sc in category['subcategories']]},
            {'_id': 0}
        )

        map_subcategories = {a['id']: a for a in list(subcategories)}
        ordered_subcategories = []

        for order_subcategory in category['subcategories']:
            subcategory = map_subcategories.get(order_subcategory['id'])

            if subcategory:
                ordered_subcategories.append(subcategory)

        return ordered_subcategories

    @staticmethod
    def _get_bundles(product):
        bundles = product.get('bundles')

        if not bundles:
            return None

        bundles_to_list = []

        for sku, bundle_info in bundles.items():
            bundles_to_list.append(
                {
                    'sku': sku,
                    'seller_id': product['seller_id'],
                    'price': bundle_info['price'],
                    'quantity': int(bundle_info['quantity'])
                }
            )

        return bundles_to_list
