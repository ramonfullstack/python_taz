from unittest.mock import Mock, patch

import pytest
from redis import Redis

from taz.consumers.media_bucket.consumer import (
    MediaBucketConsumer,
    MediaBucketProcessor
)


class FakeMessage:
    def __init__(self):
        self.attributes = {
            'objectGeneration': '1702556008396874',
            'objectId': 'magazineluiza/img/produto_grande/21/210129500.jpg',
            'payloadFormat': 'JSON_API_V1',
            'eventType': 'OBJECT_FINALIZE',
            'notificationConfig': 'projects/_/buckets/img-sandbox/notificationConfigs/622', # noqa
            'bucketId': 'img-sandbox',
            'eventTime': '2023-12-14T12:13:28.400351Z',
        }


@pytest.fixture
def message():
    return FakeMessage()


class TestMediaBucketProcessor:
    @pytest.fixture
    def sku(self):
        return '123456789'

    @pytest.fixture
    def patch_list_media(self):
        return patch('taz.consumers.media_bucket.consumer.ListMedia')

    @pytest.fixture
    def patch_redis_get(self):
        return patch.object(Redis, 'get')

    @pytest.fixture
    def patch_redis_set(self):
        return patch.object(Redis, 'set')

    @pytest.fixture
    def processor(
        self,
        patch_pubsub_client,
        patch_list_media,
    ):
        with patch_pubsub_client as mock_pubsub:
            with patch_list_media as list_media_mock:
                mock_pubsub.return_value = Mock()
                list_media_mock.find_objects.return_value = Mock()
                return MediaBucketProcessor(scope='test')

    def test_get_process_cache_key(self, sku, processor):
        result = processor.get_process_cache_key(sku)
        expected = 'media_bucket::123456789'
        assert result == expected

    def test_get_sku_media_paths(self, sku, processor):
        result = processor.get_sku_media_paths(sku)
        assert result == {'audios': [], 'images': [], 'podcasts': []}

    def test_get_sku_media_paths_without_paths(
        self,
        sku,
        patch_pubsub_client,
        patch_list_media,
        caplog
    ):
        with patch_pubsub_client as mock_pubsub:
            with patch_list_media as list_media_mock:
                mock_pubsub.return_value = Mock()
                list_media_mock.find_skus_paths.return_value = None
                processor = MediaBucketProcessor(scope='test')
                result = processor.get_sku_media_paths(sku)
                assert result is None
                assert f'not found media sku:{sku}' in caplog.text

    def test_mount_payload(self, sku, processor):
        paths = {
            'audios': ['test.mp3'],
            'images': ['test.jpg'],
            'podcasts': ['test.mp3']
        }
        result = processor.mount_payload(sku, paths)
        expected = {
            'seller_id': 'magazineluiza',
            'sku': sku,
            'images': ['test.jpg'],
            'audios': ['test.mp3'],
            'podcasts': ['test.mp3'],
        }
        assert result == expected

    def test_get_event_sku(self, processor):
        fake_attributes = {
            'objectId': 'magazineluiza/img/produto_grande/21/210129500.jpg'
        }
        expected = '210129500'
        result = processor.get_event_sku(fake_attributes)
        assert expected == result

    def test_process_message(self, processor, message):
        try:
            processor.process_message(message)
        except Exception as e:
            pytest.fail(f'test_process_message: {str(e)}')


class TestMediaBucketConsumer:
    @pytest.fixture
    def consumer(self):
        return MediaBucketConsumer(
            project_id='fake',
            subscription_name='fake_sub'
        )

    @patch('google.auth.default')
    def test_should_be_able_to_create_consumer(
        self,
        consumer,
        message,
        patch_pubsub_client
    ):
        with patch_pubsub_client:
            consumer.record_processor_class(consumer.scope).process_message(event=message) # noqa
