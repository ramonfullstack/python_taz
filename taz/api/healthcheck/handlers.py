import socket

import falcon

from taz.api.common.handlers.base import BaseHandler
from taz.api.version import __version__


class HealthcheckHandler(BaseHandler):
    def on_get(self, request, response):
        services = {
            'status': 'OK',
            'version': __version__,
            'host': socket.gethostname()
        }

        self.write_response(response, falcon.HTTP_200, services)
