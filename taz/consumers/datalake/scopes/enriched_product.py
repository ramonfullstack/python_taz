import logging
import time
from functools import cached_property

from slugify import slugify

from taz.constants import (
    DELETE_ACTION,
    SOURCE_METABOOKS,
    SOURCE_RECLASSIFICATION_PRICE_RULE,
    SOURCE_SMARTCONTENT
)
from taz.consumers.core.database.mongodb import MongodbMixin

logger = logging.getLogger(__name__)


class Scope(MongodbMixin):
    name = 'enriched_product'

    def __init__(
        self,
        sku: str,
        seller_id: str,
        **kwargs
    ):
        self.__sku = sku
        self.__seller_id = seller_id
        self.__source = kwargs.get('source')
        self.__action = kwargs.get('action')
        self.__navigation_id = kwargs.get('navigation_id')

    @cached_property
    def enriched_products(self):
        return self.get_collection('enriched_products')

    def get_data(self):
        enriched_products = self.get_enriched_products()

        if not enriched_products:
            logger.warning(
                f'Item not found with scope:{self.name} '
                f'sku:{self.__sku} seller_id:{self.__seller_id}'
            )
            return []

        data = []
        for enriched_product in enriched_products:
            timestamp = enriched_product.get('timestamp')
            if timestamp and isinstance(enriched_product['timestamp'], str):
                enriched_product['timestamp'] = (
                    float(enriched_product['timestamp'])
                )

                self.enriched_products.update_one(
                    {
                        'sku': self.__sku,
                        'seller_id': self.__seller_id,
                        'source': enriched_product['source']
                    },
                    {'$set': {'timestamp': enriched_product['timestamp']}}
                )

            enriched_metadata = enriched_product.get('metadata') or {}
            metadata = {'code_anatel': enriched_metadata.get('code_anatel')}
            for key, value in enriched_metadata.items():
                metadata[self._slugify(key)] = value

            enriched_product['metadata'] = metadata
            enriched_product['from'] = enriched_product.get('from') or {}
            enriched_product['active'] = enriched_product.get('active', True)
            enriched_product['price'] = float(enriched_product.get('price', 0))
            for field in {'identifier', 'product_type', 'rule_id'}:
                enriched_product[field] = enriched_product.get(field)

            data.append(enriched_product)

        return data

    def get_enriched_products(self):
        enriched_products = None

        if (
            self.__source == SOURCE_RECLASSIFICATION_PRICE_RULE and
            self.__action == DELETE_ACTION
        ):
            return [{
                'sku': self.__sku,
                'seller_id': self.__seller_id,
                'source': SOURCE_RECLASSIFICATION_PRICE_RULE,
                'active': False,
                'timestamp': time.time(),
                'navigation_id': self.__navigation_id,
            }]

        if self.__source:
            enriched_products = list(self.enriched_products.find(
                {
                    'sku': self.__sku,
                    'seller_id': self.__seller_id,
                    'source': {
                        '$in': [
                            self.__source,
                            SOURCE_SMARTCONTENT,
                            SOURCE_METABOOKS
                        ]
                    }
                },
                {
                    '_id': 0
                }
            ))

        if not enriched_products:
            enriched_products = list(
                self.enriched_products.find(
                    {
                        'sku': self.__sku,
                        'seller_id': self.__seller_id
                    },
                    {
                        '_id': 0
                    }
                )
            )

        return enriched_products

    @staticmethod
    def _slugify(key):
        return slugify(key).replace('-', '_')
