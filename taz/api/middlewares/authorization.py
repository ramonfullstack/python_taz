import logging

import falcon
from google.auth.transport import requests
from google.oauth2 import id_token
from mongoengine.queryset import DoesNotExist
from simple_settings import settings

from taz.api.common.exceptions import Unauthorized
from taz.api.models.token import TokenModel

ROUTES_TO_IGNORE = ('/healthcheck', '/monitor', '/metrics', '/docs', '/static')

logger = logging.getLogger(__name__)


class AuthorizationMiddleware:

    def process_request(self, request, response):
        request.token_owner = 'Unknown (Unknown)'

        if (
            request.path.startswith(ROUTES_TO_IGNORE) or
            request.method == 'OPTIONS'
        ):
            return

        received_token = self._get_token_from_request(request)
        if not received_token:
            raise Unauthorized(message='Invalid token')

        if len(received_token) > settings.TOKEN_LENGTH:
            token = self._validate_jwt(received_token)
        else:
            token = self._get_token(received_token)
            if not token:
                raise Unauthorized(message='Invalid token')
        request.token_owner = token.owner

    def _get_token_from_request(self, request):
        token = request.get_header('Authorization')

        if (
            token and (
                token.lower().startswith('token') or
                token.lower().startswith('bearer')
            )
        ):
            _, token = token.split()
        elif 'token' in request.query_string:
            query_string = falcon.uri.parse_query_string(request.query_string)
            token = query_string['token']
        return token

    def _get_token(self, token):
        try:
            return TokenModel.objects.get(token=token)
        except DoesNotExist:
            return

    def _validate_jwt(self, token: str):
        try:
            claims = id_token.verify_oauth2_token(token, requests.Request())
        except Exception as e:
            logger.exception('Failed request with error:{}'.format(e))
            raise Unauthorized(message='Request raised exception')

        if (
            not claims.get('email_verified') or
            claims.get('email') not in settings.EMAIL_SERVICE_ACCOUNT
        ):
            raise Unauthorized('Error to validate token')
        return TokenModel(owner='gcp', token=token)
