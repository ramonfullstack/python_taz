import json

from maaslogger import base_logger
from simple_settings import settings

from taz.consumers.core.brokers.stream import (
    PubSubRecordProcessorValidateSchema
)
from taz.consumers.core.brokers.stream.pubsub import PubSubBrokerRawEvent
from taz.consumers.rebuild.scopes.base import BaseRebuildWithRawMessage
from taz.consumers.rebuild.scopes.marvin_seller_paginator import (
    RebuildMarvinSellerPaginator
)

from .schema import RebuildSchema
from .scopes.catalog_notification import RebuildCatalogNotification
from .scopes.classify_product import RebuildClassifyProduct
from .scopes.complete_products import (
    RebuildCompleteProductBySeller,
    RebuildCompleteProductBySku
)
from .scopes.inactivate_seller_products import RebuildInactivateSellerProducts
from .scopes.maas_product_reprocess import MaasProductReprocess
from .scopes.marvin_seller import RebuildMarvinSeller
from .scopes.marvin_seller_ipdv import RebuildMarvinSellerIpdv
from .scopes.matching_omnilogic import RebuildMatchingOmnilogic
from .scopes.matching_product import RebuildMatchingProduct
from .scopes.media import MediaRebuild
from .scopes.product_score import (
    RebuildProductScoreBySeller,
    RebuildProductScoreBySku
)
from .scopes.seller import RebuildProductSeller
from .scopes.seller_sells_to_company import RebuildSellerSellsToCompany

logger = base_logger.get_logger(__name__)

SCOPE = 'rebuild'


class RebuildProcessor(PubSubRecordProcessorValidateSchema):
    schema_class = RebuildSchema
    SCOPES = {
        'seller': RebuildProductSeller,
        'complete_products_by_seller': RebuildCompleteProductBySeller,
        'complete_products_by_sku': RebuildCompleteProductBySku,
        'catalog_notification': RebuildCatalogNotification,
        'product_score_by_seller': RebuildProductScoreBySeller,
        'product_score_by_sku': RebuildProductScoreBySku,
        'marvin_seller': RebuildMarvinSeller,
        'rebuild_marvin_seller_paginator': RebuildMarvinSellerPaginator,
        'matching_omnilogic': RebuildMatchingOmnilogic,
        'inactivate_seller_products': RebuildInactivateSellerProducts,
        'marvin_seller_ipdv': RebuildMarvinSellerIpdv,
        'seller_sells_to_company': RebuildSellerSellsToCompany,
        'matching_by_sku': RebuildMatchingProduct,
        'classify_by_sku': RebuildClassifyProduct,
        'maas_product_reprocess': MaasProductReprocess,
        'media_rebuild': MediaRebuild
    }

    def process_message(self, event):
        logger.debug(f'event:{event}')
        decode_msg = json.loads(event.data)
        logger.debug(f'decode_msg:{decode_msg}')
        data = decode_msg.get('data') or {}
        scope = decode_msg['scope']
        action = decode_msg['action']

        logger.info('Rebuild consumer run with scope:{}'.format(scope))

        rebuild_scope = self.SCOPES[scope]()
        if isinstance(rebuild_scope, BaseRebuildWithRawMessage):
            return rebuild_scope.rebuild(event, action, data)

        return rebuild_scope.rebuild(action, data)


class RebuildConsumer(PubSubBrokerRawEvent):
    scope = SCOPE
    record_processor_class = RebuildProcessor
    project_name = settings.GOOGLE_PROJECT_ID
    subscription_name = settings.PUBSUB_REBUILD_SUB_NAME
