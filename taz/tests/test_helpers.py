from taz.tests.helpers import product_score


class TestHelper:

    def test_product_score_should_returns_ok(self):
        payload = product_score(active=True, sku='123')

        assert payload['active'] is True
        assert payload['sku'] == '123'
