from simple_settings.utils import settings_stub

from taz.pollers.core.brokers.pubsub import PubSubBroker
from taz.pollers.core.brokers.stream import KinesisBroker
from taz.pollers.price.poller import PricePoller


class TestPricePoller:

    def test_get_sender_should_kenesis(self):
        poller = PricePoller()
        sender = poller.get_sender()

        assert isinstance(sender, KinesisBroker)

    def test_get_sender_when_enable_poller_price_pubsub_is_true_should_pubsub(self):  # noqa
        with settings_stub(
            ENABLE_POLLER_PRICE_PUBSUB=True
        ):
            poller = PricePoller()
            sender = poller.get_sender()

        assert isinstance(sender, PubSubBroker)
