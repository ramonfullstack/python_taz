
from taz.pollers.core.brokers.pubsub import PubSubBrokerWithData
from taz.pollers.core.processor.sqlserver import SqlserverPoller

from .converter import VideoConverter
from .data import VideoDataStorage


class VideoPoller(SqlserverPoller):  # pragma: no cover

    scope = 'video'

    def get_converter(self):
        return VideoConverter()

    def get_data_source(self):
        return VideoDataStorage()

    def get_sender(self):
        return PubSubBrokerWithData(self.scope)
