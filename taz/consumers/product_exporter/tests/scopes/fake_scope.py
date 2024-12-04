class Scope:  # pragma: no cover
    name = 'fake_scope'

    def __init__(self, seller_id, sku):
        self.seller_id = seller_id
        self.sku = sku

    def get_data(self):
        return {
            'foo': 'bar',
            'seller_id': self.seller_id,
            'sku': self.sku,
            'navigation_id': 'bar'
        }
