import logging
from functools import partial

from simple_settings import settings

from .catalog_notification.consumer import CatalogNotificationConsumer
from .category.consumer import CategoryConsumer
from .complete_product.consumer import CompleteProductConsumer
from .datalake.consumer import DataLakeConsumer
from .enriched_product.consumer import EnrichedProductConsumer
from .factsheet.consumer import FactsheetConsumer
from .label.consumer import LabelConsumer
from .matching.consumer import MatchingConsumer
from .matching_product.consumer import MatchingProductConsumer
from .media.consumer import MediaConsumer
from .media_bucket.consumer import MediaBucketConsumer
from .metadata_input.consumer import MetadataInputConsumer
from .metadata_verify.consumer import MetadataVerifyConsumer
from .price_3p.consumer import Price3pConsumer
from .price_rule.consumer import PriceRuleConsumer
from .pricing.consumer import PricingConsumer
from .product.consumer import ProductConsumer
from .product_exporter.consumer import ProductExporterConsumer
from .product_score.consumer import ProductScoreConsumer
from .product_writer.consumer import ProductWriterConsumer
from .rebuild.consumer import RebuildConsumer
from .stock.consumer import StockConsumer
from .stock_3p.consumer import Stock3pConsumer
from .update_category.consumer import UpdateCategoryConsumer
from .user_review.consumer import UserReviewConsumer

logger = logging.getLogger(__name__)


def consumer_handler(consumer_class, args):
    consumer = consumer_class()
    execute(consumer)


media_handler = partial(consumer_handler, MediaConsumer)
factsheet_handler = partial(consumer_handler, FactsheetConsumer)
category_handler = partial(consumer_handler, CategoryConsumer)
product_handler = partial(consumer_handler, ProductConsumer)
enriched_product_handler = partial(consumer_handler, EnrichedProductConsumer)
price_3p_handler = partial(consumer_handler, Price3pConsumer)
price_rule_handler = partial(consumer_handler, PriceRuleConsumer)
pricing_handler = partial(consumer_handler, PricingConsumer)
matching_handler = partial(consumer_handler, MatchingConsumer)
product_writer_handler = partial(consumer_handler, ProductWriterConsumer)
product_score_handler = partial(consumer_handler, ProductScoreConsumer)
rebuild_handler = partial(consumer_handler, RebuildConsumer)
update_category_handler = partial(consumer_handler, UpdateCategoryConsumer)
datalake_handler = partial(consumer_handler, DataLakeConsumer)
stock_handler = partial(consumer_handler, StockConsumer)
stock3p_handler = partial(consumer_handler, Stock3pConsumer)
user_review_handler = partial(consumer_handler, UserReviewConsumer)
matching_product_handler = partial(consumer_handler, MatchingProductConsumer)
product_exporter_handler = partial(
    consumer_handler, ProductExporterConsumer
)
complete_product_handler = partial(consumer_handler, CompleteProductConsumer)
metadata_input_handler = partial(consumer_handler, MetadataInputConsumer)
metadata_verify_handler = partial(consumer_handler, MetadataVerifyConsumer)
label_handler = partial(consumer_handler, LabelConsumer)
media_bucket_handler = partial(consumer_handler, MediaBucketConsumer)
catalog_notification_handler = partial(
    consumer_handler, CatalogNotificationConsumer
)


def loop(consumer):  # pragma: no cover
    while True:
        if consumer.halt_requested:
            break

        consumer.start()


def execute(consumer):  # pragma: no cover
    try:
        logger.info('Starting consumer with scope:"{}"'.format(consumer.scope))
        if consumer.run_in_loop and settings.CONSUMER_LOOP_ENABLED:
            loop(consumer)
        else:
            consumer.start()
    except KeyboardInterrupt:
        logger.warning(
            'Halting consumer execution, user requests interruption'
        )
    except Exception as e:
        logger.exception(
            'A serious error happened in scope:{} payload:{}! '
            'RUN RUN RUN'.format(consumer.scope, consumer)
        )
        raise e
    finally:
        consumer.stop()
