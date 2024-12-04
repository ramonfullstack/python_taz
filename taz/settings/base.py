import os
import socket
from decimal import ROUND_HALF_UP, Context, setcontext

from taz import constants


def PERCENT(i):
    return i / 100


GA_PROFILE_ID = '98698542'
GA_SERVICE_ACCOUNT_EMAIL = 'intelie@dp6-magazineluiza-gap.iam.gserviceaccount.com'  # noqa
GA_SCOPES = [
    'https://www.googleapis.com/auth/analytics.readonly'
]
GA_KEY_FILE_LOCATION = '{}/taz/settings/{}'.format(
    os.getcwd(), '/keys/DP6-MagazineLuiza-GAP-02964e42606f.p12'
)

DEFAULT_PROCESSORS_COUNT = 8
MAX_CLIENTS = 50

# TIME CONSTS
SECONDS = 1
MINUTES = SECONDS * 60
HOURS = MINUTES * 60
DAYS = HOURS * 24

STRATEGIES = {
    constants.SINGLE_SELLER_STRATEGY: 'taz.core.matching.strategies.single_seller',  # noqa
    constants.AUTO_BUYBOX_STRATEGY: 'taz.core.matching.strategies.auto_buybox',
    constants.OMNILOGIC_STRATEGY: 'taz.core.matching.strategies.omnilogic',
    constants.CHESTER_STRATEGY: 'taz.core.matching.strategies.chester'
}

DEFAULT_MATCHING_STRATEGY = constants.SINGLE_SELLER_STRATEGY

SIMPLE_SETTINGS = {
    'OVERRIDE_BY_ENV': True,
    'CONFIGURE_LOGGING': True,
    'REQUIRED_SETTINGS_TYPES': {
        'OUT_OF_STOCK_RULE_IS_ACTIVE': 'bool',
        'ENABLE_POLLER_PRICE_PUBSUB': 'bool',
        'SKIP_ENRICHED_SOURCES_WHEN_NOT_METADATA_VERIFY': 'json.loads',
        'CATEGORY_DISABLE_SMARTCONTENT_VERIFY_SELLER': 'json.loads',
        'CATEGORY_SKIP_EXTERNAL_OMNILOGIC': 'json.loads',
        'GET_MEDIA_MAX_ATTEMPTS': 'int',
        'ENABLE_SMARTCONTENT_ENRICHMENT_BY_CATEGORY': 'json.loads',
        'KEEP_CATEGORIES_ATTRIBUTES': 'json.loads',
        'ENABLE_FULFILLMENT': 'bool',
        'ALLOW_PUBLISH_PRODUCT_METADATA': 'json.loads',
        'ENABLE_EXTRA_DATA': 'bool',
        'ENABLE_PARENT_MATCHING': 'bool',
        'ENABLE_MATCHING_FROM_ENTITY': 'json.loads',
        'SMARTCONTENT_CATEGORY_NOT_ALLOWED_REFERENCE': 'json.loads',
        'ONLY_DIGITS_ID_GENERATOR': 'bool',
        'SKIP_MD5_VALIDATION': 'bool',
        'KEY_LIMIT_ON_EXTRA_DATA': 'int',
        'MONGO_OPTIONS': 'str',
        'PRIORITY_EXECUTION_MERGER': 'json.loads',
        'METADATA_INPUT_DOWNLOAD_IMAGES_MAX_RETRIES': 'int',
        'INACTIVATE_SELLER_SKUS_FLOW_ENABLED': 'bool',
        'MEDIA_MAX_IMAGE_PIXELS': 'float',
        'BLOCKED_PRODUCT_TYPES_CLASSIFICATIONS_RULES': 'json.loads',
        'ENABLED_CATEGORIES_CHESTER_STRATEGY': 'json.loads',
        'ENABLED_SUBCATEGORIES_CHESTER_STRATEGY': 'json.loads',
        'ENABLED_CHESTER_STRATEGY': 'bool',
        'POLLER_PRODUCT_SHOULD_FILTER_CREATED_AT_AND_ACTIVE': 'bool',
        'MEDIA_SERVICE_STRATEGY': 'json.loads',
    }
}

context = Context(prec=2, rounding=ROUND_HALF_UP)
setcontext(context)

SENDER_MAX_WORKERS = DEFAULT_PROCESSORS_COUNT

BASE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

S3_ACCESS_KEY_ID = os.getenv('S3_ACCESS_KEY_ID')
S3_ACCESS_KEY_SECRET = os.getenv('S3_ACCESS_KEY_SECRET')
S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL')

# SQL SERVER DATABASE PER ENVIRONMENT SETTINGS
DEFAULT_DB_SETTINGS = {
    'host': '10.31.0.108',
    'user': 'usr_taz',
    'password': os.getenv('DB_PASSWORD'),
    'dbname': 'dbMagazine',
    'port': 1433
}

MONGO_DATABASE = 'taz'
MONGO_HOST = 'localhost'
MONGO_URI = f'mongodb://{MONGO_HOST}:27017/{MONGO_DATABASE}'

REDIS_SETTINGS = {
    'host': 'localhost',
    'port': 6379
}

REDIS_LOCK_SETTINGS = {
    'host': 'localhost',
    'port': 6379,
    'socket_timeout': os.getenv('REDIS_LOCK_SOCKET_TIMEOUT', 60),
    'socket_connect_timeout': os.getenv(
        'REDIS_LOCK_SOCKET_CONNECT_TIMEOUT', 60
    )
}

REDIS_SETTINGS = REDIS_LOCK_SETTINGS

# The default time in seconds that
# each iteration have to wait
# before it starts over again
DEFAULT_WAIT_TIME = MINUTES * 1


# The maximum number of messages that
# will be retrieved from queue on consumers of
# queue broker type (maximum is 10, minimum is 1)
QUEUE_BATCH_READ_SIZE = 10

QUEUE_QUANTITY_DELAY = 6


# DEFAULT SETTINGS FOR AWS
DEFAULT_AWS_SETTINGS = {
    'region': 'us-east-1',
    'account_id': '518863443564',
}

KINESIS_REGION = os.getenv('KINESIS_REGION', 'us-east-1')

GOOGLE_PROJECT_ID = 'maga-homolog'

PUBSUB_PRODUCT_TOPIC_NAME = os.getenv(
    'PUBSUB_PRODUCT_TOPIC_NAME', 'taz-product'
)
PUBSUB_PRODUCT_SUB_NAME = os.getenv(
    'PUBSUB_PRODUCT_SUB_NAME', 'taz-product-sub'
)

PUBSUB_FACTSHEET_TOPIC_NAME = os.getenv(
    'PUBSUB_PRODUCT_TOPIC_NAME', 'taz-factsheet'
)
PUBSUB_FACTSHEET_SUB_NAME = os.getenv(
    'PUBSUB_FACTSHEET_SUB_NAME', 'taz-factsheet-sub'
)

PUBSUB_POLLER_CATEGORY_TOPIC_NAME = os.getenv(
    'PUBSUB_POLLER_CATEGORY_TOPIC_NAME', 'taz-poller-category'
)
PUBSUB_POLLER_CATEGORY_SUB_NAME = os.getenv(
    'PUBSUB_POLLER_CATEGORY_SUB_NAME', 'taz-poller-category-sub'
)


