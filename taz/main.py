import argparse
import os

from taz.consumers import main as consumers
from taz.settings.otel import configure_otel_instrumentation

try:
    from taz.pollers import main as pollers
except ModuleNotFoundError:  # noqa  # pragma: no cover
    import logging
    logger = logging.getLogger(__name__)
    logger.warning('Pollers not available to current server')
    pollers = None

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# POLLERS PARSERS
if pollers:
    poller_parser = subparsers.add_parser(
        'poller',
        help=(
            'Polls "product", "category", "media", "factsheet", "price", '
            '"product_clicks_quantity", "base_price", '
            '"product_sold_quantity", "partner", "badge" or "lu_content" '
            'from Magazine Luiza data sources'
        )
    )
    poller_subparsers = poller_parser.add_subparsers()

    product_poller_parser = poller_subparsers.add_parser(
        'product', help='Product poller'
    )
    product_poller_parser.set_defaults(handler=pollers.product_handler)

    category_poller_parser = poller_subparsers.add_parser(
        'category', help='Category poller'
    )
    category_poller_parser.set_defaults(handler=pollers.category_handler)

    price_poller_parser = poller_subparsers.add_parser(
        'price', help='Price poller'
    )
    price_poller_parser.set_defaults(handler=pollers.price_handler)

    base_price_poller_parser = poller_subparsers.add_parser(
        'base_price', help='Base price poller'
    )
    base_price_poller_parser.set_defaults(handler=pollers.base_price_handler)

    price_campaign_poller_parser = poller_subparsers.add_parser(
        'price_campaign', help='Price Campaign poller'
    )
    price_campaign_poller_parser.set_defaults(
        handler=pollers.price_campaign_handler
    )

    video_poller_parser = poller_subparsers.add_parser(
        'video', help='Video poller'
    )
    video_poller_parser.set_defaults(handler=pollers.video_handler)

    factsheet_poller_parser = poller_subparsers.add_parser(
        'factsheet', help='Factsheet poller'
    )
    factsheet_poller_parser.set_defaults(handler=pollers.factsheet_handler)

    partner_poller_parser = poller_subparsers.add_parser(
        'partner', help='Partner poller'
    )
    partner_poller_parser.set_defaults(handler=pollers.partner_handler)

    lu_content_poller_parser = poller_subparsers.add_parser(
        'lu_content', help='Lu Content poller'
    )
    lu_content_poller_parser.set_defaults(handler=pollers.lu_content_handler)

# CONSUMERS PARSERS
consumer_parser = subparsers.add_parser(
    'consumer',
    help='Consumer information from Kinesis broker',
)
consumer_subparsers = consumer_parser.add_subparsers()

media_consumer_parser = consumer_subparsers.add_parser(
    'media', help='Consume medias from Kinesis broker'
)
media_consumer_parser.set_defaults(handler=consumers.media_handler)

factsheet_consumer_parser = consumer_subparsers.add_parser(
    'factsheet', help='Consume factsheets from Kinesis broker'
)
factsheet_consumer_parser.set_defaults(handler=consumers.factsheet_handler)

category_consumer_parser = consumer_subparsers.add_parser(
    'category', help='Consume categories from Kinesis broker'
)
category_consumer_parser.set_defaults(handler=consumers.category_handler)

product_consumer_parser = consumer_subparsers.add_parser(
    'product', help='Consume and rank products from Kinesis broker'
)

product_consumer_parser.set_defaults(handler=consumers.product_handler)

enriched_product_consumer_parser = consumer_subparsers.add_parser(
    'enriched_product', help='Consume enriched products from SQS broker'
)

enriched_product_consumer_parser.set_defaults(
    handler=consumers.enriched_product_handler
)

stock3p_consumer_parser = consumer_subparsers.add_parser(
    'stock_3p', help='Consume stock 3p from PubSub'
)
stock3p_consumer_parser.set_defaults(handler=consumers.stock3p_handler)

price_3p_consumer_parser = consumer_subparsers.add_parser(
    'price_3p', help='Consume price 3p from PubSub'
)
price_3p_consumer_parser.set_defaults(handler=consumers.price_3p_handler)

