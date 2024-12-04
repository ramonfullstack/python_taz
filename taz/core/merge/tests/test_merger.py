from unittest.mock import patch

import pytest
from simple_settings.utils import settings_stub

from taz import constants
from taz.constants import (
    CHESTER_STRATEGY,
    OMNILOGIC_STRATEGY,
    SINGLE_SELLER_STRATEGY,
    SOURCE_OMNILOGIC,
    UPDATE_ACTION
)
from taz.core.matching.common.enriched_products import EnrichedProductSamples
from taz.core.matching.common.samples import ProductSamples
from taz.core.merge.category import CategoryMerger
from taz.core.merge.factsheet import FactsheetMerger
from taz.core.merge.merger import Merger
from taz.helpers.json import json_dumps


class TestMerger:

    @pytest.fixture
    def merger(self, normalized_payload, raw_product):
        return Merger(raw_product, normalized_payload, UPDATE_ACTION)

    @pytest.fixture
    def patch_factsheet_merger_merge(self):
        return patch.object(FactsheetMerger, 'merge')

    @pytest.fixture
    def patch_raw_products(self):
        return patch.object(Merger, 'raw_products')

    def test_should_merge_payload(
        self,
        merger,
        raw_product,
        save_raw_product,
        config_settings,
        patch_kinesis_put,
        patch_storage_manager_upload,
        patch_factsheet_merger_merge
    ):
        with patch_kinesis_put, patch_storage_manager_upload:
            with patch_factsheet_merger_merge as mock_merger_factsheet:
                merger.merge()

        assert merger.raw_product['source'] == 'magalu'
        assert merger.raw_product['product_hash'] == merger.enriched_product['product_hash']  # noqa
        assert mock_merger_factsheet.called_with(
            sku=raw_product['sku'],
            seller_id=raw_product['seller_id']
        )

    def test_merger_without_product_hash(
        self,
        merger,
        raw_product,
        save_raw_product,
        config_settings,
        patch_kinesis_put,
        patch_storage_manager_upload,
        patch_factsheet_merger_merge
    ):
        with patch_kinesis_put, patch_storage_manager_upload:
            with patch_factsheet_merger_merge:
                merger.enriched_product['product_hash'] = None
                merger.merge()

        assert 'source' not in merger.raw_product
        assert 'product_hash' not in merger.raw_product

        assert merger.raw_product['matching_strategy'] == constants.SINGLE_SELLER_STRATEGY  # noqa

    def test_merger_not_normalize_magazineluiza_attributes(
        self,
        mongo_database,
        patch_kinesis_put,
        patch_storage_manager_get_json,
        patch_storage_manager_upload,
        patch_factsheet_merger_merge
    ):
        product = ProductSamples.magazineluiza_sku_0233847()
        mongo_database.raw_products.insert_one(product)

        enriched_product = EnrichedProductSamples.magazineluiza_sku_0233847()
        enriched_product['product_hash'] = None
        enriched_product['sku_metadata'] = []

        mongo_database.enriched_products.insert_one(enriched_product)

        with patch_kinesis_put:
            with patch_storage_manager_get_json as mock_storage:
                with patch_storage_manager_upload:
                    with patch_factsheet_merger_merge:
                        mock_storage.return_value = None
                        merger = Merger(
                            product,
                            enriched_product,
                            UPDATE_ACTION
                        )
                        merger.merge()

        raw_product = mongo_database.raw_products.find_one()

        product = ProductSamples.magazineluiza_sku_0233847()
        assert raw_product['attributes'] == product['attributes']

    def test_merger_enriched_product_from_books(
        self,
        mongo_database,
        patch_kinesis_put,
        patch_storage_manager_upload,
        patch_factsheet_merger_merge
    ):
        product = ProductSamples.lt2shop_sku_0000998113()
        mongo_database.raw_products.insert_one(product)

        enriched_product = EnrichedProductSamples.lt2shop_sku_0000998113()
        mongo_database.enriched_products.insert_one(enriched_product)

        with patch_kinesis_put, patch_storage_manager_upload:
            with patch_factsheet_merger_merge:
                merger = Merger(product, enriched_product, UPDATE_ACTION)
                merger.merge()

        raw_product = mongo_database.raw_products.find_one()
        assert raw_product['title'] == 'Livro - {}'.format(
            enriched_product['title']
        )
        assert raw_product['product_type'] == enriched_product['entity']
        assert raw_product['description'] == enriched_product['description']

    def test_merger_enriched_book_product_not_enriched_by_metabooks(
        self,
        mongo_database,
        patch_kinesis_put,
        patch_storage_manager_upload,
        patch_pubsub_client,
        patch_factsheet_merger_merge
    ):
        product = ProductSamples.lt2shop_sku_0000998113()
        mongo_database.raw_products.insert_one(product)

        enriched_product = {
            'sku': product['sku'],
            'entity': 'Livro',
            'metadata': {
                'Editora': 'Summus Editorial'
            },
            'seller_id': product['seller_id'],
            'navigation_id': '6426142',
            'category_id': 'LI',
            'subcategory_ids': [
                'LIMM'
            ],
            'product_hash': None,
            'product_name': None,
            'product_matching_metadata': [],
            'product_name_metadata': [],
            'sku_metadata': [],
            'filters_metadata': [
                'Editora'
            ],
            'source': 'magalu'
        }
        mongo_database.enriched_products.insert_one(enriched_product)

        with patch_kinesis_put, patch_pubsub_client:
            with patch_storage_manager_upload:
                with patch_factsheet_merger_merge:
                    merger = Merger(product, enriched_product, UPDATE_ACTION)
                    merger.merge()

        raw_product = mongo_database.raw_products.find_one()
        assert raw_product['title'] == product['title']
        assert raw_product['description'] == product['description']
        assert raw_product['brand'] != enriched_product['metadata']['Editora']  # noqa
        assert raw_product['main_category'] == {
            'id': enriched_product['category_id'],
            'subcategory': {'id': enriched_product['subcategory_ids'][0]}
        }
        assert raw_product['product_type'] == enriched_product['entity']

    def test_should_set_source_from_pickupstore(
        self,
        mongo_database,
        patch_kinesis_put,
        patch_storage_manager_upload,
        patch_factsheet_merger_merge
    ):
        product = ProductSamples.magazineluizaa_sku_144129900()
        mongo_database.raw_products.insert_one(product)

        enriched_product = {
            'sku': '144129900',
            'entity': 'Panela',
            'metadata': {
                'Material ': 'Alumínio',
                'Marca': 'Tramontina',
                'Cor': 'Alumínio,Vermelho',
                'Quantidade': '10'
            },
            'seller_id': 'magazineluiza',
            'navigation_id': '144129900',
            'category_id': 'UD',
            'subcategory_ids': [
                'PANL'
            ],
            'product_hash': None,
            'product_name': None,
            'product_matching_metadata': [],
            'product_name_metadata': [],
            'sku_metadata': [],
            'filters_metadata': [
                'Marca',
                'Cor',
                'Material ',
                'Revestimento',
                'Capacidade',
                'Características',
                'Quantidade'
            ],
            'source': 'api_luiza_pickupstore',
            'timestamp': 1559044922.6178071
        }
        mongo_database.enriched_products.insert_one(enriched_product)

        with patch_kinesis_put:
            with patch_storage_manager_upload:
                with patch_factsheet_merger_merge:
                    merger = Merger(product, enriched_product, UPDATE_ACTION)
                    merger.merge()

        raw_product = mongo_database.raw_products.find_one()

        assert raw_product['store_pickup_available'] is True

    def test_should_not_set_pickupstore_source_if_do_not_find_enriched_product(
        self,
        mongo_database,
        patch_kinesis_put,
        patch_storage_manager_upload,
        patch_factsheet_merger_merge
    ):
        product = ProductSamples.magazineluizaa_sku_144129900()
        mongo_database.raw_products.insert_one(product)

        enriched_product = {
            'sku': '0998113',
            'entity': 'Livro',
            'metadata': {
                'Editora': 'Summus Editorial'
            },
            'seller_id': product['seller_id'],
            'navigation_id': '6426142',
            'category_id': 'LI',
            'subcategory_ids': [
                'LIMM'
            ],
            'product_hash': None,
            'product_name': None,
            'product_matching_metadata': [],
            'product_name_metadata': [],
            'sku_metadata': [],
            'filters_metadata': [
                'Editora'
            ],
            'source': 'magalu'
        }
        mongo_database.enriched_products.insert_one(enriched_product)

        with patch_kinesis_put:
            with patch_storage_manager_upload:
                with patch_factsheet_merger_merge:
                    merger = Merger(product, enriched_product, UPDATE_ACTION)
                    merger.merge()

        raw_product = mongo_database.raw_products.find_one()

        assert raw_product['store_pickup_available'] is False

    def test_should_not_set_source_pickupstore_for_product_3p(
        self,
        mongo_database,
        patch_kinesis_put,
        patch_storage_manager_upload,
        patch_pubsub_client,
        patch_factsheet_merger_merge
    ):

        product = ProductSamples.lt2shop_sku_0000998113()
        mongo_database.raw_products.insert_one(product)

        enriched_product = {
            'sku': product['sku'],
            'entity': 'Livro',
            'metadata': {
                'Editora': 'Summus Editorial'
            },
            'seller_id': product['seller_id'],
            'navigation_id': '6426142',
            'category_id': 'LI',
            'subcategory_ids': [
                'LIMM'
            ],
            'product_hash': None,
            'product_name': None,
            'product_matching_metadata': [],
            'product_name_metadata': [],
            'sku_metadata': [],
            'filters_metadata': [
                'Editora'
            ],
            'source': 'magalu'
        }
        mongo_database.enriched_products.insert_one(enriched_product)

        with patch_kinesis_put, patch_storage_manager_upload:
            with patch_pubsub_client:
                with patch_factsheet_merger_merge:
                    merger = Merger(
                        product,
                        enriched_product,
                        UPDATE_ACTION
                    )
                    merger.merge()

        raw_product = mongo_database.raw_products.find_one()

        assert raw_product.get('store_pickup_available') is None

    def test_should_set_delivery_plus_1(
        self,
        mongo_database,
        patch_kinesis_put,
        patch_storage_manager_upload,
        patch_pubsub_client,
        patch_factsheet_merger_merge
    ):
        product = ProductSamples.magazineluizaa_sku_144129900()
        mongo_database.raw_products.insert_one(product)

        enriched_product = {
            'sku': '144129900',
            'entity': 'Panela',
            'seller_id': 'magazineluiza',
            'source': constants.SOURCE_API_LUIZA_EXPRESS_DELIVERY,
            'delivery_days': 1,
            'category_id': 'LI',
            'subcategory_ids': [
                'LIMM'
            ]
        }

        mongo_database.enriched_products.insert_one(enriched_product)

        with patch_kinesis_put, patch_storage_manager_upload:
            with patch_pubsub_client, patch_factsheet_merger_merge:
                merger = Merger(product, enriched_product, UPDATE_ACTION)
                merger.merge()

        raw_product = mongo_database.raw_products.find_one()

        assert raw_product['delivery_plus_1'] is True
        assert raw_product['delivery_plus_2'] is False

    def test_should_set_delivery_plus_2(
        self,
        mongo_database,
        patch_kinesis_put,
        patch_storage_manager_upload,
        patch_pubsub_client,
        patch_factsheet_merger_merge
    ):
        product = ProductSamples.magazineluizaa_sku_144129900()
        mongo_database.raw_products.insert_one(product)

        enriched_product = {
            'sku': '144129900',
            'entity': 'Panela',
            'seller_id': 'magazineluiza',
            'source': constants.SOURCE_API_LUIZA_EXPRESS_DELIVERY,
            'delivery_days': 2,
            'category_id': 'LI',
            'subcategory_ids': [
                'LIMM'
            ]
        }

        mongo_database.enriched_products.insert_one(enriched_product)

        with patch_kinesis_put:
            with patch_storage_manager_upload:
                with patch_pubsub_client:
                    with patch_factsheet_merger_merge:
                        merger = Merger(
                            product,
                            enriched_product,
                            UPDATE_ACTION
                        )
                        merger.merge()

        raw_product = mongo_database.raw_products.find_one()

        assert raw_product['delivery_plus_1'] is True
        assert raw_product['delivery_plus_2'] is False

    def test_should_not_set_delivery_plus_1_or_delivery_plus_2(
        self,
        mongo_database,
        patch_kinesis_put,
        patch_storage_manager_upload,
        patch_pubsub_client,
        patch_factsheet_merger_merge
    ):
        product = ProductSamples.magazineluizaa_sku_144129900()
        mongo_database.raw_products.insert_one(product)

        enriched_product = {
            'sku': '144129900',
            'entity': 'Panela',
            'seller_id': 'magazineluiza',
            'source': constants.SOURCE_API_LUIZA_EXPRESS_DELIVERY,
            'delivery_days': 4,
            'category_id': 'LI',
            'subcategory_ids': [
                'LIMM'
            ]
        }

        mongo_database.enriched_products.insert_one(enriched_product)

        with patch_kinesis_put:
            with patch_storage_manager_upload:
                with patch_pubsub_client:
                    with patch_factsheet_merger_merge:
                        merger = Merger(
                            product,
                            enriched_product,
                            UPDATE_ACTION
                        )
                        merger.merge()

        raw_product = mongo_database.raw_products.find_one()

        assert 'delivery_plus_1' not in raw_product
        assert 'delivery_plus_2' not in raw_product

    def test_should_merge_without_metadata_in_enriched_products(
        self,
        mongo_database,
        patch_storage_manager_get_file,
        patch_kinesis_put,
        patch_storage_manager_upload,
        patch_pubsub_client,
        patch_factsheet_merger_merge
    ):
        product = ProductSamples.decorvida_sku_5489()
        mongo_database.raw_products.insert_one(product)

        enriched_product = EnrichedProductSamples.decorvida_sku_5489()
        mongo_database.enriched_products.insert_one(enriched_product)

        with patch_storage_manager_get_file as mock_get:
            with patch_kinesis_put, patch_pubsub_client:
                with patch_storage_manager_upload, patch_factsheet_merger_merge:  # noqa
                    mock_get.return_value = json_dumps(
                        {'items': []},
                        ensure_ascii=False
                    )
                    merger = Merger(product, enriched_product, UPDATE_ACTION)
                    merger.merge()

        raw_product = mongo_database.raw_products.find_one()
        assert raw_product['categories'][0]['id'] == enriched_product['category_id']  # noqa

    def test_should_merge_without_entity_in_enriched_products(
        self,
        mongo_database,
        patch_kinesis_put,
        patch_storage_manager_upload,
        patch_pubsub_client,
        patch_factsheet_merger_merge
    ):
        product = ProductSamples.magazineluiza_sku_229221800()
        mongo_database.raw_products.insert_one(product)

        enriched_product = EnrichedProductSamples.magazineluiza_sku_229221800()
        mongo_database.enriched_products.insert_one(enriched_product)

        with patch_kinesis_put, patch_pubsub_client:
            with patch_storage_manager_upload:
                with patch_factsheet_merger_merge:
                    merger = Merger(product, None, UPDATE_ACTION)
                    merger.merge()

        raw_product = mongo_database.raw_products.find_one({}, {'_id': 0})
        assert raw_product == product

    def test_merger_enriched_product_from_wakko(
        self,
        mongo_database,
        patch_kinesis_put,
        patch_pubsub_client,
        patch_storage_manager_upload,
        patch_factsheet_merger_merge
    ):
        product = ProductSamples.lt2shop_sku_0000998113()
        mongo_database.raw_products.insert_one(product)

        enriched_product = EnrichedProductSamples.lt2shop_sku_0000998113()
        enriched_product['source'] = 'wakko'
        enriched_product['metadata']['normalized'] = {
            'Volume': ['90l'],
            'Quantidade': ['1 unidade'],
            'Marca': ['Novo Século']
        }
        mongo_database.enriched_products.insert_one(enriched_product)

        assert product['brand'] == 'Novo seculo'

        with patch_kinesis_put, patch_pubsub_client:
            with patch_storage_manager_upload:
                with patch_factsheet_merger_merge:
                    merger = Merger(product, enriched_product, UPDATE_ACTION)
                    merger.merge()

        raw_product = mongo_database.raw_products.find_one()
        raw_product['attributes'] = sorted(raw_product['attributes'], key=lambda x: x['type'])  # noqa

        assert raw_product['brand'] == 'Novo Século'
        assert raw_product['attributes'] == []
        assert raw_product.get('product_type') is None

    def test_merger_enriched_product_in_mongo_with_wakko(
        self,
        mongo_database,
        patch_kinesis_put,
        patch_pubsub_client,
        patch_storage_manager_upload,
        patch_factsheet_merger_merge
    ):
        product = ProductSamples.lt2shop_sku_0000998113()
        mongo_database.raw_products.insert_one(product)

        enriched_product = EnrichedProductSamples.lt2shop_sku_0000998113()
        enriched_product['source'] = 'wakko'
        enriched_product['metadata']['normalized'] = {
            'Volume': ['90l'],
            'Quantidade': ['1 unidade']
        }

        mongo_database.enriched_products.insert_many([enriched_product, ])

        with patch_kinesis_put, patch_pubsub_client:
            with patch_storage_manager_upload:
                with patch_factsheet_merger_merge:
                    merger = Merger(product, None, UPDATE_ACTION)
                    merger.merge()

        raw_product = mongo_database.raw_products.find_one()
        raw_product['attributes'] = sorted(raw_product['attributes'], key=lambda x: x['type'])  # noqa
        assert raw_product['attributes'] == []
        assert raw_product.get('product_type') is None

    def test_merger_enriched_product_with_wakko_and_metabooks(
        self,
        mongo_database,
        patch_kinesis_put,
        patch_pubsub_client,
        patch_storage_manager_upload,
        patch_factsheet_merger_merge
    ):
        product = ProductSamples.cliquebooks_sku_5752019()
        mongo_database.raw_products.insert_one(product)
        raw_product = mongo_database.raw_products.find_one()
        assert raw_product['attributes'] == [
            {'type': 'additional', 'value': '1'}
        ]

        enriched_product_metabook = EnrichedProductSamples.cliquebooks_sku_5752019()  # noqa
        enriched_product_wakko = {
            'navigation_id': 'jd3d3gdb9e',
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'metadata': {
                'descriptive': {
                    'volume': '90 g'
                },
            },
            'source': 'wakko'
        }

        mongo_database.enriched_products.insert_many([enriched_product_wakko, enriched_product_metabook])  # noqa

        with patch_kinesis_put, patch_pubsub_client:
            with patch_storage_manager_upload:
                with patch_factsheet_merger_merge:
                    merger = Merger(product, None, UPDATE_ACTION)
                    merger.merge()

        raw_product = mongo_database.raw_products.find_one()
        assert raw_product['title'] == 'Livro - {}'.format(enriched_product_metabook['title'])  # noqa
        assert raw_product['description'] == enriched_product_metabook['description']  # noqa
        assert raw_product['attributes'] == []

    def test_merger_enriched_product_with_wakko_and_omnilogic(
        self,
        mongo_database,
        patch_kinesis_put,
        patch_pubsub_client,
        patch_storage_manager_upload,
        patch_factsheet_merger_merge
    ):
        volume = '90 g'
        quantity = '01 unidades'

        product = ProductSamples.magazineluiza_sku_0233847()
        product['attributes'] = [
            {
                'type': 'volume',
                'value': volume
            },
            {
                'type': 'quantity',
                'value': quantity
            }
        ]

        mongo_database.raw_products.insert_one(product)

        enriched_product_omnilogic = EnrichedProductSamples.magazineluiza_sku_0233847()  # noqa
        enriched_product_omnilogic['metadata']['Quantidade'] = quantity
        enriched_product_omnilogic['metadata']['Volume'] = volume
        enriched_product_omnilogic['sku_metadata'] = ['Volume', 'Quantidade']

        enriched_product_wakko = {
            'navigation_id': '023384800',
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'metadata': {
                'descriptive': {
                    'Volume': volume,
                    'Quantidade': quantity
                },
                'normalized': {
                    'Volume': ['90g'],
                    'Quantidade': ['1 unidade']
                }
            },
            'source': 'wakko'
        }

        mongo_database.enriched_products.insert_many([enriched_product_wakko, enriched_product_omnilogic])  # noqa

        with patch_kinesis_put, patch_pubsub_client, patch_storage_manager_upload:  # noqa
            with patch_factsheet_merger_merge:
                merger = Merger(product, None, UPDATE_ACTION)
                merger.merge()

        raw_product = mongo_database.raw_products.find_one()
        raw_product['attributes'] = sorted(raw_product['attributes'], key=lambda x: x['type'])  # noqa

        assert raw_product['product_type'] == enriched_product_omnilogic['entity'] # noqa
        assert raw_product['attributes'] == [
            {
                'type': 'quantity',
                'value': '1 unidade'
            },
            {
                'type': 'volume',
                'value': '90g'
            },
        ]

    def test_merger_with_attributes_not_present_in_sku_metadata_should_log(
        self,
        mongo_database,
        patch_kinesis_put,
        patch_pubsub_client,
        patch_patolino_product_post,
        caplog,
        patch_storage_manager_upload,
        patch_factsheet_merger_merge
    ):
        product = ProductSamples.lojasages_sku_5973()
        mongo_database.raw_products.insert_one(product)

        enriched_product = EnrichedProductSamples.lojasages_sku_5973()
        mongo_database.enriched_products.insert_one(enriched_product)
        mongo_database.enriched_products.insert_one({
            'metadata': {
                'normalized': {
                    'Modelo': [
                        'Prestobarba 3'
                    ],
                    'Marca': [
                        'Gillette'
                    ],
                    'Quantidade': [
                        '2 unidades'
                    ]
                },
                'descriptive': {
                    'Modelo': [
                        'Prestobarba 3'
                    ],
                    'Marca': [
                        'Gillette'
                    ],
                    'Quantidade': [
                        '2'
                    ]
                }
            },
            'sku': '5973',
            'seller_id': 'lojasages',
            'navigation_id': 'kh18566g08',
            'source': 'wakko',
            'timestamp': 1594509988.1452901,
            'md5': '554be3f4c5309124ece260fc0b022192'
        })

        with patch_kinesis_put, patch_pubsub_client:
            with patch_patolino_product_post, patch_storage_manager_upload:
                with patch_factsheet_merger_merge:
                    merger = Merger(product, enriched_product, UPDATE_ACTION)
                    merger.merge()

        raw_product = mongo_database.raw_products.find_one()

        assert raw_product['attributes'] == [
            {'type': 'quantity', 'value': '2 unidades'}
        ]

    def test_merger_with_attributes_not_present_in_sku_metadata_should_keep_others(  # noqa
        self,
        mongo_database,
        patch_kinesis_put,
        patch_pubsub_client,
        patch_storage_manager_upload,
        patch_factsheet_merger_merge
    ):
        attribute = {'type': 'voltage', 'value': '110V'}
        product = ProductSamples.lojasages_sku_5973()
        product['attributes'].append(attribute)
        mongo_database.raw_products.insert_one(product)

        enriched_product = EnrichedProductSamples.lojasages_sku_5973()
        mongo_database.enriched_products.insert_one(enriched_product)

        with patch_kinesis_put, patch_pubsub_client:
            with patch_storage_manager_upload, patch_factsheet_merger_merge:
                merger = Merger(product, enriched_product, UPDATE_ACTION)
                merger.merge()

        raw_product = mongo_database.raw_products.find_one()

        assert raw_product['attributes'] == [
            {'type': 'quantity', 'value': '2'},
            {'type': 'voltage', 'value': '110V'}
        ]

    def test_merger_enriched_product_with_omnilogic_should_keep_missing_atributes_not_returned_in_enriched(  # noqa
        self,
        mongo_database,
        patch_kinesis_put,
        patch_pubsub_client,
        patch_storage_manager_upload,
        patch_factsheet_merger_merge
    ):

        product = ProductSamples.magazineluiza_sku_0233847()
        product['attributes'].append({'type': 'color', 'value': 'Branco'})

        product['categories'][0]['id'] = 'MD'
        product['seller_id'] = 'zattini'

        mongo_database.raw_products.insert_one(product)

        enriched_product_omnilogic = EnrichedProductSamples.magazineluiza_sku_0233847()  # noqa
        enriched_product_omnilogic['metadata']['Quantidade'] = '01 unidades'

        enriched_product_omnilogic['seller_id'] = 'zattini'
        enriched_product_omnilogic['category_id'] = 'MD'

        mongo_database.enriched_products.insert_one(enriched_product_omnilogic)  # noqa

        with patch_kinesis_put, patch_pubsub_client:
            with patch_storage_manager_upload, patch_factsheet_merger_merge:
                merger = Merger(product, None, UPDATE_ACTION)
                merger.merge()

        raw_product = mongo_database.raw_products.find_one()
        raw_product['attributes'] = sorted(raw_product['attributes'], key=lambda x: x['type'])  # noqa

        assert raw_product['product_type'] == enriched_product_omnilogic['entity'] # noqa
        assert raw_product['attributes'] == [{
            'type': 'color',
            'value': 'Branco'
        }, {
            'type': 'voltage',
            'value': '110 volts'
        }]

    def test_merger_enriched_product_from_smartcontent(
        self,
        mongo_database,
        patch_kinesis_put,
        patch_pubsub_client,
        patch_storage_manager_upload,
        patch_factsheet_merger_merge
    ):
        product = ProductSamples.magazineluiza_sku_0233847()
        mongo_database.raw_products.insert_one(product)

        enriched_product = EnrichedProductSamples.magazineluiza_sku_0233847_smartcontent()  # noqa
        mongo_database.enriched_products.insert_one(enriched_product)

        with patch_kinesis_put, patch_pubsub_client:
            with patch_storage_manager_upload, patch_factsheet_merger_merge:
                merger = Merger(product, enriched_product, UPDATE_ACTION)
                merger.merge()

        raw_product = mongo_database.raw_products.find_one()
        raw_product['attributes'] = sorted(raw_product['attributes'], key=lambda x: x['type'])  # noqa

        assert raw_product.get('product_type') is None
        assert raw_product['title'] == enriched_product['title']
        assert raw_product['description'] == enriched_product['description']
        assert raw_product['attributes'] == [{
            'type': 'voltage',
            'value': '220 volts'
        }]

    def test_merger_use_smartcontent_if_product_is_book( # noqa
        self,
        mongo_database,
        patch_kinesis_put,
        patch_pubsub_client,
        caplog,
        patch_storage_manager_upload,
        patch_factsheet_merger_merge
    ):
        product = ProductSamples.product_magazineluiza_230382400()
        mongo_database.raw_products.insert_one(product)

        enriched_products = EnrichedProductSamples.magazineluiza_230382400()
        mongo_database.enriched_products.insert_many(enriched_products)

        with patch_kinesis_put, patch_pubsub_client:
            with patch_storage_manager_upload, patch_factsheet_merger_merge:
                merger = Merger(product, None, UPDATE_ACTION)
                merger.merge()

        raw_product = mongo_database.raw_products.find_one()
        smartcontent = enriched_products[-1]
        assert raw_product['title'] == smartcontent['title']
        assert raw_product['brand'] == smartcontent['metadata']['Editora']
        assert raw_product['description'] == smartcontent['description']

    def test_merger_not_skip_smartcontent_if_product_no_has_isbn_field( # noqa
        self,
        mongo_database,
        patch_kinesis_put,
        patch_pubsub_client,
        caplog,
        patch_storage_manager_upload,
        patch_factsheet_merger_merge
    ):
        caplog.set_level('DEBUG')

        product = ProductSamples.product_magazineluiza_230382400()
        del product['isbn']
        mongo_database.raw_products.insert_one(product)

        enriched_products = EnrichedProductSamples.magazineluiza_230382400()
        mongo_database.enriched_products.insert_many(enriched_products)

        with patch_kinesis_put, patch_pubsub_client:
            with patch_storage_manager_upload, patch_factsheet_merger_merge:
                merger = Merger(product, None, UPDATE_ACTION)
                merger.merge()

        raw_product = mongo_database.raw_products.find_one()
        smartcontent = enriched_products[1]
        assert raw_product['brand'] == smartcontent['brand']
        assert raw_product['description'] == smartcontent['description']
        assert 'normalized in smartcontent scope' in caplog.text

    def test_should_removed_field_when_value_empty(
        self,
        mongo_database,
        patch_kinesis_put,
        patch_pubsub_client,
        patch_storage_manager_upload,
        patch_factsheet_merger_merge
    ):
        volume = '90 g'
        quantity = '0'

        product = ProductSamples.magazineluiza_sku_0233847()
        product['attributes'] = [
            {
                'type': 'volume',
                'value': volume
            },
            {
                'type': 'quantity',
                'value': quantity
            }
        ]

        mongo_database.raw_products.insert_one(product)

        enriched_product_omnilogic = EnrichedProductSamples.magazineluiza_sku_0233847()  # noqa
        enriched_product_omnilogic['metadata']['Quantidade'] = quantity
        enriched_product_omnilogic['metadata']['Volume'] = volume
        enriched_product_omnilogic['sku_metadata'] = ['Volume', 'Quantidade']

        enriched_product_wakko = {
            'navigation_id': '023384800',
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'metadata': {
                'descriptive': {
                    'Volume': volume,
                    'Quantidade': quantity
                },
                'normalized': {
                    'Volume': ['90g'],
                    'Quantidade': ['']
                }
            },
            'source': 'wakko'
        }

        mongo_database.enriched_products.insert_many(
            [
                enriched_product_wakko,
                enriched_product_omnilogic
            ]
        )

        with patch_kinesis_put, patch_pubsub_client:
            with patch_storage_manager_upload, patch_factsheet_merger_merge:
                merger = Merger(product, None, UPDATE_ACTION)
                merger.merge()

        raw_product = mongo_database.raw_products.find_one()
        raw_product['attributes'] = sorted(raw_product['attributes'], key=lambda x: x['type'])  # noqa

        assert raw_product['attributes'] == [
            {
                'type': 'volume',
                'value': '90g'
            },
        ]

    def test_when_enriched_product_is_empty_then_category_merger_should_not_be_called( # noqa
        self,
        mongo_database,
        patch_kinesis_put,
        patch_pubsub_client,
        patch_storage_manager_upload,
        patch_factsheet_merger_merge
    ):
        product = ProductSamples.lt2shop_sku_0000998113()
        with patch.object(Merger, '_merge_category') as mock_merge_category:
            with patch_kinesis_put, patch_storage_manager_upload:
                with patch_pubsub_client, patch_factsheet_merger_merge:
                    merger = Merger(product, None, UPDATE_ACTION)
                    merger.merge()

        assert not mock_merge_category.called

    @pytest.mark.parametrize('product_payload,enriched_payload', [
        (
            ProductSamples.magazineluiza_sku_0233847(),
            EnrichedProductSamples.magazineluiza_sku_0233847_smartcontent()
        ),
        (
            ProductSamples.variation_a(),
            None
        )
    ])
    def test_when_enriched_product_is_empty_or_with_invalid_source_to_merge_categories_then_should_keep_categories_from_raw_products( # noqa
        self,
        mongo_database,
        patch_kinesis_put,
        patch_pubsub_client,
        patch_storage_manager_upload,
        product_payload,
        enriched_payload,
        patch_factsheet_merger_merge
    ):
        mongo_database.raw_products.insert_one(product_payload)

        if enriched_payload:
            mongo_database.enriched_products.insert_one(enriched_payload)

        with patch.object(CategoryMerger, '_mount_data') as mock:
            with patch_kinesis_put, patch_storage_manager_upload:
                with patch_pubsub_client, patch_factsheet_merger_merge:
                    merger = Merger(
                        product_payload,
                        enriched_payload,
                        UPDATE_ACTION
                    )
                    merger.merge()

        raw_product = mongo_database.raw_products.find_one()
        assert raw_product['categories'] == product_payload['categories']
        assert raw_product.get('product_type') is None
        assert not mock.called

    def test_when_enriched_product_param_is_empty_then_use_data_from_database_to_merge_categories( # noqa
        self,
        mongo_database,
        patch_kinesis_put,
        patch_pubsub_client,
        patch_storage_manager_upload,
        patch_factsheet_merger_merge
    ):
        product = ProductSamples.lt2shop_sku_0000998113()
        enriched = EnrichedProductSamples.shoploko_sku_74471()

        category = product['categories'][0]['id']
        enriched['seller_id'] = product['seller_id']
        enriched['sku'] = product['sku']
        mongo_database.enriched_products.insert_one(enriched)

        with patch_kinesis_put, patch_storage_manager_upload:
            with patch_pubsub_client, patch_factsheet_merger_merge:
                merger = Merger(product, None, UPDATE_ACTION)
                merger.merge()

        expected_payload = [{
            'id': enriched['category_id'],
            'subcategories': [
                {
                    'id': subcategory
                } for subcategory in enriched['subcategory_ids']
            ]
        }]

        raw_product = mongo_database.raw_products.find_one()
        assert raw_product['product_type'] == enriched['entity']
        assert raw_product['categories'] == expected_payload
        assert raw_product['categories'][0]['id'] != category

    def test_when_enriched_product_source_has_invalid_entity_then_should_ignore_this_source_to_merge_category( # noqa
        self,
        mongo_database,
        patch_kinesis_put,
        patch_pubsub_client,
        patch_storage_manager_upload,
        patch_factsheet_merger_merge
    ):
        product = ProductSamples.lt2shop_sku_0000998113()

        omnilogic = EnrichedProductSamples.shoploko_sku_74471()
        omnilogic['entity'] = constants.DEFAULT_ENTITY
        omnilogic['sku'] = product['sku']
        omnilogic['seller_id'] = product['seller_id']

        hector = EnrichedProductSamples.magazineluiza_hector_230382400()
        hector['sku'] = product['sku']
        hector['seller_id'] = product['seller_id']

        enriched_products = [
            omnilogic,
            hector
        ]

        mongo_database.enriched_products.insert_many(enriched_products)

        with patch_kinesis_put, patch_storage_manager_upload:
            with patch_pubsub_client, patch_factsheet_merger_merge:
                merger = Merger(product, None, UPDATE_ACTION)
                merger.merge()

        classification = hector['classifications'][0]

        expected_payload = [{
            'id': classification['category_id'],
            'subcategories': [
                {
                    'id': subcategory
                } for subcategory in classification['subcategories']
            ]
        }]

        raw_products = mongo_database.raw_products.find_one()
        assert raw_products['categories'] == expected_payload

    def test_when_category_merger_has_all_sources_then_should_use_metabooks_by_priority( # noqa
        self,
        mongo_database,
        patch_kinesis_put,
        patch_pubsub_client,
        patch_storage_manager_upload,
        patch_factsheet_merger_merge
    ):
        product = ProductSamples.lt2shop_sku_0000998113()

        omnilogic = EnrichedProductSamples.shoploko_sku_74471()
        omnilogic['sku'] = product['sku']
        omnilogic['seller_id'] = product['seller_id']

        hector = EnrichedProductSamples.magazineluiza_hector_230382400()
        hector['sku'] = product['sku']
        hector['seller_id'] = product['seller_id']
        hector['classifications'][0]['category_id'] = 'MD'
        hector['classifications'][0]['subcategories'] = ['AA']

        enriched_products = [
            omnilogic,
            hector
        ]

        mongo_database.enriched_products.insert_many(enriched_products)

        metabooks = EnrichedProductSamples.lt2shop_sku_0000998113()
        metabooks['entity'] = 'entity_from_metabooks'

        with patch_kinesis_put, patch_storage_manager_upload:
            with patch_pubsub_client, patch_factsheet_merger_merge:
                merger = Merger(product, metabooks, UPDATE_ACTION)
                merger.merge()

        expected_payload = [{
            'id': metabooks['category_id'],
            'subcategories': [
                {
                    'id': subcategory
                } for subcategory in metabooks['subcategory_ids']
            ]
        }]

        raw_products = mongo_database.raw_products.find_one()
        assert raw_products['categories'] == expected_payload
        assert raw_products['product_type'] == 'entity_from_metabooks'

    def test_when_category_merger_receive_omnilogic_and_hector_then_should_use_omnilogic_by_priority( # noqa
        self,
        mongo_database,
        patch_kinesis_put,
        patch_storage_manager_upload,
        patch_pubsub_client,
        patch_factsheet_merger_merge
    ):
        product = ProductSamples.lt2shop_sku_0000998113()

        omnilogic = EnrichedProductSamples.shoploko_sku_74471()
        omnilogic['sku'] = product['sku']
        omnilogic['seller_id'] = product['seller_id']
        omnilogic['entity'] = 'entity_from_ol'

        hector = EnrichedProductSamples.magazineluiza_hector_230382400()
        mongo_database.enriched_products.insert_one(omnilogic)

        with patch_kinesis_put, patch_storage_manager_upload:
            with patch_pubsub_client, patch_factsheet_merger_merge:
                merger = Merger(product, hector, UPDATE_ACTION)
                merger.merge()

        expected_payload = [{
            'id': omnilogic['category_id'],
            'subcategories': [
                {
                    'id': subcategory
                } for subcategory in omnilogic['subcategory_ids']
            ]
        }]

        raw_products = mongo_database.raw_products.find_one()
        assert raw_products['categories'] == expected_payload
        assert raw_products['product_type'] == 'entity_from_ol'

    def test_when_category_merger_receive_smartcontent_and_hector_then_should_use_hector_is_the_only_valid_source( # noqa
        self,
        mongo_database,
        patch_kinesis_put,
        patch_pubsub_client,
        patch_storage_manager_upload,
        patch_factsheet_merger_merge
    ):
        product = ProductSamples.lt2shop_sku_0000998113()
        hector = EnrichedProductSamples.magazineluiza_hector_230382400()
        hector['classifications'][0]['product_type'] = 'product_type_from_hector' # noqa
        smartcontent = EnrichedProductSamples.magazineluiza_sku_0233847_smartcontent() # noqa

        mongo_database.enriched_products.insert_one(smartcontent)

        with patch_kinesis_put, patch_storage_manager_upload:
            with patch_pubsub_client, patch_factsheet_merger_merge:
                merger = Merger(product, hector, UPDATE_ACTION)
                merger.merge()

        classification = hector['classifications'][0]

        expected_payload = [{
            'id': classification['category_id'],
            'subcategories': [
                {
                    'id': subcategory
                } for subcategory in classification['subcategories']
            ]
        }]

        raw_products = mongo_database.raw_products.find_one()
        assert raw_products['categories'] == expected_payload
        assert raw_products['product_type'] == 'product_type_from_hector'

    @pytest.mark.parametrize('enriched_sources,expected_enriched_sources', [
        (
            [
                {'source': constants.SOURCE_DATASHEET},
                {'source': constants.SOURCE_WAKKO},
                {'source': constants.SOURCE_SMARTCONTENT},
                {'source': constants.SOURCE_OMNILOGIC}
            ],
            [
                {'source': constants.SOURCE_OMNILOGIC},
                {'source': constants.SOURCE_SMARTCONTENT},
                {'source': constants.SOURCE_WAKKO},
                {'source': constants.SOURCE_DATASHEET}
            ]
        ),
        (
            [
                {'source': constants.SOURCE_WAKKO},
                {'source': constants.SOURCE_OMNILOGIC},
                {'source': constants.SOURCE_SMARTCONTENT}
            ],
            [
                {'source': constants.SOURCE_OMNILOGIC},
                {'source': constants.SOURCE_SMARTCONTENT},
                {'source': constants.SOURCE_WAKKO}
            ]
        ),
        (
            [
                {'source': constants.SOURCE_API_LUIZA_EXPRESS_DELIVERY},
                {'source': constants.SOURCE_API_LUIZA_PICKUPSTORE},
                {'source': constants.SOURCE_WAKKO}
            ],
            [
                {'source': constants.SOURCE_WAKKO},
                {'source': constants.SOURCE_API_LUIZA_EXPRESS_DELIVERY},
                {'source': constants.SOURCE_API_LUIZA_PICKUPSTORE}
            ]
        )
    ])
    def test_priority_execution_based_on_list_of_enriched_sources(
        self,
        enriched_sources,
        expected_enriched_sources
    ):
        merger = Merger(None, None, constants.UPDATE_ACTION)
        sorted_sources = merger.execution_priority(enriched_sources)
        assert sorted_sources == expected_enriched_sources

    def test_when_priority_execution_no_has_enriched_products_from_db_then_should_return_enriched_from_constructor( # noqa
        self
    ):
        enriched_from_constructor = {'source': constants.SOURCE_DATASHEET}
        merger = Merger(
            raw_product=None,
            enriched_product=enriched_from_constructor,
            action=constants.UPDATE_ACTION
        )
        sorted_sources = merger.execution_priority([])
        assert sorted_sources == [enriched_from_constructor]

    def test_when_all_enriched_are_empty_then_should_return_empty_list(
        self
    ):
        merger = Merger(None, None, constants.UPDATE_ACTION)
        sorted_sources = merger.execution_priority([])
        assert sorted_sources == []

    def test_set_matching_strategy_should_return_single_seller(
        self,
        mongo_database
    ):
        product = ProductSamples.product_magazineluiza_230382400()
        product['matching_strategy'] = OMNILOGIC_STRATEGY

        with settings_stub(ENABLED_CHESTER_STRATEGY=False):
            Merger(
                raw_product=product,
                enriched_product={},
                action=UPDATE_ACTION
            ).merge()

        product_from_db = mongo_database.raw_products.find_one(
            {'sku': product['sku'], 'seller_id': product['seller_id']},
            {'_id': 0, 'matching_strategy': 1}
        )

        assert product_from_db['matching_strategy'] == SINGLE_SELLER_STRATEGY

    def test_set_matching_strategy_should_return_omnilogic(
        self,
        mongo_database
    ):
        product = ProductSamples.product_magazineluiza_230382400()
        product['matching_strategy'] = CHESTER_STRATEGY

        enriched_products = EnrichedProductSamples.magazineluiza_230382400()
        product_hash = '2ea47dcc52af6f1d3f19c35ad8b8ba30'
        enriched_products.append({
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'product_hash': product_hash,
            'category_id': 'LI',
            'entity': 'Livro',
            'source': SOURCE_OMNILOGIC
        })

        mongo_database.enriched_products.insert_many(enriched_products)

        with settings_stub(
            ENABLED_CHESTER_STRATEGY=False,
            ENABLE_MATCHING_FROM_ENTITY=['Livro']
        ):
            Merger(
                raw_product=product,
                enriched_product={},
                action=UPDATE_ACTION
            ).merge()

        product_from_db = mongo_database.raw_products.find_one(
            {'sku': product['sku'], 'seller_id': product['seller_id']},
            {'_id': 0, 'matching_strategy': 1, 'product_hash': 1}
        )

        assert product_from_db['matching_strategy'] == OMNILOGIC_STRATEGY
        assert product_from_db['product_hash'] == product_hash

    def test_set_matching_strategy_should_return_chester(
        self,
        mongo_database,
        mock_matching_uuid
    ):
        product = ProductSamples.product_magazineluiza_230382400()
        product['matching_uuid'] = mock_matching_uuid
        product['categories'] = [
            {
                'id': 'LI',
                'subcategories': [
                    {'id': 'OTLI'}
                ]
            }
        ]

        with settings_stub(
            ENABLED_CHESTER_STRATEGY=True,
            ENABLED_CATEGORIES_CHESTER_STRATEGY=['LI'],
            ENABLED_SUBCATEGORIES_CHESTER_STRATEGY=['OTLI']
        ):
            Merger(
                raw_product=product,
                enriched_product={},
                action=UPDATE_ACTION
            ).merge()

        product_from_db = mongo_database.raw_products.find_one(
            {'sku': product['sku'], 'seller_id': product['seller_id']},
            {'_id': 0, 'matching_strategy': 1}
        )

        assert product_from_db['matching_strategy'] == CHESTER_STRATEGY
