import os
import pathlib

import falcon
from falcon_swagger_ui import register_swaggerui_app
from mongoengine import connect
from prometheus_client.core import REGISTRY
from simple_settings import settings

from taz.api.badges.handlers import (
    BadgeHandler,
    BadgeListHandler,
    BadgePaginatedListHandler,
    BadgeProductItemHandler,
    BadgeProductListItemHandler
)
from taz.api.blacklist.handlers import BlacklistHandler, BlacklistListHandler
from taz.api.buybox.handlers import (
    BuyBoxHandler,
    BuyBoxProductListHandler,
    BuyBoxSellerHandler
)
from taz.api.classifications_rules.handlers import (
    ClassificationsRulesByIdHandler,
    ClassificationsRulesHandler
)
from taz.api.common.exceptions import HttpError
from taz.api.enriched_products.handlers import (
    EnrichedProductsHandler,
    EnrichedSellerProductsHandler,
    EnrichedSourceHandler
)
from taz.api.entities.handlers import EntitiesHandler
from taz.api.exports.handlers import (
    ExportsSimpleProductByNavigationIDHandler,
    ExportsSimpleProductHandler,
    ExportsSourceProductByNavigationIDHandler,
    ExportsSourceProductHandler
)
from taz.api.factsheets.handlers import FactsheetHandler
from taz.api.forbidden_terms.handlers import (
    ForbiddenTermsHandler,
    ForbiddenTermsRedisHandler
)
from taz.api.healthcheck.handlers import HealthcheckHandler
from taz.api.matching.handlers import MatchingHandler, RemoveMatchingHandler
from taz.api.medias.handlers import (
    ProductMediasNavigationIdHandler,
    ProductMediasSkuSellerHandler
)
from taz.api.metabooks.handlers import MetabooksCategoryHandler
from taz.api.metadata.handlers import MetadataInputHandler
from taz.api.metrics.collector import MetricsCollector
from taz.api.metrics.handlers import MetricsHandler
from taz.api.middlewares.access_log import AccessLogMiddleware
from taz.api.middlewares.authorization import AuthorizationMiddleware
from taz.api.middlewares.cors import CORSMiddleware
from taz.api.middlewares.json_translator import JsonTranslator
from taz.api.middlewares.version import VersionMiddleware
from taz.api.minimum_order_quantity.handlers import (
    MinimumOrderQuantityByNavigationIdHandler,
    MinimumOrderQuantityBySkuAndSellerIdHandler
)
from taz.api.notification.handlers import NotificationHandler
from taz.api.pending.handlers import (
    ListPendingHandler,
    PendingHandler,
    PendingSellerHandler
)
from taz.api.price_lock.handlers import PriceLockHandler, PriceLockListHandler
from taz.api.products.handlers import (
    CustomProductAttributes,
    ListProductHandler,
    ListProductsHandler,
    ProductEanHandler,
    ProductExtraDataHandler,
    ProductHandler,
    ProductNavigationIdHandler,
    ProductStatHandler,
    ProductUnpublishHandler,
    ProductVariationHandler,
    RawProductByNavigationHandler,
    RawProductBySkuSellerHandler,
    TrustedProductEanHandler
)
from taz.api.rebuild.handlers import (
    RebuildCatalogNotificationHandler,
    RebuildClassifyProductHandler,
    RebuildDatalakeHandler,
    RebuildHandler,
    RebuildMarvinSellerHandler,
    RebuildMatchingOmnilogicHandler,
    RebuildMatchingProductHandler,
    RebuildMediaHandler,
    RebuildMetabooksHandler,
    RebuildPriceRulesHandler,
    RebuildProductExporterHandler,
    RebuildProductHandler,
    RebuildProductScoreBySkuHandler,
    RebuildProductScoreHandler
)
from taz.api.redis.handlers import RedisPollerHandler
from taz.api.score_criterias.handlers import (
    ScoreCriteriaHandler,
    ScoreCriteriaListHandler
)
from taz.api.score_weights.handlers import (
    ScoreWeightHandler,
    ScoreWeightListHandler
)
from taz.api.scores.handlers.catalog_score_handler import CatalogScoreHandler
from taz.api.scores.handlers.category_score_handler import CategoryScoreHandler
from taz.api.scores.handlers.product_score_handler import ProductScoreHandler
from taz.api.scores.handlers.seller_score_handler import SellerScoreHandler
from taz.api.sellers.handlers import ListSellerHandler, SellerHandler
from taz.api.stocks.handlers import StockListHandler
from taz.helpers.setup_sentry import setup_sentry
from taz.settings.otel import configure_otel_instrumentation

