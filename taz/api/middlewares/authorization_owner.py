from taz.api.common.exceptions import MethodNotAllowed


class AuthOwner(object):

    def __init__(self, allowed_owners):
        self.allowed_owners = allowed_owners

    def __call__(self, method):
        def wrapper(handler_object, request, *args, **kwargs):
            if ('*' in self.allowed_owners or
                    request.token_owner in self.allowed_owners):
                return method(handler_object, request, *args, **kwargs)
            else:
                raise MethodNotAllowed(
                    message='Token not allowed for this method'
                )
        return wrapper
