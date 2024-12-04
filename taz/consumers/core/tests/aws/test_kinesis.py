import pytest
from simple_settings import settings

from taz.consumers.core.aws.kinesis import KinesisManager


class TestKinesisManager:

    @pytest.fixture
    def kinesis_manager(self):
        return KinesisManager(settings.INDEXING_PROCESS_STREAM_NAME)

    def test_send_payload_to_kinesis(self, kinesis_manager, patch_kinesis_put):
        with patch_kinesis_put as mock:
            kinesis_manager.put('create', {})

        assert mock.called
