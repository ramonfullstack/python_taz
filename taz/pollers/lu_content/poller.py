from taz.pollers.core.brokers.pubsub import PubSubBroker
from taz.pollers.core.processor.sqlserver import SqlserverPoller

from .converter import LuContentConverter
from .data import LuContentDataStorage


class LuContentPoller(SqlserverPoller):  # pragma: no cover

    scope = 'lu_content'

    def get_converter(self):
        return LuContentConverter(self.data_source)

    def get_data_source(self):
        return LuContentDataStorage()

    def get_sender(self):
        return PubSubBroker(self.scope)
