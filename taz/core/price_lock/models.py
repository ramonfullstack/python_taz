from mongoengine import DateTimeField, Document, FloatField, StringField


class PriceLockModel(Document):
    seller_id = StringField(max_length=200, required=True)
    percent = FloatField(required=True)
    user = StringField(max_length=200)
    updated_at = DateTimeField()
    meta = {
        'collection': 'price_lock',
        'indexes': [
            'seller_id'
        ]
    }
