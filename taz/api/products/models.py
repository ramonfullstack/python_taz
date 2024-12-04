import json
import logging

from mongoengine import DynamicDocument, StringField

from taz.api.common.exceptions import HttpError, NotFound
from taz.api.products.constants import GET_PRODUCT_ERROR, PRODUCT_NOT_FOUND
from taz.utils import convert_id_to_nine_digits, cut_product_id

logger = logging.getLogger(__name__)


class RawProductModel(DynamicDocument):
    meta = {
        'collection': 'raw_products',
        'shard_key': ('sku', 'seller_id',)
    }

    @classmethod
    def get_product(cls, seller_id, sku):
        try:
            payload = RawProductModel.objects(
                seller_id=seller_id, sku=sku
            ).first()

            if not payload:
                logger.debug(
                    'Product sku:{sku} seller:{seller_id} '
                    'not found'.format(
                        sku=sku,
                        seller_id=seller_id
                    )
                )
                raise NotFound(message=PRODUCT_NOT_FOUND)

            return json.loads(payload.to_json())
        except NotFound:
            raise
        except Exception:
            logger.exception(
                'Error for product sku:{sku} seller:{seller_id} '
                'information'.format(
                    sku=sku,
                    seller_id=seller_id
                )
            )
            raise HttpError(message=GET_PRODUCT_ERROR)

    @classmethod
    def get_sellers(cls):
        payload = RawProductModel.objects().distinct('seller_id')

        return payload

    @classmethod
    def get_sellers_by_strategy(cls, strategy):
        payload = RawProductModel.objects(
            matching_strategy=strategy
        ).distinct('seller_id')

        return payload

    @classmethod
    def product_list_by_strategy_and_seller(cls, strategy, seller_id):
        payload = RawProductModel.objects(
            matching_strategy=strategy,
            seller_id=seller_id,
            disable_on_matching=False
        )

        return json.loads(payload.to_json())

    @classmethod
    def get_product_by_navigation_id(cls, navigation_id):
        try:
            payload = RawProductModel.objects(
                navigation_id=navigation_id
            ).first()

            if not payload:
                logger.debug(
                    'Product navigation_id:{} not found'.format(navigation_id)
                )

                raise NotFound(message=PRODUCT_NOT_FOUND)

            return json.loads(payload.to_json())
        except NotFound:
            raise
        except Exception:
            logger.exception(
                'Error for product navigation_id:{} information'.format(
                    navigation_id
                )
            )
            raise HttpError(message=GET_PRODUCT_ERROR)

    @classmethod
    def get(cls, **kwargs):
        try:
            payload = cls.objects(**kwargs)
            if not payload:
                raise NotFound(message=PRODUCT_NOT_FOUND)
        except NotFound:
            logger.warning(
                'Could not found product with:{data}'.format(
                    data=kwargs
                )
            )
            raise
        except Exception:
            logger.exception(
                'Could not get product with:{data}'.format(
                    data=kwargs
                )
            )
            raise NotFound(PRODUCT_NOT_FOUND)

        return json.loads(payload.to_json())


class UnpublishProductModel(DynamicDocument):
    meta = {
        'collection': 'unpublished_products',
        'shard_key': ('navigation_id',)
    }

    @classmethod
    def get(cls, navigation_id):
        try:
            payload = UnpublishProductModel.objects(
                navigation_id=navigation_id
            ).first()

            if not payload:
                logger.warning(
                    'Unpublished Product navigation_id:{} not found'.format(
                        navigation_id
                    )
                )
                raise NotFound(message=PRODUCT_NOT_FOUND)

            return json.loads(payload.to_json())
        except NotFound:
            raise
        except Exception as e:
            logger.exception(
                'Error getting product navigation_id:{nav_id} '
                'error: {error}'.format(
                    nav_id=navigation_id,
                    error=e
                )
            )
            raise HttpError(message=GET_PRODUCT_ERROR)

    @classmethod
    def list(cls, navigation_id=None):
        if navigation_id:
            query = {
                '$or': [{
                    'navigation_id': convert_id_to_nine_digits(navigation_id)
                }, {
                    'navigation_id': cut_product_id(navigation_id)
                }]
            }
            payload = UnpublishProductModel.objects(
                __raw__=query
            ).order_by('-updated_at')
        else:
            payload = UnpublishProductModel.objects()

        if not payload:
            raise NotFound(message='Products not found')

        return json.loads(payload.to_json())


class CustomProductAttributesModel(DynamicDocument):
    meta = {
        'collection': 'custom_attributes',
        'shard_key': ('sku', 'seller_id',)
    }

    sku = StringField(max_length=200, required=True)
    seller_id = StringField(max_length=200, required=True)
    short_title = StringField(max_length=32, required=True)
    short_description = StringField(max_length=50, required=True)

    @classmethod
    def get(cls, sku, seller_id):
        custom_attributes = CustomProductAttributesModel.objects(
            sku=sku, seller_id=seller_id
        ).first()

        if custom_attributes:
            return {
                'seller_id': seller_id,
                'sku': sku,
                'short_title': custom_attributes.short_title,
                'short_description': custom_attributes.short_description
            }
