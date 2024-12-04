from unittest.mock import patch

import pytest

from taz.pollers.category.poller import CategoryPoller
from taz.pollers.factsheet.poller import FactsheetPoller
from taz.pollers.main import (
    category_handler,
    factsheet_handler,
    price_handler,
    product_handler
)
from taz.pollers.price.poller import PricePoller
from taz.pollers.product.poller import ProductPoller


class TestPollersHandlers:

    @pytest.fixture
    def patch_executor(self):
        return patch('taz.pollers.main.execute')

    @pytest.mark.parametrize(
        'handler,poller', [
            (product_handler, ProductPoller),
            (category_handler, CategoryPoller),
            (price_handler, PricePoller),
            (factsheet_handler, FactsheetPoller)
        ]
    )
    def test_call_poller_executor_with_right_poller_class(
        self, patch_executor, handler, poller
    ):
        with patch_executor as mock:
            handler(None)

        executor_arg = mock.call_args[0][0]
        assert isinstance(executor_arg, poller)
