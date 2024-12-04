import base64
import json
import logging
import zlib
from io import StringIO
from unittest.mock import patch

import pytest
from botocore.exceptions import ClientError
from simple_settings import settings
from simple_settings.utils import settings_stub

from taz.consumers.core.brokers.stream import (
    BotoKinesisBroker,
    BotoKinesisRecordProcessor
)

CLIENT_ERROR_MSG = 'Encountered client error'
GENERIC_ERROR_MSG = 'Encountered generic error'
methods_actions = [
    ('create', 'create'),
    ('update', 'update'),
    ('delete', 'remove')
]


class FakeBotoRecordProcessorWithDefaultAndCreateRequiredFields(
    BotoKinesisRecordProcessor
):
    required_fields = ['murcho']
    required_fields_create = ['desmanchador']


class FakeBotoRecordProcessorWithRequiredNonEmptyFields(
    BotoKinesisRecordProcessor
):
    required_non_empty_fields = ['murcho']
    required_non_empty_fields_create = ['desmanchador']


class FakeBotoRecordProcessorWithOnlyDefaultRequiredFields(
    BotoKinesisRecordProcessor
):
    required_fields = ['murcho']


class FakeBotoRecordProcessorWithRequiredFields(
    BotoKinesisRecordProcessor
):
    required_fields_create = ['murcho']
    required_fields_update = required_fields_create
    required_fields_delete = required_fields_create


