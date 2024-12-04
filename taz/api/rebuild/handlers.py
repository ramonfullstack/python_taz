import datetime
import logging
from functools import cached_property

import falcon
import pytz
from marshmallow.exceptions import ValidationError
from redis import Redis
from simple_settings import settings

from taz import constants
from taz.api.common.exceptions import BadRequest, BadRequestWithMessage
from taz.api.common.handlers.base import BaseHandler
from taz.api.rebuild.schema import (
    CatalogNotificationSchema,
    RebuildDatalakeSchema,
    RebuildMediaSchema,
    RebuildProductExporterSchema,
    RebuilPriceRulesSchema
)
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.google.stream import StreamPublisherManager
from taz.consumers.core.notification import Notification

INVALID_PARAMETERS_MSG = 'Invalid parameters for payload:{}'
logger = logging.getLogger(__name__)


class BaseRebuildHandle(BaseHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pubsub_manager = StreamPublisherManager()

    def publish_rebuild(self, payload: dict = {}):
        self.pubsub_manager.publish(
            content=payload,
            topic_name=settings.PUBSUB_REBUILD_TOPIC_NAME,
            project_id=settings.GOOGLE_PROJECT_ID
        )


class RebuildLockHandle(BaseRebuildHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis = Redis(
            host=settings.REDIS_SETTINGS['host'],
            port=settings.REDIS_SETTINGS['port'],
            password=settings.REDIS_SETTINGS.get('password')
        )

    def _rebuild_lock(self, seller_id):
        expiration_timedelta = datetime.timedelta(
            hours=int(settings.REBUILD_LOCK_TIME_HOURS[self.scope])
        )
        self.redis.set(
            f'lock-rebuild-{self.scope}-{seller_id}',
            seller_id,
            expiration_timedelta
        )

    def _check_lock_time(self, seller_id):
        remaining_time = self.redis.ttl(
            f'lock-rebuild-{self.scope}-{seller_id}'
        )

        if remaining_time and remaining_time > 0:
            remaining_time_hours = datetime.timedelta(
                seconds=remaining_time
            )
            expires_at = remaining_time_hours + datetime.datetime.now(
                pytz.timezone('America/Sao_Paulo')
            )
            return expires_at.strftime('%d-%m-%Y %H:%M')
        return


class RebuildHandler(RebuildLockHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scope = 'catalog_notification'

    def on_post(self, request, response):
        payload = request.context or {}

        if not payload or not payload.get('seller_id'):
            raise BadRequest(
                INVALID_PARAMETERS_MSG.format(payload)
            )

        seller_id = payload['seller_id']

        expires_at = self._check_lock_time(seller_id)
        if expires_at:
            raise BadRequestWithMessage(
                f'O seller {seller_id}, '
                f'escopo {self.scope}, não pode ser reprocessado. '
                f'O rebuild estará disponível após {expires_at}.'
            )

        payload = {
            'scope': self.scope,
            'action': 'update',
            'data': {
                'seller_id': seller_id
            }
        }

        self.publish_rebuild(payload)

        self._rebuild_lock(seller_id)

        logger.info('Request to rebuild notification with {}'.format(payload))
        self.write_response(response, falcon.HTTP_200)


class RebuildCatalogNotificationHandler(BaseHandler, MongodbMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sns = Notification()
        self.pubsub_manager = StreamPublisherManager()
        self.raw_products = self.get_collection('raw_products')

    def on_post(self, request, response):
        notifications = request.context or {}

        if not notifications:
            raise BadRequest(
                INVALID_PARAMETERS_MSG.format(request.context)
            )

        for notification in notifications:
            self._validate_notification(notification)
            catalog_notification = self._format_notification(notification)
            if catalog_notification:
                self._notify(
                    catalog_notification,
                    notification['type'],
                    notification['action']
                )

        self.write_response(response, falcon.HTTP_200)

    def _notify(self, payload, notification_type, notification_action):
        if notification_type in settings.CATALOG_NOTIFICATION_PUBSUB:
            try:
                self.pubsub_manager.publish(
                    content=payload,
                    topic_name=settings.MARVIN_NOTIFICATION['topic_name'],
                    project_id=settings.MARVIN_NOTIFICATION['project_id'],
                    attributes={
                        'subscription_id': 'marvin-gateway-force-taz-sub'
                    }
                )
                logger.info(
                    'Request rebuild for {topic_name} '
                    'with type: {notification_type} '
                    'and payload: {payload}'.format(
                        topic_name=settings.MARVIN_NOTIFICATION['topic_name'],
                        notification_type=notification_type,
                        payload=payload
                    )
                )
            except Exception as e:
                logger.error(
                    'An error occurred while rebuild {tp_rebuild} on pubsub '
                    'with error:{error} payload:{payload}'.format(
                        error=e,
                        payload=payload,
                        tp_rebuild=notification_type
                    )
                )

                raise
        else:
            self.sns.put(
                payload,
                notification_type,
                notification_action,
                origin='rebuild'
            )
            logger.info(
                'Request rebuild catalog SNS '
                'with payload:{payload}'.format(
                    payload=payload
                )
            )

    def _validate_notification(self, notification):
        schema = CatalogNotificationSchema()
        try:
            schema.validate(notification)
        except ValidationError as error:
            logger.error(
                'Error to validate notification error:{error}'.format(
                    error=error)
            )
            raise BadRequest()

    def _format_notification(self, notification):

        navigation_id = notification.get('navigation_id')
        seller_id = notification.get('seller_id')
        sku = notification.get('sku')

        if not navigation_id:
            navigation_id = self._get_navigation_id(
                sku,
                seller_id
            )

        if not sku:
            seller_id, sku = self._get_sku_and_seller_id(navigation_id)

        if navigation_id is None or sku is None or seller_id is None:
            return None

        payload = Notification.format_payload(
            sku,
            seller_id,
            navigation_id,
            notification['action'],
            notification['type'],
            notification['type']
        )
        return payload

    def _get_sku_and_seller_id(self, navigation_id):
        product = self.raw_products.find_one(
            {'navigation_id': navigation_id},
            {'sku': 1, 'seller_id': 1}
        )

        if not product:
            logger.warning(
                f'Notification not found with navigation_id:{navigation_id} '
                'in raw_products'
            )
            return None, None

        return product['seller_id'], product['sku']

    def _get_navigation_id(self, sku, seller_id):
        product = self.raw_products.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'navigation_id': 1}
        )

        if not product:
            logger.warning(
                f'Notification not found with sku:{sku} '
                f'and seller_id:{seller_id} '
                'in raw_products'
            )
            return

        return product['navigation_id']


class RebuildProductHandler(BaseRebuildHandle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_post(self, request, response):
        products = request.context or {}

        if not products:
            raise BadRequest(
                INVALID_PARAMETERS_MSG.format(request.context)
            )

        payload = {
            'scope': 'complete_products_by_sku',
            'action': 'update',
            'data': products
        }

        self.publish_rebuild(payload)

        logger.info('Request rebuild product with payload:{}'.format(payload))
        self.write_response(response, falcon.HTTP_200)


class RebuildMarvinSellerHandler(RebuildLockHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scope = 'rebuild_marvin_seller_paginator'

    def on_post(self, request, response):
        data = request.context or {}

        if not data:
            raise BadRequest(
                INVALID_PARAMETERS_MSG.format(request.context)
            )

        expires_at = self._check_lock_time(data.get('seller_id'))
        if expires_at:
            raise BadRequestWithMessage(
                f'O seller {data.get("seller_id")}, '
                f'escopo {self.scope}, não pode ser reprocessado. '
                f'O rebuild estará disponível após {expires_at}.'
            )

        payload = {
            'scope': self.scope,
            'action': data.get('action'),
            'data': {
                'seller_id': data.get('seller_id'),
                'scope': 'marvin_seller',
            }
        }

        self.publish_rebuild(payload)

        self._rebuild_lock(data.get('seller_id'))

        logger.info(
            'Request rebuild marvin seller with payload:{}'.format(payload)
        )
        self.write_response(response, falcon.HTTP_200)


class RebuildProductScoreHandler(BaseRebuildHandle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_post(self, request, response):
        payload = request.context or {}

        if not payload:
            raise BadRequest(
                INVALID_PARAMETERS_MSG.format(request.context)
            )

        payload = {
            'scope': 'product_score_by_seller',
            'action': 'update',
            'data': {
                'seller_id': payload['seller_id']
            }
        }

        self.publish_rebuild(payload)

        logger.info('Request to rebuild product_score with {}'.format(payload))
        self.write_response(response, falcon.HTTP_200)


class RebuildProductScoreBySkuHandler(BaseRebuildHandle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_post(self, request, response):
        products = request.context or {}

        if not products:
            raise BadRequest(
                INVALID_PARAMETERS_MSG.format(request.context)
            )

        payload = {
            'scope': 'product_score_by_sku',
            'action': 'update',
            'data': products
        }

        self.publish_rebuild(payload)

        logger.info('Request to rebuild product_score with {}'.format(payload))
        self.write_response(response, falcon.HTTP_200)


class RebuildMetabooksHandler(BaseHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @cached_property
    def pubsub_manager(self):
        return StreamPublisherManager()

    def on_get(self, request, response, ean):
        payload = {
            'identified': ean,
            'source': constants.SOURCE_METABOOKS
        }

        logger.info(f'Request to rebuild metabooks with ean:{ean}')

        self.pubsub_manager.publish(
            topic_name=settings.PUBSUB_METADATA_INPUT_TOPIC_NAME,
            project_id=settings.GOOGLE_PROJECT_ID,
            content=payload
        )

        self.write_response(response, falcon.HTTP_200)


class RebuildMatchingOmnilogicHandler(BaseRebuildHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_post(self, request, response):
        data = request.context or {}

        if not data:
            raise BadRequest(
                INVALID_PARAMETERS_MSG.format(request.context)
            )

        payload = {
            'scope': 'matching_omnilogic',
            'data': {'entity': data}
        }

        self.publish_rebuild(payload)

        logger.info(
            'Request to rebuild matching_omnilogic with {}'.format(payload)
        )

        self.write_response(response, falcon.HTTP_200)


class RebuildProductExporterHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pubsub = StreamPublisherManager()

    def on_post(self, request, response):
        payload = request.context or {}
        if not payload:
            raise BadRequest(
                INVALID_PARAMETERS_MSG.format(request.context)
            )

        if not payload.get('type'):
            payload['type'] = 'product'

        self._validate_payload(payload)

        self.pubsub.publish(
            content=payload,
            project_id=settings.GOOGLE_PROJECT_ID,
            topic_name=settings.PUBSUB_PRODUCT_EXPORTER_TOPIC_NAME,
            attributes=settings.REBUILD_EXPORTER_CUSTOM_ATTRIBUTES,
        )

        logger.info(
            'Request to rebuild product exporter with {}'.format(payload)
        )

        self.write_response(response, falcon.HTTP_200)

    def _validate_payload(self, payload: dict):
        schema = RebuildProductExporterSchema()
        try:
            schema.validate(payload)
        except ValidationError as error:
            logger.error(
                f'Error to validate payload error:{error}'
            )
            raise BadRequest()


class RebuildMatchingProductHandler(BaseRebuildHandle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_post(self, request, response):
        product = request.context or {}

        if not product:
            raise BadRequest(
                INVALID_PARAMETERS_MSG.format(request.context)
            )

        payload = {
            'scope': 'matching_by_sku',
            'action': 'update',
            'data': product
        }

        self.publish_rebuild(payload)

        logger.info(
            'Request rebuild matching product with payload:{}'.format(payload)
        )
        self.write_response(response, falcon.HTTP_200)


class RebuildClassifyProductHandler(BaseRebuildHandle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_post(self, request, response):
        product = request.context or {}

        if not product:
            raise BadRequest(
                INVALID_PARAMETERS_MSG.format(request.context)
            )

        payload = {
            'scope': 'classify_by_sku',
            'action': 'update',
            'data': product
        }

        self.publish_rebuild(payload)

        logger.info(
            'Request rebuild classify product with payload:{}'.format(
                payload
            )
        )
        self.write_response(response, falcon.HTTP_200)


class RebuildDatalakeHandler(BaseHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pubsub_manager = StreamPublisherManager()

    def on_post(self, request, response):
        payload = request.context or {}

        if not payload:
            raise BadRequest(
                INVALID_PARAMETERS_MSG.format(payload)
            )

        self._validate_payload(payload)

        payload = Notification.format_payload(
            sku=payload['sku'],
            seller_id=payload['seller_id'],
            navigation_id=payload['navigation_id'],
            action=payload['action'],
            scope=payload['type'],
            source=payload.get('source'),
            origin='rebuild'
        )

        self.pubsub_manager.publish(
            topic_name=settings.PUBSUB_DATALAKE_INPUT_TOPIC_NAME,
            project_id=settings.GOOGLE_PROJECT_ID,
            content=payload
        )
        logger.info(f'Request to datalake {payload}')
        self.write_response(response, falcon.HTTP_200)

    def _validate_payload(self, payload: dict):
        schema = RebuildDatalakeSchema()
        try:
            schema.validate(payload)
        except ValidationError as error:
            logger.error(
                f'Error to validate payload error:{error}'
            )
            raise BadRequest()


class RebuildMediaHandler(BaseRebuildHandle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_post(self, request, response):
        medias = request.context or {}

        if not medias:
            raise BadRequest(
                INVALID_PARAMETERS_MSG.format(request.context)
            )

        self._validate_payload(medias)

        is_from_bucket = str(medias.get('from_bucket', '')).lower() == 'true'
        if (
            is_from_bucket and
            medias.get('seller_id', '') != constants.MAGAZINE_LUIZA_SELLER_ID
        ):
            raise BadRequest(
                INVALID_PARAMETERS_MSG.format(request.context)
            )

        payload = {
            'scope': 'media_rebuild',
            'action': 'update',
            'data': medias
        }

        self.publish_rebuild(payload)

        logger.info('Request rebuild media with payload:{}'.format(payload))
        self.write_response(response, falcon.HTTP_200)

    def _validate_payload(self, payload: dict):
        schema = RebuildMediaSchema()
        try:
            schema.validate(payload)
        except ValidationError as error:
            logger.error(
                f'Error to validate payload error:{error}'
            )
            raise BadRequest()


class RebuildPriceRulesHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pubsub_manager = StreamPublisherManager()
        self.notification_type = 'price_rules'

    def on_post(self, request, response):
        payload = request.context or {}

        if not payload:
            raise BadRequest(
                INVALID_PARAMETERS_MSG.format(request.context)
            )

        self._validate_payload(payload)

        notification_payload = Notification.format_payload(
            payload['sku'],
            payload['seller_id'],
            payload['navigation_id'],
            constants.UPDATE_ACTION,
            self.notification_type,
            'rebuild'
        )
        self._notify(notification_payload)
        self.write_response(response, falcon.HTTP_200)

    def _notify(self, payload: dict):
        try:
            self.pubsub_manager.publish(
                content=payload,
                topic_name=settings.PUBSUB_RECLASSIFICATION_PRICE_RULE_NAME,
                project_id=settings.GOOGLE_PROJECT_ID,
            )
            logger.info(
                'Request rebuild for '
                f'{settings.PUBSUB_RECLASSIFICATION_PRICE_RULE_NAME} '
                f'with type: {self.notification_type} and payload: {payload}'
            )
        except Exception as e:
            logger.error(
                f'An error occurred while rebuild {self.notification_type} '
                f'on pubsub with error:{e} payload:{payload}'
            )
            raise

    def _validate_payload(self, payload: dict):
        schema = RebuilPriceRulesSchema()
        try:
            schema.validate(payload)
        except ValidationError as error:
            logger.error(f'Error to validate payload error:{error}')
            raise BadRequest()
