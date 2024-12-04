import datetime
import json
import logging
import uuid
from distutils.util import strtobool
from functools import cached_property
from typing import Dict

import falcon
from marshmallow.exceptions import ValidationError as SchemaValidationError
from mongoengine.errors import ValidationError
from simple_settings import settings

from taz import constants
from taz.api.common.exceptions import BadRequest, NotFound
from taz.api.common.handlers.base import BaseHandler
from taz.api.common.pagination_adelpha import Pagination as PaginationOpenApi
from taz.api.medias.models import MediaModel
from taz.api.prices.models import PriceModel
from taz.api.products.helpers import (
    convert_validation_errors,
    create_converted_payload
)
from taz.api.products.models import (
    CustomProductAttributesModel,
    RawProductModel,
    UnpublishProductModel
)
from taz.api.products.schema import ListProductsSchema, ProductExtraDataSchema
from taz.api.utils import (
    convert_fields_to_list,
    format_fields_filtered,
    format_response_with_fields,
    validate_schema
)
from taz.constants import CREATE_ACTION, DELETE_ACTION, NIAGARA, TETRIX
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.google.stream import StreamPublisherManager
from taz.consumers.core.notification import Notification
from taz.consumers.datalake.publish_datalake_context import (
    KafkaTetrix,
    PublishDatalakeContext,
    PubsubNiagara
)
from taz.consumers.product_exporter.scopes.helpers import ScopeHelper
from taz.core.common.media import build_media
from taz.core.storage.raw_products_storage import RawProductsStorage
from taz.helpers.json import strip_decimals
from taz.utils import convert_id_to_nine_digits, cut_product_id, format_ean

logger = logging.getLogger(__name__)


class ListProductHandler(BaseHandler):
    def on_get(self, request, response):
        seller_id = request.get_param('seller')

        if seller_id:
            products = RawProductModel.objects(seller_id=seller_id)
        else:
            products = RawProductModel.objects

        payload = json.loads(products.to_json())
        self.write_response(response, falcon.HTTP_200, {'data': payload})


class ProductHandler(BaseHandler):
    def on_get(self, request, response, seller_id, sku):
        product = RawProductModel.get_product(seller_id, sku)
        price = PriceModel.get_price(seller_id, sku)
        medias = MediaModel.get_media(seller_id, sku, product)

        data = product
        data.update({'price': price, 'media': medias})

        self.write_response(response, falcon.HTTP_200, {'data': data})


class ProductNavigationIdHandler(BaseHandler):
    def on_get(self, request, response, navigation_id):
        product = RawProductModel.get_product_by_navigation_id(navigation_id)

        if not product:
            raise NotFound(
                'Product navigation_id:{} not found'.format(navigation_id)
            )

        sku = product['sku']
        seller_id = product['seller_id']

        price = PriceModel.get_price(seller_id, sku)
        medias = MediaModel.get_media(seller_id, sku, product)

        data = product
        data.update({'price': price, 'media': medias})

        self.write_response(response, falcon.HTTP_200, {'data': data})


class ProductStatHandler(BaseHandler):
    def on_get(self, request, response, seller_id):
        products = RawProductModel.objects(
            seller_id=seller_id
        ).count()

        if products <= 0:
            raise NotFound('Product from seller {} were not found'.format(
                seller_id
            ))

        active_products = RawProductModel.objects(
            seller_id=seller_id,
            disable_on_matching=False
        ).count()

        price_unavailable = PriceModel.objects(
            seller_id=seller_id, stock_count=0
        ).count()

        data = {
            'total_variations': products,
            'total_active_variations': active_products,
            'available_variations': products - price_unavailable,
            'unavailable_variations': price_unavailable
        }

        self.write_response(response, falcon.HTTP_200, {'data': data})


