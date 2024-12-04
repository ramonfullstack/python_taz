from taz.pollers.core.brokers.pubsub import PubSubBrokerWithData
from taz.pollers.core.processor.sqlserver import SqlserverPoller

from .converter import FactsheetConverter
from .data import FactsheetDataStorage


class FactsheetPoller(SqlserverPoller):  # pragma: no cover

    scope = 'factsheet'

    def get_converter(self):
        return FactsheetConverter(self.data_source)

    def get_data_source(self):
        return FactsheetDataStorage()

    def get_sender(self):
        return PubSubBrokerWithData(self.scope)
