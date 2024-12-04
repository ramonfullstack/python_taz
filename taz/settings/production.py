import os

from taz.settings.base import *  # noqa

GOOGLE_PROJECT_ID = 'magalu-digital-project'

DEFAULT_DB_SETTINGS = {
    'host': os.getenv('DB_HOST', 'acme-sql.magazineluiza.com.br'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'dbname': 'dbMagazine',
    'port': 1433
}

# DEFAULT SETTINGS FOR AWS
DEFAULT_AWS_SETTINGS = {
    'region': os.getenv('AWS_REGION', 'us-east-1'),
    'account_id': '075096048015',
}

MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
MONGO_HOST = os.environ.get('MONGO_HOST', 'taz-mongos-34.taz-mongos-34')
MONGO_OPTIONS = os.environ.get('MONGO_OPTIONS', 'readPreference=primary')
MONGO_PORT = os.environ.get('MONGO_PORT', ':27017')
MONGO_HOSTS = [
    host if host.endswith(MONGO_PORT) else f'{host}{MONGO_PORT}'
    for host in MONGO_HOST.split(',')
]
MONGO_HOST = ','.join(MONGO_HOSTS)

MONGO_URI = (
    f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}/{MONGO_DATABASE}?authSource=admin&{MONGO_OPTIONS}' # noqa
)


POLLERS['product']['wait_time'] = os.getenv('DEFAULT_WAIT_TIME', DEFAULT_WAIT_TIME)  # noqa
POLLERS['product']['database'] = DEFAULT_DB_SETTINGS  # noqa: F405
POLLERS['product']['project_id'] = GOOGLE_PROJECT_ID  # noqa: F405

POLLERS['media']['wait_time'] = MINUTES * 10  # noqa: F405
POLLERS['media']['database'] = DEFAULT_DB_SETTINGS  # noqa: F405
POLLERS['media']['aws_settings'] = DEFAULT_AWS_SETTINGS  # noqa: F405
POLLERS['media']['stream_name'] = 'taz-media'  # noqa: F405

POLLERS['media_active']['wait_time'] = MINUTES * 10  # noqa: F405
POLLERS['media_active']['database'] = DEFAULT_DB_SETTINGS  # noqa: F405
POLLERS['media_active']['aws_settings'] = DEFAULT_AWS_SETTINGS  # noqa: F405
POLLERS['media_active']['stream_name'] = 'taz-media'  # noqa: F405

POLLERS['video']['wait_time'] = MINUTES * 10  # noqa: F405
POLLERS['video']['database'] = DEFAULT_DB_SETTINGS  # noqa: F405
POLLERS['video']['project_id'] = GOOGLE_PROJECT_ID  # noqa: F405

POLLERS['media_pf']['wait_time'] = HOURS * 12  # noqa: F405
POLLERS['media_pf']['database'] = DEFAULT_DB_SETTINGS  # noqa: F405
POLLERS['media_pf']['aws_settings'] = DEFAULT_AWS_SETTINGS  # noqa: F405
POLLERS['media_pf']['stream_name'] = 'taz-media'  # noqa: F405

POLLERS['factsheet']['wait_time'] = MINUTES * 5  # noqa: F405
POLLERS['factsheet']['database'] = DEFAULT_DB_SETTINGS  # noqa: F405
POLLERS['factsheet']['project_id'] = GOOGLE_PROJECT_ID  # noqa: F405

POLLERS['price']['database'] = DEFAULT_DB_SETTINGS  # noqa: F405
POLLERS['price']['aws_settings'] = DEFAULT_AWS_SETTINGS  # noqa: F405
POLLERS['price']['stream_name'] = 'taz-price'  # noqa: F405
POLLERS['price']['topic_name'] = os.getenv('TAZ_PRICES_POLLER_TOPIC', 'taz-prices')  # noqa
POLLERS['price']['project_id'] = 'magalu-digital-project'  # noqa: F405

POLLERS['price_pf']['wait_time'] = HOURS * 12  # noqa: F405
POLLERS['price_pf']['database'] = DEFAULT_DB_SETTINGS  # noqa: F405
POLLERS['price_pf']['aws_settings'] = DEFAULT_AWS_SETTINGS  # noqa: F405
POLLERS['price_pf']['stream_name'] = 'taz-price'  # noqa: F405

