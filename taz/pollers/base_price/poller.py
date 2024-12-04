from taz.pollers.core.brokers.pubsub import PubSubBrokerWithData
from taz.pollers.core.processor.sqlserver import SqlserverPoller

from .converter import BasePriceConverter
from .data import BasePriceDataStorage


class BasePricePoller(SqlserverPoller):  # pragma: no cover

    scope = 'base_price'

    def get_converter(self):
        return BasePriceConverter()

    def get_data_source(self):
        return BasePriceDataStorage()

    def get_sender(self):
        return PubSubBrokerWithData(self.scope)