price_rule_consumer_parser = consumer_subparsers.add_parser(
    'price_rule', help='Consume price rule from PubSub'
)
price_rule_consumer_parser.set_defaults(handler=consumers.price_rule_handler)

pricing_consumer_parser = consumer_subparsers.add_parser(
    'pricing', help='Consume dynamic pricing from PubSub'
)
pricing_consumer_parser.set_defaults(handler=consumers.pricing_handler)

matching_consumer_parser = consumer_subparsers.add_parser(
    'matching', help='Consume matchings from SQS broker'
)
matching_consumer_parser.set_defaults(handler=consumers.matching_handler)

product_score_consumer_parser = consumer_subparsers.add_parser(
    'product_score', help='Consume product_score from SQS broker'
)
product_score_consumer_parser.set_defaults(
    handler=consumers.product_score_handler
)

product_writer_consumer_parser = consumer_subparsers.add_parser(
    'product_writer', help='Consume and rank product_writers from SQS broker'
)
product_writer_consumer_parser.set_defaults(
    handler=consumers.product_writer_handler
)

rebuild_consumer_parser = consumer_subparsers.add_parser(
    'rebuild',
    help='Consume message to start rebuild process'
)
rebuild_consumer_parser.set_defaults(handler=consumers.rebuild_handler)

complete_product_consumer_parser = consumer_subparsers.add_parser(
    'complete_product', help='Consume Complete Product Queue'
)
complete_product_consumer_parser.set_defaults(
    handler=consumers.complete_product_handler
)

metadata_input_consumer_parser = consumer_subparsers.add_parser(
    'metadata_input', help='Consume Metadata Input Queue'
)
metadata_input_consumer_parser.set_defaults(
    handler=consumers.metadata_input_handler
)

metadata_verify_consumer_parser = consumer_subparsers.add_parser(
    'metadata_verify', help='Consume Metadata Verify Queue'
)
metadata_verify_consumer_parser.set_defaults(
    handler=consumers.metadata_verify_handler
)

update_category_consumer_parser = consumer_subparsers.add_parser(
    'update_category', help='Consume Update Category Queue'
)
update_category_consumer_parser.set_defaults(
    handler=consumers.update_category_handler
)

datalake_consumer_parser = consumer_subparsers.add_parser(
    'datalake', help='Consume SQS Datalake Queue'
)
datalake_consumer_parser.set_defaults(
    handler=consumers.datalake_handler
)

product_exporter_consumer_parser = consumer_subparsers.add_parser(
    'product_exporter', help='Consume SQS Product Exporter Queue'
)
product_exporter_consumer_parser.set_defaults(
    handler=consumers.product_exporter_handler
)

stock_consumer_parser = consumer_subparsers.add_parser(
    'stock', help='Consume Stock PubSub'
)
stock_consumer_parser.set_defaults(
    handler=consumers.stock_handler
)

user_view_consumer_parser = consumer_subparsers.add_parser(
    'user_review', help='Consume user_review PubSub'
)
user_view_consumer_parser.set_defaults(
    handler=consumers.user_review_handler
)

matching_product_consumer_parser = consumer_subparsers.add_parser(
    'matching_product', help='Consume matching_product PubSub'
)
matching_product_consumer_parser.set_defaults(
    handler=consumers.matching_product_handler
)

label_consumer_parser = consumer_subparsers.add_parser(
    'label', help='Consume label PubSub'
)
label_consumer_parser.set_defaults(handler=consumers.label_handler)

media_bucket_parser = consumer_subparsers.add_parser(
    'media_bucket', help='Consumer bucket media PubSub'
)
media_bucket_parser.set_defaults(handler=consumers.media_bucket_handler)

catalog_notification = consumer_subparsers.add_parser(
    'catalog_notification', help='Consumer catalog notification'
)
catalog_notification.set_defaults(
    handler=consumers.catalog_notification_handler
)

if __name__ == '__main__':
    configure_otel_instrumentation()
    args = parser.parse_args([
        os.getenv('JOB_TYPE'),
        os.getenv('SCOPE')
    ])
    args.handler(args)
