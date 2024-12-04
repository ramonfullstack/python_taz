from unittest.mock import patch

import pytest

from taz.pollers.core.brokers.pubsub import PubSubBroker
from taz.pollers.core.data.converter import BaseConverter
from taz.pollers.core.processor.api import ApiPoller


class FakeDataSource:
    def fetch(self):
        return [
            {
                'productSku': '216514700',
                'batch_key': '21651',
                'productName': (
                    'smartphone motorola moto g 4 geracao'
                    'play dtv - 16gb preto dual chip 4g cam. 8mp selfie 5mp'
                ),
                'productDetailViews': '717270',
                'timestamp': 1496172515764
            },
            {
                'productSku': '213981800',
                'batch_key': '21398',
                'productName': (
                    'iphone 6 apple 64gb cinza espacial 4g tela 4.7'
                    ' - retina camera 8mp ios 10 proc. m8'
                ),
                'productDetailViews': '365933',
                'timestamp': 1496172515764
            },
            {
                'productSku': '213965700',
                'batch_key': '21396',
                'productName': (
                    'smartphone samsung galaxy j7 duos 16gb dourado'
                    ' - dual chip 4g cam 13mp selfie 5mp flash tela 5.5'
                ),
                'productDetailViews': '266931',
                'timestamp': 1496172515764
            },
            {
                'productSku': '216819100',
                'batch_key': '216819',
                'productName': (
                    'notebook acer aspire es 15 intel core i5'
                    ' - 6 geracao 4gb 1tb led 15 6 windows 10',
                ),
                'productDetailViews': '261524',
                'timestamp': 1496172515764
            },
        ]

    def batch_key(self):
        return 'batch_key'

    def is_batch(self):
        return True


class FakeConverter(BaseConverter):

    def _add_item(self, raw):
        item = {
            'sku': raw['productSku'],
            'views': raw['productDetailViews']
        }

        self.items.setdefault(raw['batch_key'], {}).update({item['sku']: item})

    def from_source(self, data):
        [self._add_item(item) for item in data]


class TestApiPoller:

    @pytest.fixture
    def patch_pubsub(self):
        return patch('taz.pollers.core.brokers.pubsub.PubSubBroker')

    @pytest.fixture
    def poller(self):
        class ApiPollerFake(ApiPoller):
            scope = 'product'
            url = 'http://fake.com'

            def get_converter(self):
                return FakeConverter()

            def get_data_source(self):
                return FakeDataSource()

            def get_sender(self):
                return PubSubBroker(self.scope)

        return ApiPollerFake()

    def test_items_should_have_been_processed(
        self,
        poller
    ):
        total_items = len(FakeDataSource().fetch())

        with patch.object(PubSubBroker, 'put_many'):
            processed_items = poller.poll()

        assert total_items == processed_items

    def test_kinesis_and_poller_scope_should_be_the_same(self, poller):
        kinesis = poller.get_sender()
        assert poller.scope == kinesis.scope

    def test_batch_key_for_item_should_consider_sku_first_five_digits(
        self,
        poller
    ):
        item = FakeDataSource().fetch()[0]
        expected_batch = item['productSku'][0:5]
        batch_key = poller._get_batch_key(item)

        assert expected_batch == batch_key
