from taz.pollers.core.brokers.pubsub import PubSubBroker
from taz.pollers.price_campaign.poller import PricePoller


class TestPriceCampaignPoller:

    def test_get_sender_should_instantiate_pubsub(self):  # noqa
        poller = PricePoller()
        sender = poller.get_sender()

        assert isinstance(sender, PubSubBroker)
