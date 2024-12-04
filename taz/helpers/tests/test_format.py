from taz.helpers.format import generate_sku_seller_id_key


class TestFormat:

    def test_when_call_generate_key_then_return_key_with_sku_seller_id_success(
        self
    ):
        result = generate_sku_seller_id_key('123456789', 'magazineluiza')
        assert result == '123456789-magazineluiza'
