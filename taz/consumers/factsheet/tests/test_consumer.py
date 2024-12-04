from copy import deepcopy
from datetime import datetime
from typing import Dict
from unittest.mock import ANY, Mock, patch

import pytest
from pymongo.database import Database
from redis import Redis
from simple_settings.utils import settings_stub

from taz.constants import (
    CREATE_ACTION,
    DELETE_ACTION,
    FACTSHEET_UNFINISHED_PROCESS,
    MAGAZINE_LUIZA_SELLER_ID,
    SOURCE_DATASHEET,
    SOURCE_METADATA_VERIFY,
    SOURCE_OMNILOGIC,
    SOURCE_SMARTCONTENT,
    UPDATE_ACTION
)
from taz.consumers.factsheet.consumer import FactsheetRecordProcessor
from taz.core.matching.common.enriched_products import EnrichedProductSamples
from taz.helpers.json import json_dumps, json_loads
from taz.utils import md5


class TestFactsheetRecordProcessor:

    @pytest.fixture
    def record_processor(self):
        return FactsheetRecordProcessor('factsheet')

    @pytest.fixture
    def mock_facsheet_charset(self):
        return 'application/json; charset=utf-8'

    @pytest.fixture
    def enriched_info(self):
        return {
            'slug': 'informacoes-complementares-magazineluiza',
            'position': 1,
            'key_name': 'Informações complementares',
            'elements': [
                {
                    'key_name': 'Capacidade',
                    'slug': 'capacidade',
                    'position': 1,
                    'value': '3,2L',
                    'is_html': False
                },
                {
                    'key_name': 'Cor',
                    'slug': 'cor',
                    'position': 2,
                    'value': 'Inox Vermelho',
                    'is_html': False
                },
                {
                    'key_name': 'Marca',
                    'slug': 'marca',
                    'position': 3,
                    'value': 'Mondial',
                    'is_html': False
                },
                {
                    'key_name': 'Modelo',
                    'slug': 'modelo',
                    'position': 4,
                    'value': 'AF-14',
                    'is_html': False
                },
                {
                    'key_name': 'Modelo Nominal',
                    'slug': 'modelo-nominal',
                    'position': 5,
                    'value': 'Family',
                    'is_html': False
                },
                {
                    'key_name': 'Produto',
                    'slug': 'produto',
                    'position': 6,
                    'value': 'Fritadeira Elétrica',
                    'is_html': False
                },
                {
                    'key_name': 'Tipo',
                    'slug': 'tipo',
                    'position': 7,
                    'value': 'Sem óleo',
                    'is_html': False
                },
                {
                    'key_name': 'Voltagem',
                    'slug': 'voltagem',
                    'position': 8,
                    'value': '110 volts',
                    'is_html': False
                }
            ]
        }

    @pytest.fixture
    def enriched_factsheet(
        self,
        enriched_info,
        mock_factsheet_navigation_id
    ):
        return {
            'items': [
                {
                    'slug': 'apresentacao',
                    'position': 1,
                    'display_name': 'Apresentação',
                    'elements': [
                        {
                            'key_name': 'Apresentação do produto',
                            'position': 2,
                            'value': 'Procurando Nemo está de volta agora',
                            'is_html': False
                        },
                        {
                            'key_name': 'Apresentação do produto',
                            'position': 2,
                            'value': 'Procurando Nemo está de volta',
                            'is_html': True
                        }
                    ]
                },
                {
                    'slug': 'ficha-tecnica',
                    'position': 6,
                    'display_name': 'Ficha-Técnica',
                    'elements': [enriched_info]
                }
            ],
            'navigation_id': mock_factsheet_navigation_id
        }

    @pytest.fixture
    def mock_factsheet_enriched_with_generic_content(self, enriched_factsheet):
        enriched_factsheet['items'][1]['elements'] = [{
            'slug': 'informacoes-complementares-magazineluiza',
            'position': 1,
            'key_name': 'Informações complementares',
            'elements': [{
                    'key_name': 'Certificado homologado pela Anatel número',
                    'slug': 'certificado-homologado-pela-anatel-numero',
                    'position': 1,
                    'value': 'HHHHH-AA-FFFFF',
                    'is_html': False
            }]
        }]

        return enriched_factsheet

    @pytest.fixture
    def save_product(
        self,
        mongo_database,
        mock_factsheet_sku,
        mock_factsheet_seller_id,
        mock_factsheet_navigation_id
    ):
        payload = {
            'sku': mock_factsheet_sku,
            'seller_id': mock_factsheet_seller_id,
            'navigation_id': mock_factsheet_navigation_id
        }

        mongo_database.raw_products.insert_one(payload)

    @pytest.fixture
    def enriched_product(
        self,
        mongo_database,
        mock_factsheet_sku,
        mock_factsheet_seller_id
    ):
        enriched_product = EnrichedProductSamples.shoploko_sku_74471()

        enriched_product['seller_id'] = mock_factsheet_seller_id
        enriched_product['sku'] = mock_factsheet_sku

        mongo_database.enriched_products.insert_one(enriched_product)
        return enriched_product

    @pytest.fixture
    def patch_factsheet_storage_property(self):
        return patch.object(FactsheetRecordProcessor, 'factsheet_storage')

    @pytest.fixture
    def patch_raw_factsheet_storage_property(self):
        return patch.object(FactsheetRecordProcessor, 'raw_factsheet_storage')

    @pytest.fixture
    def patch_acme_notification_property(self):
        return patch.object(FactsheetRecordProcessor, 'acme_notification')

    @pytest.fixture
    def patch_notify(self):
        return patch.object(FactsheetRecordProcessor, '_notify')

    @pytest.fixture
    def patch_factsheets_collection(self):
        return patch.object(FactsheetRecordProcessor, 'factsheets')

    @pytest.mark.parametrize('action', [(CREATE_ACTION), (UPDATE_ACTION)])
    def test_record_processor_with_empty_dict(  # noqa
        self,
        record_processor: FactsheetRecordProcessor,
        patch_factsheet_storage_property,
        patch_raw_factsheet_storage_property,
        mock_factsheet_payload_with_empty_dict: Dict,
        patch_acme_notification_property,
        save_product: pytest.fixture,
        patch_notify,
        mock_factsheet_seller_id: str,
        mock_factsheet_sku: str,
        mock_factsheet_navigation_id: str,
        action: str,
        mongo_database: Database,
        patch_datetime
    ):
        mock_current_datetime = datetime(2023, 1, 1, 0, 0, 0)
        mock_md5_value = 'a96bf1f3a9610d5265ea01c4ff60c1ed'

        factsheet_original = deepcopy(mock_factsheet_payload_with_empty_dict)
        factsheet_original.update({
            'navigation_id': mock_factsheet_navigation_id,
            'md5': mock_md5_value,
            'last_updated_at': mock_current_datetime.isoformat()
        })

        with patch_factsheet_storage_property:
            with patch_raw_factsheet_storage_property:  # noqa
                with patch_datetime as mock_datetime:
                    mock_datetime.utcnow.return_value = mock_current_datetime  # noqa
                    getattr(record_processor, action)(mock_factsheet_payload_with_empty_dict)  # noqa

        factsheet_processed = {
            'items': mock_factsheet_payload_with_empty_dict['items'],
            'navigation_id': mock_factsheet_navigation_id
        }

        factsheet_processed['items'] = list(filter(lambda x: bool(x), factsheet_processed['items'])) # noqa

        assert mongo_database.factsheets.find_one(
            {'sku': mock_factsheet_sku, 'seller_id': mock_factsheet_seller_id},
            {'_id': 0}
        ) == {
            'seller_id': mock_factsheet_seller_id,
            'sku': mock_factsheet_sku,
            'last_updated_at': mock_current_datetime.isoformat(),
            'md5': mock_md5_value,
            **factsheet_processed
        }

    @pytest.mark.parametrize('action', [(CREATE_ACTION), (UPDATE_ACTION)])
    def test_record_processor_create_upload_factsheet_and_notify_complete_product_queue(  # noqa
        self,
        record_processor: FactsheetRecordProcessor,
        patch_factsheet_storage_property,
        patch_raw_factsheet_storage_property,
        mock_factsheet_payload: Dict,
        patch_acme_notification_property,
        save_product: pytest.fixture,
        patch_notify,
        mock_factsheet_seller_id: str,
        mock_factsheet_sku: str,
        mock_factsheet_navigation_id: str,
        action: str,
        mongo_database: Database,
        patch_datetime
    ):
        mock_current_datetime = datetime(2023, 1, 1, 0, 0, 0)
        mock_md5_value = '3f3e65fa9838ee1c9e2bf644634b912d'

        factsheet_original = deepcopy(mock_factsheet_payload)
        factsheet_original.update({
            'navigation_id': mock_factsheet_navigation_id,
            'md5': mock_md5_value,
            'last_updated_at': mock_current_datetime.isoformat()
        })

        with patch_factsheet_storage_property as mock_factsheet_storage:
            with patch_raw_factsheet_storage_property as mock_raw_factsheet_storage:  # noqa
                with patch_acme_notification_property as mock_acme_notification:  # noqa
                    with patch_notify as mock_notify:
                        with patch_datetime as mock_datetime:
                            mock_datetime.utcnow.return_value = mock_current_datetime  # noqa
                            getattr(record_processor, action)(mock_factsheet_payload)  # noqa

        factsheet_processed = {
            'items': mock_factsheet_payload['items'],
            'navigation_id': mock_factsheet_navigation_id
        }

        mock_factsheet_storage.upload_bucket_data.assert_called_with(
            sku=mock_factsheet_sku,
            seller_id=mock_factsheet_seller_id,
            payload=json_dumps(factsheet_processed, ensure_ascii=False)
        )

        mock_raw_factsheet_storage.upload_bucket_data.assert_called_with(
            sku=mock_factsheet_sku,
            seller_id=mock_factsheet_seller_id,
            payload=json_dumps(factsheet_original, ensure_ascii=False)
        )

        mock_acme_notification.send_factsheet.assert_called_with(
            action=CREATE_ACTION,
            seller_id=mock_factsheet_seller_id,
            sku=mock_factsheet_sku,
            payload=factsheet_processed
        )

        mock_notify.assert_called_with(
            action=action,
            seller_id=mock_factsheet_seller_id,
            sku=mock_factsheet_sku,
            navigation_id=mock_factsheet_navigation_id,
            send_to_datalake=True
        )

        assert mongo_database.factsheets.find_one(
            {'sku': mock_factsheet_sku, 'seller_id': mock_factsheet_seller_id},
            {'_id': 0}
        ) == {
            'seller_id': mock_factsheet_seller_id,
            'sku': mock_factsheet_sku,
            'last_updated_at': mock_current_datetime.isoformat(),
            'md5': mock_md5_value,
            **factsheet_processed
        }

    @pytest.mark.parametrize('action', [(CREATE_ACTION), (UPDATE_ACTION)])
    def test_when_has_enrichment_omnilogic_and_origin_metadata_verify_then_apply_merger_and_do_not_save_raw_factsheet(  # noqa
        self,
        record_processor: FactsheetRecordProcessor,
        patch_factsheet_storage_property,
        patch_raw_factsheet_storage_property,
        mock_factsheet_payload: Dict,
        enriched_product: pytest.fixture,
        enriched_factsheet: Dict,
        patch_notify,
        patch_acme_notification_property,
        save_product,
        action: str
    ):
        mock_factsheet_payload['source'] = 'metadata_verify'
        with patch_factsheet_storage_property as mock_factsheet_storage:
            with patch_raw_factsheet_storage_property as mock_raw_factsheet_storage:  # noqa
                with patch_acme_notification_property as mock_acme_notification:  # noqa
                    with patch_notify as mock_notify:
                        getattr(record_processor, action)(mock_factsheet_payload)  # noqa

        mock_factsheet_storage.upload_bucket_data.assert_called_with(
            sku=mock_factsheet_payload['sku'],
            seller_id=mock_factsheet_payload['seller_id'],
            payload=json_dumps(enriched_factsheet, ensure_ascii=False)
        )

        mock_acme_notification.send_factsheet.assert_called_with(
            action=CREATE_ACTION,
            seller_id=mock_factsheet_payload['seller_id'],
            sku=mock_factsheet_payload['sku'],
            payload=enriched_factsheet
        )

        mock_notify.assert_called_with(
            action=action,
            seller_id=mock_factsheet_payload['seller_id'],
            sku=mock_factsheet_payload['sku'],
            navigation_id=mock_factsheet_payload['navigation_id'],
            send_to_datalake=True
        )

        assert not mock_raw_factsheet_storage.called

    def test_record_processor_delete_factsheet_and_notify_complete_product_queue(  # noqa
        self,
        record_processor: FactsheetRecordProcessor,
        mock_factsheet_payload: Dict,
        patch_factsheet_storage_property,
        patch_raw_factsheet_storage_property,
        patch_notify,
        mock_factsheet_navigation_id: str,
        patch_mongo_collection
    ):
        with patch_factsheet_storage_property as mock_factsheet_storage:
            with patch_raw_factsheet_storage_property as mock_raw_factsheet_storage:  # noqa
                with patch_mongo_collection as mock_collection:
                    with patch_notify as mock_notify:
                        mock_find_one = Mock()
                        mock_collection.return_value = mock_find_one
                        mock_find_one.find_one.side_effect = [
                            {'navigation_id': mock_factsheet_navigation_id}
                        ]
                        record_processor.delete(mock_factsheet_payload)

        mock_factsheet_storage.delete_bucket_data.assert_called_with(
            seller_id=mock_factsheet_payload['seller_id'],
            sku=mock_factsheet_payload['sku']
        )

        mock_raw_factsheet_storage.delete_bucket_data.assert_called_with(
            seller_id=mock_factsheet_payload['seller_id'],
            sku=mock_factsheet_payload['sku']
        )

        mock_notify.assert_called_with(
            action=DELETE_ACTION,
            seller_id=mock_factsheet_payload['seller_id'],
            sku=mock_factsheet_payload['sku'],
            navigation_id=mock_factsheet_payload['navigation_id'],
            send_to_datalake=True
        )

    def test_record_processor_create_upload_factsheet_with_is_html_attribute(
        self,
        record_processor: FactsheetRecordProcessor,
        patch_factsheet_storage_property,
        patch_raw_factsheet_storage_property,
        patch_acme_notification_property,
        patch_notify,
        mock_factsheet_payload,
        patch_patolino_product_post,
        save_product
    ):
        with patch_factsheet_storage_property as mock_factsheet_storage:
            with patch_raw_factsheet_storage_property, patch_acme_notification_property, patch_notify:  # noqa
                with patch_patolino_product_post:  # noqa
                    record_processor.create(mock_factsheet_payload)

        def count_is_html_occurrences(items, occurrence=0):
            for item in items:
                if 'is_html' in item:
                    occurrence += 1
                if item.get('elements'):
                    occurrence = count_is_html_occurrences(
                        item.get('elements'), occurrence)
            return occurrence

        factsheet = mock_factsheet_storage.upload_bucket_data.call_args[1]['payload']  # noqa
        factsheet = json_loads(factsheet)
        assert count_is_html_occurrences(factsheet['items']) == 7
        assert not factsheet['items'][0]['elements'][0]['is_html']
        assert factsheet['items'][0]['elements'][1]['is_html']

    def test_count_factsheet_attributes_excluding_product_presentation(
        self,
        record_processor,
        mock_factsheet_payload
    ):
        _, attribute_amount = record_processor._sort_elements(
            mock_factsheet_payload['items']
        )

        assert attribute_amount == 5

    def test_cache_should_be_the_same_redis_instance(
        self,
        record_processor,
        save_product
    ):
        redis_instance = record_processor.cache()
        redis_instance_from_same_class = record_processor.cache()

        redis_instance_from_other_record_processor = FactsheetRecordProcessor('factsheet').cache()  # noqa

        assert isinstance(redis_instance, Redis)
        assert redis_instance is redis_instance_from_same_class
        assert redis_instance_from_other_record_processor is redis_instance

    @pytest.mark.parametrize('source,enriched_product', [
        ('metadata_verify', {'source': SOURCE_SMARTCONTENT}),
        ('metadata_verify', None)
    ])
    def test_record_processor_verify_source_metadata_verify(
        self,
        record_processor,
        patch_factsheet_storage_property,
        patch_raw_factsheet_storage_property,
        mock_factsheet_payload,
        patch_pubsub_client,
        patch_patolino_product_post,
        save_product,
        source,
        enriched_product,
        patch_mongo_collection,
        mock_factsheet_navigation_id,
        patch_factsheet_merge
    ):
        mock_factsheet_payload['source'] = source
        with patch_factsheet_storage_property, patch_raw_factsheet_storage_property:  # noqa
            with patch_factsheet_merge:
                with patch_patolino_product_post, patch_pubsub_client as mock_pubsub: # noqa
                    with patch_mongo_collection as mock_collection:
                        mock = Mock()
                        mock_collection.return_value = mock
                        mock.find.return_value = [{
                            'source': SOURCE_SMARTCONTENT
                        }] if enriched_product else []

                        mock.find_one.side_effect = [
                            None,
                            {
                                'navigation_id': mock_factsheet_navigation_id
                            },
                            {
                                'source': SOURCE_OMNILOGIC,
                                'sku': mock_factsheet_payload['sku'],
                                'seller_id': mock_factsheet_payload['seller_id'] # noqa
                            }
                        ]
                        record_processor._update(mock_factsheet_payload)

        assert mock_pubsub.call_count == 3

    def test_record_processor_verify_source_is_different_metadata_verify(
        self,
        record_processor,
        patch_storage_manager_upload,
        mock_factsheet_payload,
        patch_pubsub_client,
        patch_patolino_product_post,
        patch_mongo_collection
    ):
        mock_factsheet_payload['source'] = 'test'
        with patch_storage_manager_upload:
            with patch_patolino_product_post:
                with patch_pubsub_client as mock_pubsub:
                    with patch_mongo_collection as mock_collection:
                        mock = Mock()
                        mock_collection.return_value = mock
                        mock.find.return_value = [{
                            'source': SOURCE_SMARTCONTENT
                        }]
                        record_processor._update(mock_factsheet_payload)

        mock_pubsub.assert_not_called()

    @pytest.mark.parametrize(
        'action', [
            CREATE_ACTION,
            UPDATE_ACTION
        ]
    )
    def test_when_update_with_the_same_factsheet_payload_then_should_skip_process( # noqa
        self,
        record_processor,
        patch_storage_manager_upload,
        mock_factsheet_payload,
        patch_patolino_product_post,
        caplog,
        save_product,
        patch_pubsub_client,
        mock_factsheet_navigation_id,
        mongo_database,
        patch_datetime,
        action
    ):
        sku = mock_factsheet_payload['sku']
        seller_id = mock_factsheet_payload['seller_id']
        navigation_id = mock_factsheet_payload['navigation_id']

        mongo_database.factsheets.insert_one(
            {
                'sku': sku,
                'seller_id': seller_id,
                'md5': md5(mock_factsheet_payload)
            }
        )

        mock_current_datetime = datetime(2023, 1, 1, 0, 0, 0)
        with patch_storage_manager_upload, patch_datetime as mock_datetime:
            mock_datetime.utcnow.return_value = (
                mock_current_datetime
            )
            with patch_pubsub_client as mock_pubsub:
                with patch_patolino_product_post as patolino_mock:
                    getattr(
                        record_processor,
                        action
                    )(mock_factsheet_payload)

            mock_pubsub.assert_not_called()
            patolino_mock.assert_called_with(
                {
                    'sku': sku,
                    'seller_id': seller_id,
                    'code': FACTSHEET_UNFINISHED_PROCESS,
                    'message': f"Couldn't finish processing sku:{sku} seller_id:{seller_id} reason: Skip the update because the factsheet has not changed", # noqa
                    'payload': {
                        'navigation_id': navigation_id,
                        'action': action
                    },
                    'action': UPDATE_ACTION,
                    'last_updated_at': mock_current_datetime.isoformat()
                },
                {
                    'seller_id': seller_id,
                    'code': FACTSHEET_UNFINISHED_PROCESS,
                    'has_tracking': 'false'
                }
            )
            assert (
                f'Skip process factsheet to sku:{sku} seller_id:{seller_id} '
                'payload are the same' in caplog.text
            )

    def test_record_processor_factsheet_with_forbidden_terms(
        self,
        record_processor,
        mock_factsheet_forbidden_terms
    ):
        terms_list = record_processor._handler_forbidden_terms(
            mock_factsheet_forbidden_terms
        )

        assert terms_list == [
            {
                'field': 'Apresentação do produto',
                'replace': 'material ecológico',
                'replace_at': ANY,
                'scope': 'factsheet',
                'term': 'couro ecologico'
            },
            {
                'field': 'Apresentação do produto',
                'replace': 'tiras autocolantes',
                'replace_at': ANY,
                'scope': 'factsheet',
                'term': 'velcro'
            },
            {
                'field': 'Descrição',
                'replace': 'material ecológico',
                'replace_at': ANY,
                'scope': 'factsheet',
                'term': 'couro ecologico'
            },
            {
                'field': 'Descrição',
                'replace': 'tiras autocolantes',
                'replace_at': ANY,
                'scope': 'factsheet',
                'term': 'velcro'
            },
            {
                'field': 'Couro (sintético)',
                'replace': 'material sintético',
                'replace_at': ANY,
                'scope': 'factsheet',
                'term': 'couro (sintetico)'
            },
            {
                'field': 'Material',
                'replace': 'material ecológico',
                'replace_at': ANY,
                'scope': 'factsheet',
                'term': 'couro ecologico'
            },
            {
                'term': 'velcron',
                'replace': 'tiras autocolantes',
                'field': 'Desenvolvimento VelCRONNN',
                'scope': 'factsheet',
                'replace_at': ANY
            },
            {
                'term': 'velcro',
                'replace': 'tiras autocolantes',
                'replace_at': ANY,
                'field': 'Fechamento',
                'scope': 'factsheet'
            }
        ]

    @pytest.mark.parametrize(
        'seller_id,'
        'source,'
        'expected_enable_process,'
        'expected_enable_clean_html', [
            (
                MAGAZINE_LUIZA_SELLER_ID,
                SOURCE_METADATA_VERIFY,
                True,
                False
            ),
            (
                MAGAZINE_LUIZA_SELLER_ID,
                'fake_source',
                False,
                False
            ),
            (
                'luizalabs',
                SOURCE_METADATA_VERIFY,
                True,
                False
            ),
            (
                'luizalabs',
                'fake_source',
                False,
                False
            )
        ]
    )
    @settings_stub(SKIP_ENRICHED_SOURCES_WHEN_NOT_METADATA_VERIFY=[
        SOURCE_DATASHEET
    ])
    def test_when_product_3p_has_datasheet_then_should_ignore_clean_html(
        self,
        record_processor,
        mongo_database,
        mock_factsheet_payload,
        seller_id,
        source,
        expected_enable_process,
        expected_enable_clean_html
    ):
        enriched_datasheet = EnrichedProductSamples.magazineluiza_sku_0233847_datasheet() # noqa
        enriched_datasheet['seller_id'] = seller_id
        mongo_database.enriched_products.insert_one(enriched_datasheet)

        enabled_process, enable_clean_html = record_processor.validate_factsheet_to_process( # noqa
            sku=enriched_datasheet['sku'],
            seller_id=seller_id,
            source=source
        )

        assert enabled_process == expected_enable_process
        assert enable_clean_html == expected_enable_clean_html

    @pytest.mark.parametrize(
        'seller_id,'
        'source,'
        'expected_enable_process,'
        'expected_enable_clean_html', [
            (
                MAGAZINE_LUIZA_SELLER_ID,
                SOURCE_METADATA_VERIFY,
                True,
                False
            ),
            (
                MAGAZINE_LUIZA_SELLER_ID,
                'fake_source',
                True,
                False
            ),
            (
                'luizalabs',
                SOURCE_METADATA_VERIFY,
                True,
                True
            ),
            (
                'luizalabs',
                'fake_source',
                True,
                True
            )
        ]
    )
    @settings_stub(SKIP_ENRICHED_SOURCES_WHEN_NOT_METADATA_VERIFY=[
        SOURCE_DATASHEET
    ])
    def test_when_product_3p_not_has_datasheet_then_should_ignore_clean_html(
        self,
        record_processor,
        mongo_database,
        mock_factsheet_payload,
        seller_id,
        source,
        expected_enable_process,
        expected_enable_clean_html
    ):
        enabled_process, enable_clean_html = record_processor.validate_factsheet_to_process( # noqa
            sku='123',
            seller_id=seller_id,
            source=source
        )

        assert enabled_process == expected_enable_process
        assert enable_clean_html == expected_enable_clean_html

    @pytest.mark.parametrize('action', [(CREATE_ACTION), (UPDATE_ACTION)])
    def test_when_has_enrichment_generic_content_then_apply_merger_and_do_not_save_raw_factsheet(  # noqa
        self,
        record_processor: FactsheetRecordProcessor,
        patch_factsheet_storage_property,
        patch_raw_factsheet_storage_property,
        mock_factsheet_payload: Dict,
        mock_factsheet_enriched_with_generic_content: Dict,
        patch_notify,
        patch_acme_notification_property,
        save_product,
        action: str,
        mongo_database: Database,
        mock_factsheet_sku: str,
        mock_factsheet_seller_id: str,
        mock_factsheet_navigation_id: str
    ):
        enriched_product = EnrichedProductSamples.shoploko_sku_74471_generic_content()  # noqa
        enriched_product.update({
            'sku': mock_factsheet_sku,
            'seller_id': mock_factsheet_seller_id,
            'navigation_id': mock_factsheet_navigation_id
        })

        mongo_database.enriched_products.insert_one(enriched_product)

        with patch_factsheet_storage_property as mock_factsheet_storage:
            with patch_raw_factsheet_storage_property, patch_acme_notification_property:  # noqa
                with patch_notify:
                    getattr(record_processor, action)(mock_factsheet_payload)  # noqa

        mock_factsheet_storage.upload_bucket_data.assert_called_with(
            sku=mock_factsheet_sku,
            seller_id=mock_factsheet_seller_id,
            payload=json_dumps(
                mock_factsheet_enriched_with_generic_content,
                ensure_ascii=False
            )
        )
