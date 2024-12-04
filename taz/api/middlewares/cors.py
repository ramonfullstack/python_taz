class CORSMiddleware:
    def __init__(
        self,
        allow_origins='*',
        expose_headers=None,
        allow_credentials=None
    ):
        if allow_origins == '*':
            self.allow_origins = allow_origins
        else:
            if isinstance(allow_origins, str):
                allow_origins = [allow_origins]
            self.allow_origins = frozenset(allow_origins)

        if expose_headers is not None and not isinstance(expose_headers, str):
            expose_headers = ', '.join(expose_headers)
        self.expose_headers = expose_headers

        if allow_credentials is None:
            allow_credentials = frozenset()
        elif allow_credentials != '*':
            if isinstance(allow_credentials, str):
                allow_credentials = [allow_credentials]
            allow_credentials = frozenset(allow_credentials)
        self.allow_credentials = allow_credentials

    def process_response(self, req, resp, resource, req_succeeded):
        origin = req.get_header('Origin')
        if self.allow_origins != '*' and origin not in self.allow_origins:
            return

        if resp.get_header('Access-Control-Allow-Origin') is None:
            set_origin = '*' if self.allow_origins == '*' else origin
            if (
                self.allow_credentials == '*' or
                origin in self.allow_credentials
            ):
                set_origin = origin
                resp.set_header('Access-Control-Allow-Credentials', 'true')
            resp.set_header('Access-Control-Allow-Origin', set_origin)

        if self.expose_headers:
            resp.set_header(
                'Access-Control-Expose-Headers',
                self.expose_headers
            )

        if (
            req_succeeded and
            req.method == 'OPTIONS' and
            req.get_header('Access-Control-Request-Method')
        ):
            allow = resp.get_header('Allow')
            resp.delete_header('Allow')

            allow_headers = req.get_header(
                'Access-Control-Request-Headers', default='*'
            )

            if allow:
                resp.set_header('Access-Control-Allow-Methods', allow)
            resp.set_header('Access-Control-Allow-Headers', allow_headers)
            resp.set_header('Access-Control-Max-Age', '86400')
