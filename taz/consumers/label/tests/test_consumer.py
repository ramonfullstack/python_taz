from unittest.mock import Mock, call, patch

import pytest
from marshmallow.exceptions import ValidationError
from pymongo.database import Database

from taz.constants import UPDATE_ACTION
from taz.consumers.label.consumer import LabelMessageSchema, LabelProcessor


class TestLabelConsumer:

    @pytest.fixture
    def mock_output_label_payload(
        self,
        mock_input_label_payload: dict
    ) -> dict:
        mock_input_label_payload.update({'in_out': 'out'})
        return mock_input_label_payload

    @pytest.fixture
    def mock_extra_data_label(self):
        return [{'name': 'is_magalu_indica', 'value': 'true'}]

    @pytest.fixture
    def processor(self):
        return LabelProcessor('labels')

    def test_when_include_label_then_save_on_raw_products(
        self,
        mongo_database: Database,
        mock_raw_products_payload: dict,
        mock_input_label_payload: dict,
        processor: LabelProcessor,
        patch_notification_put: patch,
        mock_extra_data_label: dict
    ):
        mongo_database.raw_products.insert_one(mock_raw_products_payload)
        with patch_notification_put as mock_notification_put:
            success = processor.process_message(mock_input_label_payload)

        updated_product = mongo_database.raw_products.find_one({
            'seller_id': mock_raw_products_payload['seller_id'],
            'sku': mock_raw_products_payload['sku']
        })

        assert success
        assert mock_notification_put.call_args == call(
            {
                'sku': mock_raw_products_payload['sku'],
                'seller_id': mock_raw_products_payload['seller_id'],
                'navigation_id': mock_raw_products_payload['navigation_id']
            },
            'product',
            UPDATE_ACTION
        )
        assert updated_product['extra_data'] == mock_extra_data_label
        assert updated_product['md5'] == mock_raw_products_payload['md5']

    def test_when_remove_label_then_save_on_raw_products(
        self,
        mongo_database: Database,
        mock_raw_products_payload: dict,
        mock_output_label_payload: dict,
        processor: LabelProcessor,
        patch_notification_put: patch,
        mock_extra_data_label: dict
    ):
        mock_raw_products_payload.update({'extra_data': mock_extra_data_label})
        mongo_database.raw_products.insert_one(mock_raw_products_payload)
        with patch_notification_put as mock_notification_put:
            success = processor.process_message(mock_output_label_payload)

        updated_product = mongo_database.raw_products.find_one({
            'seller_id': mock_raw_products_payload['seller_id'],
            'sku': mock_raw_products_payload['sku']
        })

        assert success
        assert mock_notification_put.call_args == call(
            {
                'sku': mock_raw_products_payload['sku'],
                'seller_id': mock_raw_products_payload['seller_id'],
                'navigation_id': mock_raw_products_payload['navigation_id']
            },
            'product',
            UPDATE_ACTION
        )
        assert 'extra_data' not in updated_product
        assert updated_product['md5'] == mock_raw_products_payload['md5']

    @pytest.mark.parametrize('in_out', [('in'), ('out')])
    def test_when_label_of_product_3p_then_skip_label_message(
        self,
        in_out: str,
        mock_input_label_payload: dict,
        processor: LabelProcessor,
        patch_notification_put: patch
    ):
        mock_input_label_payload.update(
            {'seller_id': 'fake', 'in_out': in_out}
        )
        with patch_notification_put as mock_notification_put:
            success = processor.process_message(mock_input_label_payload)

        assert success
        assert not mock_notification_put.called

    def test_when_product_not_found_then_skip_label_message(
        self,
        mock_input_label_payload: dict,
        processor: LabelProcessor,
        patch_notification_put: patch,
        patch_mongo_collection: patch,
    ):
        with patch_notification_put as mock_notification_put:
            with patch_mongo_collection as mock_collection:
                mock_find_one = Mock()
                mock_collection.return_value = mock_find_one
                mock_find_one.find_one.return_value = None
                success = processor.process_message(mock_input_label_payload)

        assert success
        assert not mock_notification_put.called

    def test_when_product_has_extra_data_and_include_label_then_merge_extra_data(  # noqa
        self,
        mongo_database: Database,
        mock_raw_products_payload: dict,
        mock_input_label_payload: dict,
        processor: LabelProcessor,
        patch_notification_put: patch,
        mock_extra_data: dict,
        mock_extra_data_label: dict
    ):
        del mock_extra_data['extra_data'][1]

        mock_raw_products_payload.update(
            {
                'extra_data': mock_extra_data['extra_data']
            }
        )
        mongo_database.raw_products.insert_one(mock_raw_products_payload)

        with patch_notification_put as mock_notification_put:
            success = processor.process_message(mock_input_label_payload)

        assert success
        assert mock_notification_put.call_args == call(
            {
                'sku': mock_raw_products_payload['sku'],
                'seller_id': mock_raw_products_payload['seller_id'],
                'navigation_id': mock_raw_products_payload['navigation_id']
            },
            'product',
            UPDATE_ACTION
        )

        assert mongo_database.raw_products.find_one({
            'seller_id': mock_raw_products_payload['seller_id'],
            'sku': mock_raw_products_payload['sku']
        })['extra_data'] == mock_extra_data['extra_data'] + mock_extra_data_label  # noqa

    def test_when_product_has_extra_data_and_remove_label_then_merge_extra_data(   # noqa
        self,
        mongo_database: Database,
        mock_raw_products_payload: dict,
        mock_output_label_payload: dict,
        processor: LabelProcessor,
        patch_notification_put: patch,
        mock_extra_data: dict
    ):
        mock_raw_products_payload.update(
            {'extra_data': mock_extra_data['extra_data']}
        )
        mongo_database.raw_products.insert_one(mock_raw_products_payload)
        with patch_notification_put as mock_notification_put:
            success = processor.process_message(mock_output_label_payload)

        assert success
        assert mock_notification_put.call_args == call(
            {
                'sku': mock_raw_products_payload['sku'],
                'seller_id': mock_raw_products_payload['seller_id'],
                'navigation_id': mock_raw_products_payload['navigation_id']
            },
            'product',
            UPDATE_ACTION
        )

        del mock_extra_data['extra_data'][1]

        assert mongo_database.raw_products.find_one({
            'seller_id': mock_raw_products_payload['seller_id'],
            'sku': mock_raw_products_payload['sku']
        })['extra_data'] == mock_extra_data['extra_data']

    def test_when_product_has_label_then_skip_inclusion(
        self,
        mongo_database: Database,
        mock_raw_products_payload: dict,
        mock_input_label_payload: dict,
        processor: LabelProcessor,
        patch_notification_put: patch,
        mock_extra_data_label: dict
    ):
        mock_raw_products_payload.update({'extra_data': mock_extra_data_label})
        mongo_database.raw_products.insert_one(mock_raw_products_payload)
        with patch_notification_put as mock_notification_put:
            success = processor.process_message(mock_input_label_payload)

        updated_product = mongo_database.raw_products.find_one({
            'seller_id': mock_raw_products_payload['seller_id'],
            'sku': mock_raw_products_payload['sku']
        })

        assert success
        assert not mock_notification_put.called
        assert updated_product['extra_data'] == mock_extra_data_label

    def test_when_product_without_label_then_skip_removal(
        self,
        mongo_database: Database,
        mock_raw_products_payload: dict,
        mock_output_label_payload: dict,
        processor: LabelProcessor,
        patch_notification_put: patch
    ):
        mock_raw_products_payload.pop('extra_data', None)
        mongo_database.raw_products.insert_one(mock_raw_products_payload)
        with patch_notification_put as mock_notification_put:
            success = processor.process_message(mock_output_label_payload)

        updated_product = mongo_database.raw_products.find_one({
            'seller_id': mock_raw_products_payload['seller_id'],
            'sku': mock_raw_products_payload['sku']
        })

        assert success
        assert not mock_notification_put.called
        assert 'extra_data' not in updated_product

    def test_when_invalid_label_message_then_return_true(
        self,
        mock_input_label_payload: dict,
        processor: LabelProcessor,
        patch_notification_put: patch,
        caplog
    ):
        mock_input_label_payload.pop('seller_id')
        with patch_notification_put as mock_notification_put:
            success = processor.process_message(mock_input_label_payload)

        assert success
        assert not mock_notification_put.called

        expected_error_message = f'Error to validate payload:{mock_input_label_payload}'  # noqa
        assert expected_error_message in caplog.text

    def test_when_not_found_product_using_seller_id_and_sku_then_find_using_navigation_id(  # noqa
        self,
        mongo_database: Database,
        mock_raw_products_payload: dict,
        processor: LabelProcessor
    ):
        seller_id, sku, navigation_id = (
            mock_raw_products_payload['seller_id'],
            mock_raw_products_payload['sku'],
            mock_raw_products_payload['navigation_id']
        )
        mock_raw_products_payload.update({'sku': '-1'})
        mongo_database.raw_products.insert_one(mock_raw_products_payload)
        assert processor._get_product(
            seller_id, sku, navigation_id
        ) is not None