class ProductUnpublishHandler(BaseHandler, MongodbMixin):

    scope = 'unpublish'
    STREAMS = [NIAGARA, TETRIX]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._niagara = PublishDatalakeContext(PubsubNiagara())
        self._tetrix = PublishDatalakeContext(KafkaTetrix())
        self.__context_stream = {
            NIAGARA: self._niagara,
            TETRIX: self._tetrix
        }

    @cached_property
    def pubsub(self):
        return StreamPublisherManager()

    @cached_property
    def raw_products(self):
        return self.get_collection('raw_products')

    def on_delete(self, request, response):
        data = request.context

        logger.info(f'Unpublish delete received with data:{data}')

        now = datetime.datetime.utcnow()
        data.update({'updated_at': now})

        navigation_id = data.get('navigation_id')

        if not navigation_id:
            logger.warning(
                f'Error deleting unpublished product with data:{data} '
                'Data without navigation_id'
            )
            raise BadRequest('Invalid request')

        try:
            products = UnpublishProductModel.objects.filter(
                navigation_id=navigation_id
            )

            if not products:
                logger.warning(f'Product not found with payload {data}')
                raise NotFound(f'Product {navigation_id} not found')

            for product in products:
                product.delete()

                logger.debug(
                    f'Creating unpublished product with payload:{data}'
                )

                payload = json.loads(product.to_json())
                payload = create_converted_payload(payload)
                payload = strip_decimals(payload)
                payload['action'] = DELETE_ACTION
                del payload['_id']

                self._send_datalake(payload, navigation_id)

                logger.info(
                    f'Deleting unpublished product with payload:{data}'
                )
        except Exception as e:
            logger.warning(
                f'Error unpublished product with data:{data}, error:{e}'
            )
            raise

        self._send_product(navigation_id)
        self.write_response(response, falcon.HTTP_200)

    def on_post(self, request, response):
        data = request.context

        now = datetime.datetime.utcnow()
        data.update({'updated_at': now})

        logger.info(f'Unpublish received with data:{data}')

        navigation_id = data.get('navigation_id')
        if not navigation_id:
            logger.warning(
                f'Error unpublished product with data:{data}, '
                'Data without navigation_id'
            )
            return

        try:
            product = UnpublishProductModel.objects.get(
                navigation_id=navigation_id
            )
            product.update(**data)
            logger.debug(f'Updating unpublished product with payload:{data}')

        except UnpublishProductModel.DoesNotExist:
            logger.warning(f'Product not found with payload {data}')
            data.update({'created_at': now})
            UnpublishProductModel(**data).save()
        except Exception as e:
            logger.warning(
                f'Error unpublishing product with data:{data} error:{e}'
            )
            raise

        self._send_product(navigation_id)

        logger.debug(
            f'Creating unpublished product with payload:{data}'
        )

        payload = strip_decimals(data)
        payload['action'] = CREATE_ACTION

        self._send_datalake(payload, navigation_id)

        self.write_response(response, falcon.HTTP_200)

    def on_get(self, request, response):
        try:
            navigation_id = request.params.get('navigation_id')
            products = UnpublishProductModel.list(navigation_id)
            products = [
                create_converted_payload(product) for product in products
            ]
        except Exception:
            products = []
            logger.debug('Unpublish products not found')

        self.write_response(response, falcon.HTTP_200, {'products': products})

    def _send_product(self, navigation_id: str):
        product = self.raw_products.find_one(
            {
                '$or': [
                    {'navigation_id': convert_id_to_nine_digits(
                        navigation_id
                    )},
                    {'navigation_id': cut_product_id(navigation_id)}
                ]
            },
            {'_id': 0, 'sku': 1, 'seller_id': 1}
        )

        if not product:
            logger.warning(
                f'Product {navigation_id} not found in raw products.'
            )
            return

        attributes = {
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'action': 'update',
        }
        criteria = {
            **attributes,
            'task_id': uuid.uuid4().hex,
            'force': True
        }
        self.pubsub.publish(
            content=criteria,
            attributes=attributes,
            topic_name=settings.PUBSUB_MATCHING_PRODUCT_TOPIC_NAME,
            project_id=settings.GOOGLE_PROJECT_ID
        )

    def _send_datalake(self, payload: Dict, navigation_id: str):
        for stream in self.STREAMS:
            stream_config = settings.DATALAKE[self.scope].get(stream)
            if stream_config and stream_config['enabled']:
                context_stream = self.__context_stream.get(stream)
                data = context_stream.format_payload(
                    message=payload,
                    scope_name=self.scope
                )
                context_stream.send_message(data, stream_config)

                logger.info(
                    f'Successfully sent navigation_id:{navigation_id} '
                    f'with scope {self.scope} to Datalake '
                    f'stream:{stream}'
                )


