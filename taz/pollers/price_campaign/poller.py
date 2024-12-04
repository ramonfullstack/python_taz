from taz.pollers.core.brokers.pubsub import PubSubBroker
from taz.pollers.core.processor.sqlserver import SqlserverPoller

from .converter import PriceConverter
from .data import PriceDataStorage


class PricePoller(SqlserverPoller):  # pragma: no cover

    scope = 'price_campaign'

    def get_converter(self):
        return PriceConverter()

    def get_data_source(self):
        return PriceDataStorage()

    def get_sender(self):
        return PubSubBroker(self.scope)
