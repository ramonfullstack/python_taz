import pytest

from taz.consumers.core.reviews import Reviews


class TestReviews:

    @pytest.fixture
    def reviews(self):
        return Reviews()

    @pytest.fixture
    def product(self):
        return {
            'sku': '213445900',
            'seller_id': 'magazineluiza',
            'type': 'product',
            'navigation_id': '213445900'
        }

    @pytest.fixture
    def rating_dict(self, mongo_database):
        price = {
            'product_id': '213445900',
            'type': 'product_average_rating',
            'value': 4.3
        }

        mongo_database.customer_behaviors.save(price)

    @pytest.fixture
    def review_dict(self, mongo_database):
        price = {
            'product_id': '213445900',
            'type': 'product_total_review_count',
            'value': 83
        }

        mongo_database.customer_behaviors.save(price)

    def test_should_return_product_reviews(self, product, review_dict, reviews): # noqa
        result = reviews.get_customer_behavior(
            product['navigation_id'],
            'product_total_review_count'
        )
        assert result == 83

    def test_should_return_product_rating(self, product, rating_dict, reviews):
        result = reviews.get_customer_behavior(
            product['navigation_id'], 'product_average_rating'
        )
        assert result == 4.3

    def test_should_return_zero_product_review_if_not_found(
        self,
        reviews,
        product,
        rating_dict
    ):
        product['navigation_id'] = '12345678'

        result = reviews.get_customer_behavior(
            product['navigation_id'],
            'product_average_rating'
        )
        assert result == 0

    def test_should_return_zero_product_rating_if_not_found(
        self,
        reviews,
        product,
        rating_dict
    ):
        product['navigation_id'] = '12345678'

        result = reviews.get_customer_behavior(
            product['navigation_id'],
            'product_average_rating'
        )
        assert result == 0.0
