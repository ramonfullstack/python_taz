from unittest.mock import ANY, Mock, call, patch

import pytest
from simple_settings.utils import settings_stub

from taz.constants import CREATE_ACTION, UPDATE_ACTION, EnrichmentEventType
from taz.consumers.core.exceptions import InvalidScope
from taz.consumers.core.frajola import FrajolaRequest
from taz.consumers.metadata_verify import SCOPE
from taz.consumers.metadata_verify.consumer import MetadataVerifyProcessor
from taz.core.merge.merger import Merger


class TestMetadataVerifyConsumer:

    @pytest.fixture
    def consumer(self):
        return MetadataVerifyProcessor(SCOPE)

    @pytest.fixture
    def message(self, product):
        return {'sku': product['sku'], 'seller_id': product['seller_id']}

    @pytest.fixture
    def patch_raw_products(self):
        return patch.object(MetadataVerifyProcessor, 'raw_products')

    @pytest.fixture
    def patch_pubsub(self):
        return patch.object(MetadataVerifyProcessor, 'pubsub')

    @pytest.fixture
    def patch_media_stream(self):
        return patch.object(MetadataVerifyProcessor, 'media_stream')

    @pytest.fixture
    def patch_notification_property(self):
        return patch.object(MetadataVerifyProcessor, 'notification')

    @pytest.fixture
    def patch_get_scopes(self):
        return patch.object(MetadataVerifyProcessor, '_get_scopes')

    @pytest.fixture
    def patch_evaluate_scopes(self):
        return patch.object(MetadataVerifyProcessor, '_evaluate_scopes')

    @pytest.fixture
    def patch_put_factsheet(self):
        return patch.object(MetadataVerifyProcessor, '_put_factsheet')

    @pytest.fixture
    def patch_put_media(self):
        return patch.object(MetadataVerifyProcessor, '_put_media')

    @pytest.fixture
    def patch_merge_process(self):
        return patch.object(MetadataVerifyProcessor, '_execute_merger')

    @pytest.fixture
    def patch_notification(self):
        return patch.object(MetadataVerifyProcessor, '_send_notification')

    @pytest.fixture
    def patch_merger_merge(self):
        return patch.object(Merger, 'merge')

    @pytest.fixture
    def patch_get_scope(self):
        return patch.object(MetadataVerifyProcessor, '_get_scope')

    @pytest.fixture
    def patch_frajola_process(self):
        return patch.object(MetadataVerifyProcessor, '_frajola_process')

    @pytest.fixture
    def patch_frajola_put(self):
        return patch.object(FrajolaRequest, 'put')

    @staticmethod
    def fake_process_scope_by_source(source: str) -> dict:
        return {
            'factsheet': {'items': [f'Factsheet from {source}']},
            'media': {'images': f'Images from {source}'},
            'enriched_product': {'item': f'Enriched Product from {source}'}
        }

    @staticmethod
    def fake_scopes(
        metabooks_is_allowed: bool,
        smartcontent_is_allowed: bool,
        datasheet_is_allowed: bool,
    ):
        mock_metabooks = Mock()
        mock_metabooks.is_allowed.return_value = (
            metabooks_is_allowed,
            'metabooks_identifier'
        )
        mock_smartcontent = Mock()
        mock_smartcontent.is_allowed.return_value = (
            smartcontent_is_allowed,
            'smartcontent_identifier'
        )
        mock_datasheet = Mock()
        mock_datasheet.is_allowed.return_value = (
            datasheet_is_allowed,
            'datasheet_identifier'
        )
        return [mock_metabooks, mock_smartcontent, mock_datasheet]

    @staticmethod
    def fake_scopes_ordered_response(
        metabooks_is_allowed: bool,
        smartcontent_is_allowed: bool,
        datasheet_is_allowed: bool
    ):
        response = []
        if metabooks_is_allowed:
            response.append(('metabooks', 'metabooks_identifier'))

        if smartcontent_is_allowed:
            response.append(('smartcontent', 'smartcontent_identifier'))

        if datasheet_is_allowed:
            response.append(('datasheet', 'datasheet_identifier'))

        return response

    @pytest.fixture
    def mock_metabooks_process_payload(self):
        return self.fake_process_scope_by_source('metabooks')

    @pytest.fixture
    def mock_smartcontent_process_payload(self):
        return self.fake_process_scope_by_source('smartcontent')

    @pytest.fixture
    def mock_datasheet_process_payload(self):
        return self.fake_process_scope_by_source('datasheet')

    @pytest.mark.parametrize('field', ['sku', 'seller_id'])
    def test_when_invalid_message_then_exit_process(
        self,
        consumer,
        message,
        field,
        caplog
    ):
        message.pop(field, None)
        assert consumer.process_message(message)
        assert 'Invalid message' in caplog.text

    def test_when_product_not_found_then_return_true(
        self,
        consumer,
        message,
        caplog
    ):
        result = consumer.process_message(message)
        assert result
        assert (
            'Product sku:{sku} seller_id:{seller_id} not found'.format(
                sku=message['sku'],
                seller_id=message['seller_id']
            ) in caplog.text
        )

    @pytest.mark.parametrize(
        'metabooks_is_allowed,smartcontent_is_allowed,datasheet_is_allowed', [
            (True, False, False),
            (True, True, False),
            (True, True, True),
            (False, True, False),
            (False, True, True),
            (False, False, True),
            (False, False, False)
        ]
    )
    def test_when_get_scopes_ordered_then_return_enabled_scopes(
        self,
        consumer,
        product,
        patch_get_scope,
        metabooks_is_allowed,
        smartcontent_is_allowed,
        datasheet_is_allowed
    ):
        expected_enable_scopes = self.fake_scopes_ordered_response(
            metabooks_is_allowed,
            smartcontent_is_allowed,
            datasheet_is_allowed
        )
        with patch_get_scope as mock_get_scope:
            mock_get_scope.side_effect = self.fake_scopes(
                metabooks_is_allowed,
                smartcontent_is_allowed,
                datasheet_is_allowed
            )
            scopes = consumer._get_scopes(product)
        assert scopes == expected_enable_scopes

    @pytest.mark.parametrize('tracking_id', [('fake'), (None)])
    def test_when_none_scope_enabled_to_process_then_send_notification_to_enrichment_and_skip_message(  # noqa
        self,
        consumer,
        patch_raw_products,
        patch_get_scopes,
        product,
        message,
        patch_notification_enrichment_notify,
        tracking_id
    ):
        message.update({'tracking_id': tracking_id})
        with patch_raw_products as mock_raw_products:
            with patch_get_scopes as mock_get_scopes:
                with patch_notification_enrichment_notify as mock_notification_enrichment_notify:  # noqa
                    mock_get_scopes.return_value = []
                    mock_raw_products.find_one.return_value = product
                    success = consumer.process_message(message)

        assert success
        assert mock_notification_enrichment_notify.call_args == call(
            product=product,
            attributes={'event_type': EnrichmentEventType.ALL.value},
            trace_id=tracking_id
        )

    @pytest.mark.parametrize('tracking_id', [('fake'), (None)])
    def test_when_process_successfully_then_send_notification_to_enrichment_and_update_product(  # noqa
        self,
        consumer,
        product,
        message,
        patch_notification_put,
        patch_evaluate_scopes,
        patch_put_factsheet,
        patch_put_media,
        patch_merge_process,
        patch_notification_enrichment_notify,
        mock_metabooks_process_payload,
        mongo_database,
        tracking_id
    ):
        mongo_database.raw_products.insert_one(product)
        product.pop('_id', None)
        with patch_evaluate_scopes as mock_evaluate_scopes:
            with patch_notification_enrichment_notify as mock_notification_enrichment_notify:  # noqa
                with patch_put_factsheet as mock_put_factsheet:
                    with patch_put_media as mock_put_media:
                        with patch_merge_process, patch_notification_put as mock_notification_put:  # noqa
                            mock_evaluate_scopes.return_value = mock_metabooks_process_payload  # noqa
                            success = consumer.process_message(message)

        payload = {
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'navigation_id': product['navigation_id']
        }

        assert success
        assert mock_put_factsheet.call_args == call(
            **payload,
            payload={'items': ['Factsheet from metabooks']}
        )
        assert mock_put_media.call_args == call(
            **payload,
            payload={'images': 'Images from metabooks'}
        )

        payload.update({'tracking_id': None})
        assert mock_notification_put.call_args == call(
            data=payload,
            scope='metadata_verify',
            action=UPDATE_ACTION
        )

        assert mock_notification_enrichment_notify.call_args == call(
            product=product,
            attributes={'event_type': EnrichmentEventType.ALL.value},
            trace_id=None
        )

    def test_when_put_factsheet_then_sended_with_success(
        self,
        consumer,
        product,
        patch_pubsub
    ):
        with patch_pubsub as mock_factsheet_stream:
            consumer._put_factsheet(
                sku=product['sku'],
                seller_id=product['seller_id'],
                navigation_id=product['navigation_id'],
                payload={'item': 'Factsheet from Metabooks'},
            )

        assert mock_factsheet_stream.publish.call_args_list[0][1] == {
            'content': {
                'action': 'create',
                'data': {
                    'item': 'Factsheet from Metabooks',
                    'source': 'metadata_verify'
                }
            },
            'topic_name': 'taz-factsheet',
            'project_id': 'maga-homolog'
        }

    def test_when_put_factsheet_empty_then_not_send_message(
        self,
        consumer,
        product,
        patch_pubsub
    ):
        with patch_pubsub as mock_factsheet_stream:
            consumer._put_factsheet(
                sku=product['sku'],
                seller_id=product['seller_id'],
                navigation_id=product['navigation_id'],
                payload={},
            )

        assert not mock_factsheet_stream.called

    def test_when_put_media_then_send_with_success(
        self,
        consumer,
        product,
        patch_pubsub
    ):
        with patch_pubsub as mock_media_stream:
            consumer._put_media(
                sku=product['sku'],
                seller_id=product['seller_id'],
                navigation_id=product['navigation_id'],
                payload={'item': 'Media from Metabooks'},
            )

        assert mock_media_stream.publish.call_args_list[0][1].get('content') == { # noqa
            "action": CREATE_ACTION,
            "data": {
                "item": "Media from Metabooks",
                "source": "metadata_verify"
            }
        }

    def test_when_put_media_empty_then_not_send_message(
        self,
        consumer,
        product,
        patch_pubsub
    ):
        with patch_pubsub as mock_media_stream:
            consumer._put_media(
                sku=product['sku'],
                seller_id=product['seller_id'],
                navigation_id=product['navigation_id'],
                payload={},
            )

        assert not mock_media_stream.publish.called

    def test_when_merge_process_then_execution_success(
        self,
        consumer,
        product,
        patch_merger_merge
    ):
        with patch_merger_merge as mock_merger_merge:
            consumer._execute_merger(
                raw_product=product,
                enriched_product=None,
                action=CREATE_ACTION
            )

        assert mock_merger_merge.called

    def test_when_merge_process_with_generic_exception_then_raise_exception(
        self,
        consumer,
        product,
        patch_merger_merge
    ):
        with pytest.raises(Exception):
            with patch_merger_merge as mock_merger_merge:
                mock_merger_merge.side_effect = Exception
                consumer._execute_merger(
                    raw_product=product,
                    enriched_product=None,
                    action=CREATE_ACTION
                )

        assert mock_merger_merge.called

    def test_when_evaluate_scopes_with_invalid_scope_then_raise_exception(
        self,
        consumer,
        product,
        patch_get_scope
    ):
        with pytest.raises(InvalidScope):
            with patch_get_scope as mock_get_scope:
                mock_get_scope.side_effect = InvalidScope(scope_name='invalid')
                consumer._evaluate_scopes(
                    product['sku'],
                    product['seller_id'],
                    product['navigation_id'],
                    product,
                    [('invalid', 'fake')]
                )

    @settings_stub(SCOPES_ALLOWED_SEND_IMAGES_TO_MEDIA=[])
    def test_when_product_tm_evaluate_scopes_with_metabooks_then_send_to_frajola(  # noqa
        self,
        consumer,
        product,
        patch_frajola_process,
        patch_get_scope,
        mock_metabooks_process_payload
    ):
        product['categories'][0]['id'] = 'TM'

        mock_metabooks = Mock()
        mock_metabooks.process.return_value = mock_metabooks_process_payload  # noqa
        fake_scopes = [mock_metabooks]

        fake_expected_scopes = self.fake_scopes_ordered_response(True, False, False)  # noqa
        with patch_get_scope as mock_get_scope:
            with patch_frajola_process as mock_frajola_process:
                mock_get_scope.side_effect = fake_scopes
                consumer._evaluate_scopes(
                    product['sku'],
                    product['seller_id'],
                    product['navigation_id'],
                    product,
                    fake_expected_scopes
                )

        assert mock_frajola_process.called

    @settings_stub(SCOPES_ALLOWED_SEND_IMAGES_TO_MEDIA=[])
    def test_when_product_different_than_tm_evaluate_scopes_with_metabooks_then_skip_send_to_frajola(  # noqa
        self,
        consumer,
        product,
        patch_frajola_process,
        patch_get_scope,
        mock_metabooks_process_payload
    ):
        product['categories'][0]['id'] = 'RC'

        mock_metabooks = Mock()
        mock_metabooks.process.return_value = mock_metabooks_process_payload
        fake_scopes = [mock_metabooks]

        fake_expected_scopes = self.fake_scopes_ordered_response(True, False, False)  # noqa
        with patch_get_scope as mock_get_scope:
            with patch_frajola_process as mock_frajola_process:
                mock_get_scope.side_effect = fake_scopes
                consumer._evaluate_scopes(
                    product['sku'],
                    product['seller_id'],
                    product['navigation_id'],
                    product,
                    fake_expected_scopes
                )

        assert not mock_frajola_process.called

    @settings_stub(SCOPES_ALLOWED_SEND_IMAGES_TO_MEDIA=[])
    def test_when_disabled_enrichment_medias_then_result_is_empty(  # noqa
        self,
        consumer,
        product,
        patch_frajola_process,
        patch_get_scope,
        mock_metabooks_process_payload
    ):

        mock_metabooks = Mock()
        mock_metabooks.process.return_value = mock_metabooks_process_payload
        fake_scopes = [mock_metabooks]

        fake_expected_scopes = self.fake_scopes_ordered_response(True, False, False)  # noqa
        with patch_get_scope as mock_get_scope:
            with patch_frajola_process:
                mock_get_scope.side_effect = fake_scopes
                response = consumer._evaluate_scopes(
                    product['sku'],
                    product['seller_id'],
                    product['navigation_id'],
                    product,
                    fake_expected_scopes
                )

        assert response == {
            'factsheet': ANY,
            'media': {},
            'enriched_product': ANY
        }

    @settings_stub(SCOPES_ALLOWED_SEND_IMAGES_TO_MEDIA=['metabooks'])
    def test_when_enabled_enrichment_medias_and_scope_without_media_then_ignore_media_from_scope(  # noqa
        self,
        consumer,
        product,
        patch_frajola_process,
        patch_get_scope,
        mock_metabooks_process_payload
    ):
        mock_metabooks = Mock()
        mock_metabooks_process_payload['media'] = {}
        mock_metabooks.process.return_value = mock_metabooks_process_payload
        fake_scopes = [mock_metabooks]

        fake_expected_scopes = self.fake_scopes_ordered_response(True, False, False)  # noqa
        with patch_get_scope as mock_get_scope:
            with patch_frajola_process:
                mock_get_scope.side_effect = fake_scopes
                response = consumer._evaluate_scopes(
                    product['sku'],
                    product['seller_id'],
                    product['navigation_id'],
                    product,
                    fake_expected_scopes
                )

        assert response == mock_metabooks_process_payload

    @settings_stub(SCOPES_ALLOWED_SEND_IMAGES_TO_MEDIA=['metabooks'])
    def test_when_enabled_enrichment_medias_then_return_metabooks_medias(  # noqa
        self,
        consumer,
        product,
        patch_frajola_process,
        patch_get_scope,
        mock_metabooks_process_payload
    ):

        mock_metabooks = Mock()
        mock_metabooks.process.return_value = mock_metabooks_process_payload
        fake_scopes = [mock_metabooks]

        fake_expected_scopes = self.fake_scopes_ordered_response(True, False, False)  # noqa
        with patch_get_scope as mock_get_scope:
            with patch_frajola_process:
                mock_get_scope.side_effect = fake_scopes
                response = consumer._evaluate_scopes(
                    product['sku'],
                    product['seller_id'],
                    product['navigation_id'],
                    product,
                    fake_expected_scopes
                )

        assert response == mock_metabooks_process_payload

    @settings_stub(
        SCOPES_ALLOWED_SEND_IMAGES_TO_MEDIA=['metabooks', 'smartcontent']
    )
    def test_when_priority_scope_on_enrichment_media_is_empty_then_return_next_priority(  # noqa
        self,
        consumer,
        product,
        patch_frajola_process,
        patch_get_scope,
        mock_metabooks_process_payload,
        mock_smartcontent_process_payload
    ):
        mock_metabooks = Mock()
        mock_smartcontent = Mock()
        mock_smartcontent_process_payload['media'] = {}
        mock_metabooks.process.return_value = mock_metabooks_process_payload
        mock_smartcontent.process.return_value = mock_smartcontent_process_payload  # noqa
        fake_scopes = [mock_metabooks, mock_smartcontent]

        fake_expected_scopes = self.fake_scopes_ordered_response(True, True, False)  # noqa
        with patch_get_scope as mock_get_scope:
            with patch_frajola_process:
                mock_get_scope.side_effect = fake_scopes
                response = consumer._evaluate_scopes(
                    product['sku'],
                    product['seller_id'],
                    product['navigation_id'],
                    product,
                    fake_expected_scopes
                )

        assert response == {
            'factsheet': mock_smartcontent_process_payload['factsheet'],
            'media': mock_metabooks_process_payload['media'],
            'enriched_product': mock_smartcontent_process_payload['enriched_product']  # noqa
        }

    @settings_stub(SCOPES_ALLOWED_SEND_IMAGES_TO_MEDIA=['metabooks'])
    def test_when_evaluate_scopes_with_all_scopes_enabled_then_return_datasheet(  # noqa
        self,
        consumer,
        product,
        patch_frajola_process,
        patch_get_scope,
        mock_metabooks_process_payload,
        mock_smartcontent_process_payload,
        mock_datasheet_process_payload
    ):
        mock_metabooks = Mock()
        mock_smartcontent = Mock()
        mock_datasheet = Mock()
        mock_metabooks.process.return_value = mock_metabooks_process_payload
        mock_smartcontent.process.return_value = mock_smartcontent_process_payload  # noqa
        mock_datasheet.process.return_value = mock_datasheet_process_payload
        fake_scopes = [mock_metabooks, mock_smartcontent, mock_datasheet]

        fake_expected_scopes = self.fake_scopes_ordered_response(True, True, True)  # noqa
        with patch_get_scope as mock_get_scope:
            with patch_frajola_process:
                mock_get_scope.side_effect = fake_scopes
                response = consumer._evaluate_scopes(
                    product['sku'],
                    product['seller_id'],
                    product['navigation_id'],
                    product,
                    fake_expected_scopes
                )

        assert response == {
            'factsheet': mock_datasheet_process_payload['factsheet'],
            'media': mock_metabooks_process_payload['media'],
            'enriched_product': mock_datasheet_process_payload['enriched_product']  # noqa
        }

    @settings_stub(SCOPES_ALLOWED_SEND_IMAGES_TO_MEDIA=[])
    def test_when_process_scope_without_response_then_skip_scope(  # noqa
        self,
        consumer,
        product,
        patch_frajola_process,
        patch_get_scope
    ):

        mock_metabooks = Mock()
        mock_metabooks.process.return_value = None
        fake_scopes = [mock_metabooks]

        fake_expected_scopes = self.fake_scopes_ordered_response(True, False, False)  # noqa
        with patch_get_scope as mock_get_scope:
            with patch_frajola_process:
                mock_get_scope.side_effect = fake_scopes
                response = consumer._evaluate_scopes(
                    product['sku'],
                    product['seller_id'],
                    product['navigation_id'],
                    product,
                    fake_expected_scopes
                )

        assert response == {
            'media': {},
            'factsheet': {},
            'enriched_product': {}
        }

    def test_when_product_3p_called_frajola_then_skip_message(
        self,
        consumer,
        product,
        patch_frajola_put
    ):
        product.update({'seller_id': 'fake'})
        with patch_frajola_put as mock_frajola_put:
            consumer._frajola_process(
                product['sku'],
                product['seller_id'],
                product['navigation_id'],
                product
            )

        assert not mock_frajola_put.called

    def test_when_product_1p_called_frajola_then_put_payload(
        self,
        consumer,
        product,
        patch_frajola_put
    ):
        with patch_frajola_put as mock_frajola_put:
            consumer._frajola_process(
                product['sku'],
                product['seller_id'],
                product['navigation_id'],
                product
            )

        assert mock_frajola_put.call_args == call(
            product['sku'],
            {
                'category_id': 'TM', 'subcategory_id': 'HQRC',
                'title': product['title'],
                'reference': product['reference'],
                'brand': product['brand'],
                'active': True
            }
        )

    def test_when_get_invalid_scope_then_raise_exception(
        self,
        consumer
    ):
        with pytest.raises(InvalidScope):
            consumer._get_scope('invalid')

    def test_when_notify_then_send_notification(
        self,
        consumer,
        product,
        patch_notification_property,
        patch_notification_put
    ):
        payload = {
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'navigation_id': product['navigation_id'],
            'tracking_id': 'bbf11b38-bb18-4555-baa1-2f2616098bc4'
        }
        with patch_notification_property as mock_notification_property:
            with patch_notification_put as mock_notifitation_put:
                mock_notification_property.put = mock_notifitation_put
                consumer._send_notification(
                    product=product,
                    **payload
                )

        assert mock_notifitation_put.call_args == call(
            data=payload,
            scope='metadata_verify',
            action=UPDATE_ACTION
        )
