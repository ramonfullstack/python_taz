import pytest

from taz.consumers.catalog_notification.router import CatalogNotificationRouter
from taz.consumers.core.google.stream import StreamPublisherManager


class FakeMessage(dict):
    def __init__(
        self,
        data: bytes,
        attributes: dict
    ):
        self.data = data
        self.attributes = attributes
        self.ordering_key = None


class TestCatalogNotificationRouter:
    @pytest.fixture
    def publisher(self):
        return StreamPublisherManager()

    @pytest.fixture
    def router(
        self,
        publisher,
    ):
        return CatalogNotificationRouter(publisher)

    @pytest.mark.parametrize('attributes,expected', [
        ({'type': 'product'}, 3),
        ({'type': 'product', 'seller_id': 'magazineluiza'}, 4),
    ])
    def test_valid_message_route(
        self,
        patch_pubsub_client,
        router,
        attributes,
        expected
    ):
        with patch_pubsub_client as pubsub_mock:
            msg = FakeMessage(b'', attributes)
            router.route(msg)
            assert pubsub_mock.call_count == expected

    @pytest.mark.parametrize('attributes', [
        ({}),
    ])
    def test_valid_message_without_attrs(
        self,
        patch_pubsub_client,
        router,
        attributes,
    ):
        with patch_pubsub_client as pubsub_mock:
            msg = FakeMessage(b'', attributes)
            router.route(msg)
            assert pubsub_mock.call_count == 0

    @pytest.mark.parametrize('attributes', [
        ({'type': 'test'}),
        ({'type': 'test', 'seller_id': 'test'}),
    ])
    def test_valid_message_without_matchs(
        self,
        patch_pubsub_client,
        router,
        attributes,
    ):
        with patch_pubsub_client as pubsub_mock:
            msg = FakeMessage(b'', attributes)
            router.route(msg)
            assert pubsub_mock.call_count == 0

    @pytest.mark.parametrize('attributes', [
        ({'type': 'matching'})
    ])
    def test_should_add_custom_attributes(
        self,
        patch_pubsub_client,
        router,
        attributes
    ):
        with patch_pubsub_client as pubsub_mock:
            msg = FakeMessage(b'', attributes)
            router.route(msg)
            assert pubsub_mock.call_count == 2
            assert pubsub_mock.call_args_list[1][1] == {
                'topic': 'projects/maga-homolog/topics/taz-product-exporter',
                'data': b'',
                'ordering_key': '',
                'type': 'matching',
                'Content-Type': 'application/json'
            }

    @pytest.mark.parametrize('attributes', [
        ({'type': 'product'})
    ])
    def test_should_not_add_custom_attributes(
        self,
        patch_pubsub_client,
        router,
        attributes
    ):
        with patch_pubsub_client as pubsub_mock:
            msg = FakeMessage(b'', attributes)
            router.route(msg)
            assert pubsub_mock.call_count == 3
            assert pubsub_mock.call_args_list[1][1] == {
                'topic': 'projects/maga-homolog/topics/taz-datalake',
                'data': b'',
                'ordering_key': '',
                'type': 'product'
            }

    @pytest.mark.parametrize('attributes', [
        ({'type': 'matching', 'Content-Type': 'text/xml'})
    ])
    def test_should_not_duplicate_msg_attributes(
        self,
        patch_pubsub_client,
        router,
        attributes
    ):
        with patch_pubsub_client as pubsub_mock:
            msg = FakeMessage(b'', attributes)
            router.route(msg)
            assert pubsub_mock.call_count == 2
            assert pubsub_mock.call_args_list[1][1] == {
                'topic': 'projects/maga-homolog/topics/taz-product-exporter',
                'data': b'',
                'ordering_key': '',
                'type': 'matching',
                'Content-Type': 'application/json'
            }
