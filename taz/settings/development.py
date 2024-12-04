from .base import *  # noqa

DEFAULT_PROCESSORS_COUNT = 1

DEFAULT_DB_SETTINGS = {
    'host': '172.19.90.71',
    'user': 'ml_test_write',
    'password': '',
    'dbname': 'dbMagazine',
    'port': 1433
}

# ACME SETTINGS
ACME_URL = 'http://catalogo-sandbox.luizalabs.com/'
ACME_TOKEN = ''
ACME_REQUEST_HEADER['Authorization'] = 'Token {}'.format(ACME_TOKEN)  # noqa

POLLERS.update({  # noqa
    'product': {
        'wait_time': DEFAULT_WAIT_TIME,  # noqa
        'database': DEFAULT_DB_SETTINGS,  # noqa
        'aws_settings': DEFAULT_AWS_SETTINGS,  # noqa
        'stream_name': 'taz-product-dev'
    }
})

ALLOWED_OWNERS_TO_DELETE_ENRICHED_SOURCE = ['*']
ALLOWED_OWNERS_WRITE_CLASSIFICATIONS_RULES = ['*']
