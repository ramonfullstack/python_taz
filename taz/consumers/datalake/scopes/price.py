import logging

from taz.consumers.core.database.mongodb import MongodbMixin

logger = logging.getLogger(__name__)


class Scope(MongodbMixin):
    name = 'price'

    def __init__(
        self,
        sku: str,
        seller_id: str,
        navigation_id: str = None,
        **kwargs
    ):
        self.__sku = sku
        self.__seller_id = seller_id
        self.__navigation_id = navigation_id

    @property
    def prices(self):
        return self.get_collection('prices')

    def get_data(self):
        price = self.prices.find_one(
            {
                'sku': self.__sku,
                'seller_id': self.__seller_id
            },
            {
                '_id': 0,
                'sku': 1,
                'seller_id': 1,
                'price': 1,
                'list_price': 1,
                'last_updated_at': 1,
                'currency': 1
            }
        )

        if not price:
            logger.warning(
                f'Price not found with scope:{self.name} '
                f'sku:{self.__sku} seller_id:{self.__seller_id}'
            )
            return

        return price