# LISTS ALL KNOWN POLLERS
POLLERS = {
    'product': {
        'wait_time': os.getenv('DEFAULT_WAIT_TIME', DEFAULT_WAIT_TIME),
        'database': DEFAULT_DB_SETTINGS,
        'topic_name': PUBSUB_PRODUCT_TOPIC_NAME,
        'project_id': GOOGLE_PROJECT_ID,
    },
    'category': {
        'wait_time': os.getenv('DEFAULT_WAIT_TIME', DEFAULT_WAIT_TIME),
        'database': DEFAULT_DB_SETTINGS,
        'topic_name': PUBSUB_POLLER_CATEGORY_TOPIC_NAME,
        'project_id': GOOGLE_PROJECT_ID
    },
    'video': {
        'wait_time': os.getenv('DEFAULT_WAIT_TIME', DEFAULT_WAIT_TIME),
        'database': DEFAULT_DB_SETTINGS,
        'topic_name': 'taz-media',
        'project_id': GOOGLE_PROJECT_ID
    },
    'media': {
        'wait_time': os.getenv('DEFAULT_WAIT_TIME', DEFAULT_WAIT_TIME),
        'database': DEFAULT_DB_SETTINGS,
        'aws_settings': DEFAULT_AWS_SETTINGS,
        'stream_name': 'taz-media-sandbox'
    },
    'media_active': {
        'wait_time': os.getenv('DEFAULT_WAIT_TIME', DEFAULT_WAIT_TIME),
        'database': DEFAULT_DB_SETTINGS,
        'aws_settings': DEFAULT_AWS_SETTINGS,
        'stream_name': 'taz-media-sandbox'
    },
    'media_pf': {
        'wait_time': os.getenv('DEFAULT_WAIT_TIME', DEFAULT_WAIT_TIME),
        'database': DEFAULT_DB_SETTINGS,
        'aws_settings': DEFAULT_AWS_SETTINGS,
        'stream_name': 'taz-media-sandbox'
    },
    'factsheet': {
        'wait_time': os.getenv('DEFAULT_WAIT_TIME', DEFAULT_WAIT_TIME),
        'database': DEFAULT_DB_SETTINGS,
        'topic_name': PUBSUB_FACTSHEET_TOPIC_NAME,
        'project_id': GOOGLE_PROJECT_ID,
    },
    'price': {
        'wait_time': os.getenv('DEFAULT_WAIT_TIME', DEFAULT_WAIT_TIME),
        'database': DEFAULT_DB_SETTINGS,
        'aws_settings': DEFAULT_AWS_SETTINGS,
        'stream_name': 'taz-price-sandbox',
        'topic_name': 'taz-poller-price-sandbox',
        'project_id': 'maga-homolog'
    },
    'price_pf': {
        'wait_time': os.getenv('DEFAULT_WAIT_TIME', DEFAULT_WAIT_TIME),
        'database': DEFAULT_DB_SETTINGS,
        'aws_settings': DEFAULT_AWS_SETTINGS,
        'stream_name': 'taz-price-sandbox'
    },
    'price_campaign': {
        'wait_time': os.getenv('DEFAULT_WAIT_TIME', DEFAULT_WAIT_TIME),
        'database': DEFAULT_DB_SETTINGS,
        'topic_name': os.getenv('TAZ_PRICE_CAMPAIGN_POLLER_TOPIC', 'taz-price-campaign'),  # noqa
        'project_id': GOOGLE_PROJECT_ID,
    },
    'product_clicks_quantity': {
        'stream_name': 'taz-customer-behavior-sandbox',
        'aws_settings': DEFAULT_AWS_SETTINGS,
        'wait_time': HOURS * 6,
    },
    'product_sold_quantity': {
        'database': {
            'host': '127.0.0.1',
            'user': 'p52',
            'password': os.getenv('PRODUCT_SOLD_QUANTITY_PASSWORD'),
            'dbname': 'p52',
            'port': 3308
        },
        'aws_settings': DEFAULT_AWS_SETTINGS,
        'stream_name': 'taz-customer-behavior-sandbox',
        'wait_time': MINUTES * 1
    },
    'base_price': {
        'wait_time': os.getenv('DEFAULT_WAIT_TIME', DEFAULT_WAIT_TIME),
        'database': DEFAULT_DB_SETTINGS,
        'topic_name': 'fry-base-price',
        'project_id': GOOGLE_PROJECT_ID
    },
    'partner': {
        'wait_time': os.getenv('DEFAULT_WAIT_TIME', DEFAULT_WAIT_TIME),
        'database': DEFAULT_DB_SETTINGS,
        'topic_name': 'taz-partner',
        'project_id': GOOGLE_PROJECT_ID
    },
    'lu_content': {
        'wait_time': os.getenv('DEFAULT_WAIT_TIME', DEFAULT_WAIT_TIME),
        'database': DEFAULT_DB_SETTINGS,
        'topic_name': 'taz-poller-lu-content',
        'project_id': 'magalu-digital-project'
    }
}


FACTSHEET_FETCH_MAX_RETRIES = 3

REBUILD_LOCK_TIME_HOURS = {
    'catalog_notification': int(
        os.getenv('REBUILD_LOCK_TIME_HOURS_NOTIFICATION', 24)
    ),
    'rebuild_marvin_seller_paginator': int(
        os.getenv('REBUILD_LOCK_TIME_HOURS_MARVIN', 24)
    )
}

# LIST OF ALL CONSUMERS
CONSUMERS = {
    'product': {
        'stream_name': 'taz-product-sandbox'
    },
    'category': {
        'stream_name': 'taz-category-sandbox'
    },
    'media': {
        'stream_name': 'taz-media-sandbox'
    },
    'factsheet': {
        'stream_name': 'taz-factsheet-sandbox'
    },
    'price': {
        'stream_name': 'taz-price-sandbox'
    },
    'customer_behavior': {
        'stream_name': 'taz-customer-behavior-sandbox',
    },
    'buybox_pending': {
        'stream_name': 'taz-product-sandbox'
    },
    'media_bucket': {
        'stream_name': 'taz-media-sandbox'
    },
}

# FLAGS IF DATA SHOULD BE SENT IN PARALLEL OR SERIAL
ASYNC_SENDER = False

# THE ENVIRONMENT THE APP IS RUNNING
ENVIRONMENT = os.environ.get('ENV', 'development')
APP_NAME = os.getenv('APP_NAME', None)
# THE HOST MACHINE IP
HOST_IP = os.environ.get('HOST_IP', [
    (s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close())
    for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]
][0][1])


# A FEW DEFAULT BUSINESS PARAMETERS
DEFAULT_STORE_ID = 200
DEFAULT_PARTNER_ID = 0

# ID GENERATOR SETTINGS
BLACKLIST_CHARACTERS = ('I', 'l')
ID_LENGTH = 9
ID_PREFIX = '99'
ONLY_DIGITS_ID_GENERATOR = True

STAMP_MAX_WORKERS = DEFAULT_PROCESSORS_COUNT

BASE_DESKTOP_URL = 'https://www.magazineluiza.com.br'

# LEGACY MEDIA
MEDIA_APP_NAME = APP_NAME
GET_MEDIA_MAX_WORKERS = 16
GET_MEDIA_MAX_ATTEMPTS = 1
GET_MEDIA_TEMPLATE_URL = 'http://medialist.magazineluiza.com.br/media-md5/{}/'
IMAGE_TEMPLATE_URL = 'http://img.magazineluiza.com.br/1500x1500/x-{}'
AUDIO_TEMPLATE_URL = 'http://img.magazineluiza.com.br/audio/{}/{}/{}/{}'
PODCAST_TEMPLATE_URL = 'http://img.magazineluiza.com.br/podcast/{}'

# ListMedia
MEDIA_LIST_BUCKET = os.getenv('MEDIA_LIST_BUCKET', 'img-sandbox')
MEDIA_BASE_PATH = 'magazineluiza/img'
IMAGE_BASE_PATH = 'produto_grande'
AUDIO_BASE_PATH = 'audio'
PODCAST_BASE_PATH = 'podCast'
SKU_MIN_SIZE = 7
SKU_SIZE_VALIDATION_RANGE = [7, 9]
MEDIA_LIST_MAX_RETRIES = 1
MEDIA_LIST_TIMEOUT_IN_SECONDS = 10
MEDIA_LIST_MAX_POLL_CONNECTIONS = 128
MEDIA_LIST_MAX_POLL_MAXSIZE = 128
MEDIA_LIST_MAX_POLL_BLOCK = os.getenv(
    'MEDIA_LIST_MAX_POLL_BLOCK', 'True'
) == 'True'

BUCKET_MEDIA_TTL = 120
BUCKET_MEDIA_VIDEO_TTL = 1200
BUCKET_MEDIA_LOCK_BLOCKING = os.getenv(
    'BUCKET_MEDIA_LOCK_BLOCKING', 'True'
) == 'True'
BUCKET_MEDIA_LOCK_TIMEOUT = 60
BUCKET_MEDIA_LOCK_ACQUIRE_TIMEOUT = 0.200

