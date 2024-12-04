from taz import constants
from taz.consumers.core.database.mongodb import MongodbMixin


class StockHelper(MongodbMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.stocks = self.get_collection('stocks')

    def mount(
        self,
        sku,
        seller_id,
        navigation_id,
        stock_type=constants.STOCK_TYPE_DC,
        branch_id=None
    ):
        stocks = self._get_stocks(
            sku=sku,
            seller_id=seller_id,
            stock_type=stock_type,
            branch_id=branch_id
        )

        return self.create_stock_payload(
            sku=sku,
            seller_id=seller_id,
            navigation_id=navigation_id,
            stocks=stocks
        )

    def _get_stocks(self, sku, seller_id, stock_type, branch_id=None):
        if stock_type == constants.STOCK_TYPE_DC:
            return list(self.stocks.find({
                'sku': sku,
                'seller_id': seller_id,
                'type': stock_type
            }))

        if not str(branch_id):
            return

        return list(self.stocks.find({
            'sku': sku,
            'seller_id': seller_id,
            'branch_id': branch_id
        }))

    @staticmethod
    def create_stock_payload(sku, seller_id, navigation_id, stocks):
        stock_count = 0
        stock_details = {}

        current_availability = constants.AVAILABILITY_REGIONAL
        stock_type = constants.STOCK_TYPE_ON_SUPPLIER

        for stock in stocks:
            stock_physic = stock['position']['physic']['available']
            stock_logic = stock['position']['logic']['available']

            amount = stock_physic + stock_logic
            stock_count += amount

            if stock['delivery_availability'] == constants.AVAILABILITY_NATIONWIDE:  # noqa
                current_availability = constants.AVAILABILITY_NATIONWIDE

            if stock_physic > 0:
                stock_type = constants.STOCK_TYPE_ON_SELLER

            if amount == 0:
                continue

            stock_details.update({
                str(stock['branch_id']): [{
                    'stock_type': 'on_seller',
                    'quantity': amount
                }]
            })

        payload = {
            'sku': sku,
            'seller_id': seller_id,
            'stock_count': stock_count,
            'stock_type': stock_type,
            'delivery_availability': current_availability,
            'navigation_id': navigation_id
        }

        if seller_id == constants.MAGAZINE_LUIZA_SELLER_ID:
            payload['stock_details'] = stock_details

        return payload
