import pytest
from pymongo import MongoClient

from taz.consumers.core.database.mongodb import MongodbMixin


class TestMongodb:

    @pytest.fixture
    def mongodb(self):
        client = MongoClient('127.0.0.1', 27017)
        client.test.Test.insert_one({'a': 1})
        return MongodbMixin()

    def test_mongo_collection(self, mongodb):
        collection = mongodb.get_collection('test')
        assert collection

    def test_mongo_connection_reuse(self):
        a = MongodbMixin()
        b = MongodbMixin()

        a.get_collection('a')
        b.get_collection('b')

        assert a._conn is b._conn and a._database is b._database
        assert (
            id(a._conn) == id(b._conn) and
            id(a._database) == id(b._database)
        )