class CustomProductAttributes(BaseHandler):

    @cached_property
    def pubsub(self):
        return StreamPublisherManager()

    def on_get(self, request, response, seller_id, sku):
        custom_attributes = CustomProductAttributesModel.get(
            sku, seller_id
        )

        self.write_response(
            response,
            falcon.HTTP_200 if custom_attributes else falcon.HTTP_404,
            custom_attributes
        )

    def on_post(self, request, response, seller_id, sku):
        payload = request.context

        custom_attributes = CustomProductAttributesModel.objects(
            sku=sku, seller_id=seller_id
        ).first()

        payload.update({
            'seller_id': seller_id,
            'sku': sku
        })

        try:
            if custom_attributes:
                custom_attributes.update(**payload)
            else:
                CustomProductAttributesModel(**payload).save()

            self._send_product(seller_id, sku)
            self.write_response(response, falcon.HTTP_200, payload)

        except ValidationError as err:
            self.write_response(response, falcon.HTTP_400, {
                'error': 400,
                'message': 'Validation Error',
                'detail': convert_validation_errors(err)
            })

    def on_delete(self, request, response, seller_id, sku):
        custom_attributes = CustomProductAttributesModel.objects(
            sku=sku, seller_id=seller_id
        ).first()

        if not custom_attributes:
            return self.write_response(response, falcon.HTTP_404)

        custom_attributes.delete()
        self._send_product(seller_id, sku)
        self.write_response(response, falcon.HTTP_200)

    def _send_product(self, seller_id, sku):
        payload = {
            'seller_id': seller_id,
            'sku': sku,
            'action': 'update',
            'task_id': self._new_uuid(),
            'force': True
        }
        self.pubsub.publish(
            content=payload,
            topic_name=settings.PUBSUB_PRODUCT_WRITER_TOPIC_NAME,
            project_id=settings.GOOGLE_PROJECT_ID
        )

    @staticmethod
    def _new_uuid():
        return uuid.uuid4().hex


class ProductEanBaseHandler(BaseHandler):
    def _create_payload(self, product, medias):
        full_title = product.title
        if product.reference:
            full_title += ' - {}'.format(product.reference)

        images = []
        for image in medias.get('images') or []:
            images.append('{domain}{path}'.format(
                domain=settings.ACME_MEDIA_DOMAIN,
                path=image
            ))

        return {
            'title': full_title,
            'brand': product.brand if hasattr(product, 'brand') else '',
            'description': product.description if hasattr(product, 'description') else '',  # noqa
            'dimensions': product.dimensions if hasattr(product, 'dimensions') else {},  # noqa
            'images': images,
            'ean': product.ean if hasattr(product, 'ean') else '',
            'attributes': product.attributes if hasattr(product, 'attributes') else []  # noqa
        }


class ProductEanHandler(ProductEanBaseHandler):
    def on_get(self, request, response, ean):
        products = RawProductModel.objects(ean=format_ean(ean))

        payload = []
        for product in products:
            medias = MediaModel.get_media(
                product.seller_id,
                product.sku,
                product
            )

            if product.seller_id == constants.MAGAZINE_LUIZA_SELLER_ID:
                payload = [self._create_payload(product, medias)]
                break

            payload.append(self._create_payload(product, medias))

        self.write_response(response, falcon.HTTP_200, {'data': payload})


