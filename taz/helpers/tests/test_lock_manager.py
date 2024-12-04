from datetime import datetime
from threading import Thread
from time import sleep

import pytest
from slugify import slugify

from taz.helpers.lock_manager import MongoLock


class TestLockManager:

    @pytest.fixture
    def configure_lock(self, mongo_database):
        mongo_database.lock.create_index([("key", 1)], unique=True)
        mongo_database.lock.create_index(
            [("created_at", 1)],
            expireAfterSeconds=60
        )

    @pytest.mark.parametrize('enable_lock', [
        False,
        True,
    ])
    def test_lock_key(
        self,
        configure_lock,
        mongo_database,
        enable_lock
    ):
        def save_data(waiting_time, enablelock):
            sku = '012345678'
            seller_id = 'magazineluiza'

            with MongoLock(
                mongo_database,
                slugify(seller_id + sku),
                enablelock
            ):
                sleep(waiting_time)
                mongo_database.documents.insert_one(
                    {
                        'seller_id': seller_id,
                        'sku': sku,
                        'created_at': datetime.utcnow()
                    }
                )

        mongo_database.documents.delete_many({})
        t1 = Thread(target=save_data, args=[2, enable_lock])
        t2 = Thread(target=save_data, args=[0, enable_lock])
        t1.start()
        t2.start()
        sleep(3)
        t1.join()
        t2.join()
        documents = list(mongo_database.documents.find({}))
        time_1 = documents[0]['created_at']
        time_2 = documents[1]['created_at']
        diff = (time_1 - time_2).total_seconds()

        if enable_lock:
            assert abs(diff) < 1
        else:
            assert abs(diff) >= 2