class TestBotoKinesisRecordProcessor:

    @pytest.fixture
    def record_processor(self):
        return BotoKinesisRecordProcessor('test')

    @pytest.fixture
    def record_processor_with_required_fields(self):
        return FakeBotoRecordProcessorWithRequiredFields('test')

    @pytest.fixture
    def record_processor_with_only_default_required_fields(self):
        return FakeBotoRecordProcessorWithOnlyDefaultRequiredFields('test')

    @pytest.fixture
    def record_processor_with_default_and_create_required_fields(self):
        return FakeBotoRecordProcessorWithDefaultAndCreateRequiredFields(
            'test'
        )

    @pytest.fixture
    def record_processor_with_required_non_empty_fields(self):
        return FakeBotoRecordProcessorWithRequiredNonEmptyFields('test')

    def get_data_dict(self, action):
        return {
            'Data': json.dumps({
                'data': {'foo': 'murcho'},
                'action': action
            }).encode()
        }

    def get_data_compress_dict(self, action):
        payload = json.dumps({
            'data': {'foo': 'murcho'},
            'action': action
        })

        payload = zlib.compress(payload.encode())

        return {'Data': payload}

    @pytest.mark.parametrize('method,action', methods_actions)
    def test_process_record_call_create_with_decoded_data(
        self, record_processor, method, action
    ):
        expected_dict = {'foo': 'murcho'}
        with patch.object(record_processor, method) as mock:
            record_processor.process_record(
                record=self.get_data_dict(action),
                shard_id='fake_shard_id'
            )

        mock.assert_called_with(expected_dict)

    @settings_stub(ENABLE_KINESIS_COMPRESS=True)
    @pytest.mark.parametrize('method,action', methods_actions)
    def test_process_record_call_json_data_with_enable_kinesis_compress(
        self, record_processor, method, action
    ):
        expected_dict = {'foo': 'murcho'}
        with patch.object(record_processor, method) as mock:
            record_processor.process_record(
                record=self.get_data_dict(action),
                shard_id='fake_shard_id'
            )

        mock.assert_called_with(expected_dict)

    @settings_stub(ENABLE_KINESIS_COMPRESS=True)
    @pytest.mark.parametrize('method,action', methods_actions)
    def test_process_record_call_create_with_decoded_compress_data(
        self, record_processor, method, action
    ):
        expected_dict = {'foo': 'murcho'}
        with patch.object(record_processor, method) as mock:
            record_processor.process_record(
                record=self.get_data_compress_dict(action),
                shard_id='fake_shard_id'
            )

        mock.assert_called_with(expected_dict)

    @pytest.mark.parametrize('method,action', methods_actions)
    def test_process_record_dont_call_process_method_without_data(
        self, record_processor, method, action
    ):
        with patch.object(record_processor, method) as mock:
            record_processor.process_record(
                record={'data': base64.b64encode(
                    json.dumps({'action': action}).encode()
                )},
                shard_id='fake_shard_id'
            )

        assert not mock.called

    @pytest.mark.parametrize('method', [m for m, _ in methods_actions])
    def test_process_record_dont_call_process_method_without_action(
        self, record_processor, method
    ):
        with patch.object(record_processor, method) as mock:
            data = {
                'data': base64.b64encode(json.dumps({
                    'data': {'foo': 'murcho'}
                }).encode())
            }
            record_processor.process_record(
                record=data,
                shard_id='fake_shard_id'
            )
        assert not mock.called

    @pytest.mark.parametrize('method,action', methods_actions)
    def test_validate_required_fields_validations(
        self, record_processor_with_required_fields, method, action
    ):
        private_method_name = '_{}'.format(method)
        with patch.object(
            record_processor_with_required_fields,
            private_method_name
        ) as mock:
            record_processor_with_required_fields.process_record(
                record=self.get_data_dict(action),
                shard_id='fake_shard_id'
            )
        assert not mock.called

    @pytest.mark.parametrize('method,action', methods_actions)
    def test_validate_default_required_fields_validations(
        self, record_processor_with_only_default_required_fields,
        method, action
    ):
        private_method_name = '_{}'.format(method)
        with patch.object(
            record_processor_with_only_default_required_fields,
            private_method_name
        ) as mock:
            record_processor_with_only_default_required_fields.process_record(
                record=self.get_data_dict(action),
                shard_id='fake_shard_id'
            )
        assert not mock.called

    @pytest.mark.parametrize('action, invalid_data', [
        ('create', {'murcho': 'foo'}),
        ('update', {'foo': 'bar'})
    ])
    def test_validate_default_and_specific_required_fields_validations(
        self, record_processor_with_default_and_create_required_fields,
        action, invalid_data
    ):
        rp = record_processor_with_default_and_create_required_fields
        private_method_name = '_{}'.format(action)
        with patch.object(rp, private_method_name) as mock:
            data = {
                'data': base64.b64encode(json.dumps({
                    'data': invalid_data,
                    'action': action
                }).encode())
            }
            rp.process_record(
                record=data,
                shard_id='fake_shard_id'
            )
        assert not mock.called

    @pytest.mark.parametrize('action, invalid_data', [
        ('create', {'desmanchador': []}),
        ('update', {'murcho': None})
    ])
    def test_validate_default_and_specific_required_non_empty_fields_validations(  # noqa
        self, record_processor_with_required_non_empty_fields,
        action, invalid_data
    ):
        rp = record_processor_with_required_non_empty_fields
        private_method_name = '_{}'.format(action)
        with patch.object(rp, private_method_name) as mock:
            data = {
                'data': base64.b64encode(json.dumps({
                    'data': invalid_data,
                    'action': action
                }).encode())
            }
            rp.process_record(
                record=data,
                shard_id='fake_shard_id'
            )
        assert not mock.called

    @pytest.mark.parametrize('method,action', methods_actions)
    def test_process_record_called_and_logged_with_scope_timestamp_and_status(
        self, record_processor, method, action
    ):
        stream = StringIO()
        handler = logging.StreamHandler(stream)

        logger = logging.getLogger('taz.consumers.core.brokers.stream')
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

        expected_dict = {'foo': 'murcho'}
        with patch.object(record_processor, method) as mock:
            record_processor.process_record(
                record=self.get_data_dict(action),
                shard_id='fake_shard_id'
            )
        mock.assert_called_with(expected_dict)

        log = stream.getvalue()
        logger.removeHandler(handler)

        assert log

    @pytest.mark.parametrize('method,action', methods_actions)
    def test_should_validate_required_field(
        self, record_processor_with_required_fields, method, action
    ):
        with patch.object(
                record_processor_with_required_fields, '_' + method
        ) as mock:
            record_processor_with_required_fields.process_record(
                record=self.get_data_dict(action)
            )
        assert not mock.called


class FakeBotoKinesisBroker(BotoKinesisBroker):
    record_processor_class = FakeBotoRecordProcessorWithRequiredFields
    scope = 'fake'
    app_name = scope
    chunk_size = settings.KINESIS_CHUNK_SIZE
    fetch_interval = 0
    error_retry_interval = 0
    max_process_workers = int(settings.PROCESSOR_MAX_THREAD_WORKERS)


