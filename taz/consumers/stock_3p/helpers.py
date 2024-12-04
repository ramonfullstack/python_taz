import copy

from taz.constants import AVAILABILITY_NATIONWIDE, STOCK_TYPE_DC
from taz.consumers.core.stock import StockHelper
from taz.utils import md5


class Stock3pHelper:

    @staticmethod
    def prepare_md5(new_payload):
        payload = new_payload.copy()
        payload.pop('source', None)
        old_md5 = payload.pop('md5', None)

        return md5(payload, old_md5)

    @staticmethod
    def is_missing_stock(data):
        return 'stock_count' not in data

    @staticmethod
    def merge(old_payload, new_payload):
        payload_merged = copy.deepcopy(old_payload)
        payload_merged.update(new_payload)
        return payload_merged

    @staticmethod
    def mount_payload_stocks(sku, seller_id, navigation_id, stock_count):
        stocks = [
            {
                'seller_id': seller_id,
                'sku': sku,
                'branch_id': 0,
                'delivery_availability': AVAILABILITY_NATIONWIDE,
                'position': {
                    'physic': {
                        'amount': stock_count,
                        'reserved': 0,
                        'available': stock_count
                    },
                    'logic': {
                        'amount': 0,
                        'reserved': 0,
                        'available': 0
                    }
                },
                'type': STOCK_TYPE_DC
            }
        ]

        return StockHelper.create_stock_payload(
            sku,
            seller_id,
            navigation_id,
            stocks
        )
