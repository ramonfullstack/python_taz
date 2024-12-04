from copy import deepcopy

from taz import constants
from taz.api.badges.helpers import (
    BadgeProductCache,
    BadgeProductQueue,
    validate,
    validate_product_list
)


class TestBadgeValidateHelper:

    def test_validate_badges_returns_true(self, badge_dict):
        status = validate(badge_dict)
        assert status

    def test_validate_badges_returns_false(self):
        status = validate({})
        assert not status

    def test_validate_badges_missing_image_url_returns_false(self, badge_dict):
        del badge_dict['image_url']
        status = validate(badge_dict)
        assert not status

    def test_validate_product_list_found_product(self, badge_dict):
        products_list = badge_dict['products']
        main_product = badge_dict['products'][0]
        result = validate_product_list(main_product, products_list)
        assert result is True

    def test_validate_product_list_not_found_product(self, badge_dict):
        products_list = badge_dict['products']
        main_product = deepcopy(badge_dict['products'][0])
        main_product['sku'] = 'mock_diff_sku'

        result = validate_product_list(main_product, products_list)
        assert result is False


class TestBadgeProductCache:

    def test_remove(self, patch_redis, badge_dict, logger_stream):
        product = badge_dict['products'][0]

        with patch_redis as mock:
            BadgeProductCache().remove(product)

        assert mock.call_args[0][0] == constants.BADGE_CACHE_KEY.format(
            sku=product['sku'],
            seller_id=product['seller_id'],
        )
        assert (
            'Removed cache from product badge '
            'sku:{sku} seller:{seller} successfully.'.format(
                sku=product['sku'],
                seller=product['seller_id'],
            )
        ) in logger_stream.getvalue()


class TestBadgeProductQueue:

    def test_send_update(
        self, patch_publish_manager, badge_dict, logger_stream
    ):
        product = badge_dict['products'][0]

        with patch_publish_manager as mock:
            BadgeProductQueue().send_update(product)

        call_args = mock.call_args_list[0][1]['content']
        assert call_args['sku'] == product['sku']
        assert call_args['seller_id'] == product['seller_id']
        assert call_args['origin'] == 'taz.api.badges.helpers'
        assert call_args['action'] == constants.UPDATE_ACTION
        assert call_args['force']
        assert (
            'Notifying the product sku:{sku} seller:{seller_id} '
            'action:{action} in the product writer queue through '
            'badge product API'.format(
                sku=product['sku'],
                seller_id=product['seller_id'],
                action=constants.UPDATE_ACTION
            )
        ) in logger_stream.getvalue()
