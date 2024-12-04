
class TestBasePriceConverter:

    def test_pricing_converter_success(
            self,
            converter,
            database_row,
            expected_transformed_set,
    ):

        converter.from_source([database_row])

        assert len(converter.get_items()) > 0
        assert expected_transformed_set == converter.get_items()

    def test_pricing_converter_success_without_bundle(
            self,
            converter,
            database_row_without_bundle,
            expected_transformed_set_without_bundle,
    ):

        converter.from_source([database_row_without_bundle])

        assert len(converter.get_items()) > 0
        assert expected_transformed_set_without_bundle == converter.get_items()
