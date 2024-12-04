import pytest

from taz.consumers import main as consumers
from taz.main import parser
from taz.pollers import main as pollers


class TestTazParsers:

    @pytest.fixture
    def taz_parser(self):
        return parser

    @pytest.mark.parametrize(
        'command, expected_handler', [
            ('consumer media', consumers.media_handler),
            ('consumer factsheet', consumers.factsheet_handler),
            ('consumer product', consumers.product_handler),
            ('consumer product_writer', consumers.product_writer_handler),
            ('consumer product_exporter', consumers.product_exporter_handler),
            ('consumer product_score', consumers.product_score_handler),
            ('consumer category', consumers.category_handler),
            ('consumer price_3p', consumers.price_3p_handler),
            ('consumer stock_3p', consumers.stock3p_handler),
            ('consumer matching', consumers.matching_handler),
            ('consumer matching_product', consumers.matching_product_handler),
            ('consumer rebuild', consumers.rebuild_handler),
            ('poller factsheet', pollers.factsheet_handler),
            ('poller product', pollers.product_handler),
            ('poller category', pollers.category_handler),
            ('poller price', pollers.price_handler)
        ]
    )
    def test_parser_get_right_handler(self, command, expected_handler):
        args = parser.parse_args(command.split())
        assert args.handler is expected_handler
