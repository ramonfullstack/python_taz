import pytest

from taz.consumers.update_category import SCOPE
from taz.consumers.update_category.consumer import UpdateCategoryProcessor
from taz.helpers.test_utils import mock_response


class TestUpdateCategoryConsumer:

    @pytest.fixture
    def consumer(self):
        return UpdateCategoryProcessor(scope=SCOPE)

    @pytest.fixture
    def message(self, product_dict):
        return {
            'sku': product_dict['sku'],
            'seller_id': product_dict['seller_id']
        }

    def test_should_discarting_message_from_other_sellers(self, consumer):
        message = {
            'sku': '1223456789',
            'seller_id': 'murcho'
        }

        status = consumer.process_message(message)
        assert status

    def test_should_skip_message_with_not_found_product(
        self,
        consumer,
        message
    ):
        status = consumer.process_message(message)
        assert status

    def test_should_update_category_from_product(
        self,
        consumer,
        product_dict,
        patch_requests_get,
        patch_requests_put,
        mongo_database,
        save_product,
        message
    ):
        with patch_requests_get as mock_get:
            mock_get.return_value = mock_response(json_data={
                'code': product_dict['sku'][:7],
                'category_id': 'TE',
                'subcategory_id': 'PANL',
                'title': product_dict['title'],
                'reference': product_dict['reference'],
                'brand': product_dict['brand'],
                'active': True
            })

            with patch_requests_put as mock_put:
                status = consumer.process_message(message)

        assert status
        assert mock_get.called
        assert mock_put.called

        category_history = mongo_database.category_history.find_one()

        assert category_history['sku'] == product_dict['sku']
        assert category_history['seller_id'] == product_dict['seller_id']
        assert category_history['category_id'] == 'UD'
        assert category_history['subcategory_id'] == 'PANL'
        assert category_history['original'] == {
            'category_id': 'TE',
            'subcategory_id': 'PANL'
        }

    def test_should_do_not_put_when_categories_are_equal(
        self,
        consumer,
        patch_requests_get,
        product_dict,
        patch_requests_put,
        save_product,
        message
    ):
        with patch_requests_get as mock_get:
            mock_get.return_value = mock_response(json_data={
                'code': product_dict['sku'][:7],
                'category_id': 'UD',
                'subcategory_id': 'PANL',
                'title': product_dict['title'],
                'reference': product_dict['reference'],
                'brand': product_dict['brand'],
                'active': True
            })

            with patch_requests_put as mock_put:
                status = consumer.process_message(message)

        assert status
        assert mock_get.called
        assert not mock_put.called
