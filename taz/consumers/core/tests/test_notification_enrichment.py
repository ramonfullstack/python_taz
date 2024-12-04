from unittest.mock import ANY, patch

import pytest
from simple_settings.utils import settings_stub

from taz.constants import EnrichmentEventType
from taz.consumers.core.notification_enrichment import NotificationEnrichment
from taz.core.matching.common.samples import ProductSamples


class TestNotificationEnrichment:

    @pytest.fixture
    def mock_notification_enrichment(self):
        return NotificationEnrichment()

    @pytest.fixture
    def mock_product_payload(self):
        return ProductSamples.magazineluiza_sku_011704400()

    @pytest.fixture
    def patch_is_enabled_notify(self):
        return patch.object(NotificationEnrichment, '_is_enabled_notify')

    @pytest.fixture
    def patch_find_product_type(self):
        return patch.object(NotificationEnrichment, '_find_product_type')

    @pytest.fixture
    def mock_attributes_enrichment(self):
        return {'event_type': EnrichmentEventType.ALL.value}

    @pytest.fixture
    def mock_product_type(self) -> str:
        return 'Forno Elétrico'

    @pytest.fixture
    def expected_payload(self, mock_product_type: str):
        return {
            'sku': '011704400',
            'seller_id': 'magazineluiza',
            'navigation_id': '011704400',
            'parent_sku': '0117044',
            'identifiers': [
                {
                    'type': 'ean',
                    'value': '7891129204836'
                }
            ],
            'metadata': {
                'title': 'Lava-Louças Brastemp Ative! BLF08AS',
                'description': 'A nova lava-louças Brastemp Ative! 8 serviços traz mais liberdade para você e sua família. São 5 diferentes ciclos pré-programados que lavam louças de até 8 pessoas. Seu cesto superior tem regulagem de altura permitindo acondicionar qualquer tamanho de louça. Conta com indicador de etapas e visor na porta que permite o acompanhamento de todo processo de lavagem além de permitir acompanhar em qual fase a lavagem está. É, ainda, compacta e flexível e pode ser instalada em bancadas ou nichos.\n', # noqa
                'factsheet': 'http://pis.static-tst.magazineluiza.com.br/magazineluiza/factsheet/011704400.json', # noqa
                'medias': [],
                'product_type': mock_product_type
            },
            'trace_id': ANY
        }

    @pytest.mark.parametrize(
        'entity_allowed,entity_product,title,enabled', [
            ('Microondas', 'Microondas', 'title product', True),
            ('Microondas', 'Geladeira', 'title product', False),
            ('*', 'Geladeira', 'title product', True),
            ('*', 'Geladeira', '', False),
            ('*', 'Geladeira', None, False)
        ]
    )
    def test_when_checking_if_the_product_is_valid_for_matching_then_return_if_valid( # noqa
        self,
        mock_notification_enrichment,
        entity_allowed,
        entity_product,
        title,
        enabled
    ):
        with settings_stub(ALLOW_PUBLISH_PRODUCT_METADATA=[entity_allowed]):
            assert mock_notification_enrichment._is_enabled_notify(
                entity_product,
                title,
            ) == enabled

    def test_when_product_enabled_to_matching_then_send_message(
        self,
        patch_find_product_type,
        patch_is_enabled_notify,
        mock_notification_enrichment,
        patch_publish_manager,
        mock_product_payload,
        mock_attributes_enrichment,
        expected_payload,
        mock_product_type,
        patch_generate_uuid,
        mock_uuid
    ):
        expected_payload.update({'trace_id': str(mock_uuid)})
        with patch_is_enabled_notify as mock_is_enabled_notify:
            with patch_publish_manager as mock_pubsub:
                with patch_find_product_type as mock_find_product_type:
                    with patch_generate_uuid:
                        mock_find_product_type.return_value = mock_product_type
                        mock_is_enabled_notify.return_value = True

                        mock_notification_enrichment.notify(
                            mock_product_payload,
                            mock_attributes_enrichment
                        )
                        assert mock_pubsub.call_args_list[0][1]['content'] == expected_payload # noqa

    def test_when_product_disabled_to_matching_then_not_send_message(
        self,
        patch_find_product_type,
        patch_is_enabled_notify,
        mock_notification_enrichment,
        patch_publish_manager,
        mock_product_payload,
        mock_attributes_enrichment
    ):
        with patch_is_enabled_notify as mock_is_enabled_notify:
            with patch_publish_manager as mock_pubsub:
                with patch_find_product_type as mock_find_product_type:
                    mock_find_product_type.return_value = 'Microondas'
                    mock_is_enabled_notify.return_value = False
                    mock_notification_enrichment.notify(
                        mock_product_payload,
                        mock_attributes_enrichment
                    )

                    assert not mock_pubsub.called

    def test_when_product_not_has_title_field_then_not_send_message(
        self,
        patch_publish_manager,
        mock_notification_enrichment,
        mock_product_payload,
        mock_attributes_enrichment
    ):
        del mock_product_payload['title']
        with patch_publish_manager as mock_pubsub:
            mock_notification_enrichment.notify(
                mock_product_payload,
                mock_attributes_enrichment
            )
            mock_pubsub.assert_not_called()

    def test_when_notify_without_event_type_then_not_nofify(
        self,
        patch_publish_manager,
        mock_notification_enrichment,
        mock_product_payload,
        caplog
    ):
        with patch_publish_manager as mock_pubsub:
            mock_notification_enrichment.notify(mock_product_payload)
            mock_pubsub.assert_not_called()
            assert 'Failed send product' in caplog.text

    @pytest.mark.parametrize('invalid_event_type', [('fake'), (None)])
    def test_when_notify_invalid_event_type_then_not_nofify(
        self,
        patch_publish_manager,
        mock_notification_enrichment,
        mock_product_payload,
        invalid_event_type,
        mock_attributes_enrichment,
        caplog
    ):
        mock_attributes_enrichment['event_type'] = invalid_event_type
        with patch_publish_manager as mock_pubsub:
            mock_notification_enrichment.notify(
                mock_product_payload,
                mock_attributes_enrichment
            )
            mock_pubsub.assert_not_called()
            assert 'Failed send product' in caplog.text

    def test_when_product_has_images_then_should_send_message_with_images_paths_with_success( # noqa
        self,
        patch_find_product_type,
        patch_is_enabled_notify,
        mock_notification_enrichment,
        patch_publish_manager,
        mock_product_payload,
        mock_product_images,
        expected_payload,
        mock_attributes_enrichment,
        mock_product_type
    ):
        with patch_is_enabled_notify as mock_is_enabled_notify:
            with patch_publish_manager as mock_pubsub:
                with patch_find_product_type as mock_find_product_type:
                    mock_find_product_type.return_value = mock_product_type
                    mock_is_enabled_notify.return_value = True

                    mock_notification_enrichment.notify(
                        mock_product_payload,
                        mock_attributes_enrichment
                    )

        expected_payload['metadata']['medias'] = [
            'https://x.xx.xxx/600x400/lava-loucas-brastemp-ative-blf08as-8-servicos/magazineluiza/011704400/d4a9dda16aebf1d8fe2bb115669c4155.jpg', # noqa
            'https://x.xx.xxx/600x400/lava-loucas-brastemp-ative-blf08as-8-servicos/magazineluiza/011704400/d4a9dda16aebf1d8fe2bb115669c4155.jpg', # noqa
            'https://x.xx.xxx/600x400/lava-loucas-brastemp-ative-blf08as-8-servicos/magazineluiza/011704400/c2d88c66d6d53a082e52787df7790c01.jpg', # noqa
            'https://x.xx.xxx/600x400/lava-loucas-brastemp-ative-blf08as-8-servicos/magazineluiza/011704400/4ba8da09a782be6a190a79419f4d51a9.jpg' # noqa
        ]

        assert mock_pubsub.call_args_list[0][1]['content'] == expected_payload

    def test_when_product_no_has_images_then_should_send_message_with_images_field_empty( # noqa
        self,
        patch_find_product_type,
        patch_is_enabled_notify,
        mock_notification_enrichment,
        patch_publish_manager,
        mock_product_payload,
        expected_payload,
        caplog,
        mock_attributes_enrichment,
        mock_product_type
    ):
        with patch_is_enabled_notify as mock_is_enabled_notify:
            with patch_publish_manager as mock_pubsub:
                with patch_find_product_type as mock_find_product_type:
                    mock_find_product_type.return_value = mock_product_type
                    mock_is_enabled_notify.return_value = True

                    mock_notification_enrichment.notify(
                        mock_product_payload,
                        mock_attributes_enrichment
                    )

        assert mock_pubsub.call_args_list[0][1]['content'] == expected_payload
        assert 'Images not found for product sku:{} seller_id:{}'.format(
            mock_product_payload['sku'],
            mock_product_payload['seller_id'],
        ) in caplog.text

    def test_when_product_has_tracking_id_then_send_message_trace_using_tracking_id(  # noqa
        self,
        patch_find_product_type,
        patch_is_enabled_notify,
        mock_notification_enrichment,
        patch_publish_manager,
        mock_product_payload,
        mock_attributes_enrichment,
        expected_payload,
        mock_product_type,
        mock_tracking_id
    ):
        expected_payload.update({'trace_id': mock_tracking_id})
        with patch_is_enabled_notify as mock_is_enabled_notify:
            with patch_publish_manager as mock_pubsub:
                with patch_find_product_type as mock_find_product_type:
                    mock_find_product_type.return_value = mock_product_type
                    mock_is_enabled_notify.return_value = True

                    mock_notification_enrichment.notify(
                        mock_product_payload,
                        mock_attributes_enrichment,
                        mock_tracking_id
                    )
                    assert mock_pubsub.call_args_list[0][1]['content'] == expected_payload # noqa
