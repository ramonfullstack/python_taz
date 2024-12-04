import pytest

from taz import constants
from taz.consumers.metadata_verify.scopes.smartcontent.helpers import (
    create_enriched_product_payload,
    create_factsheet_payload,
    create_media_payload
)
from taz.consumers.metadata_verify.scopes.smartcontent.tests.samples import (
    SmartcontentSamples
)


class TestCreateFactsheetSmartContentPayload:

    @pytest.fixture
    def navigation_id_smartcontent(self):
        return '12345'

    @pytest.mark.parametrize('payload_smartcontent, expected', [
        (SmartcontentSamples.payload_smartcontent()),
        (SmartcontentSamples.payload_smartcontent_with_special_content()),
        (SmartcontentSamples.payload_smartcontent_with_manual())
    ])
    def test_create_factsheet_payload_smartcontent(
        self,
        payload_smartcontent,
        expected,
        sku,
        seller_id
    ):
        payload = create_factsheet_payload(
            sku=sku,
            seller_id=seller_id,
            metadata=payload_smartcontent
        )
        assert expected == payload

    @pytest.mark.parametrize('payload_media, expected', [
        (SmartcontentSamples.payload_smartcontent_media()),
        (SmartcontentSamples.payload_smartcontent_media_with_manual())
    ])
    def test_create_media_payload_smartcontent(
        self,
        sku,
        seller_id,
        payload_media,
        expected
    ):
        payload = create_media_payload(
            sku=sku,
            seller_id=seller_id,
            metadata=payload_media
        )

        assert expected == payload

    def test_create_enriched_product_payload_smartcontent(
        self,
        sku,
        seller_id,
        navigation_id_smartcontent,
        product_smartcontent
    ):
        payload = create_enriched_product_payload(
            sku=sku,
            seller_id=seller_id,
            navigation_id=navigation_id_smartcontent,
            metadata=product_smartcontent
        )

        assert payload == {
            'seller_id': seller_id,
            'sku': sku,
            'navigation_id': navigation_id_smartcontent,
            'metadata': {
                'Cor': 'Preto',
                'Tamanho': '20 metros'
            },
            'title': 'Freezer Vertical Consul 246L - CVU30EBANA',
            'description': 'O Freezer Consul Vertical',
            'source': constants.SOURCE_SMARTCONTENT,
            'entity': 'Freezer',
            'brand': 'Consul'
        }

    @pytest.mark.parametrize('payload_smartcontent, expected', [
        (SmartcontentSamples.payload_smartcontent())
    ])
    def test_payload_smartcontent_without_description_should_not_return_presentation_field( # noqa
        self,
        payload_smartcontent,
        expected,
        sku,
        seller_id
    ):

        del payload_smartcontent['description']
        del expected['items'][0]

        payload = create_factsheet_payload(
            sku=sku,
            seller_id=seller_id,
            metadata=payload_smartcontent
        )
        assert expected == payload
