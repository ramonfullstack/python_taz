from unittest.mock import call, patch

import pytest
from boto import kinesis
from simple_settings.utils import settings_stub

from taz.pollers.core.brokers.exceptions import MissingPollerSettingException
from taz.pollers.core.brokers.stream import KinesisBroker


class TestKinesisBroker:

    @pytest.fixture
    def patch_kinesis_connection(self):
        return patch.object(kinesis, 'connect_to_region')

    @pytest.fixture
    def fake_poller_stream(self):
        return {
            'fake': {
                'stream_name': 'fake_stream',
                'aws_settings': {
                    'region': 'br-hue-1'
                }
            }
        }

    @pytest.fixture
    def patch_process_record(self):
        return patch.object(KinesisBroker, '_process_record')

    def test_instantiation_sets_up_connection_with_kinesis(
        self,
        patch_kinesis_connection,
        fake_poller_stream
    ):
        with patch_kinesis_connection as kinesis_connection:
            with settings_stub(
                POLLERS=fake_poller_stream,
                AWS_ACCESS_KEY_ID='xablau',
                AWS_SECRET_ACCESS_KEY='auAUau'
            ):
                fake_broker = KinesisBroker('fake')

        assert fake_broker.stream_name == 'fake_stream'
        assert fake_broker.region == 'br-hue-1'

        kinesis_connection.assert_called_with(
            region_name='br-hue-1',
            aws_access_key_id='xablau',
            aws_secret_access_key='auAUau'
        )

    def test_instantiation_with_missing_settings_raises_exception(self):
        with pytest.raises(MissingPollerSettingException):
            KinesisBroker('invalid')

    def test_put_many_records_should_called(
        self,
        patch_kinesis_connection,
        fake_poller_stream,
        caplog
    ):
        with patch_kinesis_connection:
            with settings_stub(
                POLLERS=fake_poller_stream,
                AWS_ACCESS_KEY_ID='xablau',
                AWS_SECRET_ACCESS_KEY='auAUau'
            ):
                fake_broker = KinesisBroker('fake')
                fake_broker.put_many('delete', ['010009400'])

        assert 'Sent to scope:fake with action:delete' in caplog.text # noqa

    @pytest.mark.parametrize('action,dataset,calls', [
        (
            'update',
            ['99999'],
            [
                call('d3eb9a9233e52948740d7eb8c3062d14', 'update', '99999')
            ]
        ),
        (
            'delete',
            ['00000', '11111'],
            [
                call('dcddb75469b4b4875094e14561e573d8', 'delete', '00000'),
                call('b0baee9d279d34fa1dfd71aadb908c3f', 'delete', '11111')
            ]
        )
    ])
    def test_put_many_records_stream_should_different_partition_keys(
        self,
        patch_kinesis_connection,
        patch_process_record,
        fake_poller_stream,
        action,
        dataset,
        calls
    ):
        with patch_kinesis_connection:
            with settings_stub(
                POLLERS=fake_poller_stream,
                AWS_ACCESS_KEY_ID='xablau',
                AWS_SECRET_ACCESS_KEY='auAUau'
            ):
                with patch_process_record as mock_process_record:
                    fake_broker = KinesisBroker('fake')
                    fake_broker.put_many(action, dataset)

                    assert mock_process_record.call_args_list == calls
