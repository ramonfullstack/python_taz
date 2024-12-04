from taz.pollers.core.brokers.pubsub import PubSubBrokerWithData
from taz.pollers.core.processor.sqlserver import SqlserverPoller

from .converter import PartnerConverter
from .data import PartnerDataStorage


class PartnerPoller(SqlserverPoller):  # pragma: no cover

    scope = 'partner'

    def get_converter(self):
        return PartnerConverter()

    def get_data_source(self):
        return PartnerDataStorage()

    def get_sender(self):
        return PubSubBrokerWithData(self.scope, 'id')
