from functools import cached_property
from typing import Dict

from maaslogger import base_logger

from taz import constants
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.utils import valid_ean

logger = base_logger.get_logger(__name__)


class RankGenerator(MongodbMixin):

    @cached_property
    def raw_products(self):
        return self.get_collection('raw_products')

    def _handle_default_seller_specific_rules(self, product: Dict) -> int:
        if 'ean' in product:
            similar_products = self.raw_products.find({
                'ean': product['ean'],
                'seller_id': product['seller_id']
            })

            if similar_products.count() > 0:
                return 0

        return 1000

    def compute_grade(self, product: Dict) -> int:
        grade = 0
        sku = product['sku']
        seller_id = product['seller_id']

        if seller_id == constants.MAGAZINE_LUIZA_SELLER_ID:
            grade = self._handle_default_seller_specific_rules(product)

        if len(product.get('title', '')) >= 70:
            grade += 10

        if valid_ean(product.get('ean', '')):
            grade += 10

        logger.debug(
            f'Grade computed for sku:{sku} '
            f'seller_id:{seller_id} grade:{grade}'
        )

        return grade
