
from maaslogger import base_logger
from pymongo import MongoClient
from simple_settings import settings

logger = base_logger.get_logger(__name__)


class MongodbMixin:
    _conn = None
    _database = None

    @classmethod
    def conn(cls):
        if cls._conn is None:
            logger.debug('Starting new connection with MongoDB...{}'.format(
                settings.MONGO_HOST,
            ))
            cls._conn = MongoClient(settings.MONGO_URI)
        return cls._conn

    @classmethod
    def database(cls):
        if cls._database is None:
            logger.debug('Using database instance on {}'.format(
                settings.MONGO_HOST,
            ))
            cls._database = getattr(
                cls.conn(),
                settings.MONGO_DATABASE
            )
        return cls._database

    def get_collection(self, collection_name):
        logger.debug('Getting collection {} on {}:{}'.format(
            collection_name,
            settings.MONGO_HOST,
            settings.MONGO_DATABASE,
        ))
        return getattr(
            MongodbMixin.database(),
            collection_name,
        )