MEDIA_CONSUMER_MAX_WORKERS = DEFAULT_PROCESSORS_COUNT

# ACME S3 MEDIA
IMAGES_PATH = '/{{w}}x{{h}}/{slug}/{seller_id}/{sku}/{filename}'
AUDIOS_VIDEOS_PODCASTS_PATH = '/{seller_id}/{media_type}/{sku}/{filename}'
CATEGORY_PATH = '{}/l/{}/'
SUBCATEGORY_PATH = '{}/{}/s/{}/{}/'
ACME_MEDIA_DOMAIN = 'https://pis-static-tst.magazineluiza.com.br'
FACTSHEET_DOMAIN = 'http://pis.static-tst.magazineluiza.com.br'

# CONSUMER BROKER SETTINGS
CHECKPOINT_FREQUENCE = MINUTES * 1
CHECKPOINT_MAX_RETRIES = 5
CHECKPOINT_RETRY_SLEEP_TIME = 5

# GENERAL CONSUMER SETTINGS
PROCESSOR_MAX_THREAD_WORKERS = (
    os.environ.get('PROCESSOR_MAX_THREAD_WORKERS', DEFAULT_PROCESSORS_COUNT)
)

# MEDIA CONSUMER SETTINGS
MEDIA_S3_BUCKET = 'taz-medias-sandbox'
MEDIA_BUCKET = 'taz-medias-sandbox'

# CATEGORIES CONSUMER SETTINGS
CATEGORY_CONSUMER_MAX_WORKERS = 1
CATEGORY_APP_NAME = APP_NAME

# FACTSHEET CONSUMER SETTINGS
FACTSHEET_S3_BUCKET = 'taz-factsheet-sandbox'
FACTSHEET_APP_NAME = APP_NAME
FACTSHEET_PROCESSOR_MAX_WORKERS = DEFAULT_PROCESSORS_COUNT
FACTSHEET_CONSUMER_MAX_WORKERS = DEFAULT_PROCESSORS_COUNT

FACTSHEET_STORAGE = 'taz-factsheet-sandbox'
RAW_FACTSHEET_STORAGE = 'taz-raw-factsheet-sandbox'

# PRODUCT CONSUMER SETTINGS
PRODUCT_WRITER_V2_QUEUE_NAME = 'taz-product-writer-v2-sandbox'
PRODUCT_WRITER_V2_PROCESS_WORKERS = DEFAULT_PROCESSORS_COUNT
SHIPPING_LOGGER_QUEUE_NAME = 'taz-shipping-logger-sandbox'

ENRICHED_PRODUCT_PROCESS_WORKERS = DEFAULT_PROCESSORS_COUNT

# PRODUCT SCORE CONSUMER SETTINGS
PRODUCT_SCORE_PROCESS_WORKERS = DEFAULT_PROCESSORS_COUNT

# CUSTOMER BEHAVIOR CONSUMER SETTINGS
CUSTOMER_BEHAVIOR_CONSUMER_MAX_WORKERS = 2
CUSTOMER_BEHAVIOR_APP_NAME = APP_NAME

# ACME OLD IMPORTER
FTP_IMAGE_QUEUE_NAME = 'acme-images'
FTP_IMAGE_REGION_NAME = 'us-east-1'
DISABLE_FTP_IMAGE = False

# MATCHING SETTINGS
COSINE_THRESHOLD = 0.9
NGRAM_COSINE_THRESHOLD = 0.75
ACCEPTABLE_NGRAM_COSINE_THRESHOLD = 0.90
TITLE_COMPARISON_THRESHOLD = 1
MATCHER_MAX_WORKERS = 10

CONSUMER_LOOP_ENABLED = True

ID_GENERATOR_RETRIES = 1000

# Linx SETTINGS
LINX_INDEXING_APP_NAME = APP_NAME
LINX_INDEXING_CONSUMER_MAX_WORKERS = DEFAULT_PROCESSORS_COUNT
LINX_INDEXING_HOST = 'https://collect.chaordicsystems.com/v7'
LINX_INDEXING_PRODUCT_ENDPOINT = '/products/'
LINX_APIKEY = 'magazineluiza'

# SOLR SETTINGS
SOLR_MASTER = {
    'write_url': os.getenv('SOLR_WRITE_URL', 'http://172.19.90.122:8983'),
    'write_core': 'ml-products-v1',
}
SOLR_SUGGESTION = {
    'write_url': os.getenv('SOLR_WRITE_URL', 'http://172.19.90.122:8983'),
    'write_core': 'ml-suggestion',
}
SOLR_INDEXING_CONSUMER_MAX_WORKERS = DEFAULT_PROCESSORS_COUNT
SOLR_INDEXING_APP_NAME = APP_NAME

# SOLR SUGGESTION
SOLR_SUGGESTION_CONSUMER_MAX_WORKERS = DEFAULT_PROCESSORS_COUNT

SOLR_READ_URL = 'http://172.19.90.109:8080'
SOLR_READ_CORE = 'ml-product-price'

CATEGORIES_ALLOWED_FOR_PRICE = ()

# PRODUCT
PRODUCT_APP_NAME = APP_NAME
PRODUCT_CONSUMER_MAX_WORKERS = DEFAULT_PROCESSORS_COUNT

# BUYBOX PENDING
BUYBOX_PENDING_CONSUMER_MAX_WORKERS = 2
BUYBOX_PENDING_APP_NAME = APP_NAME

# PRICE
PRICE_CONSUMER_MAX_WORKERS = DEFAULT_PROCESSORS_COUNT
PRICE_APP_NAME = APP_NAME

# DATALAKE
DATALAKE_PROCESS_WORKERS = DEFAULT_PROCESSORS_COUNT

# SHIPPING
SHIPPING_PROCESS_WORKERS = DEFAULT_PROCESSORS_COUNT


# HAMILTON SETTINGS
APIS = {
    'taz': {
        'url': 'https://taz-api-sandbox.mgc-hml.mglu.io',
        'token': os.getenv('TAZ_TOKEN'),
        'timeout': 5,
    },
    'arcoiro': {
        'url': 'http://arcoiro-sandbox.luizalabs.com',
        'token': os.getenv('ARCOIRO_TOKEN'),
        'timeout': 20
    },
    'bazaarvoice': {
        'url': 'https://luizalabs-dev.apigee.net/v2',
        'token': os.getenv('BAZAAR_VOICE_TOKEN'),
        'timeout': 5,
        'ssl_verify': False
    },
    'fry': {
        'url': 'https://fry-sandbox.luizalabs.com',
        'token': 'Test',
        'timeout': 20
    },
    'frajola': {
        'url': 'http://frajola-sandbox.luizalabs.com',
        'token': os.getenv('FRAJOLA_TOKEN'),
        'timeout': 20
    },
    'branches': {
        'url': 'https://api.apiluiza.com.br/v1',
        'token': 'Bearer bAVjocvJtyZgp0YAHhjLIo1BGi9I',
        'timeout': 5
    },
    'stock': {
        'url': 'https://api.apiluiza.com.br/v2.1',
        'token': 'Bearer bAVjocvJtyZgp0YAHhjLIo1BGi9I',
        'timeout': 5
    },
    'helena': {
        'url': 'http://helena-sandbox.luizalabs.com',
        'client_secret': os.getenv('HELENA_SECRET'),
        'client_id': os.getenv('HELENA_CLIENT_ID'),
        'timeout': 5
    },
    'apiluiza': {
        'url': 'https://stage.apiluiza.com.br',
        'client_secret': os.getenv('APILUIZA_SECRET'),
        'client_id': os.getenv('APILUIZA_CLIENT_ID'),
        'accesstoken': {
            'path': '/oauth/jwt/client_credential/accesstoken'
        },
        'pickup_store': {
            'path': '/v1/pickupstores',
        },
        'total_attempts_token': int(os.getenv('APILUIZA_TOTAL_ATTEMPTS', 3)),
    },
    'transformers': {
        'url': 'http://api.apiluiza.com.br/v2/shoppingcarts/shippings',
        'token': 'Bearer 7O6wD6S3Hh04s6c2IHiJd865bn0F',
        'timeout': 5
    },
    'patolino': {
        'url': 'http://notificacao-produtos-sandbox.luizalabs.com',
        'token': os.getenv('PATOLINO_TOKEN', 'test'),
        'timeout': 5
    },
    'marvin': {
        'url': os.getenv('MARVIN_URL', 'http://marvin-sandbox.luizalabs.com')
    },
    'maas-product': {
        'url': os.getenv(
            'MAAS_PRODUCT_URL',
            'https://api-product-staging-origin.luizalabs.com'
        ),
        'timeout': int(os.getenv('MAAS_PRODUCT_TIMEOUT', 5)),
        'max_retries': int(os.getenv('MAAS_PRODUCT_MAX_RETRIES', 3)),
        'authorization_server_url': os.getenv('MAAS_PRODUCT_KEYCLOAK'),
        'client_id': os.getenv('MAAS_PRODUCT_CLIENT_ID'),
        'client_secret': os.getenv('MAAS_PRODUCT_CLIENT_SECRET')
    },
    'omnilogic': {
        'url': os.getenv(
            'NOTIFY_OMNILOGIC_MAGALU_URL',
            'http://integration-omnilogic-sandbox.luizalabs.com/magalu/notification'  # noqa
        ),
        'headers': {
            'Content-type': 'application/json',
            'Authorization': os.getenv('NOTIFY_OMNILOGIC_MAGALU_TOKEN')
        }
    }
}

