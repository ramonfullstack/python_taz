import pytest

from taz.core.matching.common.samples import ProductSamples


@pytest.fixture
def product():
    return ProductSamples.magazineluiza_sku_0233847()


@pytest.fixture
def save_product(mongo_database, product):
    mongo_database.raw_products.save(product)


@pytest.fixture
def save_medias(mongo_database, product):
    media = {
        'images': [
            'd2e14e48997a911745931e6a2991b2cf.jpg'
        ],
        'seller_id': product['seller_id'],
        'sku': product['sku']
    }

    mongo_database.medias.save(media)
