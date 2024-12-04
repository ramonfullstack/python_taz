import pytest
from simple_settings.utils import settings_stub

from taz.core.matching.common.enriched_products import EnrichedProductSamples
from taz.core.matching.common.samples import ProductSamples
from taz.core.merge.scopes.wakko import WakkoScope


class TestWakkoScope:

    @pytest.fixture
    def product(self):
        return ProductSamples.lt2shop_sku_0000998113()

    @pytest.fixture
    def enriched_product(self):
        return EnrichedProductSamples.lt2shop_sku_0000998113()

    @pytest.fixture
    def wakko(self, product, enriched_product):
        return WakkoScope(product, enriched_product)

    def test_should_get_normalized_brand(
        self,
        wakko,
        product,
        enriched_product
    ):
        expected_brand = 'Novo Século'

        assert wakko.raw_product['brand'] != expected_brand

        enriched_product['metadata']['normalized'] = {
            'Marca': [expected_brand]
        }

        wakko._normalize_brand()

        assert wakko.raw_product['brand'] == expected_brand

    @pytest.mark.parametrize('attributes, normalized, expected', [
        (
            [{
                'type': 'volume',
                'value': '50 ml'
            }, {
                'type': 'weight',
                'value': '90 g'
            }],
            {
                'Volume': ['50ml'],
                'Peso': ['90g'],
            },
            [{
                'type': 'volume',
                'value': '50ml'
            }, {
                'type': 'weight',
                'value': '90g'
            }]
        ),
        (
            [{
                'type': 'volume',
                'value': '50 ml'
            }, {
                'type': 'weight',
                'value': '90 g'
            }, {
                'type': 'test',
                'value': 'Novo'
            }],
            {
                'Volume': ['50ml'],
                'Peso': ['90g'],
            },
            [{
                'type': 'volume',
                'value': '50ml'
            }, {
                'type': 'weight',
                'value': '90g'
            }, {
                'type': 'test',
                'value': 'Novo'
            }]
        ),
        (
            [{
                'type': 'volume',
                'value': '50 ML'
            }, {
                'type': 'weight',
                'value': '90 G'
            }],
            {
                'Volume': ['50ml'],
                'Editora': ['Magalu']
            },
            [{
                'type': 'volume',
                'value': '50ml'
            }, {
                'type': 'weight',
                'value': '90 G'
            }]
        ),
        (
            [{
                'type': 'volume',
                'value': '50ml'
            }, {
                'type': 'weight',
                'value': '90g'
            }],
            {
                'Quantity': ['1 unidade'],
                'Marca': ['Novo Século']
            },
            [{
                'type': 'volume',
                'value': '50ml'
            }, {
                'type': 'weight',
                'value': '90g'
            }]
        ),
        (
            [],
            {
                'Quantity': ['1 unidade'],
                'Marca': ['Novo Século']
            },
            []
        ),
        (
            [],
            {},
            []
        ),
        (
            [{
                'type': 'color',
                'value': 'Branco+Preto'
            }],
            {
                'Cor': ['Branco', 'Preto']
            },
            [{
                'type': 'color',
                'value': 'Branco, Preto'
            }]
        ),
    ])
    def test_should_normalize_attributes(
        self,
        wakko,
        product,
        attributes,
        normalized,
        expected
    ):
        product['attributes'] = attributes

        enriched_product = {
            'metadata': {
                'normalized': normalized
            },
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'navigation_id': product['navigation_id'],
            'source': 'wakko'
        }

        wakko.enriched_product = enriched_product
        wakko._normalize_attributes()

        assert wakko.raw_product['attributes'] == expected

    @settings_stub(ENABLE_WAKKO_SCOPE=True)
    def test_should_do_nothing_for_disable_wakko_scope(
        self,
        wakko,
        product,
        enriched_product
    ):
        wakko.apply()
        assert wakko.raw_product == ProductSamples.lt2shop_sku_0000998113()
