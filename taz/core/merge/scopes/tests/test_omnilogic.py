from unittest.mock import patch

import pytest
from simple_settings.utils import settings_stub

from taz.constants import MAGAZINE_LUIZA_SELLER_ID, PRODUCT_ORIGIN
from taz.consumers.core.exceptions import NotFound
from taz.core.matching.common.enriched_products import EnrichedProductSamples
from taz.core.matching.common.samples import ProductSamples
from taz.core.merge.merger import Merger
from taz.core.merge.scopes.omnilogic import OmnilogicScope


class TestOminilogicScope:

    @pytest.fixture
    def omnilogic(self, normalized_payload, raw_product):
        return OmnilogicScope(raw_product, normalized_payload)

    @pytest.fixture
    def scope_omnilogic_origin_product(self, normalized_payload, raw_product):
        return OmnilogicScope(
            raw_product,
            normalized_payload,
            origin=PRODUCT_ORIGIN
        )

    @pytest.fixture
    def merger(self, normalized_payload, raw_product):
        return Merger(raw_product, normalized_payload, 'update')

    @pytest.fixture
    def patch_get_original_product(self):
        return patch.object(OmnilogicScope, 'get_original_product')

    @pytest.mark.parametrize('seller_id, title, product_name, sku_name, reference, source, expected_title, expected_reference', [  # noqa
        (
            'murcho',
            'Fritadeira sem óleo Air fryer inox 1.500w capacidade 2,5 litros (110V)',  # noqa
            'Fritadeira Elétrica Gourmet CE13 Multilaser Preto 2,5L',
            '',
            '',
            None,
            'Fritadeira Elétrica Gourmet CE13 Multilaser Preto 2,5L',
            ''
        ),
        (
            'magazineluiza',
            'Fritadeira sem óleo Air fryer inox 1.500w capacidade 2,5 litros (110V)',  # noqa
            'Fritadeira Elétrica Gourmet CE13 Multilaser Preto 2,5L',
            '',
            'Câm 12MP + Selfie 5MP Tela 5.1” Quad HD Octa Core',
            None,
            'Fritadeira sem óleo Air fryer inox 1.500w capacidade 2,5 litros (110V)',  # noqa
            'Câm 12MP + Selfie 5MP Tela 5.1” Quad HD Octa Core'
        ),
        (
            'murcho',
            'Fritadeira sem óleo Air fryer',  # noqa
            'Fritadeira Elétrica Gourmet CE13 Multilaser Preto 2,5L',
            '',
            '',
            None,
            'Fritadeira Elétrica Gourmet CE13 Multilaser Preto 2,5L',
            ''
        ),
        (
            'magazineluiza',
            'Fritadeira sem óleo Air',  # noqa
            'Fritadeira Elétrica Gourmet CE13 Multilaser Preto 2,5L',
            '',
            '',
            None,
            'Fritadeira sem óleo Air',
            ''
        ),
        (
            'magazineluiza',
            'Fritadeira sem óleo Air fryer inox 1.500w capacidade 2,5 litros (110V)',  # noqa
            'Fritadeira Elétrica Gourmet CE13 Multilaser Preto 2,5L',
            '',
            '',
            'magalu',
            'Fritadeira sem óleo Air fryer inox 1.500w capacidade 2,5 litros (110V)',  # noqa
            ''
        ),
        (
            'magazineluiza',
            'Fritadeira sem óleo Air fryer inox 1.500w capacidade 2,5 litros (110V)',  # noqa
            None,
            None,
            '',
            None,
            'Fritadeira sem óleo Air fryer inox 1.500w capacidade 2,5 litros (110V)',  # noqa
            ''
        ),
        (
            'magazineluiza',
            'Água Micelar L\'Óréal Solução de Limpeza 5 em 1',
            'Água Micelar L\'Óréal Solução de Limpeza 5 em 1',
            '100 ml',
            '',
            None,
            'Água Micelar L\'Óréal Solução de Limpeza 5 em 1',  # noqa
            ''
        ),
        (
            'murcho',
            'Água Micelar L\'Óréal Solução de Limpeza 5 em 1',
            'Água Micelar L\'Óréal Solução de Limpeza 5 em 1',
            '100 ml',
            '',
            None,
            'Água Micelar L\'Óréal Solução de Limpeza 5 em 1',  # noqa
            '100 ml'
        ),
    ])
    def test_normalize_title(
        self,
        normalized_payload,
        raw_product,
        omnilogic,
        seller_id,
        title,
        product_name,
        sku_name,
        reference,
        source,
        expected_title,
        expected_reference
    ):
        raw_product['seller_id'] = seller_id
        raw_product['title'] = title
        raw_product['reference'] = reference

        if source:
            raw_product['source'] = source

        normalized_payload['product_name'] = product_name
        normalized_payload['sku_name'] = sku_name

        omnilogic._normalize_title()

        assert omnilogic.raw_product['title'] == expected_title
        assert omnilogic.raw_product['reference'] == expected_reference

    def test_should_get_normalized_brand_from_marca(
        self,
        normalized_payload,
        raw_product,
        omnilogic,
        logger_stream
    ):
        normalized_payload['metadata']['Marca'] = 'Samsung'
        raw_product['brand'] = 'Apple'
        omnilogic._normalize_brand()

        assert omnilogic.raw_product['brand'] == 'Apple'

    def test_should_get_normalized_attributes(self, omnilogic):
        expected_attributes = [
            {
                'value': '32GB',
                'type': 'capacity'
            },
            {
                'value': 'Preto',
                'type': 'color'
            }
        ]
        omnilogic._normalize_attributes()

        assert omnilogic.raw_product['attributes'] == expected_attributes

    @settings_stub(KEEP_CATEGORIES_ATTRIBUTES=[])
    def test_should_slugify_in_attribute_not_exists_from_specification(
        self,
        omnilogic
    ):
        omnilogic.enriched_product = {
            'metadata': {'Tom de Pele': 'Castanho Escuro'},
            'sku_metadata': ['Tom de Pele'],
            'category_id': 'RC'
        }

        omnilogic._normalize_attributes()

        assert omnilogic.raw_product['attributes'] == [{
            'type': 'tom-de-pele',
            'value': 'Castanho Escuro'
        }]

    @settings_stub(KEEP_CATEGORIES_ATTRIBUTES=[])
    def test_should_normalize_original_attributes_when_sku_metadata_is_empty( # noqa
        self,
        omnilogic,
        patch_storage_manager_get_json
    ):
        raw_product_mock = ProductSamples.ateliefestaemagia_sku_4795_251()
        enriched_product_mock = EnrichedProductSamples.ateliefestaemagia_sku_4795_251()  # noqa

        omnilogic.enriched_product = enriched_product_mock
        omnilogic.raw_product = raw_product_mock

        expect_attributes = [
            {'type': 'color', 'value': 'preto'},
            {'type': 'size', 'value': '5'}
        ]

        with patch_storage_manager_get_json as mock_storage:
            mock_storage.return_value = {'attributes': expect_attributes}
            omnilogic._normalize_attributes()

        assert omnilogic.raw_product['attributes'] == expect_attributes

    @settings_stub(KEEP_CATEGORIES_ATTRIBUTES=['AF'])
    def test_should_normalize_original_attributes_when_has_category_in_keep_categories_attributes( # noqa
        self,
        omnilogic,
        patch_storage_manager_get_json
    ):
        raw_product_mock = ProductSamples.ateliefestaemagia_sku_4795_251()
        enriched_product_mock = EnrichedProductSamples.ateliefestaemagia_sku_4795_251()  # noqa
        enriched_product_mock['sku_metadata'] = ['Tema']
        omnilogic.enriched_product = enriched_product_mock
        omnilogic.raw_product = raw_product_mock

        expect_attributes = [
            {'type': 'color', 'value': 'preto'},
            {'type': 'size', 'value': '5'}
        ]

        with patch_storage_manager_get_json as mock_storage:
            mock_storage.return_value = {'attributes': expect_attributes}
            omnilogic._normalize_attributes()

        assert omnilogic.raw_product['attributes'] == expect_attributes

    @settings_stub(KEEP_CATEGORIES_ATTRIBUTES=[])
    def test_should_normalize_attributes_with_empty_values(
        self,
        omnilogic,
        patch_storage_manager_get_json
    ):
        raw_product_mock = ProductSamples.ateliefestaemagia_sku_4795_251()
        enriched_product_mock = EnrichedProductSamples.ateliefestaemagia_sku_4795_251()  # noqa

        omnilogic.enriched_product = enriched_product_mock
        omnilogic.raw_product = raw_product_mock

        with patch_storage_manager_get_json as mock_storage:
            mock_storage.return_value = {'attributes': []}
            omnilogic._normalize_attributes()

        assert not omnilogic.raw_product['attributes']

    @settings_stub(KEEP_CATEGORIES_ATTRIBUTES=[])
    def test_return_the_same_attributes_when_receive_exception_read_bucket(
        self,
        omnilogic,
        patch_storage_manager_get_json
    ):
        raw_product_mock = ProductSamples.ateliefestaemagia_sku_4795_251()
        enriched_product_mock = EnrichedProductSamples.ateliefestaemagia_sku_4795_251()  # noqa

        omnilogic.enriched_product = enriched_product_mock
        omnilogic.raw_product = raw_product_mock

        with patch_storage_manager_get_json as mock_storage:
            mock_storage.side_effect = NotFound()
            omnilogic._normalize_attributes()

        assert raw_product_mock['attributes'] == omnilogic.raw_product['attributes']  # noqa

    def test_should_keep_missing_attributes_type_for_md_category(
        self,
        omnilogic
    ):
        expected_attributes = [{'type': 'size', 'value': 'G'}]
        omnilogic.raw_product['categories'][0]['id'] = 'MD'
        omnilogic.raw_product['attributes'] = [{'value': 'G', 'type': 'size'}]
        omnilogic.raw_product['seller_id'] = 'zattini'

        omnilogic.enriched_product['category_id'] = 'MD'

        omnilogic._normalize_attributes()

        assert omnilogic.raw_product['attributes'] == expected_attributes

    def test_apply_omnilogic_should_use_original_title(
        self,
        omnilogic,
        normalized_payload,
        raw_product,
        patch_pubsub_client
    ):
        raw_product.update(seller_id='xablau')
        normalized_payload.update(product_name=None, seller_id='xablau')

        omnilogic.raw_product = raw_product
        omnilogic.enriched_product = normalized_payload

        with patch_pubsub_client:
            omnilogic.apply()

        assert omnilogic.raw_product['title'] is not None
        assert omnilogic.raw_product['title'] != omnilogic.enriched_product['product_name']  # noqa
        assert omnilogic.raw_product['seller_id'] != MAGAZINE_LUIZA_SELLER_ID

    @pytest.mark.parametrize('keep_categories,enable_enrichment', [
        (['*'], False),
        (['AF'], True),
        (['TE'], False),
    ])
    def test_should_enable_enrichment_scope_omnilogic(
        self,
        keep_categories,
        enable_enrichment,
        omnilogic
    ):
        with settings_stub(KEEP_CATEGORIES_ATTRIBUTES=keep_categories):
            assert omnilogic._enable_enrichment() == enable_enrichment

    def test_when_normalize_brand_with_origin_consumer_product_then_not_change_value(  # noqa
        self,
        scope_omnilogic_origin_product,
        patch_get_original_product
    ):
        with patch_get_original_product as mock_get_original_product:
            scope_omnilogic_origin_product._normalize_brand()

        mock_get_original_product.assert_not_called()

    def test_when_normalize_attributes_with_origin_consumer_product_then_not_change_value(  # noqa
        self,
        scope_omnilogic_origin_product,
        patch_get_original_product
    ):
        with patch_get_original_product as mock_get_original_product:
            scope_omnilogic_origin_product._normalize_attributes()

        mock_get_original_product.assert_not_called()
