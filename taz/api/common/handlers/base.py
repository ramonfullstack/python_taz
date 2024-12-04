import json

import falcon

from taz.api.common.json import custom_json_encoder


class BaseHandler(falcon.Response):

    id_fields = ('_id',)

    def _clean_ids(self, content):
        if isinstance(content, list):
            [self._clean_ids(i) for i in content]
            return

        if not isinstance(content, dict):
            return

        for key in list(content.keys()):
            if key in self.id_fields:
                del content[key]
            else:
                self._clean_ids(content[key])

    def write_response(self, response, status_code, content=None):

        if isinstance(content, (dict, list)):
            self._clean_ids(content)
            content = json.dumps(content, default=custom_json_encoder)

        content_type = 'application/json' if content else None

        response.status = status_code
        response.body = content

        if content_type:
            response.content_type = content_type