connect('acme', host=settings.MONGO_URI)
configure_otel_instrumentation()


class App(falcon.API):
    def __init__(self, *args, **kwargs):

        SENTRY_DSN = os.getenv('SENTRY_DSN')
        if SENTRY_DSN:  # pragma: no cover
            setup_sentry(SENTRY_DSN)

        super().__init__(*args, **kwargs)

        # handlers
        self.add_route('/healthcheck', HealthcheckHandler())
        self.add_route(
            '/matching/seller/{seller_id}/sku/{sku}', MatchingHandler()
        )
        self.add_route(
            '/matching/remove/{variation_id}', RemoveMatchingHandler()
        )
        self.add_route('/product/list', ListProductHandler())
        self.add_route(
            '/product/seller/{seller_id}/sku/{sku}', ProductHandler()
        )
        self.add_route(
            '/product/variation/{seller_id}/count', ProductStatHandler()
        )
        self.add_route(
            '/product/variation/unpublish', ProductUnpublishHandler()
        )
        self.add_route(
            '/product/navigation/{navigation_id}', ProductNavigationIdHandler()
        )
        self.add_route(
            '/product/medias/seller/{seller}/sku/{sku}',
            ProductMediasSkuSellerHandler()
        )
        self.add_route(
            '/product/medias/navigation_id/{navigation_id}',
            ProductMediasNavigationIdHandler()
        )
        self.add_route(
            '/product/custom-attributes/{seller_id}/{sku}',
            CustomProductAttributes()
        )
        self.add_route('/product/ean/{ean}', ProductEanHandler())
        self.add_route(
            '/trusted_product/ean/{ean}',
            TrustedProductEanHandler()
        )
        self.add_route(
            '/product/parent_sku/{parent_sku}/seller_id/{seller_id}',
            ProductVariationHandler()
        )
        self.add_route(
            '/product/raw/seller_id/{seller_id}/sku/{sku}',
            RawProductBySkuSellerHandler()
        )
        self.add_route(
            '/product/raw/navigation_id/{navigation_id}',
            RawProductByNavigationHandler()
        )
        self.add_route('/pending/list', ListPendingHandler())
        self.add_route(
            '/pending/seller/{seller_id}/sku/{sku}', PendingHandler()
        )
        self.add_route('/pending/sellers', PendingSellerHandler())

        self.add_route(
            '/badge/{slug}/sku/{sku}/seller/{seller_id}',
            BadgeProductItemHandler()
        )
        self.add_route(
            '/badge/{slug}/products',
            BadgeProductListItemHandler()
        )
        self.add_route('/badge/list', BadgeListHandler())
        self.add_route('/v1/badges', BadgePaginatedListHandler())
        self.add_route('/badge/{slug}', BadgeHandler())
        self.add_route('/badge', BadgeHandler())
        self.add_route(
            '/price_lock/list', PriceLockListHandler()
        )
        self.add_route(
            '/price_lock', PriceLockHandler()
        )
        self.add_route(
            '/price_lock/seller/{seller_id}', PriceLockHandler()
        )

        self.add_route('/buybox/sellers', BuyBoxSellerHandler())
        self.add_route(
            '/buybox/products/{seller_id}',
            BuyBoxProductListHandler()
        )
        self.add_route('/buybox/seller/{seller_id}/sku/{sku}', BuyBoxHandler())

        self.add_route('/notification/{source}', NotificationHandler())

        self.add_route('/blacklist', BlacklistHandler())
        self.add_route('/blacklist/list', BlacklistListHandler())

        self.add_route('/rebuild/notification', RebuildHandler())
        self.add_route(
            '/rebuild/catalog/notification',
            RebuildCatalogNotificationHandler()
        )

        self.add_route('/rebuild/products', RebuildProductHandler())
        self.add_route('/rebuild/marvin/seller', RebuildMarvinSellerHandler())
        self.add_route('/rebuild/medias', RebuildMediaHandler())
        self.add_route('/rebuild/score', RebuildProductScoreHandler())
        self.add_route('/rebuild/metabooks/{ean}', RebuildMetabooksHandler())

        self.add_route(
            '/rebuild/score/products', RebuildProductScoreBySkuHandler()
        )

        self.add_route(
            '/rebuild/matching/omnilogic', RebuildMatchingOmnilogicHandler()
        )
        self.add_route(
            '/rebuild/product/exporter', RebuildProductExporterHandler()
        )
        self.add_route(
            '/rebuild/matching/product',
            RebuildMatchingProductHandler()
        )
        self.add_route(
            '/rebuild/classify/product',
            RebuildClassifyProductHandler()
        )

        self.add_route('/seller/list', ListSellerHandler())
        self.add_route('/seller', SellerHandler())
        self.add_route('/seller/{seller_id}', SellerHandler())

        self.add_route('/metrics', MetricsHandler())

        self.add_route(
            '/enriched_product/{navigation_id}',
            EnrichedProductsHandler()
        )
        self.add_route(
            '/enriched_product/sku/{sku}/seller/{seller_id}',
            EnrichedSellerProductsHandler()
        )

        self.add_route(
            '/enriched_product/sku/{sku}/seller/{seller_id}/source/{source}',
            EnrichedSourceHandler()
        )

        self.add_route(
            '/enriched_product/navigation_id/{navigation_id}/source/{source}',
            EnrichedSourceHandler()
        )

        self.add_route('/entity/list', EntitiesHandler())

        self.add_route(
            '/score/seller/{seller_id}', SellerScoreHandler()
        )

        self.add_route(
            '/score/category/{category_id}', CategoryScoreHandler()
        )

        self.add_route(
            '/score/seller/{seller_id}/sku/{sku}', ProductScoreHandler()
        )

        self.add_route('/metabooks/categories', MetabooksCategoryHandler())

        self.add_route('/score/criteria/list', ScoreCriteriaListHandler())
        self.add_route('/score/criteria', ScoreCriteriaHandler())
        self.add_route('/score/criteria/{entity_name}', ScoreCriteriaHandler())

        self.add_route('/score/weight/list', ScoreWeightListHandler())
        self.add_route('/score/weight', ScoreWeightHandler())
        self.add_route(
            '/score/weight/{entity_name}/{criteria_name}',
            ScoreWeightHandler()
        )
        self.add_route('/score', CatalogScoreHandler())

        self.add_route(
            '/factsheet/seller/{seller_id}/sku/{sku}', FactsheetHandler()
        )

        self.add_route('/redis/poller/key/{key}', RedisPollerHandler())

        self.add_route(
            '/stocks/seller/{seller_id}/sku/{sku}', StockListHandler()
        )

        self.add_route('/metadatainput/notification/', MetadataInputHandler())

        self.add_route('/v1/products', ListProductsHandler())

        self.add_route('/v1/products/forbidden_terms', ForbiddenTermsHandler())

        self.add_route('/forbidden_terms/', ForbiddenTermsRedisHandler())

        self.add_route('/product/extra_data', ProductExtraDataHandler())

        self.add_route(
            '/exports/simple_product/seller_id/{seller_id}/sku/{sku}',
            ExportsSimpleProductHandler()
        )

        self.add_route(
            '/exports/simple_product/navigation_id/{navigation_id}',
            ExportsSimpleProductByNavigationIDHandler()
        )

        self.add_route(
            '/exports/source_product/seller_id/{seller_id}/sku/{sku}',
            ExportsSourceProductHandler()
        )

        self.add_route(
            '/exports/source_product/navigation_id/{navigation_id}',
            ExportsSourceProductByNavigationIDHandler()
        )

        self.add_route('/rebuild/datalake', RebuildDatalakeHandler())
        self.add_route('/classifications_rules', ClassificationsRulesHandler())
        self.add_route('/classifications_rules/{id}', ClassificationsRulesByIdHandler())
        self.add_route('/rebuild/price_rules', RebuildPriceRulesHandler())

        self.add_route(
            '/moq/seller_id/{seller_id}/sku/{sku}',
            MinimumOrderQuantityBySkuAndSellerIdHandler()
        )

        self.add_route(
            '/moq/navigation_id/{navigation_id}',
            MinimumOrderQuantityByNavigationIdHandler()
        )

        # custom error
        self.add_error_handler(HttpError, HttpError.handler)

        jobtype = os.getenv('JOB_TYPE') or 'API'
        if jobtype not in ('poller', 'consumer'):
            REGISTRY.register(MetricsCollector())


app = App(middleware=[
    AccessLogMiddleware(),
    VersionMiddleware(),
    AuthorizationMiddleware(),
    JsonTranslator(),
    CORSMiddleware(allow_origins=settings.CORS_ALLOW_ORIGINS)
])

SWAGGERUI_URL = '/docs'
SCHEMA_URL = '/static/v1/swagger.yaml'
STATIC_PATH = pathlib.Path(__file__).parent / 'static'
app.add_static_route('/static', str(STATIC_PATH))
page_title = 'Taz API Swagger'
favicon_url = 'https://falconframework.org/favicon-32x32.png'

register_swaggerui_app(
    app, SWAGGERUI_URL, SCHEMA_URL,
    page_title=page_title,
    favicon_url=favicon_url,
    config={'supportedSubmitMethods': ['get', 'post', 'put', 'delete'], }
)
