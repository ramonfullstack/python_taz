
import falcon
from prometheus_client import CONTENT_TYPE_LATEST, REGISTRY, generate_latest


class MetricsHandler:
    def on_get(self, request, response):
        response.status = falcon.HTTP_200
        response.set_header('Content-Type', CONTENT_TYPE_LATEST)
        response.body = generate_latest(REGISTRY)
