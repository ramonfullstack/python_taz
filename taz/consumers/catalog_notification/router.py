import json
import os

from google.cloud import pubsub_v1
from maaslogger import base_logger
from simple_settings import settings

from taz.consumers.catalog_notification import SCOPE
from taz.consumers.core.google.stream import StreamPublisherManager

logger = base_logger.get_logger(__name__)


class InvalidRouterConfig(Exception):
    def __init__(self, endpoint='', *args: object) -> None:
        msg = (
            f'Router Config param is required for {endpoint}'
            if endpoint else
            'Router Config param is required'
        )
        super().__init__(msg, *args)


def load_config():
    router_config = {}
    enabled_endpoints = settings.CATALOG_NOTIFICATION_ROUTER_ENABLED_ENDPOINTS
    if isinstance(enabled_endpoints, str):
        enabled_endpoints = enabled_endpoints.split(',')

    logger.info(f'loading router configs: {str(enabled_endpoints)}')
    for endpoint in enabled_endpoints:
        try:
            endpoint_config = (
                getattr(
                    settings,
                    f'CATALOG_NOTIFICATION_ROUTER_{endpoint}'.replace('-', '_')
                )
            )
            if isinstance(endpoint_config, str):
                endpoint_config = json.loads(endpoint_config)
        except AttributeError:
            endpoint_config = None

        try:
            custom_attributes = getattr(
                settings,
                f'CATALOG_NOTIFICATION_ROUTER_CUSTOM_ATTRIBUTES_{endpoint}'.replace('-', '_') # noqa
            )
            if isinstance(custom_attributes, str):
                custom_attributes = json.loads(custom_attributes)
        except AttributeError:
            custom_attributes = {}

        if endpoint_config is None and os.getenv('SCOPE') == SCOPE:
            raise InvalidRouterConfig(endpoint)

        router_config[endpoint] = {
            'filters': endpoint_config,
            'custom_attributes': custom_attributes,
        }

    if not router_config:
        raise InvalidRouterConfig()

    return router_config


class CatalogNotificationRouter:
    __config = None

    def __init__(self, publisher: StreamPublisherManager):
        self.publisher = publisher
        CatalogNotificationRouter.load_config()

    @classmethod
    def load_config(cls):
        if cls.__config is None:
            cls.__config = load_config()

    def route(self, message: pubsub_v1.subscriber.message.Message):
        attrs = message.attributes
        logger.debug(f'routing msg:{str(attrs)}')
        for endpoint, config in self.__config.items():
            filters = config.get('filters')
            custom_attrs = config.get('custom_attributes')
            if self.should_route(filters, attrs):
                logger.debug(
                    f'routed msg:{str(message)} attr:{str(attrs)} '
                    f'endpoint:{endpoint} custom_attrs:{str(custom_attrs)}'
                )
                self.publish(endpoint, message, custom_attrs)

    def publish(
        self,
        endpoint: str,
        message: pubsub_v1.subscriber.message.Message,
        custom_attributes={}
    ):
        self.publisher.publish(
            topic_name=endpoint,
            content=message.data,
            attributes={**message.attributes, **custom_attributes},
            ordering_key=message.ordering_key,
        )

    @staticmethod
    def msg_has_valid_attr(attributes, values, field):
        return field in attributes and attributes[field] in values

    @staticmethod
    def should_route(required_fields, attributes):
        required_fields_count = 0
        for endpoint_filter in required_fields:
            for field, values in endpoint_filter.items():
                if CatalogNotificationRouter.msg_has_valid_attr(
                    attributes,
                    values,
                    field
                ):
                    required_fields_count += 1
                    break

        return len(required_fields) == required_fields_count
