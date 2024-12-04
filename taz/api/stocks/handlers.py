import json

import falcon

from taz.api.common.handlers.base import BaseHandler
from taz.api.stocks.models import StockModel


class StockListHandler(BaseHandler):
    def on_get(self, request, response, sku, seller_id):
        stocks = StockModel.objects(sku=sku, seller_id=seller_id)

        if not stocks:
            self.write_response(response, falcon.HTTP_404)
            return

        payload = []
        for stock in stocks:
            payload.append(json.loads(stock.to_json()))

        self.write_response(response, falcon.HTTP_200, payload)