# UNAVAILABLE IMAGE SETTINGS
UNAVAILABLE_IMAGE_OPTIONS = {
    'sku': '000000000',
    'title': 'imagem-indisponivel',
    'reference': '',
    'seller_id': 'appmockups',
    'media_type': 'images',
    'items': ['1bd79dc863d30982501d43e14bccc8f0.jpg']
}

ALLOWED_NON_ALPHANUMERIC_CHARACTERES = (
    ' ', '-', '!', '.', ':', '/', '"', '=',
    '+', '(', ')', ',', '_', '/\\', 'ª', 'º', '”',
    '*', '@', '%', '\'', '&', '~'
)

ALLOWED_HTML_TAGS = os.getenv(
    'ALLOWED_HTML_TAGS',
    'p,b,i,h1,h2,h3,h4,h5,h6,strong,div,span,ul,li'
)

STAMP_SELECTION = 14934

TOKEN_LENGTH = 30

FACET_MAX_LENGTH = 60
FIXED_FACTSHEET_ATTRIBUTE_IDS = {
    'apresentacao': 123,
    'apresentacao do produto': 123,
    'destaques': 99923,
}
SNS_PRODUCT_TOPIC = 'arn:aws:sns:us-east-1:518863443564:taz-tests'

SHERLOCK_CACHE_DIR = os.environ.get(
    'SHERLOCK_CACHE_DIR',
    os.path.join(BASE_PATH, '..', '..', '.extensions')
)

SHERLOCK_CACHE_MINUTES = int(os.environ.get('SHERLOCK_CACHE_MINUTES', '10'))
SHERLOCK_S3_BUCKET = 'development-solr-sinonimos'

CLOUDFRONT_DISTRIBUTION_ID = 'E2QXPQHXZ71VI6'

INDEXING_PROCESS_STREAM_NAME = 'taz-indexing-process-sandbox'
INDEXING_PROCESS_STREAM_PROJECT_ID = 'maga-homolog'
INDEXING_PROCESS_STREAM_TOPIC_NAME = INDEXING_PROCESS_STREAM_NAME
PUBLISH_STREAM = True

KINESIS_LOCK_EXPIRE = int(os.getenv('KINESIS_LOCK_EXPIRE', '120'))
KINESIS_STOP = os.getenv('KINESIS_STOP', 'False') == 'True'  # noqa
KINESIS_ITERATOR_TYPE = os.getenv('KINESIS_ITERATOR_TYPE', 'TRIM_HORIZON')  # noqa
KINESIS_CHUNK_SIZE = int(os.getenv('KINESIS_CHUNK_SIZE', '300'))  # noqa
KINESIS_INTERVAL = float(os.getenv('KINESIS_INTERVAL', '0.5'))  # noqa
KINESIS_ERROR_RETRY_INTERVAL = float(os.getenv('KINESIS_ERROR_RETRY_INTERVAL', '10'))  # noqa
KINESIS_MAX_TIME_PROCESS = float(os.getenv('KINESIS_MAX_TIME_PROCESS', '600'))

COMPLETE_PRODUCT_PROCESS_WORKERS = DEFAULT_PROCESSORS_COUNT

CATALOG_NOTIFICATION = 'arn:aws:sns:us-east-1:518863443564:catalog-notification-sandbox'  # noqa

CATALOG_NOTIFICATION_PUBSUB = [
    'checkout_price'
]

RAW_PRODUCT_S3_BUCKET = 'taz-raw-products-sandbox'
RAW_PRODUCT_STORAGE = 'taz-raw-products-sandbox'
BAZAARVOICE_XML_STORAGE_NAME = 'taz-bazaarvoice-sandbox'
BAZAARVOICE_XML_CRON_HOURS = os.environ.get('BAZAARVOICE_XML_CRON_HOURS', 1)
DEFAULT_PRICE_LOCK_PERCENT = 50
ENABLE_PRICE_LOCK_PERCENT = True
ENABLE_POLLER_PRICE_PUBSUB = False
POLLER_PRODUCT_SELECTIONS = '19366,19367,18459,18098,18669,22036,22037,22038,22039,20845,19368,19369,18035,18036,18030,18033,18032,22013,22833,18039,18038,17637,14980,18790,24169,18792,24166,18422,18423,18818,23033,19371,19370,23643,22780,18026,22044,18025,18022,18023,22043,22042,18028,18791,19107,19108,19109,24115,18538,18539,18789,18788,19365,24444,22041,18787,18786,18536,22040,19366,19367,19365,18669,22036,16735,22038,22039,20845,22042,19368,19369,18035,18034,18037,18036,18031,18030,18033,18032,22013,22833,18039,18038,9356,19110,18790,18791,18792,24165,6973,22037,18422,18423,10811,18421,16734,18818,16736,16737,19371,19370,14844,23643,18026,18027,18024,18025,18022,18023,22043,18021,22037,18028,24169,19107,22044,19108,19109,24115,18786,18538,18539,18789,18788,8162,22041,18787,24166,22040,24448,24449,24447,24450,24451,24452,24453,24454,24456,24458,24459,24460,24461,24465,24466,24467,24468,24469,24470,24471,24472,24473,24474,24475'  # noqa

MINIMUM_AMOUNT_METADATA = 3

METABOOKS_HOST = 'ftp.metabooks.com'
METABOOKS_USER = 'magalu-integration'
METABOOKS_PASSWORD = os.getenv('METABOOKS_PASSWORD')

METADATA_INPUT_PROCESS_WORKERS = DEFAULT_PROCESSORS_COUNT
METADATA_INPUT_BUCKET = 'taz-metadata-input-sandbox'
METADATA_IMAGE_BUCKET = os.getenv('METADATA_IMAGE_BUCKET', 'taz-metadata-images-sandbox')  # noqa
METADATA_IMAGE_URL = 'https://taz-metadata-images-sandbox.magalu.com/{source}/{identified}/{filename}'  # noqa
MAAS_PRODUCT_IMAGE_BUCKET = os.getenv('MAAS_PRODUCT_IMAGE_BUCKET', 'maas-file-product-api-staging')  # noqa

METABOOKS_URL = 'https://www.metabooks.com/api/v2'
METABOOKS_TOKEN = os.getenv('METABOOKS_TOKEN')
METABOOKS_COVER_TOKEN = os.getenv('METABOOKS_COVER_TOKEN')
METABOOKS_MMO_TOKEN = os.getenv('METABOOKS_MMO_TOKEN')

METADATA_VERIFY_PROCESS_WORKERS = DEFAULT_PROCESSORS_COUNT

PRODUCT_SCORE_QUEUE_NAME = 'taz-score-sandbox'
SMARTCONTENT_URL = os.getenv('SMARTCONTENT_URL')
SMARTCONTENT_TOKEN = os.getenv('SMARTCONTENT_TOKEN')

