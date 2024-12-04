import requests
from simple_settings import settings


class HttpClient:

    def post(self, product_id, price, zipcode):
        url = settings.APIS['transformers']['url']

        headers = {
            'Authorization': settings.APIS['transformers']['token']
        }

        payload = {
            'zipCode': zipcode,
            'identification': {
                'pageName': 'product',
                'platform': 'ecommerce'
            },
            'salesChannel': {
                'id': 45
            },
            'products': [{
                'sku': product_id,
                'quantity': 1,
                'value': price
            }]
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        content = response.json()

        return content
