from taz.pollers.core.brokers.pubsub import PubSubBrokerWithData
from taz.pollers.core.processor.sqlserver import (
    SqlServerPollerWithCircuitBreaker
)
from taz.pollers.product.converter import ProductConverter
from taz.pollers.product.data import ProductDataStorage


class ProductPoller(SqlServerPollerWithCircuitBreaker):  # pragma: no cover

    scope = 'product'

    def get_converter(self):
        return ProductConverter()

    def get_data_source(self):
        return ProductDataStorage()

    def get_sender(self):
        return PubSubBrokerWithData(self.scope)