POLLERS['price_campaign']['database'] = DEFAULT_DB_SETTINGS  # noqa: F405
POLLERS['price_campaign']['topic_name'] = os.getenv('TAZ_PRICE_CAMPAIGN_POLLER_TOPIC', 'taz-price-campaign')  # noqa
POLLERS['price_campaign']['project_id'] = GOOGLE_PROJECT_ID  # noqa

POLLERS['lu_content'] = {
    'wait_time': MINUTES * 15,
    'database': DEFAULT_DB_SETTINGS,
    'topic_name': 'taz-poller-lu-content',
    'project_id': 'magalu-digital-project'
}

POLLERS['category'] = {
    'wait_time': MINUTES * 15,
    'database': DEFAULT_DB_SETTINGS,
    'topic_name': 'taz-poller-category',
    'project_id': 'magalu-digital-project'
}

POLLERS['product_sold_quantity'] = {
    'database': {
        'host': 'p52-replica.luizalabs.com',
        'user': 'usr_taz',
        'password': os.getenv('PRODUCT_SOLD_QUANTITY_PASSWORD'),
        'dbname': 'p52',
        'port': 3306
    },
    'aws_settings': DEFAULT_AWS_SETTINGS,
    'stream_name': 'taz-customer-behavior',
    'wait_time': MINUTES * 60
}

POLLERS['product_clicks_quantity']['aws_settings'] = DEFAULT_AWS_SETTINGS  # noqa
POLLERS['product_clicks_quantity']['stream_name'] = 'taz-customer-behavior'  # noqa

POLLERS['base_price']['wait_time'] = DEFAULT_WAIT_TIME  # noqa: F405
POLLERS['base_price']['database'] = DEFAULT_DB_SETTINGS  # noqa: F405
POLLERS['base_price']['project_id'] = GOOGLE_PROJECT_ID  # noqa: F405

POLLERS['partner']['wait_time'] = DEFAULT_WAIT_TIME  # noqa: F405
POLLERS['partner']['database'] = DEFAULT_DB_SETTINGS  # noqa: F405
POLLERS['partner']['project_id'] = GOOGLE_PROJECT_ID  # noqa: F405

# LIST OF ALL CONSUMERS
CONSUMERS = {
    'product': {
        'stream_name': 'taz-product'
    },
    'category': {
        'stream_name': 'taz-category'
    },
    'media': {
        'stream_name': 'taz-media'
    },
    'factsheet': {
        'stream_name': 'taz-factsheet'
    },
    'price': {
        'stream_name': 'taz-price'
    },
    'customer_behavior': {
        'stream_name': 'taz-customer-behavior'
    },
    'buybox_pending': {
        'stream_name': 'taz-product'
    },
    'media_bucket': {
        'stream_name': 'taz-media'
    }
}

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# PRODUCT CONSUMER SETTINGS
PRODUCT_WRITER_V2_QUEUE_NAME = 'taz-product-writer-v2'
SHIPPING_LOGGER_QUEUE_NAME = 'taz-shipping-logger'

MEDIA_S3_BUCKET = 'taz-medias-production'
MEDIA_BUCKET = 'taz-medias-production'
FACTSHEET_S3_BUCKET = 'taz-sp-factsheet-production'

FACTSHEET_STORAGE = 'taz-factsheet-production'
RAW_FACTSHEET_STORAGE = 'taz-raw-factsheet-production'

REDIS_POLLER_HOST = os.getenv(
    'REDIS_POLLER_HOST',
    'taz-poller-0.magalu-digital-project.y4z42.us-east1-b.redishot.ipet.sh'
)

REDIS_SETTINGS = {
    'host': REDIS_POLLER_HOST,
    'port': 6379
}

REDIS_CONSUMER_HOST = os.getenv(
    'REDIS_CONSUMER_HOST',
    'taz-consumer-0.magalu-digital-project.y4z42.us-east1-b.redishot.ipet.sh'
)

REDIS_LOCK_SETTINGS = {
    'host': REDIS_CONSUMER_HOST,
    'port': 6379,
    'socket_timeout': os.getenv('REDIS_LOCK_SOCKET_TIMEOUT', 10),
    'socket_connect_timeout': os.getenv(
        'REDIS_LOCK_SOCKET_CONNECT_TIMEOUT', 10
    )
}