class TrustedProductEanHandler(ProductEanBaseHandler):
    def on_get(self, request, response, ean):
        payload = []
        products = RawProductModel.objects(
            ean=format_ean(ean),
            seller_id__in=settings.TRUSTED_SELLERS
        )

        trusted_product = None
        for product in sorted(products, key=lambda p: p['created_at']):
            if product['seller_id'] in constants.MAGAZINE_LUIZA_SELLER_ID:
                trusted_product = product
                break
            else:
                trusted_product = product

        if trusted_product:
            medias = MediaModel.get_media(
                product.seller_id,
                product.sku,
                product
            )
            payload = [self._create_payload(product, medias)]

        self.write_response(response, falcon.HTTP_200, {'data': payload})


class ProductVariationHandler(BaseHandler):

    def on_get(self, request, response, parent_sku, seller_id):
        payload = RawProductModel.get(
            parent_sku=parent_sku,
            seller_id=seller_id
        )

        self.write_response(response, falcon.HTTP_200, {'data': payload})


class RawProductBySkuSellerHandler(BaseHandler):

    def __init__(self):
        super().__init__()
        self.__raw_products_storage = RawProductsStorage()

    def on_get(self, request, response, seller_id, sku):

        raw_product = self.__raw_products_storage.get_bucket_data(
            sku=sku,
            seller_id=seller_id
        )

        if not raw_product:
            raise NotFound(
                f'Product sku:{sku} seller_id:{seller_id} '
                'not found in raw products storage'
            )

        self.write_response(
            response,
            falcon.HTTP_200,
            {'data': raw_product}
        )


class RawProductByNavigationHandler(BaseHandler):

    def __init__(self):
        super().__init__()
        self.__raw_products_storage = RawProductsStorage()

    def on_get(self, request, response, navigation_id):
        product = RawProductModel.get_product_by_navigation_id(navigation_id)

        if not product:
            raise NotFound(
                'Navigation id {} not found in raw products'.format(
                    navigation_id
                )
            )

        sku = product['sku']
        seller_id = product['seller_id']

        raw_product = self.__raw_products_storage.get_bucket_data(
            sku=sku,
            seller_id=seller_id
        )

        if not raw_product:
            raise NotFound(
                f'Product sku:{sku} seller_id:{seller_id} '
                'not found in raw products storage'
            )

        self.write_response(
            response,
            falcon.HTTP_200,
            {'data': raw_product}
        )


