from .base import *  # noqa

DEFAULT_DB_SETTINGS = None

ENABLE_MATCHING_PRODUCT_HASH = ['Celular']

MONGO_DATABASE = 'taz_tests'
MONGO_HOST = os.environ.get('MONGO_HOST', '127.0.0.1')
MONGO_PORT = os.environ.get('MONGO_PORT', ':27017')
MONGO_HOSTS = [
    host if host.endswith(MONGO_PORT) else f'{host}{MONGO_PORT}'
    for host in MONGO_HOST.split(',')
]
MONGO_HOST = ','.join(MONGO_HOSTS)
MONGO_URI = f'mongodb://{MONGO_HOST}/{MONGO_DATABASE}'

# PRODUCT CONSUMER SETTINGS
DEFAULT_WAIT_TIME = 0

CONSUMER_LOOP_ENABLED = False

ONLY_DIGITS_ID_GENERATOR = False

ACME_MEDIA_DOMAIN = 'https://x.xx.xxx'

DISABLE_STAMP = False

SHERLOCK_CACHE_DIR = '/tmp/exclusions/'

CATALOG_NOTIFICATION = SNS_PRODUCT_TOPIC

TEST_TOPIC_NAME = 'taz-datalake'

DATALAKE = {
    'fake_scope': {
        'niagara': {
            'topic_name': 'fake',
            'project_id': 'maga-homolog',
            'enabled': True
        },
        'tetrix': {
            'topic_name': 'fake',
            'enabled': True
        }
    },
    'product_original': {
        'niagara': {
            'topic_name': 'fake',
            'project_id': 'maga-homolog',
            'enabled': True
        }
    }
}

PRODUCT_EXPORTER_SCOPES = {
    'product': [{
        'scope': 'fake_scope',
        'topic_name': 'fake',
        'project_id': 'maga-homolog'
    }],
    'enriched_product': [{
        'scope': 'invalid_scope',
        'topic_name': 'fake',
        'project_id': 'maga-homolog'
    }]
}

FALLBACK_MISSING_CATEGORY = 'RC'
FALLBACK_MISSING_SUBCATEGORY = 'RCNM'

PUBSUB_LOOP_ENABLED = False

ENABLE_MATCHING_FROM_ENTITY = ['Fritadeira Elétrica', 'Celular']

NOTIFY_SOURCES = {
    'omnilogic-magalu': {
        'url': os.getenv(
            'NOTIFY_OMNILOGIC_MAGALU_URL',
            'http://integration-omnilogic-sandbox.luizalabs.com/magalu/notification'  # noqa
        ),
        'headers': {
            'Content-type': 'application/json',
            'Authorization': os.getenv('NOTIFY_OMNILOGIC_MAGALU_TOKEN')
        },
    },
    'omnilogic-own': {
        'url': os.getenv(
            '',
            'test'
        ),
        'headers': {
            'Content-type': 'application/json',
            'Authorization': 'token'
        }
    }
}

ENABLE_SMARTCONTENT_ENRICHMENT_BY_CATEGORY = ['*']

ALLOW_PUBLISH_PRODUCT_METADATA = ['Forno Elétrico']

ALLOWED_OWNERS_TO_DELETE_ENRICHED_SOURCE = ['TazApi']
ALLOWED_OWNERS_WRITE_CLASSIFICATIONS_RULES = ['TazApi']

EXPIRES_CACHE_CATEGORIES = 1
EXPIRES_REDIS_CACHE_CATEGORIES = 1
EXPIRES_CACHE_DEFAULT_CATEGORIES = 1
CACHE_CLEANING_INTERVAL = 0.1
ENABLE_FULFILLMENT = False

MARVIN_NOTIFICATION = {
    'topic_name': 'fake-marvin-force-manual',
    'project_id': 'fake-magalu-digital-project'
}

SCORE_VERSION = '0.2.0'

METADATA_INPUT_DOWNLOAD_IMAGES_MAX_RETRIES = 1

MEDIA_MAX_IMAGE_PIXELS = os.getenv(
    'MEDIA_MAX_IMAGE_PIXELS', 2048 * 2048 * 2048 / 4 / 3
)


# SQL SERVER DATABASE PER ENVIRONMENT SETTINGS
DEFAULT_DB_SETTINGS = {
    'host': 'localhost',
    'user': 'test',
    'password': 'test',
    'dbname': 'test',
    'port': 1433
}

CATALOG_NOTIFICATION_ROUTER_ENABLED_ENDPOINTS = [
    'taz-score',
    'taz-datalake',
    'taz-product-writer',
    'taz-match-products',
    'taz-update-category',
    'taz-metadata-verify',
    'taz-complete-product',
    'taz-product-exporter',
]

CATALOG_NOTIFICATION_ROUTER_taz_score = [
    {
        'type': [
            'product'
        ]
    }
]

CATALOG_NOTIFICATION_ROUTER_taz_datalake = [
    {
        'type': [
            'product',
            'enriched_product',
            'media',
            'score',
            'product_score',
            'stock',
            'price',
            'factsheet',
            'matching_product',
            'metadata_verify'
        ]
    }
]

CATALOG_NOTIFICATION_ROUTER_taz_product_writer = [
    {
        'type': [
            'badge',
            'matching',
            'price',
            'stock',
            'media'
        ]
    }
]

CATALOG_NOTIFICATION_ROUTER_taz_complete_product = [
    {
        'type': [
            'metadata_verify'
        ]
    }
]

CATALOG_NOTIFICATION_ROUTER_taz_product_exporter = [
    {
        'type': [
            'matching',
            'badge',
            'stock',
            'media',
            'price',
            'matching_product',
            'metadata_verify'
        ]
    }
]

CATALOG_NOTIFICATION_ROUTER_taz_match_products = [
    {
        'type': [
            'metadata_verify',
            'reviews'
        ]
    }
]

CATALOG_NOTIFICATION_ROUTER_taz_update_category = [
    {
        'seller_id': [
            'magazineluiza'
        ]
    },
    {
        'type': [
            'product'
        ]
    }
]

CATALOG_NOTIFICATION_ROUTER_taz_metadata_verify = [
    {
        'type': [
            'product',
            'enriched_product'
        ]
    }
]

PUBSUB_SUBSCRIPTION_ID = 'test'

PUBSUB_MATCHING_PRODUCT_TOPIC_NAME = 'taz-match-products'
PUBSUB_MATCHING_PRODUCT_SUB_NAME = 'taz-match-products-sub'

PAGINATION_LIMIT_PRICE_RULE_CRON = 1
