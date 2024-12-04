import logging

import falcon

from taz.api.common.handlers.base import BaseHandler
from taz.consumers.core.database.mongodb import MongodbMixin

logger = logging.getLogger(__name__)


class EntitiesHandler(BaseHandler, MongodbMixin):

    @property
    def enriched_products(self):
        return self.get_collection('enriched_products')

    def on_get(self, request, response):
        entities = self.enriched_products.distinct('entity')

        self.write_response(
            response,
            falcon.HTTP_200,
            {'data': entities}
        )