class ListProductsHandler(BaseHandler, MongodbMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = ListProductsSchema()
        self.raw_products = self.get_collection('raw_products')
        self.medias = self.get_collection('medias')
        self.pagination = PaginationOpenApi(self.raw_products, '/v1/products')
        self.scope_helper = ScopeHelper()

    def on_get(self, request, response):
        query_string = falcon.uri.parse_query_string(request.query_string)
        parameters = self.__load_parameters(query_string)
        fields = parameters['fields']
        fields_to_request = (
            fields
            if not fields or 'media' not in fields
            else fields + ['sku', 'seller_id', 'title', 'reference']
        )

        if (
            'active' in fields_to_request and
            'disable_on_matching' not in fields_to_request
        ):
            fields_to_request.append('disable_on_matching')

        result = self.pagination.paginate(
            criteria=self.__format_criteria(parameters),
            fields=format_fields_filtered(
                fields_to_request
            ),
            offset=parameters['_offset'],
            limit=parameters['_limit']
        )

        if not fields or 'active' in fields:
            self._update_products_active(result['results'])

        if not fields or 'media' in fields:
            self.__get_products_medias(result['results'])

        self.write_response(
            response,
            falcon.HTTP_200,
            format_response_with_fields(fields, result) if fields else result
        )

    def _update_products_active(self, product_data):
        for product in product_data:
            active = not product.get('disable_on_matching', False)
            if active:
                unpublished = self.scope_helper.create_unavailable_product_payload( # noqa
                    product.get('navigation_id')
                )
                active = not bool(unpublished)
            product.update({'active': active})

        return product_data

    def __load_parameters(self, query_string):
        limit = int(query_string.get('_limit') or 10)
        offset = int(query_string.get('_offset') or 0)

        parameters = {
            'identifier_type': query_string.get('identifier.type'),
            'identifier_value': query_string.get('identifier.value'),
            'matching_uuid': query_string.get('matching_uuid'),
            'navigation_id': query_string.get('navigation_id'),
            'disable_on_matching': query_string.get('disable_on_matching'),
            'fields': convert_fields_to_list(query_string.get('fields')),
            '_limit': min(limit, 999),
            '_offset': max(offset, 0)
        }
        try:
            self.schema.validate(parameters)
            return self.schema.load(parameters)
        except SchemaValidationError as error:
            logger.error(
                'Error to validate request error:{error}'.format(
                    error=error
                )
            )
            raise BadRequest(message=error.messages)

    def __format_criteria(self, parameters):
        if parameters.get('identifier_type'):
            criteria = {
                parameters['identifier_type']: parameters['identifier_value']
            }
        elif parameters.get('matching_uuid'):
            criteria = {'matching_uuid': parameters['matching_uuid']}
        else:
            criteria = {'navigation_id': parameters['navigation_id']}

        if parameters.get('disable_on_matching') is not None:
            criteria.update(
                {'disable_on_matching': parameters['disable_on_matching']}
            )

        return criteria

    def __get_products_medias(self, products):
        if not products:
            return

        products_info = [
            {
                'sku': product.get('sku'),
                'seller_id': product.get('seller_id')
            }
            for product in products
        ]

        results_media = list(self.medias.find(
            {'$or': products_info},
            {'_id': 0}
        ))

        products_medias = {
            '{}:{}'.format(
                item.get('sku'),
                item.get('seller_id')
            ): item
            for item in results_media
        }

        for product in products:
            sku = product.get('sku')
            seller_id = product.get('seller_id')

            key_medias = '{}:{}'.format(sku, seller_id)
            product_media = products_medias.get(key_medias)

            if not product_media:
                product['media'] = {}
                continue

            product_media.pop('sku')
            product_media.pop('seller_id')

            self.__format_medias(product, product_media)

    def __format_medias(self, product, product_media):
        medias = {}
        for media_type in constants.MEDIA_TYPES:
            if media_type not in product_media:
                continue

            medias[media_type] = build_media(
                sku=product.get('sku'),
                title=product.get('title'),
                reference=product.get('reference'),
                seller_id=product.get('seller_id'),
                media_type=media_type,
                items=product_media[media_type]
            )

            if media_type == 'images':
                medias[media_type] = [
                    '{domain}{path}'.format(
                        domain=settings.ACME_MEDIA_DOMAIN,
                        path=image.format(
                            w=600,
                            h=400
                        )
                    ) for image in medias[media_type]
                ]

        product['media'] = medias


class ProductExtraDataHandler(BaseHandler, MongodbMixin):

    def __init__(self):
        super().__init__()
        self.__notification = Notification()

    @cached_property
    def raw_products(self):
        return self.get_collection('raw_products')

    def on_post(self, request, response):
        data = validate_schema(
            data=request.context,
            schema=ProductExtraDataSchema
        )

        criteria = {
            'sku': data['sku'],
            'seller_id': data['seller_id']
        }

        product = self.raw_products.find_one(
            criteria,
            {'navigation_id': 1, '_id': 0}
        )

        if not product:
            return self.write_response(
                response,
                falcon.HTTP_404,
                {'message': 'Product not exists'}
            )

        self.__save(data, criteria)

        self.__notify_sns(
            sku=criteria['sku'],
            seller_id=criteria['seller_id'],
            navigation_id=product['navigation_id']
        )

        self.write_response(
            response,
            falcon.HTTP_200
        )

    def __notify_sns(
        self,
        seller_id: str,
        sku: str,
        navigation_id: str
    ) -> None:
        payload = {
            'sku': sku,
            'seller_id': seller_id,
            'navigation_id': navigation_id
        }

        self.__notification.put(payload, 'product', constants.UPDATE_ACTION)

    def __save(self, data: Dict, criteria: Dict) -> None:
        fields_to_update = {'extra_data': data['extra_data']}

        for info in data['extra_data']:
            if info['name'] == 'fulfillment':
                fields_to_update.update(
                    {info['name']: bool(strtobool(info['value']))}
                )
                break

        self.raw_products.update_many(
            criteria,
            {'$set': fields_to_update}
        )
