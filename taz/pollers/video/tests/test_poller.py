import pytest

from taz.pollers.core.brokers.pubsub import PubSubBroker
from taz.pollers.video.converter import VideoConverter
from taz.pollers.video.data import VideoDataStorage
from taz.pollers.video.poller import VideoPoller


class TestVideoPoller:
    @pytest.fixture
    def poller(self):
        return VideoPoller()

    def test_poller_converter(self, poller):
        converter = poller.get_converter()
        assert isinstance(converter, VideoConverter)

    def test_poller_data_source(self, poller):
        data_source = poller.get_data_source()
        assert isinstance(data_source, VideoDataStorage)

    def test_poller_sender(self, poller):
        sender = poller.get_sender()
        assert isinstance(sender, PubSubBroker)
