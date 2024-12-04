import json

from taz.api.common.exceptions import BadRequest, HttpError


class JsonTranslator:

    def process_request(self, request, response):
        if request.content_length in (None, 0):
            return

        body = request.stream.read()
        if not body:
            raise BadRequest('A valid JSON document is required.')

        try:
            request.context = json.loads(body.decode('utf-8'))
        except ValueError:
            raise HttpError(
                'Could not decode the request body. The JSON was '
                'incorrect or not encoded as UTF-8.'
            )