DATASHEET_URL = os.getenv('DATASHEET_URL')
DATASHEET_TOKEN = os.getenv('DATASHEET_TOKEN')

ENRICHED_PRODUCTS_NOTIFICATION = 'arn:aws:sns:us-east-1:518863443564:enriched-products-notification-sandbox'  # noqa

CHANNEL_GCHAT = os.getenv('CHANNEL_GCHAT')

BAZAARVOICE_HOST = 'sftp.bazaarvoice.com'
BAZAARVOICE_USER = 'magazineluiza'
BAZAARVOICE_PASS = 'sTZAThD2jI%M'

SCORE_CRITERIA_TYPES = {
    constants.RANGE_TYPE: 'taz.core.score.criteria.types.ranges'
}

SCORE_VERSION = '0.3.0'

BUCKET_REPORT = 'taz-report-sandbox'

UPDATE_CATEGORY_PROCESS_WORKERS = DEFAULT_PROCESSORS_COUNT

MAGA_BIGDATA_PROJECT_ID = 'maga-bigdata'
PRODUCT_METADATA_TOPIC_NAME = 'taz-metadata-product-sandbox'
PUBSUB_METADATA_VERIFY_TOPIC_NAME = 'taz-metadata-verify'

ALLOW_PUBLISH_PRODUCT_METADATA = ['*']

KAFKA_CLUSTERS_CONFIG = {
    'datalake': {
        'bootstrap.servers': 'localhost:9092'
    }
}

DATALAKE = {
    'enriched_product': {
        'niagara': {
            'topic_name': 'niagara-catalogo-enriched',
            'project_id': 'maga-homolog',
            'enabled': str(os.getenv('NIAGARA_ENRICHED_PRODUCT_ENABLED', 'true')).lower() == 'true' # noqa
        },
        'tetrix': {
            'topic_name': os.getenv('TETRIX_ENRICHED_PRODUCT_TOPIC', 'taz.enriched.product.tetrix.1'), # noqa
            'enabled': str(os.getenv('TETRIX_ENRICHED_PRODUCT_ENABLED', 'false')).lower() == 'true' # noqa
        }

    },
    'product_score': {
        'niagara': {
            'topic_name': 'niagara-catalogo-score',
            'project_id': 'maga-homolog',
            'enabled': str(os.getenv('NIAGARA_PRODUCT_SCORE_ENABLED', 'true')).lower() == 'true' # noqa
        },
        'tetrix': {
            'topic_name': os.getenv('TETRIX_PRODUCT_SCORE_TOPIC', 'taz.product.score.tetrix.1'), # noqa
            'enabled': str(os.getenv('TETRIX_PRODUCT_SCORE_ENABLED', 'false')).lower() == 'true' # noqa
        }
    },
    'product_original': {
        'niagara': {
            'topic_name': 'niagara-catalogo-product-original',
            'project_id': 'maga-homolog',
            'enabled': str(os.getenv('NIAGARA_PRODUCT_ORIGINAL_ENABLED', 'true')).lower() == 'true' # noqa
        },
        'tetrix': {
            'topic_name': os.getenv('TETRIX_PRODUCT_ORIGINAL_TOPIC', 'taz.product.original.tetrix.1'), # noqa
            'enabled': str(os.getenv('TETRIX_PRODUCT_ORIGINAL_ENABLED', 'false')).lower() == 'true' # noqa
        }
    },
    'product': {
        'niagara': {
            'topic_name': 'niagara-catalogo-product',
            'project_id': 'maga-homolog',
            'enabled': str(os.getenv('NIAGARA_PRODUCT_ENABLED', 'true')).lower() == 'true' # noqa
        },
        'tetrix': {
            'topic_name': os.getenv('TETRIX_PRODUCT_TOPIC', 'taz.product.tetrix.1'), # noqa
            'enabled': str(os.getenv('TETRIX_PRODUCT_ENABLED', 'false')).lower() == 'true' # noqa
        }
    },
    'unpublish': {
        'niagara': {
            'topic_name': 'niagara-catalogo-unpublish',
            'project_id': 'maga-homolog',
            'enabled': str(os.getenv('NIAGARA_UNPUBLISH_ENABLED', 'true')).lower() == 'true' # noqa
        },
        'tetrix': {
            'topic_name': os.getenv('TETRIX_UNPUBLISH_TOPIC', 'taz.unpublish.tetrix.1'), # noqa
            'enabled': str(os.getenv('TETRIX_UNPUBLISH_ENABLED', 'false')).lower() == 'true' # noqa
        }
    },
    'price': {
        'niagara': {
            'topic_name': 'niagara-catalogo-product',
            'project_id': 'maga-homolog',
            'enabled': str(os.getenv('NIAGARA_PRICE_ENABLED', 'true')).lower() == 'true' # noqa

        },
        'tetrix': {
            'topic_name': os.getenv('TETRIX_PRICE_TOPIC', 'taz.price.tetrix.1'), # noqa
            'enabled': str(os.getenv('TETRIX_PRICE_ENABLED', 'false')).lower() == 'true' # noqa
        }
    },
    'media': {
        'niagara': {
            'topic_name': 'niagara-catalogo-media',
            'project_id': 'maga-homolog',
            'enabled': str(os.getenv('NIAGARA_MEDIA_ENABLED', 'true')).lower() == 'true' # noqa
        },
        'tetrix': {
            'topic_name': os.getenv('TETRIX_MEDIA_TOPIC', 'taz.media.tetrix.1'), # noqa
            'enabled': str(os.getenv('TETRIX_MEDIA_ENABLED', 'false')).lower() == 'true' # noqa
        }
    },
    'shipping': {
        'niagara': {
            'topic_name': 'niagara-catalogo-shipping',
            'project_id': 'maga-homolog',
            'enabled': str(os.getenv('NIAGARA_SHIPPING_ENABLED', 'true')).lower() == 'true' # noqa
        },
        'tetrix': {
            'topic_name': os.getenv('TETRIX_SHIPPING_TOPIC', 'taz.shipping.tetrix.1'), # noqa
            'enabled': str(os.getenv('TETRIX_SHIPPING_ENABLED', 'false')).lower() == 'true' # noqa
        }
    },
    'stock': {
        'niagara': {
            'topic_name': 'niagara-catalogo-stock',
            'project_id': 'maga-homolog',
            'enabled': str(os.getenv('NIAGARA_STOCK_ENABLED', 'true')).lower() == 'true' # noqa
        },
        'tetrix': {
            'topic_name': os.getenv('TETRIX_STOCK_TOPIC', 'taz.stock.tetrix.1'), # noqa
            'enabled': str(os.getenv('TETRIX_STOCK_ENABLED', 'false')).lower() == 'true' # noqa
        }
    },
    'factsheet': {
        'niagara': {
            'topic_name': 'niagara-catalogo-factsheet',
            'project_id': 'maga-homolog',
            'enabled': str(os.getenv('NIAGARA_FACTSHEET_ENABLED', 'true')).lower() == 'true' # noqa
        },
        'tetrix': {
            'topic_name': os.getenv('TETRIX_FACTSHEET_TOPIC', 'taz.factsheet.tetrix.1'), # noqa
            'enabled': str(os.getenv('TETRIX_FACTSHEET_ENABLED', 'false')).lower() == 'true' # noqa
        }
    }
}

USE_GEODELIVERY = bool(os.getenv('USE_GEODELIVERY', True))
GEODELIVERY_URL = os.getenv(
    'GEODELIVERY_URL',
    'http://localhost:8081/delivery/'
)
GEO_TIMEOUT = os.getenv('GEO_TIMEOUT', 30)

FALLBACK_MISSING_CATEGORY = 'RC'
FALLBACK_MISSING_SUBCATEGORY = 'RCNM'

EXPRESS_DELIVERY_ZIPCODE = '01001001'

CRON_STOP = False

PUBSUB_LOOP_ENABLED = True

OUT_OF_STOCK_RULE_IS_ACTIVE = True

MAX_DAYS_OUT_OF_STOCK = 15

ENABLE_MATCHING_FROM_ENTITY = ['Livro']

