from typing import Dict, List
from unittest.mock import ANY

import pytest
from pymongo.database import Database

from taz.constants import (
    DELETE_ACTION,
    MAGAZINE_LUIZA_SELLER_ID,
    SOURCE_DATASHEET,
    SOURCE_GENERIC_CONTENT,
    SOURCE_HECTOR,
    SOURCE_OMNILOGIC,
    SOURCE_RECLASSIFICATION_PRICE_RULE,
    SOURCE_WAKKO
)
from taz.consumers.datalake.scopes.enriched_product import Scope
from taz.core.matching.common.enriched_products import EnrichedProductSamples


class TestEnrichedProductScope:

    @pytest.fixture
    def scope(self, mock_sku):
        return Scope(mock_sku, MAGAZINE_LUIZA_SELLER_ID)

    @pytest.fixture
    def enriched_product_payload(self):
        return EnrichedProductSamples.magazineluiza_230382400()

    @pytest.fixture
    def mock_sku(self, enriched_product_payload: List):
        return enriched_product_payload[0]['sku']

    @pytest.fixture
    def saved_enriched_product(
        self,
        mongo_database: Database,
        omnilogic_message: Dict,
        enriched_product_payload: List,
        mock_sku: str
    ):
        omnilogic_message.update({
            'sku': mock_sku,
            'seller_id': MAGAZINE_LUIZA_SELLER_ID
        })

        enriched_product_payload.append(omnilogic_message)
        mongo_database.enriched_products.insert_many(enriched_product_payload)


    def test_get_data_should_return_specific_source_and_smartcontent_and_metabooks_sources( # noqa
        self,
        saved_enriched_product,
        mock_sku,
        scope
    ):
        data = scope.get_data()

        assert len(data) == 3

    def test_when_source_is_empty_then_should_return_all_sources_from_enriched_product( # noqa
        self,
        mongo_database,
        mock_sku,
        scope
    ):

        mongo_database.enriched_products.insert_many([
            {
                'sku': mock_sku,
                'seller_id': MAGAZINE_LUIZA_SELLER_ID,
                'source': SOURCE_WAKKO
            },
            {
                'sku': mock_sku,
                'seller_id': MAGAZINE_LUIZA_SELLER_ID,
                'source': SOURCE_HECTOR
            }
        ])

        data = scope.get_data()

        assert len(data) == 2

    def test_get_data_returns_empty_result(
        self,
        mock_sku,
        scope
    ):
        assert not scope.get_data()

    def test_get_data_should_returns_payload_without_metadata(
        self,
        mongo_database,
        mock_sku,
        scope
    ):
        payload = {
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'source': SOURCE_OMNILOGIC,
            'sku': mock_sku,
            'navigation_id': '9452723',
            'category_id': 'CP',
            'timestamp': 1638392769.0682776
        }

        mongo_database.enriched_products.insert_one(payload)
        payload.pop('_id', None)
        payload.update({
            'identifier': None,
            'from': {},
            'rule_id': None,
            'product_type': None,
            'active': True,
            'price': 0.0
        })

        enriched_product = scope.get_data()

        assert enriched_product == [{
            'metadata': {'code_anatel': None},
            **payload
        }]

    def test_get_data_with_timestamp_string_should_returns_payload_with_timestamp_float( # noqa
        self,
        mongo_database,
        mock_sku,
        scope
    ):
        payload = {
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'source': SOURCE_OMNILOGIC,
            'sku': mock_sku,
            'navigation_id': '9452723',
            'category_id': 'CP',
            'timestamp': '1638392769.0682776',
            'active': True
        }
        mongo_database.enriched_products.insert_one(payload)
        payload.pop('_id', None)
        payload.update({
            'identifier': None,
            'from': {},
            'rule_id': None,
            'product_type': None,
            'active': True,
            'price': 0.0
        })

        enriched_product = scope.get_data()

        assert enriched_product == [{
            **payload,
            'metadata': {'code_anatel': None},
            'timestamp': 1638392769.0682776
        }]

    def test_all_sources_from_enriched_products_should_return_identifier_field(
        self,
        mongo_database
    ):
        datasheet = EnrichedProductSamples.magazineluiza_sku_0233847_datasheet() # noqa
        ol = EnrichedProductSamples.magazineluiza_sku_0233847()
        smartcontent = EnrichedProductSamples.magazineluiza_sku_0233847_smartcontent() # noqa

        mongo_database.enriched_products.insert_many(
            [datasheet, ol, smartcontent]
        )

        enriched_product = Scope(
            '023384700',
            MAGAZINE_LUIZA_SELLER_ID
        ).get_data()

        assert len(enriched_product) == 3
        for e in enriched_product:
            if e['source'] == SOURCE_DATASHEET:
                assert e['identifier'] == datasheet['identifier']
            else:
                assert e['identifier'] is None

    def test_when_is_payload_to_remove_price_rule(
        self,
        mock_sku
    ):
        payload = {
            'sku': mock_sku,
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'source': SOURCE_RECLASSIFICATION_PRICE_RULE,
            'active': False,
            'navigation_id': '9452723',
            'identifier': None,
            'timestamp': ANY,
            'from': {},
            'product_type': None,
            'rule_id': None,
            'metadata': {'code_anatel': None},
            'price': 0.0
        }

        enriched_product = Scope(
            mock_sku,
            MAGAZINE_LUIZA_SELLER_ID,
            source=SOURCE_RECLASSIFICATION_PRICE_RULE,
            action=DELETE_ACTION,
            navigation_id='9452723'
        ).get_data()

        assert enriched_product == [payload]

    def test_get_data_should_return_active_field_for_all_enriched_sources(
        self,
        saved_enriched_product,
        mongo_database,
        mock_sku,
        scope
    ):
        generic = EnrichedProductSamples.generic_content_sku_fd3e322aab()
        generic['sku'] = mock_sku
        generic['seller_id'] = MAGAZINE_LUIZA_SELLER_ID
        generic['active'] = False
        mongo_database.enriched_products.insert_one(generic)

        enriched_products = scope.get_data()

        assert len(enriched_products) == 4

        for e in enriched_products:
            if e['source'] == SOURCE_GENERIC_CONTENT:
                assert not e['active']
            else:
                assert e['active']

    def test_get_data_of_reclassification_should_return_from_product_type_and_rule_id(  # noqa
        self,
        mongo_database,
        mock_sku,
        scope
    ):
        enriched_product = EnrichedProductSamples.magazineluiza_sku_213445900_reclassification_price_rule()  # noqa
        enriched_product.update({
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'sku': mock_sku,
            'navigation_id': mock_sku
        })
        mongo_database.enriched_products.insert_one(enriched_product)

        enriched_product.pop('_id', None)
        enriched_product.update({
            'identifier': None,
            'metadata': {'code_anatel': None},
            'active': True,
            'price': 0.01
        })
        enriched_products = scope.get_data()

        assert enriched_products == [enriched_product]