# ACME SETTINGS
ACME_URL = 'https://acme-api.magazineluiza.com.br'
ACME_TOKEN = os.getenv('ACME_TOKEN')
ACME_REQUEST_HEADER = {
    'Authorization': 'Token {}'.format(ACME_TOKEN),
    'Content-type': 'application/json',
}


# INTEGRA COMMERCE SETTINGS
INTEGRACOMMERCE_URL = 'https://mma.integracommerce.com.br'
INTEGRACOMMERCE_TOKEN = (
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJoZW5yaXF1ZS5icmFnYSIsInV'
    'uaXF1ZV9uYW1lIjoiaGVucmlxdWUuYnJhZ2EiLCJqdGkiOiI5NjMzNWI5Ni04ZWQ0LTRiYjY'
    'tOGJlNi1jNTJiMzRkYjYxMTIiLCJpYXQiOjE1MDc3MzE3MjAsIm5iZiI6MTUwNzczMTcyMCw'
    'iZXhwIjoxNTEwMzIzNzIwLCJpc3MiOiJFbWlzc29yTWFnYXppbmUiLCJhdWQiOiJBdWRpZW5'
    'jaWFNYXN0ZXJNYWdhemluZSJ9.bYXlDqErCm1kWtHat2ofQmvMVnqBHWSjLUvxvSqYaFY'
)

# BABEL SETTINGS
BABEL_URL = 'https://mkp.luizalabs.com'
BABEL_TOKEN = os.getenv('BABEL_TOKEN')

# SOLR SETTINGS
SOLR_MASTER = {
    'write_url': os.getenv('SOLR_WRITE_URL', 'http://acme-solr-master-b-private.magazineluiza.com.br:8983'),  # noqa
    'write_core': 'ml-products-v1'
}

SOLR_SUGGESTION = {
    'write_url': 'http://acme-solr-master-b-private.magazineluiza.com.br:8983',  # noqa
    'write_core': 'ml-suggestion'
}

SOLR_READ_URL = 'http://acme-solr-master.magazineluiza.com.br:8080'  # noqa
SOLR_READ_CORE = 'ml-products-v1'

