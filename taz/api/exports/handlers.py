import falcon

from taz.api.common.handlers.base import BaseHandler
from taz.api.products.models import RawProductModel
from taz.consumers.product_exporter.scopes.simple_product import (
    Scope as SimpleProductScope
)
from taz.consumers.product_exporter.scopes.source_product import (
    Scope as SourceProductScope
)


class ExportsSimpleProductHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_get(self, request, response, seller_id, sku):
        payload = SimpleProductScope(seller_id, sku).get_data()
        if payload:
            self.write_response(response, falcon.HTTP_200, {'data': payload})
        else:
            self.write_response(response, falcon.HTTP_404)


class ExportsSimpleProductByNavigationIDHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_get(self, request, response, navigation_id):
        payload = {}
        product = RawProductModel.get_product_by_navigation_id(navigation_id)
        if product:
            payload = SimpleProductScope(
                product['seller_id'], product['sku']
            ).get_data()

        if payload:
            self.write_response(response, falcon.HTTP_200, {'data': payload})
        else:
            self.write_response(response, falcon.HTTP_404)


class ExportsSourceProductHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_get(self, request, response, seller_id, sku):
        payload = SourceProductScope(seller_id, sku).get_data()
        if payload:
            self.write_response(response, falcon.HTTP_200, {'data': payload})
        else:
            self.write_response(response, falcon.HTTP_404)


class ExportsSourceProductByNavigationIDHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_get(self, request, response, navigation_id):
        payload = {}
        product = RawProductModel.get_product_by_navigation_id(navigation_id)
        if product:
            payload = SourceProductScope(
                product['seller_id'], product['sku']
            ).get_data()

        if payload:
            self.write_response(response, falcon.HTTP_200, {'data': payload})
        else:
            self.write_response(response, falcon.HTTP_404)
