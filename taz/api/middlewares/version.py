from taz.api.version import __version__


class VersionMiddleware:

    def process_response(self, request, response, resource, req_succeeded):
        response.set_header('version', __version__)