# HAMILTON SETTINGS
APIS = {
    'taz': {
        'url': 'https://taz-api.magazineluiza.com.br',
        'token': os.getenv('TAZ_TOKEN'),
        'timeout': 5,
    },
    'arcoiro': {
        'url': 'http://arcoiro-external.luizalabs.com',
        'token': os.getenv('ARCOIRO_TOKEN'),
        'timeout': 15
    },
    'bazaarvoice': {
        'url': 'https://luizalabs-prod.apigee.net/v2',
        'token': os.getenv('BAZAAR_VOICE_TOKEN'),
        'timeout': 5,
        'ssl_verify': True
    },
    'fry': {
        'url': 'https://fry.luizalabs.com',
        'token': os.getenv('FRY_TOKEN'),
        'timeout': 5
    },
    'frajola': {
        'url': 'https://frajola.luizalabs.com',
        'token': os.getenv('FRAJOLA_TOKEN'),
        'timeout': 10
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
        'url': 'https://helena.magazineluiza.com.br',
        'client_secret': os.getenv('HELENA_SECRET'),
        'client_id': os.getenv('HELENA_CLIENT_ID'),
        'timeout': 5
    },
    'apiluiza': {
        'url': 'https://api.apiluiza.com.br/v1',
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
    'marvin': {
        'url': os.getenv('MARVIN_URL', 'https://marvin.luizalabs.com')
    },
    'patolino': {
        'url': os.getenv('PATOLINO_URL', 'https://notificacao-produtos.luizalabs.com'),  # noqa
        'token': os.getenv('PATOLINO_TOKEN', ''),
        'timeout': os.getenv('PATOLINO_TIMEOUT', 5)
    },
    'maas-product': {
        'url': os.getenv(
            'MAAS_PRODUCT_URL',
            'https://api-admin-product.magalu.com'
        ),
        'timeout': os.getenv('MAAS_PRODUCT_TIMEOUT', 5),
        'max_retries': int(os.getenv('MAAS_PRODUCT_MAX_RETRIES', 3)),
        'authorization_server_url': os.getenv('MAAS_PRODUCT_KEYCLOAK'),
        'client_id': os.getenv('MAAS_PRODUCT_CLIENT_ID'),
        'client_secret': os.getenv('MAAS_PRODUCT_CLIENT_SECRET')
    },
    'omnilogic': {
        'url': os.getenv(
            'NOTIFY_OMNILOGIC_OMNILOGIC_URL',
            'https://integration.oppuz.com/magalu/notification'
        ),
        'headers': {
            'Content-type': 'application/json',
            'Authorization': os.getenv('NOTIFY_OMNILOGIC_OMNILOGIC_TOKEN')
        },
    }
}

ACME_MEDIA_DOMAIN = 'https://a-static.mlcdn.com.br'
FACTSHEET_DOMAIN = 'https://f-static.mlcdn.com.br'

PRODUCT_METADATA_TOPIC_NAME = 'taz-metadata-product'

# ACME OLD IMPORTER
FTP_IMAGE_REGION_NAME = 'sa-east-1'

# ID GENERATOR SETTINGS
# ID_PREFIX = (
#     '56', '79', '78', '80', '81', '98', '97', '96', '95',
#     '40', '41', '42', '43', '44', '45', '46', '47', '48', '49'
# )

BLACKLIST_CHARACTERS = (
    'I', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X',
    'W', 'Y', 'z', 'i', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'x', 'w', 'y', 'z'
)
ID_LENGTH = 10
ID_PREFIX = (
    'aa', 'ab', 'ac', 'ad', 'ae', 'af', 'ag', 'ah', 'aj', 'ak',
    'ba', 'bb', 'bc', 'bd', 'be', 'bf', 'bg', 'bh', 'bj', 'bk',
    'ca', 'cb', 'cc', 'cd', 'ce', 'cf', 'cg', 'ch', 'cj', 'ck',
    'da', 'db', 'dc', 'dd', 'de', 'df', 'dg', 'dh', 'dj', 'dk',
    'ea', 'eb', 'ec', 'ed', 'ee', 'ef', 'eg', 'eh', 'ej', 'ek',
    'fa', 'fb', 'fc', 'fd', 'fe', 'ff', 'fg', 'fh', 'fj', 'fk',
    'ga', 'gb', 'gc', 'gd', 'ge', 'gf', 'gg', 'gh', 'gj', 'gk',
    'ha', 'hb', 'hc', 'hd', 'he', 'hf', 'hg', 'hh', 'hj', 'hk',
    'ja', 'jb', 'jc', 'jd', 'je', 'jf', 'jg', 'jh', 'jj', 'jk',
    'ka', 'kb', 'kc', 'kd', 'ke', 'kf', 'kg', 'kh', 'kj', 'kk',
)
ONLY_DIGITS_ID_GENERATOR = False

STAMP_SELECTION = 19504
DISABLE_STAMP = True

SHERLOCK_CACHE_DIR = os.environ.get(
    'SHERLOCK_CACHE_DIR', '/srv/taz/.exclusions/'
)

CLOUDFRONT_DISTRIBUTION_ID = 'E3PLOFO00ZXN4A'

INDEXING_PROCESS_STREAM_NAME = 'taz-indexing-process'
PUBLISH_STREAM = True

MARVIN_NOTIFICATION = {
    'topic_name': os.getenv('MARVIN_NOTIFICATION_TOPIC_NAME') or 'marvin-gateway', # noqa
    'project_id': os.getenv('MARVIN_NOTIFICATION_PROJECT_ID') or 'magalu-digital-project' # noqa
}

CATALOG_NOTIFICATION = 'arn:aws:sns:us-east-1:075096048015:catalog-notification'  # noqa


RAW_PRODUCT_STORAGE = 'taz-raw-products'

DEFAULT_PRICE_LOCK_PERCENT = 1
ENABLE_PRICE_LOCK_PERCENT = False

METADATA_INPUT_BUCKET = 'taz-metadata-input'
METADATA_IMAGE_BUCKET = os.getenv('METADATA_IMAGE_BUCKET', 'taz-metadata-images')  # noqa
MAAS_PRODUCT_IMAGE_BUCKET = os.getenv('MAAS_PRODUCT_IMAGE_BUCKET', 'maas-files-product')  # noqa

PRODUCT_SCORE_QUEUE_NAME = 'taz-score'

ENRICHED_PRODUCTS_NOTIFICATION = 'arn:aws:sns:us-east-1:075096048015:enriched-products-notification'  # noqa

CHANNEL_GCHAT = os.getenv('CHANNEL_GCHAT')

BUCKET_REPORT = 'taz-report'

KAFKA_CLUSTERS_CONFIG = {
    'datalake': {
        'bootstrap.servers': os.getenv(
            'KAFKA_BOOTSTRAP_SERVERS_DATALAKE',
            'kafka-data-engineering-ext.gcp.luizalabs.com:19092'
        )
    }
}

DATALAKE = {
    'enriched_product': {
        'niagara': {
            'topic_name': 'niagara-catalogo-enriched',
            'project_id': 'maga-bigdata',
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
            'project_id': 'maga-bigdata',
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
            'project_id': 'maga-bigdata',
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
            'project_id': 'maga-bigdata',
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
            'project_id': 'maga-bigdata',
            'enabled': str(os.getenv('NIAGARA_UNPUBLISH_ENABLED', 'true')).lower() == 'true' # noqa
        },
        'tetrix': {
            'topic_name': os.getenv('TETRIX_UNPUBLISH_TOPIC', 'taz.unpublish.tetrix.1'), # noqa
            'enabled': str(os.getenv('TETRIX_UNPUBLISH_ENABLED', 'false')).lower() == 'true' # noqa
        }
    },
    'price': {
        'niagara': {
            'topic_name': 'catalog-dag-price',
            'project_id': 'maga-bigdata',
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
            'project_id': 'maga-bigdata',
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
            'project_id': 'maga-bigdata',
            'enabled': str(os.getenv('NIAGARA_SHIPPING_ENABLED', 'true')).lower() == 'true' # noqa
        },
        'tetrix': {
            'topic_name': os.getenv('TETRIX_SHIPPING_TOPIC', 'taz.shipping.tetrix.1'), # noqa,
            'enabled': str(os.getenv('TETRIX_SHIPPING_ENABLED', 'false')).lower() == 'true' # noqa
        }
    },
    'stock': {
        'niagara': {
            'topic_name': 'niagara-catalogo-stock',
            'project_id': 'maga-bigdata',
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
            'project_id': 'maga-bigdata',
            'enabled': str(os.getenv('NIAGARA_FACTSHEET_ENABLED', 'true')).lower() == 'true' # noqa
        },
        'tetrix': {
            'topic_name': os.getenv('TETRIX_FACTSHEET_TOPIC', 'taz.factsheet.tetrix.1'), # noqa
            'enabled': str(os.getenv('TETRIX_FACTSHEET_ENABLED', 'false')).lower() == 'true' # noqa
        }
    }
}

ENABLE_MATCHING_FROM_ENTITY = ['Livro']

PRODUCT_EXPORTER_SCOPES = {
    'product': [
        {
            'scope': 'simple_product',
            'topic_name': 'taz-product-exporter-simple-product',
            'project_id': 'magalu-digital-project'
        }
    ],
    'metadata_verify': [
        {
            'scope': 'product_features',
            'topic_name': 'taz-product-exporter-product-features',
            'project_id': 'magalu-digital-project'
        }
    ],
    'matching_product': [
        {
            'scope': 'product_features',
            'topic_name': 'taz-product-exporter-product-features',
            'project_id': 'magalu-digital-project'
        }
    ],
    'badge': [
        {
            'scope': 'simple_product',
            'topic_name': 'taz-product-exporter-simple-product',
            'project_id': 'magalu-digital-project'
        }
    ],
    'stock': [
        {
            'scope': 'simple_product',
            'topic_name': 'taz-product-exporter-simple-product',
            'project_id': 'magalu-digital-project'
        }
    ],
    'price': [
        {
            'scope': 'simple_product',
            'topic_name': 'taz-product-exporter-simple-product',
            'project_id': 'magalu-digital-project'
        }
    ],
    'matching': [
        {
            'scope': 'simple_product',
            'topic_name': 'taz-product-exporter-simple-product',
            'project_id': 'magalu-digital-project'
        },
        {
            'scope': 'source_product',
            'topic_name': 'taz-product-exporter-source-product',
            'project_id': 'magalu-digital-project'
        }
    ],
    'media': [
        {
            'scope': 'simple_product',
            'topic_name': 'taz-product-exporter-simple-product',
            'project_id': 'magalu-digital-project'
        },
        {
            'scope': 'source_product',
            'topic_name': 'taz-product-exporter-source-product',
            'project_id': 'magalu-digital-project'
        }
    ]
}

ENABLE_WAKKO_SCOPE = True

STOCK_NOTIFICATION = {
    'DC': {
        'topic_name': os.getenv('STOCK_NOTIFICATION_DC_TOPIC_NAME') or 'taz-stock-dc',  # noqa
        'project_id': os.getenv('STOCK_NOTIFICATION_DC_PROJECT_ID') or 'magalu-digital-project'   # noqa
    },
    'STORE': {
        'topic_name': os.getenv('STOCK_NOTIFICATION_STORE_TOPIC_NAME') or 'taz-stock-store',  # noqa
        'project_id': os.getenv('STOCK_NOTIFICATION_STORE_PROJECT_ID') or 'magalu-digital-project'  # noqa
    }
}

PUBSUB_PUBLISHER_NOTIFY_TOPIC = 'catalog-notification'
PUBSUB_NOTIFY_PROJECT_ID = 'magalu-digital-project'
PATOLINO_STREAM_TOPIC_NAME = 'patolino-products'
PATOLINO_STREAM_PROJECT_ID = 'magalu-digital-project'

OMNILOGIC_NOTIFICATION_URL = 'http://integration-omnilogic.luizalabs.com/store/{source}/notification'  # noqa

PUBSUB_TOPIC_TAZ_SELLERS = 'taz-sellers'

PUBSUB_FACTSHEET_EXPORT_TOPIC_NAME = 'taz-factsheet-export'

PUBSUB_MEDIA_EXPORT_TOPIC_NAME = 'taz-media-export'

PUBSUB_MEDIA_TOPIC_NAME = 'taz-media'

PUBSUB_METADATA_INPUT_TOPIC_NAME = 'taz-metadata-input'

# ListMedia
MEDIA_LIST_BUCKET = os.getenv('MEDIA_LIST_BUCKET', 'img.magazineluiza.com.br')

PUBSUB_DATALAKE_INPUT_TOPIC_NAME = 'taz-datalake'
PUBSUB_DATALAKE_INPUT_SUB_NAME = 'taz-datalake-sub'

PUBSUB_COMPLETE_PRODUCT_TOPIC_NAME = 'taz-complete-product'
PUBSUB_COMPLETE_PRODUCT_SUB_NAME = 'taz-complete-product-sub'

PUBSUB_SCORE_TOPIC_NAME = 'taz-score'
PUBSUB_SCORE_SUB_NAME = 'taz-score-sub'

PUBSUB_REBUILD_TOPIC_NAME = 'taz-rebuild'
PUBSUB_REBUILD_SUB_NAME = 'taz-rebuild-sub'

ALLOWED_OWNERS_TO_DELETE_ENRICHED_SOURCE = ['catalogo']
ALLOWED_OWNERS_WRITE_CLASSIFICATIONS_RULES = ['catalogo', 'acme-admin']

PRICE_RULE_PROGRESS_TTL = 10 * MINUTES

MEDIA_SERVICE_STRATEGY = {
    MAAS_PRODUCT_IMAGE_BUCKET: os.getenv(
        'MEDIA_SERVICE_STRATEGY_MAAS_PRODUCT_IMAGE_BUCKET', ''
    ),
    MEDIA_LIST_BUCKET: os.getenv(
        'MEDIA_SERVICE_STRATEGY_MEDIA_LIST_BUCKET', ''
    ),
    METADATA_IMAGE_BUCKET: os.getenv(
        'MEDIA_SERVICE_STRATEGY_METADATA_IMAGE_BUCKET',
        'https://taz-metadata-images.storage.googleapis.com'
    )
}
