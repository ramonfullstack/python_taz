import logging
from functools import cached_property

from taz.consumers.core.database.mongodb import MongodbMixin

logger = logging.getLogger(__name__)


class Scope(MongodbMixin):
    name = 'product_score'

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
    def scores(self):
        return self.get_collection('scores')

    def get_data(self):
        product_score = self.scores.find_one(
            {
                'sku': self.__sku,
                'seller_id': self.__seller_id,
                'active': True
            },
            {
                '_id': 0,
                'sku': 1,
                'seller_id': 1,
                'sources': 1,
                'final_score': 1
            }
        )

        if not product_score:
            logger.warning(
                f'Item not found with scope:{self.name} '
                f'sku:{self.__sku} seller_id:{self.__seller_id}'
            )
            return []

        for source in product_score.get('sources') or []:
            source['value'] = str(source['value'])

        return product_score
