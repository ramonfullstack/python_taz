import logging
from functools import cached_property

from taz.constants import MAGAZINE_LUIZA_SELLER_ID
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.stock import StockHelper
from taz.utils import convert_id_to_nine_digits

logger = logging.getLogger(__name__)


class Scope(MongodbMixin):
    name = 'stock'

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
    def stocks(self):
        return self.get_collection('stocks')

    @cached_property
    def prices(self):
        return self.get_collection('prices')

    @cached_property
    def stock_helper(self):
        return StockHelper()

    def get_data(self):
        if not self.__navigation_id:
            logger.warning(
                f'Stock event with sku:{self.__sku} and '
                f'seller_id:{self.__seller_id} without navigation_id'
            )
            return []

        self.__navigation_id = convert_id_to_nine_digits(self.__navigation_id)
        stock = self._get_stock()

        return {
            'sku': self.__sku,
            'seller_id': self.__seller_id,
            'navigation_id': self.__navigation_id,
            'stock_count': stock.get('stock_count', 0),
            'minimum_order_quantity': stock.get('minimum_order_quantity', 0)
        }

    def _get_stock(self):
        if self.__seller_id == MAGAZINE_LUIZA_SELLER_ID:
            stock = self.stock_helper.mount(
                sku=self.__sku,
                seller_id=self.__seller_id,
                navigation_id=self.__navigation_id
            )

            price = self.prices.find_one(
                {'sku': self.__sku, 'seller_id': self.__seller_id},
                {'_id': 0, 'minimum_order_quantity': 1}
            ) or {}

            stock.update({**price})
        else:
            stock = self.stocks.find_one(
                {
                    'sku': self.__sku,
                    'seller_id': self.__seller_id,
                    'branch_id': 0
                },
                {'_id': 0, 'stock_count': 1}
            ) or {}

        return stock
