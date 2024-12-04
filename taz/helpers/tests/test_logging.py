import io
import logging

from taz.helpers.logging import IgnoreIfContains


def test_ignore_if_contains():
    logger = logging.getLogger('test_logger')
    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)

    filter_substrings = ['/healthcheck/', '/monitor/', '/ping/']
    ignore_filter = IgnoreIfContains(filter_substrings)
    stream_handler.addFilter(ignore_filter)

    formatter = logging.Formatter('%(levelname)s: %(message)s')
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    test_messages = [
        "This is a test message.",
        "Checking /healthcheck/ status.",
        "Monitoring the system.",
        "Ping response received.",
        "This message should pass through."
    ]

    def capture_logs():
        log_capture = io.StringIO()
        stream_handler.setStream(log_capture)
        return log_capture

    log_capture = capture_logs()

    for message in test_messages:
        logger.info(message)

    log_contents = log_capture.getvalue()
    log_capture.close()

    expected_output = [
        "INFO: This is a test message.",
        "INFO: This message should pass through."
    ]

    for expected_message in expected_output:
        assert expected_message in log_contents, (
            f"Expected '{expected_message}' in logs, but it was not found."
        )
