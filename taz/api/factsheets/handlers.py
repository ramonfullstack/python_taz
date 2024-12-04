import logging

import falcon

from taz.api.common.handlers.base import BaseHandler
from taz.core.storage.factsheet_storage import FactsheetStorage

logger = logging.getLogger(__name__)


class FactsheetHandler(FactsheetStorage, BaseHandler):
    def on_get(self, request, response, sku, seller_id):
        payload = self.get_bucket_data(
            sku=sku,
            seller_id=seller_id
        )

        if not payload:
            self.write_response(response, falcon.HTTP_404)
            return

        self.write_response(response, falcon.HTTP_200, payload)
