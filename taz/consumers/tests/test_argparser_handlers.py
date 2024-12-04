from unittest.mock import Mock, patch

import pytest

from taz.consumers.category.consumer import CategoryConsumer
from taz.consumers.enriched_product.consumer import EnrichedProductConsumer
from taz.consumers.factsheet.consumer import FactsheetConsumer
from taz.consumers.main import (
    category_handler,
    enriched_product_handler,
    execute,
    factsheet_handler,
    matching_handler,
    matching_product_handler,
    media_handler,
    price_3p_handler,
    product_handler,
    product_writer_handler,
    rebuild_handler,
    stock3p_handler
)
from taz.consumers.matching.consumer import MatchingConsumer
from taz.consumers.matching_product.consumer import MatchingProductConsumer
from taz.consumers.media.consumer import MediaConsumer
from taz.consumers.price_3p.consumer import Price3pConsumer
from taz.consumers.product.consumer import ProductConsumer
from taz.consumers.product_writer.consumer import ProductWriterConsumer
from taz.consumers.rebuild.consumer import RebuildConsumer
from taz.consumers.stock_3p.consumer import Stock3pConsumer


class TestConsumerHandlers:

    @pytest.fixture
    def patch_executor(self):
        return patch('taz.consumers.main.execute')

    @pytest.mark.parametrize(
        'handler,consumer', [
            (media_handler, MediaConsumer),
            (factsheet_handler, FactsheetConsumer),
            (category_handler, CategoryConsumer),
            (product_handler, ProductConsumer),
            (enriched_product_handler, EnrichedProductConsumer),
            (price_3p_handler, Price3pConsumer),
            (stock3p_handler, Stock3pConsumer),
            (matching_handler, MatchingConsumer),
            (product_writer_handler, ProductWriterConsumer),
            (rebuild_handler, RebuildConsumer),
            (matching_product_handler, MatchingProductConsumer)
        ]
    )
    def test_call_consumer_executor_with_right_consumer_class(
        self,
        patch_executor,
        handler,
        consumer
    ):
        with patch_executor as mock:
            handler(None)

        executor_arg = mock.call_args[0][0]
        assert isinstance(executor_arg, consumer)


class TestExecutor:

    @pytest.fixture
    def fake_consumer(self):
        return Mock()

    def test_executor_starts_consumer(
        self,
        fake_consumer
    ):
        execute(fake_consumer)
        assert fake_consumer.start.called

    def test_executor_stops_consumer_on_finally(
        self,
        fake_consumer
    ):
        execute(fake_consumer)
        assert fake_consumer.stop.called

    def test_executor_stops_consumer_after_any_exception(
        self,
        fake_consumer
    ):
        fake_consumer.start.side_effect = Exception('boom')
        with pytest.raises(Exception):
            execute(fake_consumer)
        assert fake_consumer.stop.called

    def test_executor_dont_raise_exception_for_keyboard_interrupt(
        self,
        fake_consumer
    ):
        fake_consumer.start.side_effect = KeyboardInterrupt()
        try:
            execute(fake_consumer)
        except Exception as e:
            pytest.fail('Should not have raised: {}'.format(e))

    def test_executor_stops_consumer_after_a_keyboard_interrupt(
        self,
        fake_consumer
    ):
        fake_consumer.start.side_effect = KeyboardInterrupt()
        execute(fake_consumer)

        assert fake_consumer.stop.called
