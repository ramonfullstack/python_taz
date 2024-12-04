from json import loads
from typing import Dict, List, Optional
from unittest.mock import Mock, call, patch
from uuid import uuid4

import pytest
from _pytest.logging import LogCaptureFixture
from pymongo.database import Database
from redis import Redis
from simple_settings.utils import settings_stub

from taz.api.classifications_rules.schemas import ClassificationsRulesOperation
from taz.constants import (
    MAGAZINE_LUIZA_SELLER_ID,
    SOURCE_HECTOR,
    SOURCE_OMNILOGIC
)
from taz.crontabs.price_rules.cron import PriceRulesCrontab


class TestPriceRulesCrontab:

    @pytest.fixture
    def cron(self) -> PriceRulesCrontab:
        return PriceRulesCrontab()

    @pytest.fixture
    def patch_send_notification(self):
        return patch.object(PriceRulesCrontab, 'send_notification')

    @pytest.fixture
    def patch_cron_get_progress(self):
        return patch.object(PriceRulesCrontab, '_get_progress')

    @pytest.fixture
    def classification_rules(self) -> List[Dict]:
        return [
            {
                '_id': str(uuid4()),
                'operation': ClassificationsRulesOperation.MENOR_IGUAL.value,
                'price': 400,
                'product_type': 'Refrigerador',
                'to': {
                    'product_type': 'Peças para Refrigerador',
                    'category_id': 'ED',
                    'subcategory_ids': ['FAPG', 'REFR', 'ACRF']
                },
                'created_at': '2024-02-27T00:00:00',
                'updated_at': '2024-03-27T00:00:00',
                'status': 'updated',
                'active': True
            },
            {
                '_id': str(uuid4()),
                'operation': ClassificationsRulesOperation.MAIOR_IGUAL.value,
                'price': 5000,
                'product_type': 'Microondas',
                'to': {
                    'product_type': 'Refrigerador',
                    'category_id': 'ED',
                    'subcategory_ids': ['FAPG', 'REFR', 'ACRF']
                },
                'created_at': '2024-02-27T00:00:00',
                'updated_at': '2024-03-27T00:00:00',
                'status': 'updated',
                'active': True
            },
            {
                '_id': str(uuid4()),
                'operation': ClassificationsRulesOperation.MENOR_IGUAL.value,
                'price': 400,
                'product_type': 'Microondas',
                'to': {
                    'product_type': 'Peças para Microondas',
                    'category_id': 'ED',
                    'subcategory_ids': ['MOND', 'MIAC']
                },
                'created_at': '2024-02-27T00:00:00',
                'updated_at': '2024-03-27T00:00:00',
                'status': 'updated',
                'active': True
            },
            {
                '_id': str(uuid4()),
                'operation': ClassificationsRulesOperation.MAIOR_IGUAL.value,
                'price': 500,
                'product_type': 'Microondas',
                'to': {
                    'product_type': 'Peças para Microondas',
                    'category_id': 'ED',
                    'subcategory_ids': ['MOND', 'MIAC']
                },
                'created_at': '2024-02-27T00:00:00',
                'updated_at': '2024-03-27T00:00:00',
                'status': 'updated',
                'active': True
            }
        ]

    @pytest.fixture
    def mock_enriched_products_refrigerador_source_omnilogic(
        self
    ) -> List[Dict]:
        return [
            {
                'sku': '849018412',
                'seller_id': MAGAZINE_LUIZA_SELLER_ID,
                'navigation_id': '849018412',
                'source': SOURCE_OMNILOGIC,
                'entity': 'Refrigerador'
            },
            {
                'sku': '5832098532',
                'seller_id': 'luizalabs',
                'navigation_id': 'aaaaaaaaa',
                'source': SOURCE_OMNILOGIC,
                'entity': 'Refrigerador'
            },
            {
                'sku': 'dmlsamdsalk',
                'seller_id': 'kabum',
                'navigation_id': 'bbbbbbbbb',
                'source': SOURCE_OMNILOGIC,
                'entity': 'Refrigerador'
            }
        ]

    @pytest.fixture
    def mock_enriched_products_refrigerador_source_hector(self) -> List[Dict]:
        return [
            {
                'sku': '43523423432',
                'seller_id': 'luizalabs',
                'navigation_id': 'dddddddddd',
                'source': SOURCE_HECTOR,
                'classifications': [{'product_type': 'Refrigerador'}]
            },
            {
                'sku': '849018412',
                'seller_id': MAGAZINE_LUIZA_SELLER_ID,
                'navigation_id': '849018412',
                'source': SOURCE_HECTOR,
                'classifications': [{'product_type': 'Refrigerador'}]
            }
        ]

    @pytest.fixture
    def mock_enriched_products_refrigerador(
        self,
        mock_enriched_products_refrigerador_source_omnilogic: List[Dict],
        mock_enriched_products_refrigerador_source_hector: List[Dict]
    ) -> List[Dict]:
        return (
            mock_enriched_products_refrigerador_source_omnilogic +
            mock_enriched_products_refrigerador_source_hector
        )

    @pytest.fixture
    def mock_enriched_products_microondas_source_omnilogic(self) -> List[Dict]:
        return [{
            'sku': 'fdkljdsfdspj',
            'seller_id': 'kabum',
            'navigation_id': '432u4i2u34',
            'source': SOURCE_OMNILOGIC,
            'entity': 'Microondas'
        }]

    @pytest.fixture
    def mock_enriched_products_microondas_source_hector(self) -> List[Dict]:
        return [
            {
                'sku': 'rewjpjfdsd',
                'seller_id': 'olistplus',
                'navigation_id': 'daskjdsadsa',
                'source': SOURCE_HECTOR,
                'classifications': [{'product_type': 'Microondas'}]
            },
            {
                'sku': '5832098532',
                'seller_id': MAGAZINE_LUIZA_SELLER_ID,
                'navigation_id': '5832098532',
                'source': SOURCE_HECTOR,
                'classifications': [{'product_type': 'Microondas'}]
            }
        ]

    @pytest.fixture
    def mock_enriched_products_microondas(
        self,
        mock_enriched_products_microondas_source_omnilogic: List[Dict],
        mock_enriched_products_microondas_source_hector: List[Dict]
    ) -> List[Dict]:
        return (
            mock_enriched_products_microondas_source_omnilogic +
            mock_enriched_products_microondas_source_hector
        )

    @pytest.fixture
    def enriched_products(
        self,
        mock_enriched_products_refrigerador: List[Dict],
        mock_enriched_products_microondas: List[Dict]
    ) -> List[Dict]:
        return (
            mock_enriched_products_refrigerador +
            mock_enriched_products_microondas
        )

    @pytest.fixture
    def save_classification_rules(
        self,
        mongo_database: Database,
        classification_rules: List[Dict]
    ) -> None:
        mongo_database.classifications_rules.insert_many(classification_rules)

    @pytest.fixture
    def save_enriched_products(
        self,
        mongo_database: Database,
        enriched_products: List[Dict]
    ) -> None:
        mongo_database.enriched_products.insert_many(enriched_products)

    def format_paginate_key_set_call(
        self,
        source: str,
        product_type: str,
        offset: Optional[str]
    ):
        return call(
            criteria=(
                {'source': source, 'entity': product_type}
                if source == SOURCE_OMNILOGIC
                else {
                    'source': source,
                    'classifications.product_type': product_type
                }
            ),
            fields={'_id': 0, 'sku': 1, 'seller_id': 1, 'navigation_id': 1},
            limit_size=1, sort=[('navigation_id', 1)],
            field_offset='navigation_id', offset=offset,
            no_cursor_timeout=False
        )

    def test_cron_execute_with_success(
        self,
        cron: PriceRulesCrontab,
        save_classification_rules: Mock,
        save_enriched_products: Mock,
        patch_pubsub_client: Mock,
        caplog: LogCaptureFixture,
        mongo_database: Database
    ):
        assert mongo_database.classifications_rules.count_documents(
            {'status': {'$ne': 'applied'}}
        ) == 4

        with patch_pubsub_client as mock_pubsub:
            cron.run()

        assert mock_pubsub.call_count == 7

        assert 'Price rules crontab finish process with success' in caplog.text
        assert (
            'Sent 1 products out of a total:1 with product_type:Refrigerador '
            'and source:magalu to taz-price-rule' in caplog.text
        )
        assert (
            'Sent 1 products out of a total:1 with product_type:Refrigerador '
            'and source:hector to taz-price-rule' in caplog.text
        )

        assert mongo_database.classifications_rules.count_documents(
            {'status': {'$ne': 'applied'}}
        ) == 0

    @pytest.mark.parametrize('page_size,call_count', [
        (1, 3),
        (2, 2),
        (3, 1)
    ])
    def test_paginate_mongo_with_success(
        self,
        cron: PriceRulesCrontab,
        classification_rules: List[Dict],
        enriched_products: List[Dict],
        patch_send_notification: Mock,
        mongo_database: Database,
        page_size: int,
        call_count: int
    ):
        mongo_database.classifications_rules.insert_one(
            classification_rules[0]
        )

        mongo_database.enriched_products.insert_many(
            [
                product for product in enriched_products
                if product['source'] == SOURCE_OMNILOGIC
            ]
        )
        with settings_stub(PAGINATION_LIMIT_PRICE_RULE_CRON=page_size):
            with patch_send_notification as mock_send_notification:
                cron.run()

        assert mock_send_notification.call_count == call_count

    def test_when_rules_not_found_then_should_save_log(
        self,
        cron: PriceRulesCrontab,
        caplog: LogCaptureFixture,
        patch_pubsub_client: Mock,
        mongo_database: Database
    ):
        with patch_pubsub_client as mock_pubsub:
            cron.run()

        mock_pubsub.assert_not_called()
        assert 'Rules without applied status not found' in caplog.text

    def test_when_products_not_found_then_should_save_log(
        self,
        cron: PriceRulesCrontab,
        save_classification_rules: Mock,
        caplog: LogCaptureFixture,
        patch_pubsub_client: Mock,
    ):
        product_types = ['Refrigerador', 'Microondas']

        with patch_pubsub_client as mock_pubsub:
            cron.run()

        mock_pubsub.assert_not_called()
        for product_type in product_types:
            for source in [SOURCE_OMNILOGIC, SOURCE_HECTOR]:
                assert (
                    'Products not found in enriched products with '
                    f'product_type:{product_type} and source:{source}'
                ) in caplog.text

    def test_when_an_error_ocurred_in_magalu_hector_then_save_progress(
        self,
        cron: PriceRulesCrontab,
        cache_connection,
        mock_enriched_products_microondas_source_omnilogic: List[Dict],
        patch_pubsub_client: Mock,
        patch_paginate_keyset: Mock,
    ):
        current_product_type: str = 'Microondas'
        current_cache_key: str = cron.mount_cache_key(current_product_type)
        next_cache_key: str = cron.mount_cache_key('Refrigerador')
        cron._clear_progress(current_product_type)

        with pytest.raises(Exception):
            with patch_pubsub_client:
                with patch_paginate_keyset as mock_paginate_keyset:
                    mock_paginate_keyset.side_effect = [
                        mock_enriched_products_microondas_source_omnilogic,
                        Exception()
                    ]
                    cron.find_products_and_notify([current_product_type])

        assert mock_paginate_keyset.call_args_list == [
            self.format_paginate_key_set_call(SOURCE_OMNILOGIC, current_product_type, offset=None),  # noqa
            self.format_paginate_key_set_call(SOURCE_OMNILOGIC, current_product_type, offset='432u4i2u34')  # noqa
        ]

        assert loads(cache_connection.get(current_cache_key).decode()) == {
            'source': SOURCE_OMNILOGIC,
            'navigation_id': '432u4i2u34'
        }

        assert cache_connection.get(next_cache_key) is None

    def test_when_an_error_ocurred_in_source_hector_then_save_progress(
        self,
        cron: PriceRulesCrontab,
        cache_connection: Redis,
        mock_enriched_products_microondas_source_omnilogic: List[Dict],
        mock_enriched_products_microondas_source_hector: List[Dict],
        patch_pubsub_client: Mock,
        patch_paginate_keyset: Mock,
    ):
        current_product_type: str = 'Microondas'
        current_cache_key: str = cron.mount_cache_key(current_product_type)
        next_cache_key: str = cron.mount_cache_key('Refrigerador')
        cron._clear_progress(current_product_type)

        with pytest.raises(Exception):
            with patch_pubsub_client:
                with patch_paginate_keyset as mock_paginate_keyset:
                    mock_paginate_keyset.side_effect = [
                        mock_enriched_products_microondas_source_omnilogic,
                        [],
                        mock_enriched_products_microondas_source_hector,
                        Exception()
                    ]
                    cron.find_products_and_notify([current_product_type])

        assert mock_paginate_keyset.call_args_list == [
            self.format_paginate_key_set_call(SOURCE_OMNILOGIC, current_product_type, offset=None),  # noqa
            self.format_paginate_key_set_call(SOURCE_OMNILOGIC, current_product_type, offset='432u4i2u34'),  # noqa
            self.format_paginate_key_set_call(SOURCE_HECTOR, current_product_type, offset=None),  # noqa
            self.format_paginate_key_set_call(SOURCE_HECTOR, current_product_type, offset='5832098532'),  # noqa
        ]

        assert loads(cache_connection.get(current_cache_key).decode()) == {
            'source': SOURCE_HECTOR,
            'navigation_id': '5832098532'
        }

        assert cache_connection.get(next_cache_key) is None

    @pytest.mark.parametrize('position_processed', [(0), (2)])
    def test_when_restart_execution_saved_omnilogic_progress_then_where_progress_stopped(  # noqa
        self,
        cron: PriceRulesCrontab,
        cache_connection: Redis,
        mock_enriched_products_refrigerador: List[Dict],
        patch_pubsub_client: Mock,
        mongo_database: Database,
        mock_classification_rule_refrigerador_menor_400: Dict,
        position_processed: int
    ):
        mongo_database.classifications_rules.insert_one(
            mock_classification_rule_refrigerador_menor_400
        )
        mongo_database.enriched_products.insert_many(
            mock_enriched_products_refrigerador
        )
        current_product_type: str = 'Refrigerador'
        current_cache_key: str = cron.mount_cache_key(current_product_type)

        enriched_products_source_magalu: List[Dict] = sorted(
            [
                enriched
                for enriched in mock_enriched_products_refrigerador
                if enriched['source'] == SOURCE_OMNILOGIC
            ],
            key=lambda item: item['navigation_id']
        )

        unique_products = {
            (enriched['sku'], enriched['seller_id'])
            for enriched in mock_enriched_products_refrigerador
        }

        products_processed = set()
        for position in range(position_processed + 1):
            enriched: Dict = enriched_products_source_magalu[position]
            products_processed.add((enriched['sku'], enriched['seller_id']))

        cron._save_progress(
            product_type=current_product_type,
            source=SOURCE_OMNILOGIC,
            navigation_id=enriched_products_source_magalu[position_processed]['navigation_id']  # noqa
        )

        with patch_pubsub_client as mock_pubsub_publish:
            cron.find_products_and_notify([current_product_type])

        assert mock_pubsub_publish.call_count == len(unique_products) - len(products_processed)  # noqa
        assert cache_connection.get(current_cache_key) is None

    @pytest.mark.parametrize('position_processed', [(0), (1)])
    def test_when_restart_execution_saved_hector_progress_then_where_progress_stopped(  # noqa
        self,
        cron: PriceRulesCrontab,
        cache_connection: Redis,
        mock_enriched_products_refrigerador: List[Dict],
        patch_pubsub_client: Mock,
        mongo_database: Database,
        mock_classification_rule_refrigerador_menor_400: Dict,
        position_processed: int
    ):
        mongo_database.classifications_rules.insert_one(
            mock_classification_rule_refrigerador_menor_400
        )
        mongo_database.enriched_products.insert_many(
            mock_enriched_products_refrigerador
        )

        current_product_type: str = 'Refrigerador'
        current_cache_key: str = cron.mount_cache_key(current_product_type)

        enriched_products_source_hector: List[Dict] = sorted(
            [
                enriched
                for enriched in mock_enriched_products_refrigerador
                if enriched['source'] == SOURCE_HECTOR
            ],
            key=lambda item: item['navigation_id']
        )

        unique_products = {
            (enriched['sku'], enriched['seller_id'])
            for enriched in mock_enriched_products_refrigerador
        }

        products_processed = {
            (enriched['sku'], enriched['seller_id'])
            for enriched in mock_enriched_products_refrigerador
            if enriched['source'] == SOURCE_OMNILOGIC
        }

        for position in range(position_processed + 1):
            enriched: Dict = enriched_products_source_hector[position]
            products_processed.add((enriched['sku'], enriched['seller_id']))

        cron._save_progress(
            product_type=current_product_type,
            source=SOURCE_HECTOR,
            navigation_id=enriched_products_source_hector[position_processed]['navigation_id']  # noqa
        )

        with patch_pubsub_client as mock_pubsub_publish:
            cron.find_products_and_notify([current_product_type])

        assert mock_pubsub_publish.call_count == len(unique_products) - len(products_processed)  # noqa
        assert cache_connection.get(current_cache_key) is None

    def test_when_load_progress_without_data_then_return_all_sources_and_navigation_none(  # noqa
        self,
        cron: PriceRulesCrontab,
        patch_cron_get_progress: Mock,
    ):
        with patch_cron_get_progress as mock_get_progress:
            mock_get_progress.return_value = None
            recovered_source, recovered_navigation_id = (
                cron._load_progress('Refrigerador')
            )

        assert recovered_source is None
        assert recovered_navigation_id is None

    def test_when_load_progress_with_one_or_more_navigation_of_source_omnilogic_processed_then_return_all_sources_and_navigation_processed(  # noqa
        self,
        cron: PriceRulesCrontab,
        patch_cron_get_progress: Mock,
    ):
        with patch_cron_get_progress as mock_get_progress:
            mock_get_progress.return_value = {
                'source': SOURCE_OMNILOGIC,
                'navigation_id': 'fake'
            }
            recovered_source, recovered_navigation_id = (
                cron._load_progress('Refrigerador')
            )

        assert recovered_source == SOURCE_OMNILOGIC
        assert recovered_navigation_id == 'fake'

    def test_when_load_progress_with_source_omnilogic_processed_then_return_only_hector_source_and_navigation_processed(  # noqa
        self,
        cron: PriceRulesCrontab,
        patch_cron_get_progress: Mock,
    ):
        with patch_cron_get_progress as mock_get_progress:
            mock_get_progress.return_value = {
                'source': SOURCE_HECTOR,
                'navigation_id': 'fake'
            }
            recovered_source, recovered_navigation_id = (
                cron._load_progress('Refrigerador')
            )

        assert recovered_source == SOURCE_HECTOR
        assert recovered_navigation_id == 'fake'

    @pytest.mark.parametrize(
        'recovered_source,recovered_navigation_id,current_source,last_navigation_id', [  # noqa
            ('magalu', 'z', 'magalu', 'a'),
            ('hector', 'a', 'magalu', 'a'),
            ('hector', 'a', 'hector', 'a'),
        ]
    )
    def test_when_check_skip_notification_then_return_true(
        self,
        cron: PriceRulesCrontab,
        recovered_source: str,
        recovered_navigation_id: str,
        current_source: str,
        last_navigation_id: str
    ):
        assert cron._check_skip_notification(
            recovered_source=recovered_source,
            recovered_navigation_id=recovered_navigation_id,
            current_source=current_source,
            last_navigation_id=last_navigation_id
        )

    @pytest.mark.parametrize(
        'recovered_source,recovered_navigation_id,current_source,last_navigation_id', [  # noqa
            (None, 'z', 'magalu', 'a'),
            ('magalu', None, 'magalu', 'a'),
            (None, None, 'magalu', 'a'),
            (None, 'z', 'hector', 'a'),
            ('magalu', None, 'hector', 'a'),
            (None, None, 'hector', 'a'),
            ('magalu', 'a', 'magalu', 'b'),
            ('magalu', 'b', 'hector', 'a'),
            ('hector', 'a', 'hector', 'b'),
        ]
    )
    def test_when_check_skip_notification_then_return_false(
        self,
        cron: PriceRulesCrontab,
        recovered_source: str,
        recovered_navigation_id: str,
        current_source: str,
        last_navigation_id: str
    ):
        assert not cron._check_skip_notification(
            recovered_source=recovered_source,
            recovered_navigation_id=recovered_navigation_id,
            current_source=current_source,
            last_navigation_id=last_navigation_id
        )
