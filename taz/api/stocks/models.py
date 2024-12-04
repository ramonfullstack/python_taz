from mongoengine import DynamicDocument


class StockModel(DynamicDocument):
    meta = {
        'collection': 'stocks',
        'shard_key': ('sku', 'seller_id',)
    }
