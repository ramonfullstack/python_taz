from .sandbox import *  # noqa

REDIS_SETTINGS = {
    'host': 'taz-sandbox-0.maga-homolog.y4z42.us-east1-b.redishot.ipet.sh',
    'port': 6379,
    'socket_timeout': os.getenv('REDIS_LOCK_SOCKET_TIMEOUT', 60),
    'socket_connect_timeout': os.getenv(
        'REDIS_LOCK_SOCKET_CONNECT_TIMEOUT', 60
    )
}

REDIS_LOCK_SETTINGS = REDIS_SETTINGS
