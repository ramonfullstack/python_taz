import pytest

from taz.core.matching.common.samples import ProductSamples


@pytest.fixture
def product_dict():
    return ProductSamples.magazineluizaa_sku_144129900()


@pytest.fixture
def save_product(mongo_database, product_dict):
    mongo_database.raw_products.save(product_dict)
