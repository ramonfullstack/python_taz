from maaslogger import base_logger
from simple_settings import settings

from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.reviews import Reviews
from taz.consumers.product_exporter.helpers import (
    _create_enriched_payload,
    _generate_factsheet_url,
    _get_product_url,
    build_images
)
from taz.consumers.product_exporter.scopes.helpers import ScopeHelper
from taz.core.storage.raw_products_storage import RawProductsStorage

logger = base_logger.get_logger(__name__)


class Scope(MongodbMixin):
    name = 'source_product'

    def __init__(self, seller_id, sku):
        self.seller_id = seller_id
        self.sku = sku
        self.scope_helper = ScopeHelper()
        self.__raw_products_storage = RawProductsStorage()
        self.reviews = Reviews()

    @property
    def raw_products(self):
        return self.get_collection('raw_products')

    @property
    def unpublished_products(self):
        return self.get_collection('unpublished_products')

    def get_data(self):
        product = self.__raw_products_storage.get_bucket_data(
            sku=self.sku,
            seller_id=self.seller_id
        )

        if not product:
            logger.warning(
                'Product not found in storage when searching for '
                f'sku:{self.sku} and seller_id:{self.seller_id}.'
            )
            return

        categories = self._get_categories(product)
        if categories:
            product.update(categories)

        main_category = product.get('main_category', {}).get('id') or ''
        if main_category == 'TM':
            logger.warning(
                'Discarding the product because not categorized for '
                'sku:{sku} seller_id:{seller_id} '
                'navigation_id:{navigation_id}'.format(
                    sku=self.sku,
                    seller_id=self.seller_id,
                    navigation_id=product['navigation_id']
                )
            )

            return

        path = _get_product_url(product)
        if not path:
            logger.info(
                'Discarding sku:{sku} seller_id:{seller_id} '
                'navigation_id:{navigation_id} because it was '
                'not possible to generate the url'.format(
                    sku=self.sku,
                    seller_id=self.seller_id,
                    navigation_id=product['navigation_id']
                )
            )
            return

        media = self.scope_helper.get_medias(self.seller_id, self.sku)
        factsheet_url = _generate_factsheet_url(self.sku, self.seller_id)

        images = build_images(
            sku=self.sku,
            seller_id=self.seller_id,
            title=product['title'],
            reference=product.get('reference') or '',
            media=media.get('images') or {} if media else {}
        )

        navigation_id = product['navigation_id']
        if navigation_id.isnumeric():
            navigation_id = navigation_id.ljust(9, '0')

        seller_name = product.get('seller_description')
        if not seller_name:
            seller_name = self.scope_helper.get_seller_name(self.seller_id)

        payload = {
            'scope': self.name,
            'sku': self.sku,
            'seller_id': self.seller_id,
            'seller_name': seller_name,
            'type': product['type'],
            'dimensions': product.get('dimensions') or {},
            'ean': product.get('ean') or product.get('isbn') or '',
            'brand': product['brand'],
            'title': product['title'],
            'description': product['description'] or '',
            'categories': self.scope_helper.get_categories_detail(
                product['categories']
            ),
            'reference': product['reference'],
            'active': not product['disable_on_matching'],
            'attributes': product.get('attributes') or [],
            'medias': images,
            'factsheet_url': factsheet_url,
            'created_at': product['created_at'],
            'parent_sku': product['parent_sku'],
            'navigation_id': navigation_id,
            'path': '{base_url}/{path}'.format(
                base_url=settings.BASE_DESKTOP_URL,
                path=path
            ),
            'selections': product.get('selections') or {},
            'review_count': self.reviews.get_customer_behavior(
                navigation_id=product['navigation_id'],
                behavior_type='product_total_review_count'
            ),
            'review_rating': self.reviews.get_customer_behavior(
                navigation_id=product['navigation_id'],
                behavior_type='product_average_rating'
            )
        }

        ids_info = self.scope_helper.get_offer_id_and_id_correlations(
            self.sku,
            self.seller_id
        )
        if ids_info:
            payload.update(ids_info)

        enriched_products = self.scope_helper.get_enriched_products(
            self.seller_id,
            self.sku,
            skip=settings.SKIP_ENRICHED_SOURCE_IN_SOURCE_PRODUCT
        )

        metadata = _create_enriched_payload(enriched_products)
        payload.update(metadata)

        payload.update(
            self.scope_helper.create_unavailable_product_payload(navigation_id)
        )

        return payload

    def _get_categories(self, product):
        return self.raw_products.find_one(
            {
                'sku': product['sku'],
                'seller_id': product['seller_id']
            },
            {'_id': 0, 'categories': 1}
        )
