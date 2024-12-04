from unittest.mock import patch

import pytest


@pytest.fixture
def patch_sqs_manager():
    return patch('taz.consumers.core.brokers.queue.SQSManager')
