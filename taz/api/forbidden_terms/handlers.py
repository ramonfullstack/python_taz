import falcon

from taz.api.common.exceptions import (
    BadRequest,
    ForbiddenTermsNotFound,
    HttpError
)
from taz.api.common.handlers.base import BaseHandler
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.core.forbidden_terms.forbidden_terms import ForbiddenTerms


class ForbiddenTermsHandler(BaseHandler, MongodbMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__forbidden_terms = None

    @property
    def forbidden_terms(self):
        if self.__forbidden_terms is None:
            self.__forbidden_terms = self.get_collection('forbidden_terms')
        return self.__forbidden_terms

    def on_get(self, request, response):
        query_string = falcon.uri.parse_query_string(request.query_string)
        sku = query_string.get('sku')
        seller_id = query_string.get('seller_id')

        if not sku or not seller_id:
            raise BadRequest(message='sku and seller_id is required')

        forbidden_terms = self.forbidden_terms.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0}
        )

        if not forbidden_terms:
            raise ForbiddenTermsNotFound(
                message='Not found forbidden terms'
            )

        self.write_response(
            response=response,
            status_code=falcon.HTTP_200,
            content=forbidden_terms
        )


class ForbiddenTermsRedisHandler(BaseHandler, MongodbMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__forbidden_terms = None

    @property
    def forbidden_terms(self):
        if self.__forbidden_terms is None:
            self.__forbidden_terms = ForbiddenTerms()
        return self.__forbidden_terms

    def on_post(self, request, response):
        data = request.context
        self.forbidden_terms.save_redis_terms(data)
        self.write_response(response, falcon.HTTP_201)

    def on_get(self, request, response):
        result = self.forbidden_terms.get_redis_terms()
        self.write_response(
            response=response,
            status_code=falcon.HTTP_200,
            content=result
        )

    def on_delete(self, request, response):
        data = request.context
        success, keys_not_found = self.forbidden_terms.delete_redis_terms(data)

        if not keys_not_found:
            if success:
                return self.write_response(
                    response=response,
                    status_code=falcon.HTTP_204
                )

            raise HttpError(
                message='Redis key forbidden_terms not exist'
            )

        if len(data) == len(keys_not_found):
            raise ForbiddenTermsNotFound(
                message='All keys not found to delete'
            )

        self.write_response(
            response=response,
            status_code=falcon.HTTP_200,
            content={'message': f'keys not found to delete:{keys_not_found}'}
        )
