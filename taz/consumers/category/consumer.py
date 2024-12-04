from functools import cached_property

import requests
from maaslogger import base_logger
from simple_settings import settings

from taz import constants
from taz import http_status as status
from taz.consumers.core.brokers.stream import (
    PubSubBroker,
    PubSubRecordProcessor
)
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.exceptions import InvalidAcmeResponseException
from taz.core.cache.layers import RedisCache
from taz.helpers.category import build_category_data

logger = base_logger.get_logger(__name__)


class CategoryRecordProcessor(MongodbMixin, PubSubRecordProcessor):

    required_fields = ['id', 'description', 'slug', 'parent_id']
    required_fields_delete = ['id']

    @cached_property
    def mongo_collection(self):
        return self.get_collection('categories')

    @cached_property
    def cache(self):
        return RedisCache(
            key_pattern=settings.PRODUCT_WRITER_REDIS_KEY_PATTERN,
            ttl=int(settings.EXPIRES_REDIS_CACHE_CATEGORIES),
            host=settings.REDIS_SETTINGS['host'],
            port=settings.REDIS_SETTINGS['port'],
            password=settings.REDIS_SETTINGS.get('password')
        )

    def process_message(self, message):
        action = message['action']
        data = message['item']

        if action == constants.CREATE_ACTION:
            self.create(data)
        elif action == constants.UPDATE_ACTION:
            self.update(data)
        elif action == constants.DELETE_ACTION:
            self.delete(data)

    def delete(self, data):
        req = requests.delete(
            '{}/category/{}/'.format(settings.ACME_URL, data['id']),
            headers=settings.ACME_REQUEST_HEADER
        )

        if req.status_code == status.HTTP_404_NOT_FOUND:
            logger.error(
                'Error deleting category in {url} '
                'category {data} not found'.format(
                    url=req.url,
                    data=data['id']
                ),
                detail={
                    "url": req.url,
                    "id": data['id']
                }
            )
        elif req.status_code != status.HTTP_204_NO_CONTENT:
            raise InvalidAcmeResponseException(
                'Error deleting category in {url}: - {response}'.format(
                    url=req.url,
                    response=req.text
                )
            )

        document = self.mongo_collection.delete_one({'id': data['id']})
        if document.deleted_count > 0:
            self.cache.delete(data['id'])
            logger.info('Successfully deleted category:{}'.format(data['id']))
        else:
            logger.error('Could not delete category:{}'.format(
                data['id']
            ))

    def create(self, data):
        data = self._build_category_data(data)

        req = requests.post(
            '{}/category/'.format(settings.ACME_URL),
            json=data,
            headers=settings.ACME_REQUEST_HEADER
        )

        if req.status_code == status.HTTP_409_CONFLICT:
            self.cache.delete(data['id'])
            self.update(data)
            return
        elif req.status_code != status.HTTP_201_CREATED:
            raise InvalidAcmeResponseException(
                'Error creating category in '
                '{url}: {data} - {response}'.format(
                    url=req.url,
                    data=data,
                    response=req.text
                )
            )

        self._save(data)
        self.cache.delete(data['id'])
        logger.info('Successfully created category:{}'.format(data['id']))

    def update(self, data):
        data = self._build_category_data(data)

        req = requests.put(
            '{}/category/{}/'.format(settings.ACME_URL, data['id']),
            json=data,
            headers=settings.ACME_REQUEST_HEADER
        )

        if req.status_code not in (
            status.HTTP_200_OK,
            status.HTTP_404_NOT_FOUND
        ):
            raise InvalidAcmeResponseException(
                'Error updating category in '
                '{url}: {data} - {response}'.format(
                    url=req.url,
                    data=data,
                    response=req.text
                )
            )
        elif req.status_code == status.HTTP_404_NOT_FOUND:
            self.create(data)
            self.cache.delete(data['id'])
            return

        self._save(data)
        self.cache.delete(data['id'])
        logger.info('Successfully updated category:{}'.format(data['id']))

    def _save(self, data):
        self.mongo_collection.update_one(
            {'id': data['id']}, {'$set': data}, upsert=True
        )

    def _build_category_data(self, data):
        parent_id = data['parent_id']
        if parent_id == constants.MAGAZINE_LUIZA_DEFAULT_CATEGORY:
            url = build_category_data(data)
        else:
            category = self.mongo_collection.find_one({'id': parent_id})
            url = build_category_data(category, data)

        data['url'] = url
        return data


class CategoryConsumer(PubSubBroker):
    record_processor_class = CategoryRecordProcessor
    scope = 'category'
    project_name = settings.GOOGLE_PROJECT_ID
    subscription_name = settings.PUBSUB_POLLER_CATEGORY_SUB_NAME
