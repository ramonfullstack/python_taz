import pytest
from marshmallow import ValidationError

from taz.api.products.schema import ListProductsSchema, ProductExtraDataSchema


class TestListProductsSchema:

    @pytest.fixture
    def mock_schema(self):
        return ListProductsSchema()

    @pytest.fixture
    def mock_identifier(self):
        return {
            'identifier_type': 'ean',
            'identifier_value': '7891112250536',
        }

    @pytest.fixture
    def mock_matching_uuid(self):
        return {
            'matching_uuid': 'a0069aee16d441cab4030cce086debbc'
        }

    @pytest.fixture
    def mock_query_params(self):
        return {
            'fields': [
                'title',
                'matching_uuid',
                'datasheet_uuid',
                'ean',
                'isbn'
            ],
            '_limit': 10,
            '_offset': 0
        }

    def test_when_load_params_with_identifier_then_return_success(
        self,
        mock_schema,
        mock_query_params,
        mock_identifier
    ):
        mock_query_params.update(mock_identifier)
        params = mock_schema.load(mock_query_params)
        assert params == mock_query_params

    def test_when_load_params_with_matching_uuid_then_return_success(
        self,
        mock_schema,
        mock_query_params,
        mock_matching_uuid
    ):
        mock_query_params.update(mock_matching_uuid)
        params = mock_schema.load(mock_query_params)
        assert params == mock_query_params

    def test_when_validate_params_without_query_string_valid_then_raise_exception( # noqa
        self,
        mock_schema,
        mock_query_params
    ):
        with pytest.raises(ValidationError) as error:
            mock_schema.validate(mock_query_params)
        assert 'Request without a valid query string' in error.value.messages[0] # noqa

    def test_when_validate_invalid_identifier_then_raise_exception(
        self,
        mock_schema,
        mock_query_params,
        mock_identifier
    ):
        with pytest.raises(ValidationError) as error:
            mock_identifier['identifier_type'] = 'other'
            mock_query_params.update(mock_identifier)
            mock_schema.validate(mock_query_params)

        assert 'Type of identifier invalid:other' in error.value.messages[0]


class TestProductExtraDataSchema:

    def test_when_load_data_with_extra_data_then_should_return_with_success(
        self,
        mock_extra_data
    ):
        data = ProductExtraDataSchema().load(mock_extra_data)
        assert data == mock_extra_data

    @pytest.mark.parametrize(
        'field_to_delete', [
            'seller_id',
            'sku',
            'extra_data'
        ]
    )
    def test_when_required_field_not_exists_then_should_raise_exception(
        self,
        mock_extra_data,
        field_to_delete
    ):
        del mock_extra_data[field_to_delete]

        with pytest.raises(ValidationError):
            ProductExtraDataSchema().load(mock_extra_data)
