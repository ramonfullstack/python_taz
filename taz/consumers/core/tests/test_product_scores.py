import pytest

from taz.constants import (
    META_TYPE_PRODUCT_FACTSHEET_SCORE,
    META_TYPE_PRODUCT_IMAGE_SCORE
)
from taz.consumers.core.database.productscoresdb import ProductScoresCollection


class TestProductScoresCollection:

    @pytest.fixture
    def processor(self):
        return ProductScoresCollection()

    @pytest.fixture
    def database(self, mongo_database):
        return mongo_database.get_collection('product_scores')

    @pytest.fixture
    def product_score_factsheet_data(self):
        return {
            'sku': '2165147',
            'seller_id': 'epoca',
            'type': META_TYPE_PRODUCT_FACTSHEET_SCORE,
            'value': '16'
        }

    @pytest.fixture
    def product_score_image_data(self):
        return {
            'sku': '2165147',
            'seller_id': 'epoca',
            'type': META_TYPE_PRODUCT_IMAGE_SCORE,
            'value': '16'
        }

    def test_should_record_product_score_factsheet_data(
        self, processor, database,
        product_score_factsheet_data
    ):
        processor.save(product_score_factsheet_data)
        saved_data = database.find_one({
            'sku': product_score_factsheet_data['sku'],
            'seller_id': product_score_factsheet_data['seller_id']
        })
        assert META_TYPE_PRODUCT_FACTSHEET_SCORE == saved_data['type']
        assert (
            product_score_factsheet_data['value'] == saved_data['value']
        )

    def test_should_persist_both_types_behavior_data_to_same_sku(
        self, processor, database,
        product_score_factsheet_data,
        product_score_image_data
    ):
        processor.save(product_score_factsheet_data)
        processor.save(product_score_image_data)

        cursor = database.find(
            {'sku': product_score_factsheet_data['sku']}
        )
        assert cursor.count() == 2
        assert cursor[0]['type'] != cursor[1]['type']
        assert (
            cursor[0]['type'] == META_TYPE_PRODUCT_FACTSHEET_SCORE or
            cursor[0]['type'] == META_TYPE_PRODUCT_IMAGE_SCORE
        )
        assert (
            cursor[1]['type'] == META_TYPE_PRODUCT_FACTSHEET_SCORE or
            cursor[1]['type'] == META_TYPE_PRODUCT_IMAGE_SCORE
        )

    def test_should_delete_products_scores_data_by_type(
        self, database, processor,
        product_score_factsheet_data,
        product_score_image_data
    ):
        criteria = {
            'sku': product_score_factsheet_data['sku'],
            'seller_id': product_score_factsheet_data['seller_id'],
            'type': product_score_factsheet_data['type']
        }
        data = {
            'type': product_score_factsheet_data['type'],
            'value': product_score_factsheet_data['value']
        }
        database.update(criteria, {'$set': data}, upsert=True)

        criteria = {
            'sku': product_score_image_data['sku'],
            'seller_id': product_score_image_data['seller_id'],
            'type': product_score_image_data['type']
        }
        data = {
            'type': product_score_image_data['type'],
            'value': product_score_image_data['value']
        }
        database.update(criteria, {'$set': data}, upsert=True)

        cursor = database.find(
            {'sku': product_score_factsheet_data['sku']}
        )
        assert cursor.count() == 2

        processor.delete(product_score_factsheet_data)

        cursor = database.find(criteria)
        assert cursor.count() == 1
        assert cursor[0]['type'] == META_TYPE_PRODUCT_IMAGE_SCORE
