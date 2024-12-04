import os

from .base import *  # noqa

QUEUE_QUANTITY_DELAY = 0

# ACME SETTINGS
ACME_URL = os.getenv('ACME_URL', 'http://acme-api.tst-5.magazineluiza.com.br')
ACME_TOKEN = os.getenv('ACME_TOKEN')
ACME_REQUEST_HEADER = {
    'Authorization': 'Token {}'.format(ACME_TOKEN),
    'Content-type': 'application/json',
}

# ACME OLD IMPORTER
FTP_IMAGE_REGION_NAME = 'us-east-1'

MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
MONGO_HOST = os.environ.get('MONGO_HOST')
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

CATEGORIES_ALLOWED_FOR_PRICE = ()

BAZAARVOICE_HOST = 'sftp-stg.bazaarvoice.com'

APIS['patolino']['url'] = os.getenv('PATOLINO_URL', 'http://patolino.patolino-api.svc.cluster.local')  # noqa
APIS['patolino']['timeout'] = int(os.getenv('PATOLINO_TIMEOUT', 20))


DEFAULT_DB_SETTINGS = {
    'host': 's500hmlsql01.gcp.luizalabs.com',
    'user': 'usr_taz',
    'password': os.getenv('DEFAULT_DB_PASSWORD'),
    'dbname': 'dbMagazine',
    'port': 11433
}

for poller in POLLERS.keys():
    POLLERS[poller].update(database=DEFAULT_DB_SETTINGS)

PRODUCT_METADATA_TOPIC_NAME = 'taz-metadata-product-sandbox'

LIMIT_REBUILD_SELLER_PRODUCTS = 10
EXPIRES_CACHE_CATEGORIES = 60
EXPIRES_CACHE_DEFAULT_CATEGORIES = 120

ENABLE_PRICE_LOCK_PERCENT = False

KAFKA_CLUSTERS_CONFIG = {
    'datalake': {
        'bootstrap.servers': os.getenv(
            'KAFKA_BOOTSTRAP_SERVERS_DATALAKE',
            'maas-kafka-sellers-01-hmg-internal.mglu.io:9092'
        )
    }
}

CHANNEL_GCHAT = os.getenv('CHANNEL_GCHAT')

ALLOWED_OWNERS_TO_DELETE_ENRICHED_SOURCE = ['*']
ALLOWED_OWNERS_WRITE_CLASSIFICATIONS_RULES = ['*']

PRICE_RULE_PROGRESS_TTL = 1 * MINUTES