ENABLED_CATEGORIES_CHESTER_STRATEGY = ['LI']
ENABLED_SUBCATEGORIES_CHESTER_STRATEGY = []

ENABLED_CHESTER_STRATEGY = False

ENABLE_MATCHING_PRODUCT_HASH = os.environ.get(
    'ENABLE_MATCHING_PRODUCT_HASH', ''
).split(',')

COMPLETE_PRODUCT_CATEGORY_SKIP = ['LI']
CATEGORY_SKIP_EXTERNAL_OMNILOGIC = []

MAGAZINELUIZA_IMG_URL = 'img.magazineluiza'

PRODUCT_EXPORTER_SCOPES = {
    'product': [
        {
            'scope': 'simple_product',
            'topic_name': 'taz-simple-product-sandbox',
            'project_id': 'maga-homolog'
        }
    ],
    'metadata_verify': [
        {
            'scope': 'product_features',
            'topic_name': 'taz-product-features-sandbox',
            'project_id': 'maga-homolog'
        }
    ],
    'matching_product': [
        {
            'scope': 'product_features',
            'topic_name': 'taz-product-features-sandbox',
            'project_id': 'maga-homolog'
        }
    ],
    'badge': [
        {
            'scope': 'simple_product',
            'topic_name': 'taz-simple-product-sandbox',
            'project_id': 'maga-homolog'
        }
    ],
    'stock': [
        {
            'scope': 'simple_product',
            'topic_name': 'taz-simple-product-sandbox',
            'project_id': 'maga-homolog'
        }
    ],
    'price': [
        {
            'scope': 'simple_product',
            'topic_name': 'taz-simple-product-sandbox',
            'project_id': 'maga-homolog'
        }
    ],
    'matching': [
        {
            'scope': 'simple_product',
            'topic_name': 'taz-simple-product-sandbox',
            'project_id': 'maga-homolog'
        },
        {
            'scope': 'source_product',
            'topic_name': 'taz-source-product-sandbox',
            'project_id': 'maga-homolog'
        }
    ],
    'media': [
        {
            'scope': 'simple_product',
            'topic_name': 'taz-simple-product-sandbox',
            'project_id': 'maga-homolog'
        },
        {
            'scope': 'source_product',
            'topic_name': 'taz-source-product-sandbox',
            'project_id': 'maga-homolog'
        }
    ]
}

IMAGE_RESIZE_ENABLE = True
IMAGE_RESIZE_MAX_WIDTH = 2500
IMAGE_RESIZE_MAX_HEIGHT = 2500
IMAGE_RESIZE_QUALITY = 80
IMAGE_TRANSPARENCY_ENABLE = True

ENABLE_WAKKO_SCOPE = os.getenv('ENABLE_WAKKO_SCOPE', 'False') == 'True'

SUBSCRIBER_MAX_MESSAGES = 10
PUBSUB_PUBLISHER_NOTIFY_TOPIC = 'taz-catalog-notification'
PUBSUB_NOTIFY_PROJECT_ID = 'maga-homolog'
PATOLINO_STREAM_TOPIC_NAME = 'patolino-sandbox'
PATOLINO_STREAM_PROJECT_ID = 'maga-homolog'

STOCK_NOTIFICATION = {
    'DC': {
        'topic_name': os.getenv('STOCK_NOTIFICATION_DC_TOPIC_NAME'),
        'project_id': os.getenv('STOCK_NOTIFICATION_DC_PROJECT_ID')
    },
    'STORE': {
        'topic_name': os.getenv('STOCK_NOTIFICATION_STORE_TOPIC_NAME'),
        'project_id': os.getenv('STOCK_NOTIFICATION_STORE_PROJECT_ID')
    }
}

ALLOWED_SMARTCONTENT_CATEGORY = ['AF']
ALLOWED_SMARTCONTENT_SELLER = ['magazineluiza']
CATEGORY_DISABLE_SMARTCONTENT_VERIFY_SELLER = ['LI']
SMARTCONTENT_CATEGORY_NOT_ALLOWED_REFERENCE = []

ALLOW_OMNILOGIC_LUIZALABS_ENTITY = os.environ.get(
    'ALLOW_OMNILOGIC_LUIZALABS_ENTITY', 'Microondas'
).split(',')

KEEP_CATEGORIES_ATTRIBUTES = ['MD']

ENABLE_SELLER_PAYLOAD_LOG = [constants.MAGAZINE_LUIZA_SELLER_ID] + (
    os.environ.get(
        'ENABLE_SELLER_PAYLOAD_PRODUCT_LOG', ''
    ).split(',')
)

ENABLE_KINESIS_COMPRESS = (
    os.getenv('ENABLE_KINESIS_COMPRESS', 'False') == 'True'
)

DISABLE_PRICE_MAGAZINELUIZA = (
    os.getenv('DISABLE_PRICE_MAGAZINELUIZA', 'False') == 'True'
)

OMNILOGIC_NOTIFICATION_URL = 'http://integration-omnilogic-sandbox.luizalabs.com/store/{source}/notification'  # noqa


UNBLOCKABLE_SELLERS = (
    os.environ.get(
        'UNBLOCKABLE_SELLERS',
        'magazineluiza, netshoes, zattini, samsung, epocacosmeticos-integra, magalu2, magazineluizacommission, mlentregas'  # noqa
    ).split(',')
)

SCOPES_METADATA_INPUT = [
    constants.SOURCE_METABOOKS,
    constants.SOURCE_DATASHEET,
    constants.SOURCE_SMARTCONTENT
]

SKIP_ENRICHED_SOURCE_IN_SOURCE_PRODUCT = 'wakko'
SKIP_ENRICHED_SOURCE_IN_PRODUCT_FEATURES = 'wakko,smartcontent'

SKIP_ENRICHED_SOURCES_WHEN_NOT_METADATA_VERIFY = [
    constants.SOURCE_METABOOKS,
    constants.SOURCE_SMARTCONTENT
]

SCOPES_ALLOWED_SEND_IMAGES_TO_MEDIA = [
    constants.SOURCE_METABOOKS
]

BIGDATACORP_MAGALU_CATEGORIES = {
    'alimentos-e-bebidas': {'id': 'BA', 'description': 'Bebidas e Alimentos'},
    'ar-condicionado': {'id': 'AR', 'description': 'Ar e Ventilação'},
    'audio': {'id': 'EA', 'description': 'Áudio'},
    'automotivo': {'id': 'AU', 'description': 'Automotivo'},
    'bebes': {'id': 'BB', 'description': 'Bebê'},
    'beleza-e-perfumaria': {'id': 'PF', 'description': 'Beleza e Perfumaria'},
    'brinquedos': {'id': 'BR', 'description': 'Brinquedos'},
    'cama-mesa-e-banho': {'id': 'CM', 'description': 'Cama, Mesa e Banho'},
    'cameras': {'id': 'CF', 'description': 'Câmeras e Drones'},
    'casa-e-construcao': {'id': 'CJ', 'description': 'Casa e Construção'},
    'celulares-e-telefones': {'id': 'TE', 'description': 'Celulares e Smartphones'},  # noqa
    'decoracao': {'id': 'DE', 'description': 'Decoração'},
    'dvd': {'id': 'ET', 'description': 'TV e Vídeo'},
    'e-books': {'id': 'LI', 'description': 'Livros'},
    'eletrodomesticos': {'id': 'ED', 'description': 'Eletrodomésticos'},
    'eletroportateis': {'id': 'EP', 'description': 'Eletroportáteis'},
    'esporte': {'id': 'ES', 'description': 'Esporte e Lazer'},
    'ferramentas-e-jardim': {'id': 'FS', 'description': 'Ferramentas'},
    'games': {'id': 'GA', 'description': 'Games'},
    'informatica': {'id': 'IN', 'description': 'Informática'},
    'instrumentos-musicais': {'id': 'IM', 'description': 'Instrumentos Musicais'},  # noqa
    'livros': {'id': 'LI', 'description': 'Livros'},
    'malas': {'id': 'MD', 'description': 'Moda e Acessórios'},
    'moda': {'id': 'MD', 'description': 'Moda e Acessórios'},
    'medicamentos': {'id': 'CP', 'description': 'Saúde e Cuidados Pessoais'},
    'moveis': {'id': 'MO', 'description': 'Móveis'},
    'musica': {'id': 'MS', 'description': 'Música e Shows'},
    'papelaria': {'id': 'PA', 'description': 'Papelaria'},
    'petshop': {'id': 'PE', 'description': 'Pet Shop'},
    'relogios-e-joias': {'id': 'RE', 'description': 'Relógios'},
    'saude': {'id': 'CP', 'description': 'Saúde e Cuidados Pessoais'},
    'suplementos-e-vitaminas': {'id': 'SA', 'description': 'Suplementos Alimentares'},  # noqa
    'tv': {'id': 'ET', 'description': 'TV e Vídeo'},
    'recem-chegados': {'id': 'RC', 'description': 'Recém Chegados'}
}

