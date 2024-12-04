import logging
import time
from io import StringIO

from taz.constants import MessageStatus
from taz.consumers.core.brokers.base import log_processing_status


class TestLogProcessingStatus:

    def test_create_log_message(self):
        stream = StringIO()
        handler = logging.StreamHandler(stream)

        logger = logging.getLogger('taz.consumers.core.brokers.base')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)

        log_processing_status(
            logger.info,
            'murcho',
            MessageStatus.DELAYED,
            time.time(),
            time.time()
        )

        log = stream.getvalue()
        logger.removeHandler(handler)

        assert log
