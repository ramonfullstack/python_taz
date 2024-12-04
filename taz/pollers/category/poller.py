from taz.pollers.category.converter import CategoryConverter
from taz.pollers.category.data import CategoryDataStorage
from taz.pollers.core.brokers.pubsub import PubSubBroker
from taz.pollers.core.processor.sqlserver import SqlserverPoller


class CategoryPoller(SqlserverPoller):  # pragma: no cover

    scope = 'category'

    def get_converter(self):
        return CategoryConverter()

    def get_data_source(self):
        return CategoryDataStorage()

    def get_sender(self):
        return PubSubBroker(self.scope)
