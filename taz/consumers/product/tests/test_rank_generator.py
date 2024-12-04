import pytest

from taz import constants
from taz.consumers.product.rank_generator import RankGenerator


class TestRankGenerator:

    @pytest.fixture
    def rank_generator(self):
        return RankGenerator()

    @pytest.mark.parametrize('product,expected_grade', [
        ({'seller_id': 'magazineluiza', 'sku': '123'}, 1000),
        ({'seller_id': 'abc', 'sku': '123', 'title': 'a' * 70}, 10),
        ({'seller_id': 'abc', 'sku': '321', 'ean': '123456789'}, 0),
        ({'seller_id': 'abc', 'sku': '432', 'ean': '7897712096055'}, 10),
        ({'seller_id': 'abc', 'sku': '231', 'ean': '17896110005697'}, 10),
        ({'seller_id': 'abc', 'sku': '323', 'ean': '0'}, 0),
        ({'seller_id': 'abc', 'sku': '122', 'ean': ''}, 0),
        ({'seller_id': 'abc', 'sku': '111', 'ean': 'xablau'}, 0),
    ])
    def test_grade_computation(
        self,
        rank_generator,
        product,
        expected_grade
    ):
        product_grade = rank_generator.compute_grade(product)
        assert product_grade == expected_grade

    def test_grade_computation_for_duplicated_eans(
        self,
        rank_generator,
        mongo_database
    ):
        product = {
            'seller_id': constants.MAGAZINE_LUIZA_SELLER_ID,
            'sku': '123abc',
            'ean': '7897712096055'
        }

        first_grade = rank_generator.compute_grade(product)
        assert first_grade == 1010

        mongo_database.raw_products.insert(product)

        second_grade = rank_generator.compute_grade(product)
        assert second_grade == 10
