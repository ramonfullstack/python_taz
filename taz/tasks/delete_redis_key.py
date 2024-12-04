import argparse
import logging

from redis import Redis
from simple_settings import settings

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--key', help='App name')


class RedisDeleteKey:

    def __init__(self):
        self.redis = Redis(
            host=settings.REDIS_LOCK_SETTINGS['host'],
            port=settings.REDIS_LOCK_SETTINGS['port'],
            password=settings.REDIS_LOCK_SETTINGS.get('password')
        )

    def execute(self, key):
        if key.strip() == '*':
            logger.error('Error while deleting key:{} from Redis'.format(key))

            return False

        keys = self.redis.keys(key)
        if not keys:
            logger.error(
                'Error while deleting key not found keys with:{}'.format(key)
            )

            return False

        [self.redis.delete(k) for k in keys]

        logger.info('Deleted keys {} from Redis'.format(keys))

        return True


if __name__ == '__main__':  # pragma: no cover
    args = parser.parse_args()

    redis_delete = RedisDeleteKey()
    redis_delete.execute(keys=args.key)
