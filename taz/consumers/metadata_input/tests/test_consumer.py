from unittest.mock import ANY, Mock, call, patch

import pytest
from simple_settings.utils import settings_stub

from taz.constants import (
    SOURCE_DATASHEET,
    SOURCE_METABOOKS,
    SOURCE_SMARTCONTENT
)
from taz.consumers.core.exceptions import NotFound
from taz.consumers.metadata_input.consumer import MetadataInputRecordProcessor
from taz.consumers.metadata_input.scopes.metabooks import (
    Scope as MetabooksScope
)
from taz.consumers.metadata_input.scopes.smartcontent import (
    Scope as SmartcontentScope
)


class TestMetadataInputRecordProcessor:

    @pytest.fixture
    def consumer(self):
        return MetadataInputRecordProcessor('metadata_input')

    @pytest.fixture
    def patch_save(self, consumer):
        return patch.object(consumer, '_save')

    @pytest.fixture
    def patch_save_images(self, consumer):
        return patch.object(consumer, '_save_images')

    @pytest.fixture
    def patch_consumer_download_image(self, consumer):
        return patch.object(consumer, '_download_image')

    @pytest.fixture
    def patch_notify(self, consumer):
        return patch.object(consumer, '_notify')

    @pytest.fixture
    def patch_scope_process(self):
        return patch.object(
            MetabooksScope,
            'process',
            side_effect=NotFound
        )

    @pytest.fixture
    def metabooks_message(self, metabooks_identified):
        return {
            'identified': metabooks_identified,
            'source': SOURCE_METABOOKS
        }

    @pytest.fixture
    def smartcontent_message(self, smartcontent_identified):
        return {
            'identified': smartcontent_identified,
            'source': SOURCE_SMARTCONTENT
        }

    @pytest.fixture
    def datasheet_message(self, datasheet_identified):
        return {
            'identified': datasheet_identified,
            'source': SOURCE_DATASHEET,
        }

    @pytest.fixture
    def mock_url(self):
        return 'https://murcho.com/test.jpg?access_token=secret_token'

    @pytest.fixture
    def save_product(
        self,
        metabooks_identified,
        smartcontent_identified,
        mongo_database
    ):
        payload = [
            {
                'sku': '123456789',
                'seller_id': 'magazineluiza',
                'ean': metabooks_identified,
                'isbn': metabooks_identified
            },
            {
                'sku': '987654321',
                'seller_id': 'magazineluiza',
                'ean': smartcontent_identified,
                'isbn': smartcontent_identified
            }
        ]

        mongo_database.raw_products.insert_many(payload)

    @pytest.fixture
    def save_enriched_product(
        self,
        metabooks_identified,
        smartcontent_identified,
        datasheet_identified,
        mongo_database
    ):
        payload = [
            {
                'sku': '1234567890',
                'identifier': datasheet_identified,
                'seller_id': 'luizalabs',
                'source': 'datasheet',
            },
            {
                'sku': '987654321',
                'identifier': smartcontent_identified,
                'seller_id': 'magazineluiza',
                'source': 'smartcontent',
            },
            {
                'sku': '0987654321',
                'identifier': datasheet_identified,
                'seller_id': 'luizalabs',
                'source': 'datasheet',
            },
            {
                'sku': '123456789',
                'identifier': metabooks_identified,
                'seller_id': 'magazineluiza',
                'source': 'metabooks',
            },
        ]

        mongo_database.enriched_products.insert_many(payload)

    @pytest.mark.parametrize('message,log_expected', [
        (
            {'source': SOURCE_METABOOKS},
            'Remove message from queue because is invalid payload'
        ),
        (
            {'identifier:': '123'},
            'Remove message from queue because is invalid payload'
        ),
        (
            {'source': 'NOT_EXISTS', 'identified': '123'},
            'Source is unknown for payload'
        )
    ])
    def test_when_consumer_receive_invalid_message_then_should_save_log_and_discard_event( # noqa
        self,
        consumer,
        logger_stream,
        message,
        log_expected
    ):
        result = consumer._is_invalid_message(message)

        assert result
        assert log_expected in logger_stream.getvalue()

    def test_when_identifier_not_found_then_should_save_log_and_return(
        self,
        consumer,
        patch_pubsub_client,
        logger_stream,
        patch_scope_process
    ):
        identified = '00000000'
        with patch_scope_process, patch_pubsub_client as mock_pubsub:
            consumer.process_message(
                {
                    'identified': identified,
                    'source': SOURCE_METABOOKS
                }
            )

        assert not mock_pubsub.called
        assert (
            f'Not found metadata for identifier:'
            f'{identified} source:{SOURCE_METABOOKS}'
        ) in logger_stream.getvalue()

    @settings_stub(METABOOKS_TOKEN='')
    def test_consumer_returns_unauthorized(
        self,
        consumer,
        patch_pubsub_client,
        metabooks_message,
        patch_requests_get
    ):
        with patch_requests_get as mock_get:
            mock_get.return_value = Mock(status_code=401)
            with patch_pubsub_client as mock_pubsub:
                consumer.process_message(metabooks_message)

        assert not mock_pubsub.called

    def test_consumer_save_metabooks_payload(
        self,
        consumer,
        patch_pubsub_client,
        patch_storage_manager_upload,
        metabooks_message,
        patch_requests_get,
        metabooks_payload,
        save_product,
        patch_consumer_download_image
    ):
        with patch_requests_get as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = metabooks_payload
            mock_get.return_value = mock_response
            with patch_consumer_download_image as mock_download_images:
                mock_download_images.return_value = ('==123hfiuha', 'jpg')
                with patch_pubsub_client as mock_pubsub:
                    with patch_storage_manager_upload as mock_storage:
                        consumer.process_message(metabooks_message)

        assert mock_pubsub.called
        assert mock_storage.call_count == 3

    def test_consumer_save_datasheet_payload(
        self,
        consumer,
        patch_pubsub_client,
        patch_storage_manager_upload,
        datasheet_message,
        patch_requests_get,
        smartcontent_payload,
        save_enriched_product,
        patch_consumer_download_image
    ):
        with patch_requests_get as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'data': smartcontent_payload}
            mock_get.return_value = mock_response
            with patch_consumer_download_image as mock_download_images:
                mock_download_images.return_value = ('==123hfiuha', 'jpg')
                with patch_pubsub_client as mock_pubsub:
                    with patch_storage_manager_upload as mock_storage:
                        consumer.process_message(datasheet_message)

        assert mock_pubsub.called
        assert mock_pubsub.call_args_list == [
            call(
                topic='projects/maga-homolog/topics/taz-metadata-verify',
                data=b'{"sku": "1234567890", "seller_id": "luizalabs"}',
                ordering_key='luizalabs/1234567890'
            ),
            call(
                topic='projects/maga-homolog/topics/taz-metadata-verify',
                data=b'{"sku": "0987654321", "seller_id": "luizalabs"}',
                ordering_key='luizalabs/0987654321'
            )
        ]
        assert mock_storage.call_count == 3

    def test_consumer_save_smartcontent_payload(
        self,
        consumer,
        patch_pubsub_client,
        patch_storage_manager_upload,
        smartcontent_message,
        patch_requests_get,
        smartcontent_payload,
        save_product,
        patch_consumer_download_image
    ):
        with patch_requests_get as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'data': smartcontent_payload}
            mock_get.return_value = mock_response
            with patch_consumer_download_image as mock_download_images:
                mock_download_images.return_value = ('==123hfiuha', 'jpg')
                with patch_pubsub_client as mock_pubsub:
                    with patch_storage_manager_upload as mock_storage:
                        consumer.process_message(smartcontent_message)

        assert mock_pubsub.called
        assert mock_storage.call_count == 3

    @settings_stub(METADATA_INPUT_DOWNLOAD_IMAGES_MAX_RETRIES=5)
    def test_when_download_image_return_404_then_should_ignore_retries_and_return( # noqa
        self,
        consumer,
        patch_requests_get,
        metabooks_identified,
        metabooks_message,
        mock_url,
        caplog
    ):
        with patch_requests_get as mock_get:
            mock_get.return_value = Mock(status_code=404)
            data, content_type = consumer._download_image(mock_url)

            assert data is None
            assert content_type is None
            assert (
                'Image not found url:https://murcho.com/test.jpg'
                in caplog.text
            )

    @settings_stub(METADATA_INPUT_DOWNLOAD_IMAGES_MAX_RETRIES=2)
    def test_when_download_image_return_status_code_between_400_and_600_then_should_retry( # noqa
        self,
        consumer,
        patch_requests_get,
        metabooks_identified,
        metabooks_message,
        mock_url,
        caplog
    ):
        with patch_requests_get as mock_get:
            mock_get.return_value = Mock(status_code=500)
            data, content_type = consumer._download_image(mock_url)

            assert data is None
            assert content_type is None
            assert mock_get.call_count == 2
            assert (
                'Could not process url:https://murcho.com/test.jpg '
                'status_code:500' in caplog.text
            )

    @settings_stub(METADATA_INPUT_DOWNLOAD_IMAGES_MAX_RETRIES=2)
    def test_when_download_image_throw_exception_then_should_retry(
        self,
        consumer,
        patch_requests_get,
        metabooks_identified,
        metabooks_message,
        mock_url,
        caplog
    ):
        with patch_requests_get as mock_get:
            mock_get.side_effect = Exception('Generic Error')
            data, content_type = consumer._download_image(mock_url)

            assert data is None
            assert content_type is None
            assert mock_get.call_count == 2
            assert (
                'Error process download with url:'
                'https://murcho.com/test.jpg error:Generic Error'
                in caplog.text
            )

    def test_when_download_images_return_empty_data_then_should_skip_process( # noqa
        self,
        consumer,
        patch_requests_get,
        patch_consumer_download_image,
        metabooks_identified,
        metabooks_payload,
        caplog
    ):
        with patch_consumer_download_image as mock_download_images:
            mock_download_images.return_value = None, None
            result = consumer._save_images(
                metabooks_identified,
                metabooks_payload,
                SOURCE_METABOOKS
            )

        assert not result
        assert (
            f'Skip process download images to identifier:{metabooks_identified}' # noqa
            f' and source:{SOURCE_METABOOKS} because a error occurred'
            in caplog.text
        )

    def test_when_save_images_return_false_then_should_skip_process_and_return_true( # noqa
        self,
        consumer,
        patch_storage_manager_upload,
        metabooks_message,
        patch_requests_get,
        metabooks_payload,
        save_product,
        patch_save,
        patch_save_images
    ):
        with patch_requests_get as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = metabooks_payload
            mock_get.return_value = mock_response
            with patch_save_images as mock_save_images:
                mock_save_images.return_value = False
                with patch_storage_manager_upload, patch_save as mock_save:
                    result = consumer.process_message(metabooks_message)

            assert result
            mock_save.assert_not_called()

    def test_format_ean_to_thirteen_digits_after_get_info_from_specify_source(
        self,
        consumer,
        patch_storage_manager_upload,
        smartcontent_message,
        patch_requests_get,
        smartcontent_payload,
        save_product,
        patch_save,
        patch_save_images,
        patch_notify,
        caplog
    ):
        ean = '123456789'
        format_ean = ean.rjust(13, '0')

        with patch.object(SmartcontentScope, 'process') as mock_sc_scope:
            with patch_requests_get as mock_get:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = smartcontent_payload
                mock_get.return_value = mock_response
                with patch_notify, patch_save_images as mock_save_images:
                    mock_save_images.return_value = True
                    with patch_storage_manager_upload, patch_save as mock_save:
                        smartcontent_message['identified'] = ean
                        result = consumer.process_message(smartcontent_message)

            assert result
            mock_sc_scope.assert_called_once_with(ean)
            mock_save.assert_called_once_with(
                format_ean,
                ANY,
                SOURCE_SMARTCONTENT
            )
            assert (
                'Metadata successfully processed for '
                f'identifier:{format_ean} source:{SOURCE_SMARTCONTENT}'
            ) in caplog.text
