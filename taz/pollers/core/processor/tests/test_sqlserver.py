from datetime import datetime
from decimal import Decimal

import pytest

from taz.pollers.partner.poller import PartnerPoller
from taz.pollers.product.converter import ProductType
from taz.pollers.product.poller import ProductPoller


class TestSqlServerPoller:

    @pytest.fixture
    def product_data(self):
        return {
            'batch_key': '02',
            'ean': '0841667100531',
            'sku': '12345678',
            'parent_sku': '12345678',
            'main_variation': 1,
            'product_type': ProductType.product.value,
            'title': 'Kindle Paperwhite Wi-Fi 4GB Tela 6',
            'description': 'Especialmente feito para os amantes da leitura',
            'reference': 'Amazon',
            'brand': 'amazon',
            'sold_count': 35,
            'review_count': 12,
            'review_score': Decimal(4.5),
            'category_id': 'TB',
            'subcategory_id': 'KIND',
            'width': Decimal(1.0),
            'height': Decimal(1.8399999999999999),
            'depth': Decimal(0.1477777777),
            'weight': Decimal(0.44),
            'voltage': 'Bivolt',
            'color': 'Azul',
            'specification_id': 5,
            'specification_description': '16 GB',
            'release_date': datetime.now(),
            'updated_at': datetime.now(),
            'created_at': datetime.now(),
            'extra_categories': 'EL;LEDD|TB;TAA1|TB;TBB2|TB;TCC3|EL;WIFI',
            'selections': '0;13358|0;13400|24;13401|69;13414',
            'bundles': '1766084;00;179.00;1|2017461;00;95.00;1',
            'gift_product': '150658700',
            'active': True
        }

    @pytest.fixture
    def partner_data(self):
        return {
            'batch_key': '01',
            'id': '01234',
            'strdescricao': 'bacon ipsum'
        }

    def test_format_latest_run_message_should_work_for_product(
        self,
        product_data
    ):
        message = ProductPoller._format_latest_run_message(
            data=product_data,
            latest_batch_cursor_key='any-product-key'
        )

        assert message == 'Skipping batch 02 for product 12345678. Reason: seeking batch any-product-key from latest run'  # noqa

    def test_format_latest_run_message_should_work_for_partner(
        self,
        partner_data
    ):
        message = PartnerPoller._format_latest_run_message(
            data=partner_data,
            latest_batch_cursor_key='any-partner-key'
        )

        assert message == 'Skipping batch 01 for partner . Reason: seeking batch any-partner-key from latest run'  # noqa
