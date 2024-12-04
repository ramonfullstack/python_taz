import pytest

from taz import constants
from taz.api.prices.models import PriceModel
from taz.api.products.models import RawProductModel
from taz.consumers.matching.consumer import MatchingRecordProcessor
from taz.core.matching.common.samples import ProductSamples


@pytest.fixture
def matching_consumer():
    return MatchingRecordProcessor(
        persist_changes=False,
        exclusive_strategy=False
    )


@pytest.fixture
def save_buybox_product():
    variations = [
        ProductSamples.magazineluiza_sku_011704400(),
        ProductSamples.cookeletroraro_sku_2000159(),
        ProductSamples.magazineluiza_sku_011704500(),
        ProductSamples.whirlpool_sku_335(),
    ]

    for variation in variations:
        variation['matching_strategy'] = constants.AUTO_BUYBOX_STRATEGY
        RawProductModel(**variation).save()

        price = {
            'sku': variation['sku'],
            'seller_id': variation['seller_id'],
            'list_price': '234.56',
            'price': '123.45',
            'delivery_availability': 'nationwide',
            'stock_count': 321,
            'stock_type': 'on_seller'
        }

        PriceModel(**price).save()

    return variation


@pytest.fixture
def save_buybox_unified(matching_consumer, save_buybox_product):
    variation = save_buybox_product

    message = {
        'action': 'update',
        'sku': variation['sku'],
        'seller_id': variation['seller_id'],
        'task_id': '186e1006ae3541128b6055b99bab7ca1',
        'timestamp': 0.1
    }

    matching_consumer.persist_changes = True
    matching_consumer.process_message(message)
