from mongoengine import DynamicDocument


class PendingProductModel(DynamicDocument):
    meta = {
        'collection': 'pending_products'
    }