class MockCache:

    def _verify_shard_lock(self, *args, **kwargs):
        return False

    def get(self, *args, **kwargs):
        return True


class TestBotoKinesisBroker:

    @pytest.fixture
    def kinesis_broker(self):
        return FakeBotoKinesisBroker()

    @pytest.fixture(scope='session')
    def mock_process_records(self):
        return patch.object(FakeBotoKinesisBroker, '_process_records')

    @pytest.fixture(scope='session')
    def mock_verify_shard_lock(self):
        return patch.object(FakeBotoKinesisBroker, '_verify_shard_lock')

    def test_run_processor_success(
        self,
        kinesis_broker,
        logger_stream,
        mock_process_records,
        mock_verify_shard_lock
    ):
        with mock_process_records as mock_process_records:
            with mock_verify_shard_lock as mock_shard_lock:
                mock_shard_lock.return_value = False
                mock_process_records.return_value = True

                kinesis_broker._cache = MockCache()
                kinesis_broker.run_processor({'ShardId': 'mock_test'})
                log = logger_stream.getvalue()

                assert CLIENT_ERROR_MSG not in log
                assert GENERIC_ERROR_MSG not in log

    def test_run_processor_raise_client_exception(
        self,
        kinesis_broker,
        logger_stream,
        mock_process_records,
        mock_verify_shard_lock
    ):
        with mock_process_records as mock_process_records:
            with mock_verify_shard_lock as mock_shard_lock:
                mock_shard_lock.return_value = False
                mock_process_records.side_effect = ClientError(
                    {'Error': {'Code': '500', 'Message': 'Mocked Error'}},
                    'MockedError'
                )

                kinesis_broker._cache = MockCache()
                kinesis_broker.run_processor({'ShardId': 'mock_test'})
                log = logger_stream.getvalue()

                assert CLIENT_ERROR_MSG in log
                assert GENERIC_ERROR_MSG not in log

    def test_run_processor_raise_generic_exception(
        self,
        kinesis_broker,
        logger_stream,
        mock_process_records,
        mock_verify_shard_lock
    ):
        with mock_process_records as mock_process_records:
            with mock_verify_shard_lock as mock_shard_lock:
                mock_shard_lock.return_value = False
                mock_process_records.side_effect = Exception

                kinesis_broker._cache = MockCache()
                kinesis_broker.run_processor({'ShardId': 'mock_test'})
                log = logger_stream.getvalue()

                assert CLIENT_ERROR_MSG not in log
                assert GENERIC_ERROR_MSG in log

    def test_should_return_none_getting_last_sequence_number_when_not_value(
        self, kinesis_broker
    ):

        kinesis_broker._cache.set(
            'taz_kinesis_fake_shard_id_fake_last_sequence', bytes(0)
        )
        assert (
            kinesis_broker._get_last_sequence_number('fake_shard_id') is None
        )

    def test_should_generate_key_lock_using_shard_id(self, kinesis_broker):
        lock_key = kinesis_broker._generate_lock_key('fake_shard_id')
        assert lock_key == 'taz_kinesis_fake_shard_id_fake_lock'

    def test_should_generate_key_using_shard_id(self, kinesis_broker):
        lock_key = kinesis_broker._generate_key('fake_shard_id')
        assert lock_key == 'taz_kinesis_fake_shard_id_fake_last_sequence'

    def test_should_lock_shard(self, kinesis_broker):
        kinesis_broker._lock_shard('fake_shard_id')
        key = kinesis_broker._generate_lock_key('fake_shard_id')
        assert kinesis_broker._cache.get(key)

    def test_should_unlock_shard(self, kinesis_broker):
        kinesis_broker._lock_shard('fake_shard_id')
        key = kinesis_broker._generate_lock_key('fake_shard_id')

        assert kinesis_broker._cache.get(key)

        kinesis_broker._unlock_shard('fake_shard_id')

        assert not kinesis_broker._cache.get(key)

    def test_should_return_none_when_shard_is_not_locked(self, kinesis_broker):
        is_locked = kinesis_broker._verify_shard_lock('fake_shard_id')

        assert not is_locked

    def test_should_return_true_when_shard_is_locked(self, kinesis_broker):
        kinesis_broker._lock_shard('fake_shard_id')
        is_locked = kinesis_broker._verify_shard_lock('fake_shard_id')

        assert is_locked
