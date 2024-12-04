import logging
import time

logger = logging.getLogger(__name__)

ROUTES_TO_IGNORE = ('/healthcheck', '/monitor',)


class AccessLogMiddleware:
    start = None

    def clear_token_in_url(self, url):
        start_token = url.find('token')
        if start_token > 0:
            end_token = str.find(url, '&', start_token)
            return (
                url[:start_token].rstrip('&')
                if end_token == -1
                else url[:start_token] + url[end_token + 1:]
            )
        return url

    def process_request(self, request, response):
        self.start = time.time()

    def process_response(self, request, response, resource, req_succeeded):
        if request.relative_uri in ROUTES_TO_IGNORE:
            return

        relative_uri = self.clear_token_in_url(request.relative_uri)
        logger.info(
            '{request_method} to {request_relative_uri} '
            'by {request_token_owner} took {time_spent}s '
            'with {response_status}'.format(
                request_method=request.method,
                request_relative_uri=relative_uri,
                request_token_owner=request.token_owner,
                response_status=response.status,
                time_spent='{0:.3f}'.format(time.time() - self.start)
            )
        )
