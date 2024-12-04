from simple_settings import settings

from taz.pollers.core.brokers.pubsub import PubSubBroker
from taz.pollers.core.brokers.stream import KinesisBroker
from taz.pollers.core.processor.sqlserver import SqlserverPoller

from .converter import PriceConverter
from .data import PriceDataStorage


class PricePoller(SqlserverPoller):  # pragma: no cover

    scope = 'price'

    def get_converter(self):
        return PriceConverter()

    def get_data_source(self):
        return PriceDataStorage()

    def get_sender(self):
        if not settings.ENABLE_POLLER_PRICE_PUBSUB:
            return KinesisBroker(self.scope)
        return PubSubBroker(self.scope)