METABOOKS_FTP_CRON_HOURS_RETROACTIVE = 24

CONNECTION_TIMEOUT_REQUEST_OMNILOGIC = 5
READ_TIMEOUT_REQUEST_OMNILOGIC = 10

CONNECTION_TIMEOUT_REQUEST_MEDIA = 5
READ_TIMEOUT_REQUEST_MEDIA = 10

ENABLE_SMARTCONTENT_ENRICHMENT_BY_CATEGORY = ['MD', 'LI']

TRUSTED_SELLERS = ['magazineluiza', 'epocacosmeticos', 'kabum', 'netshoes', 'zattini']  # noqa

LIMIT_MARVIN_SELLER_REBUILD = int(
    os.getenv(
        'LIMIT_MARVIN_SELLER_REBUILD', 10000
    )
)
MAX_ITERATION_SECONDS_MARVIN_SELLER_REBUILD = int(
    os.getenv(
        'MAX_ITERATION_SECONDS_MARVIN_SELLER_REBUILD', 60
    )
)
ACK_DEADLINE_SECONDS_MARVIN_SELLER_REBUILD = int(
    os.getenv(
        'ACK_DEADLINE_SECONDS_MARVIN_SELLER_REBUILD', 600
    )
)
MAX_PUBSUB_SEND_THREADS_MARVIN_SELLER_REBUILD = int(
    os.getenv(
        'MAX_PUBSUB_SEND_THREADS_MARVIN_SELLER_REBUILD', 10
    )
)

LIMIT_REBUILD_SELLER_PRODUCTS = 10000

PUBSUB_TOPIC_TAZ_SELLERS = 'taz-sellers-sandbox'

CORS_ALLOW_ORIGINS = '*'

ENABLE_FULFILLMENT = False

ALLOWED_OWNERS_TO_DELETE_ENRICHED_SOURCE = os.getenv(
    'ALLOWED_OWNERS_TO_DELETE_ENRICHED_SOURCE'
) or []

ALLOWED_OWNERS_WRITE_CLASSIFICATIONS_RULES = os.getenv(
    'ALLOWED_OWNERS_WRITE_CLASSIFICATIONS_RULES'
) or []

CUSTOM_ATTRIBUTES_SELLERS = ['magazineluiza']


PRODUCT_WRITER_REDIS_KEY_PATTERN = 'PRODUCT_WRITER::CATEGORIES::'
EXPIRES_CACHE_CATEGORIES = 43200
EXPIRES_REDIS_CACHE_CATEGORIES = 86400
EXPIRES_CACHE_DEFAULT_CATEGORIES = 86400
CACHE_CLEANING_INTERVAL = 60

DATASHEET_NOTFOUND_KEY_PATTERN = 'DATASHEET::NOTFOUND::'
EXPIRES_DATASHEET_NOTFOUND_KEY_PATTERN = int(
    os.getenv('EXPIRES_DATASHEET_NOTFOUND_KEY_PATTERN', 60)
)

ENABLE_EXTRA_DATA = False
ENABLE_PARENT_MATCHING = False

# ACME SETTINGS
ACME_URL = 'http://localhost:9530/acme-api'
ACME_REQUEST_HEADER = {
    'Authorization': 'Token',
    'Content-type': 'application/json',
}

EMAIL_SERVICE_ACCOUNT = ''

MARVIN_NOTIFICATION = {
    'topic_name': os.getenv('MARVIN_NOTIFICATION_TOPIC_NAME') or 'marvin-gateway-sandbox', # noqa
    'project_id': os.getenv('MARVIN_NOTIFICATION_PROJECT_ID') or 'maga-homolog' # noqa
}

ENABLE_LOCK_CONSUMER_PRICE = (
    os.getenv('ENABLE_LOCK_CONSUMER_PRICE', 'False') == 'True'
)

PUBSUB_FACTSHEET_EXPORT_TOPIC_NAME = 'taz-factsheet-export-sandbox'

PUBSUB_MEDIA_EXPORT_TOPIC_NAME = 'taz-media-export-sandbox'

PUBSUB_MEDIA_TOPIC_NAME = 'taz-media'

FORBIDDEN_TERMS = {
    'colrino': 'material sintético',
    'corino': 'material sintético',
    'courino': 'material sintético',
    'courissimo': 'material sintético',
    'couro (sintetico)': 'material sintético',
    'couro ecologico': 'material ecológico',
    'couro fake': 'material sintético',
    'couro organico': 'material orgânico',
    'couro sintetico': 'material sintético',
    'couro tecnologico': 'material tecnologico',
    'couro vegano': 'material vegano',
    'couro verde': 'material sintético',
    'couro(sintetico)': 'material sintético',
    'courvin': 'material sintético',
    'criado - mudos': 'mesa de cabeceira',
    'criado -mudos': 'mesa de cabeceira',
    'criado mudos': 'mesa de cabeceira',
    'criado- mudos': 'mesa de cabeceira',
    'criado-mudo': 'mesa de cabeceira',
    'criado-mudos': 'mesa de cabeceira',
    'criados - mudo': 'mesa de cabeceira',
    'criados - mudos': 'mesa de cabeceira',
    'criados -mudo': 'mesa de cabeceira',
    'criados -mudos': 'mesa de cabeceira',
    'criados mudo': 'mesa de cabeceira',
    'criados mudos': 'mesa de cabeceira',
    'criados- mudo': 'mesa de cabeceira',
    'criados- mudos': 'mesa de cabeceira',
    'criados-mudo': 'mesa de cabeceira',
    'criados-mudos': 'mesa de cabeceira',
    'criado- mudo': 'mesa de cabeceira',
    'criado -mudo': 'mesa de cabeceira',
    'criado mudo': 'mesa de cabeceira',
    'cros fit': 'exercício funcional',
    'crosfit': 'exercício funcional',
    'cross fit': 'exercício funcional',
    'crossfit': 'exercício funcional',
    'korino': 'material sintético',
    'kourino': 'material sintético',
    'semi coro': 'material sintético',
    'tomara que caia': 'sem alça',
    'velcron': 'tiras autocolantes',
    'velcros': 'tiras autocolantes',
    'v.e.l.c.r.o': 'tiras autocolantes',
    'v.e.l.c.r.o.': 'tiras autocolantes',
    'vel.cro': 'tiras autocolantes',
    'velcro': 'tiras autocolantes',
    'velkro': 'tiras autocolantes',
    'veucros': 'tiras autocolantes',
    'veucro': 'tiras autocolantes',
    'velcroo': 'tiras autocolantes',
    'biirken': '',
    'biken': '',
    'binken': '',
    'bir ken': '',
    'bircken': '',
    'birk': '',
    'birke': '',
    'birkein': '',
    'birkem': '',
    'birken': '',
    'birkens': '',
    'birkenstock': '',
    'birker': '',
    'birkien': '',
    'birkin': '',
    'birking': '',
    'birquen': '',
    'crossfits': 'exercício funcional',
    'tomara q caia': 'sem alça',
    'tomara-que-caia': 'sem alça',
    'tomara caia': 'sem alça',
    'brirken': '',
    '(couro sintetico': 'material sintético',
    '(couro sintetico)': 'material sintético',
    'c0rino': 'material sintético',
    'promocao': '',
    'em promocao': '',
    'promocao incrivel': '',
    'promocao presente': '',
    'promocao: leve 3 pague 2': '',
    '(promocao)': '',
    'promocao barato': '',
    'promocao !': '',
    'promocao!!!': '',
    '!promocao!': '',
    'promocao!': '',
    'promocao!!': '',
    '12x sem juros': '',
    'frete grati': '',
    'frete gratis': '',
    'frete grats': '',
    'fretegratis': '',
    'promoaao': ''
}

