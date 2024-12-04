class Scope:  # pragma: no cover
    name = 'fake_scope'

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

    def get_data(self):
        return [
            {
                'foo': 'bar',
                'seller_id': self.__seller_id,
                'sku': self.__sku,
                'scope_name': 'product_original'
            },
            {
                'foo': 'bar',
                'seller_id': self.__seller_id,
                'sku': self.__sku,
            }
        ]
