import logging

import falcon
from slugify import slugify

from taz.api.badges.models import BadgeModel
from taz.api.common.exceptions import BadgeNotFound, BadRequest
from taz.api.common.handlers.base import BaseHandler

from .helpers import (
    BadgeProductCache,
    BadgeProductQueue,
    create_interval_payload,
    create_payload,
    validate,
    validate_product_list
)

logger = logging.getLogger(__name__)


class BadgeListHandler(BaseHandler):
    def on_get(self, request, response):
        show_all = request.get_param('show_all') or False

        payload = BadgeModel.list(show_all=show_all)
        badges = [create_interval_payload(badge) for badge in payload]

        self.write_response(response, falcon.HTTP_200, badges)


class BadgePaginatedListHandler(BaseHandler):
    def on_get(self, request, response):
        query_string = falcon.uri.parse_query_string(request.query_string)
        page_number = query_string.get('page_number', 1)
        offset = query_string.get('offset', 10)

        payload = BadgeModel.paginate(page_number=page_number, offset=offset)
        payload['records'] = (
            [
                create_interval_payload(badge)
                for badge in payload.get('records')
            ]
        )

        self.write_response(response, falcon.HTTP_200, payload)


class BadgeHandler(BaseHandler):
    def on_get(self, request, response, slug):
        payload = BadgeModel.get(slug)

        if not payload:
            raise BadgeNotFound(slug=slug)

        badge = create_interval_payload(payload)

        self.write_response(response, falcon.HTTP_200, badge)

    def on_post(self, request, response):
        if not validate(request.context):
            raise BadRequest(
                'Invalid parameters for payload:{}'.format(request.context)
            )

        badge = request.context
        badge['slug'] = slugify(badge['name'])

        payload = BadgeModel.objects(slug=badge['slug']).first()
        if payload:
            raise BadRequest('Badge slug {} already exists'.format(
                badge['slug']
            ))

        BadgeModel(**badge).save()
        self.write_response(response, falcon.HTTP_201)

    def on_put(self, request, response):
        if not validate(request.context):
            raise BadRequest(
                'Invalid parameters for payload:{}'.format(request.context)
            )

        data = request.context

        payload = BadgeModel.objects(slug=data['slug']).first()
        if not payload:
            raise BadgeNotFound(slug=data['slug'])

        badge = create_payload(payload, data)

        BadgeModel.objects(slug=data['slug']).update_one(**badge)

        self.write_response(response, falcon.HTTP_200)

    def on_delete(self, request, response, slug):
        payload = BadgeModel.get(slug)
        if not payload:
            raise BadgeNotFound(slug=slug)

        BadgeModel.objects(slug=slug).delete()

        self.write_response(response, falcon.HTTP_204)


class BadgeProductItemHandler(BaseHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.badge_product_cache = BadgeProductCache()
        self.badge_product_queue = BadgeProductQueue()

    def on_delete(self, request, response, slug, sku, seller_id):
        payload = BadgeModel.objects(slug=slug).first()
        if not payload:
            raise BadgeNotFound(slug=slug)

        products = payload['products'].copy()
        for product in products:
            if (
                product['sku'] == sku and
                product['seller_id'] == seller_id
            ):
                payload['products'].remove(product)
                self.badge_product_cache.remove(product)
                self.badge_product_queue.send_update(product)

        payload.save()
        self.write_response(response, falcon.HTTP_204)


class BadgeProductListItemHandler(BaseHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.badge_product_cache = BadgeProductCache()
        self.badge_product_queue = BadgeProductQueue()

    def on_delete(self, request, response, slug):
        payload = BadgeModel.objects(slug=slug).first()
        if not payload:
            raise BadgeNotFound(slug=slug)

        data = request.context
        products = payload['products'].copy()
        for product in products:
            if validate_product_list(product, data):
                payload['products'].remove(product)
                self.badge_product_cache.remove(product)
                self.badge_product_queue.send_update(product)

        payload.save()
        self.write_response(response, falcon.HTTP_204)
