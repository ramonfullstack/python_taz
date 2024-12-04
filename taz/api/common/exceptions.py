import json

import falcon


class HttpError(Exception):
    status = falcon.HTTP_500
    code = 500
    message = 'Internal server error'

    def __init__(self, code=None, message=None):
        if code:
            self.code = code

        if message:
            self.message = message

    @staticmethod
    def handler(exception, request, response, error=None):
        response.status = exception.status
        response.body = json.dumps({'error_message': exception.message})


class BadRequest(HttpError):
    status = falcon.HTTP_400
    code = 400
    message = 'Bad request'


class BadRequestWithMessage(HttpError):
    status = falcon.HTTP_400
    code = 400

    def __init__(self, message='Bad request'):
        super().__init__(message=message)


class Unauthorized(HttpError):
    status = falcon.HTTP_401
    code = 401
    message = 'Unauthorized'


class NotFound(HttpError):
    status = falcon.HTTP_404
    code = 404
    message = 'Not Found'


class NotFoundWithMessage(HttpError):
    status = falcon.HTTP_404
    code = 404

    def __init__(self, message='Not Found'):
        super().__init__(message=message)


class BadgeNotFound(NotFound):

    def __init__(self, *args, **kwargs):
        message = 'Badge {} not found'.format(
            kwargs.pop('slug') or ''
        )
        kwargs['message'] = message
        super().__init__(*args, **kwargs)


class Conflict(HttpError):
    status = falcon.HTTP_409
    code = 409
    message = 'Conflict'


class MethodNotAllowed(HttpError):
    status = falcon.HTTP_405
    code = 405
    message = 'Method not allowed'


class ForbiddenTermsNotFound(NotFound):
    def __init__(self, *args, **kwargs):
        message = kwargs.get('message')
        if not message:
            kwargs['message'] = 'Forbidden terms key is empty'
        super().__init__(*args, **kwargs)
