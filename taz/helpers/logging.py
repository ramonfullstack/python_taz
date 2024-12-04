import logging
import logging.config
import socket

from simple_settings import settings


def setup_logging():
    logging.captureWarnings(True)
    logging.config.dictConfig(settings.LOGGING)


class GetHostName(logging.Filter):  # pragma: no cover
    hostname = socket.gethostname()

    def filter(self, record):
        record.hostname = self.hostname
        return True


class IgnoreIfContains(logging.Filter):
    def __init__(self, substrings=None):
        self.substrings = substrings or []

    def filter(self, record):
        message = record.getMessage()
        return not any(
            substrings in message
            for substrings in self.substrings
        )
