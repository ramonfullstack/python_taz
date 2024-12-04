import logging

from marshmallow import Schema, fields

from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.maas_product import MaasProductHTTPClient
from taz.consumers.rebuild.scopes.base import BaseRebuild

logger = logging.getLogger(__name__)


class MaasProductReprocessDataSchema(Schema):
    seller_id = fields.String(required=True)
    sku = fields.String(required=True)
    source = fields.String(required=True)


class MaasProductReprocess(MongodbMixin, BaseRebuild):
    schema_class = MaasProductReprocessDataSchema
    poller_scope = 'maas_product_reprocess'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maas_product_client = MaasProductHTTPClient()

    def _rebuild(self, action: str, data: dict) -> bool:
        success = self.maas_product_client.reprocess(data)
        logger.info(
            f'Processed rebuild {self.poller_scope} with action:{action} '
            f'request:{data} success:{success}'
        )
        return True
