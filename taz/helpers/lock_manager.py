import logging
from datetime import datetime

from pymongo.errors import DuplicateKeyError

logger = logging.getLogger(__name__)


class MongoLock:
    def __init__(self, database, key, block=True):
        self.database = database
        self.key = key
        self.block = block

    def __enter__(self):
        while self.block:
            try:
                self.database.lock.insert_one(
                    {
                        'key': self.key,
                        'created_at': datetime.utcnow()
                    }
                )
                return self
            except DuplicateKeyError:
                logger.info(f'waiting lock for key:{self.key}')

    def __exit__(self, type, value, traceback):
        if self.block:
            self.database.lock.delete_one({'key': self.key})