class TestLabelMessageSchema:

    @pytest.fixture
    def schema(self):
        return LabelMessageSchema()

    def test_when_valid_message_then_return_none(
        self,
        schema: LabelMessageSchema,
        mock_input_label_payload: dict
    ):
        assert schema.validate(mock_input_label_payload) is None

    @pytest.mark.parametrize('field,value', [
        ('seller_id', ''),
        ('seller_id', ' '),
        ('sku', ''),
        ('sku', ' '),
        ('navigation_id', ''),
        ('navigation_id', ' '),
        ('label', ''),
        ('label', ' '),
        ('in_out', ''),
        ('in_out', ' '),
        ('rules_version', ''),
        ('rules_version', ' ')
    ])
    def test_when_field_is_empty_then_raise_exception(
        self,
        schema: LabelMessageSchema,
        mock_input_label_payload: dict,
        field: str,
        value: str
    ):
        mock_input_label_payload[field] = value
        with pytest.raises(ValidationError):
            schema.validate(mock_input_label_payload)

    @pytest.mark.parametrize('field', [
        ('seller_id'),
        ('sku'),
        ('navigation_id'),
        ('label'),
        ('in_out'),
        ('rules_version')
    ])
    def test_when_field_without_then_raise_exception(
        self,
        schema: LabelMessageSchema,
        mock_input_label_payload: dict,
        field: str
    ):
        mock_input_label_payload.pop(field)
        with pytest.raises(ValidationError):
            schema.validate(mock_input_label_payload)