SKIP_MD5_VALIDATION = False

ENABLED_RETRY_STORAGE = False

KEY_LIMIT_ON_EXTRA_DATA = 10

PRIORITY_EXECUTION_MERGER = {
    constants.SOURCE_OMNILOGIC: 0,
    constants.SOURCE_METABOOKS: 1,
    constants.SOURCE_SMARTCONTENT: 2,
    constants.SOURCE_WAKKO: 3,
    constants.SOURCE_DATASHEET: 4
}

PUBSUB_METADATA_INPUT_TOPIC_NAME = 'taz-metadata-input-sandbox'

METADATA_INPUT_DOWNLOAD_IMAGES_MAX_RETRIES = 3

INACTIVATE_SELLER_SKUS_FLOW_ENABLED = True

MEDIA_MAX_IMAGE_PIXELS = os.getenv(
    'MEDIA_MAX_IMAGE_PIXELS', 2048 * 2048 * 2048 / 4 / 3
)


USER_REVIEW_CACHE_TTL = int(os.getenv('USER_REVIEW_CACHE_TTL', 60 * 24 * 2))


BUCKET_MEDIA_PROCESSOR_TTL = 100

CATALOG_NOTIFICATION_ROUTER_ENABLED_ENDPOINTS = os.getenv(
    'CATALOG_NOTIFICATION_ROUTER_ENABLED_ENDPOINTS', ''
)

CATALOG_NOTIFICATION_ROUTER_taz_score = os.getenv(
    'CATALOG_NOTIFICATION_ROUTER_taz_score', '{}'
)

CATALOG_NOTIFICATION_ROUTER_taz_datalake = os.getenv(
    'CATALOG_NOTIFICATION_ROUTER_taz_datalake', '{}'
)

CATALOG_NOTIFICATION_ROUTER_taz_product_writer = os.getenv(
    'CATALOG_NOTIFICATION_ROUTER_taz_product_writer', '{}'
)

CATALOG_NOTIFICATION_ROUTER_taz_complete_product = os.getenv(
    'CATALOG_NOTIFICATION_ROUTER_taz_complete_product', '{}'
)

CATALOG_NOTIFICATION_ROUTER_taz_product_exporter = os.getenv(
    'CATALOG_NOTIFICATION_ROUTER_taz_complete_product', '{}'
)

CATALOG_NOTIFICATION_ROUTER_taz_match_products = os.getenv(
    'CATALOG_NOTIFICATION_ROUTER_taz_complete_product', '{}'
)

CATALOG_NOTIFICATION_ROUTER_taz_update_category = os.getenv(
    'CATALOG_NOTIFICATION_ROUTER_taz_complete_product', '{}'
)

CATALOG_NOTIFICATION_ROUTER_taz_metadata_verify = os.getenv(
    'CATALOG_NOTIFICATION_ROUTER_taz_complete_product', '{}'
)

CATALOG_NOTIFICATION_ROUTER_taz_price_rule = os.getenv(
    'CATALOG_NOTIFICATION_ROUTER_taz_price_rule', '{}'
)

REBUILD_EXPORTER_CUSTOM_ATTRIBUTES = os.getenv(
    'REBUILD_EXPORTER_CUSTOM_ATTRIBUTES',
    {'Content-Type': 'text/plain; charset=UTF-8'}
)

CATALOG_NOTIFICATION_ROUTER_CUSTOM_ATTRIBUTES_taz_product_exporter = os.getenv(
    'CATALOG_NOTIFICATION_ROUTER_CUSTOM_ATTRIBUTES_taz_product_exporter',
    {'Content-Type': 'application/json'}
)

# OTEL
OTEL_EXPORTER_ENABLED = (
    str(os.getenv('OTEL_EXPORTER_ENABLED', 'false')).lower() == 'true'
)
OTEL_INSTRUMENTATIONS_ENABLED = str(
    os.getenv(
        'OTEL_INSTRUMENTATIONS_ENABLED',
        'pymongo,redis,grpc,falcon,boto,requests'
    )
).split(',')

PUBSUB_DATALAKE_INPUT_TOPIC_NAME = 'taz-datalake'
PUBSUB_DATALAKE_INPUT_SUB_NAME = 'taz-datalake-sub'

PUBSUB_COMPLETE_PRODUCT_TOPIC_NAME = 'taz-complete-product'
PUBSUB_COMPLETE_PRODUCT_SUB_NAME = 'taz-complete-product-sub'

PUBSUB_SCORE_TOPIC_NAME = 'taz-score'
PUBSUB_SCORE_SUB_NAME = 'taz-score-sub'

PUBSUB_REBUILD_TOPIC_NAME = 'taz-rebuild-products'
PUBSUB_REBUILD_SUB_NAME = 'taz-rebuild-products-sub'

PUBSUB_UPDATE_CATEGORY_TOPIC_NAME = 'taz-update-category'
PUBSUB_UPDATE_CATEGORY_SUB_NAME = 'taz-update-category-sub'

PUBSUB_SUBSCRIPTION_ID = ''

PUBSUB_MATCHING_PRODUCT_TOPIC_NAME = 'taz-match-products'
PUBSUB_MATCHING_PRODUCT_SUB_NAME = 'taz-match-products-sub'

PUBSUB_RECLASSIFICATION_PRICE_RULE_NAME = 'taz-price-rule'

PUBSUB_PRODUCT_WRITER_TOPIC_NAME = 'taz-product-writer'
PUBSUB_PRODUCT_WRITER_SUB_NAME = 'taz-product-writer-sub'

PUBSUB_PRODUCT_EXPORTER_TOPIC_NAME = 'taz-product-exporter'
PUBSUB_PRODUCT_EXPORTER_SUB_NAME = 'taz-product-exporter-sub'

PUBSUB_NOTIFICATION_TOPIC_NAME = 'taz-notification'
PUBSUB_NOTIFICATION_SUB_NAME = 'taz-notification-sub'

PAGINATION_LIMIT_PRICE_RULE_CRON = 1000
MAX_WORKERS_PRICE_RULE_CRON = 25
PRICE_RULE_PROGRESS_TTL = 1 * SECONDS
BLOCKED_PRODUCT_TYPES_CLASSIFICATIONS_RULES = ['Livro']
ALLOW_INACTIVATION_PERCENTAGE = int(os.getenv(
    'ALLOW_INACTIVATION_PERCENTAGE', '15'
))

POLLER_PRODUCT_SHOULD_FILTER_CREATED_AT_AND_ACTIVE = bool(str(
    os.getenv('POLLER_PRODUCT_SHOULD_FILTER_CREATED_AT_AND_ACTIVE', 'true')
).lower() == 'true')

MEDIA_SERVICE_STRATEGY = {
    MAAS_PRODUCT_IMAGE_BUCKET: os.getenv(
        'MEDIA_SERVICE_STRATEGY_MAAS_PRODUCT_IMAGE_BUCKET', ''
    ),
    MEDIA_LIST_BUCKET: os.getenv(
        'MEDIA_SERVICE_STRATEGY_MEDIA_LIST_BUCKET', ''
    ),
    METADATA_IMAGE_BUCKET: os.getenv(
        'MEDIA_SERVICE_STRATEGY_METADATA_IMAGE_BUCKET',
        'https://taz-metadata-images-sandbox.magalu.com,https://taz-metadata-images-sandbox.storage.googleapis.com'  # noqa
    )
}

# CURRENCY
DEFAULT_CURRENCY = os.getenv(
    'DEFAULT_CURRENCY', 'BRL'
)

BUCKET_CONFIG = {
    'write': [
        {
            'storage': 'gcp',
            'bucket_name': 'taz-medias-sandbox',
            'active': True
        },
    ],
    'read': [
        {
            'storage': 'gcp',
            'bucket_name': 'taz-medias-sandbox',
            'active': True
        },
    ],
}
