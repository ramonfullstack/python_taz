from unittest import TestCase, mock

import pytest
from google.cloud import pubsub

from taz.consumers.core.google.stream import (
    PubSubSubscriber,
    StreamPublisherManager
)
from taz.helpers.json import json_dumps


class TestPubSubPublisher:

    @pytest.fixture
    def pubsub_publisher(self):
        return StreamPublisherManager()

    def test_pubsub_publisher_is_called(
        self,
        patch_pubsub_client,
        pubsub_publisher,
    ):

        with patch_pubsub_client as mock:
            pubsub_publisher.publish({'data': 'content'}, 'topic_name')

        assert mock.called

    def test_publish_with_attributes_should_return_ok(
        self,
        patch_pubsub_client,
        pubsub_publisher,
    ):
        attrs = {'slug': 'murcho', 'id': 100}

        with patch_pubsub_client as mock:
            pubsub_publisher.publish(
                content={'data': 'content'},
                topic_name='topic_name',
                attributes=attrs
            )

        assert mock.call_args[1] == {
            'topic': 'projects/maga-homolog/topics/topic_name',
            'data': b'{"data": "content"}',
            'ordering_key': '',
            'slug': 'murcho',
            'id': 100
        }
        assert mock.called

    def test_publish_try_create_ordering_key_using_content_bytes(
        self,
        patch_pubsub_client,
        pubsub_publisher,
    ):
        with patch_pubsub_client as mock:
            pubsub_publisher.publish(
                content=json_dumps({
                    'seller_id': '123', 'sku': '321'
                }).encode('utf-8'),
                topic_name='topic_name',
                attributes={}
            )
        assert mock.call_args[1] == {
            'topic': 'projects/maga-homolog/topics/topic_name',
            'data': b'{"seller_id": "123", "sku": "321"}',
            'ordering_key': '123/321',
        }

    def test_publish_try_create_ordering_key_using_attrs(
        self,
        patch_pubsub_client,
        pubsub_publisher,
    ):
        attrs = {
            'seller_id': '123',
            'sku': '321'
        }
        with patch_pubsub_client as mock:
            pubsub_publisher.publish(
                content={'data': 'content'},
                topic_name='topic_name',
                attributes=attrs
            )
        assert mock.call_args[1] == {
            'topic': 'projects/maga-homolog/topics/topic_name',
            'data': b'{"data": "content"}',
            'ordering_key': '123/321',
            'seller_id': '123',
            'sku': '321'
        }

    def test_publish_try_create_ordering_key_using_attrs_none(
        self,
        patch_pubsub_client,
        pubsub_publisher,
    ):
        attrs = {}
        with patch_pubsub_client as mock:
            pubsub_publisher.publish(
                content={'data': 'content'},
                topic_name='topic_name',
                attributes=attrs
            )
        assert mock.call_args[1] == {
            'topic': 'projects/maga-homolog/topics/topic_name',
            'data': b'{"data": "content"}',
            'ordering_key': '',
        }

    def test_publish_try_create_ordering_key_using_only_seller_id(
        self,
        patch_pubsub_client,
        pubsub_publisher,
    ):
        attrs = {
            'seller_id': '123',
        }
        with patch_pubsub_client as mock:
            pubsub_publisher.publish(
                content={'data': 'content'},
                topic_name='topic_name',
                attributes=attrs
            )
        assert mock.call_args[1] == {
            'topic': 'projects/maga-homolog/topics/topic_name',
            'data': b'{"data": "content"}',
            'ordering_key': '',
            'seller_id': '123',
        }

    def test_publish_try_create_ordering_key_using_only_sku(
        self,
        patch_pubsub_client,
        pubsub_publisher,
    ):
        attrs = {
            'sku': '123',
        }
        with patch_pubsub_client as mock:
            pubsub_publisher.publish(
                content={'data': 'content'},
                topic_name='topic_name',
                attributes=attrs
            )
        assert mock.call_args[1] == {
            'topic': 'projects/maga-homolog/topics/topic_name',
            'data': b'{"data": "content"}',
            'ordering_key': '',
            'sku': '123',
        }

    def test_publish_try_create_ordering_key_using_content(
        self,
        patch_pubsub_client,
        pubsub_publisher,
    ):
        content = {
            'seller_id': '123',
            'sku': '321'
        }
        with patch_pubsub_client as mock:
            pubsub_publisher.publish(
                content=content,
                topic_name='topic_name',
                attributes={}
            )
        assert mock.call_args[1] == {
            'topic': 'projects/maga-homolog/topics/topic_name',
            'data': b'{"seller_id": "123", "sku": "321"}',
            'ordering_key': '123/321',
        }


class TestPubSubSubscriber:

    @pytest.fixture
    def patch_client(self):
        return mock.patch.object(pubsub.SubscriberClient, 'subscribe')

    @pytest.fixture
    def pubsub_subscriber(self):
        return PubSubSubscriber('project_id', 'subscription_name')

    @pytest.fixture
    def handler_function(self):  # pragma: no cover
        pass

    def test_pubsub_subscriber_is_called(
        self,
        patch_client,
        pubsub_subscriber,
        handler_function
    ):
        with patch_client as mock:
            pubsub_subscriber.subscribe(handler_function)

        assert mock.called

    def test_pubsub_subscriber_raise_error(
        self,
        caplog,
        patch_client,
        pubsub_subscriber,
        handler_function
    ):
        with patch_client as mock:
            mock.side_effect = Exception
            pubsub_subscriber.subscribe(handler_function)

        assert mock.called
        assert 'Failed to close subscription gracefully' in caplog.text

    def test_pubsub_subscriber_when_wrapper_function_raise_error(
        self,
        caplog,
        patch_client,
        pubsub_subscriber
    ):
        TestCase().assertRaises(
            Exception,
            pubsub_subscriber._wrapper, mock.MagicMock()
        )
        assert 'Error while processing event' in caplog.text
