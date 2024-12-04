import logging
import re
from io import StringIO

import pytest

from taz.api.middlewares.access_log import AccessLogMiddleware


class Fake:
    def __init__(self, headers=None, relative_uri='/foo', query_string=''):
        self.method = 'GET'
        self.token_owner = 'Unknown'
        self.headers = headers or {}
        self.relative_uri = relative_uri
        self.query_string = query_string
        self.status = '200 OK'


class TestAccessLog:

    @pytest.fixture
    def access_log(self):
        return AccessLogMiddleware()

    @pytest.fixture
    def fake(self):
        return Fake()

    def test_middleware_logs_request_info(self, access_log, fake):

        stream = StringIO()
        handler = logging.StreamHandler(stream)

        logger = logging.getLogger('taz.api.middlewares.access_log')
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

        access_log.process_request(fake, fake)
        access_log.process_response(fake, fake, fake, fake)

        log = stream.getvalue()
        logger.removeHandler(handler)

        assert log
        assert bool(re.match(
            '^GET to /foo by Unknown took [0-9]+.[0-9]+s with 200 OK$', log
        ))

    def test_middleware_logs_route_ignores(self, access_log):

        fake = Fake(relative_uri='/healthcheck')

        stream = StringIO()
        handler = logging.StreamHandler(stream)

        logger = logging.getLogger('taz.api.middlewares.access_log')
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

        access_log.process_request(fake, fake)
        access_log.process_response(fake, fake, fake, fake)

        log = stream.getvalue()
        logger.removeHandler(handler)

        assert log == ''

    @pytest.mark.parametrize('uri,expected', [
        ('/url', '/url'),
        ('/url?token=fake-token', '/url?'),
        ('/url?token=fake-token&navigation_id=1', '/url?navigation_id=1'),
        ('/url?navigation_id=1&token=fake-token', '/url?navigation_id=1')
    ])
    def test_clear_token_in_url(self, access_log, uri, expected):
        assert access_log.clear_token_in_url(uri) == expected
