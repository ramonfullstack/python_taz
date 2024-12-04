from unittest.mock import patch

import pytest
from simple_settings.utils import settings_stub

from taz.core.matching.common.enriched_products import EnrichedProductSamples
from taz.core.matching.common.samples import ProductSamples
from taz.core.merge.scopes.smartcontent import SmartContentScope


class TestSmartContentScope:

    @pytest.fixture
    def product(self):
        return ProductSamples.magazineluiza_sku_0233847()

    @pytest.fixture
    def enriched_product(self):
        return EnrichedProductSamples.magazineluiza_sku_0233847_smartcontent()

    @pytest.fixture
    def smartcontent(self, product, enriched_product):
        return SmartContentScope(product, enriched_product)

    @pytest.fixture
    def mock_apply_cleanup_title(self):
        return patch.object(SmartContentScope, '_apply_title_cleanup')

    @settings_stub(
        ENABLE_SMARTCONTENT_ENRICHMENT_BY_CATEGORY=['*']
    )
    def test_when_call_apply_from_scope_smartcontent_then_should_process_with_success( # noqa
        self,
        smartcontent,
        enriched_product
    ):
        smartcontent.raw_product['attributes'] = []
        smartcontent.apply()

        assert smartcontent.raw_product['title'] == enriched_product['title']
        assert smartcontent.raw_product['description'] == enriched_product['description']  # noqa
        assert smartcontent.raw_product['brand'] == enriched_product['brand']
        assert smartcontent.raw_product['attributes'] == [{
            'type': 'voltage',
            'value': '220 volts'
        }]

    @pytest.mark.parametrize('attribute, expected', [
        (
            {'Voltagem': '110 volts'},
            [{
                'type': 'voltage',
                'value': '110 volts'
            }],
        ),
        (
            {},
            [],
        ),
        (
            {
                'Voltagem': '110 volts',
                'Cor': 'Azul'
            },
            [
                {
                    'type': 'voltage',
                    'value': '110 volts'
                },
                {
                    'type': 'color',
                    'value': 'Azul'
                }
            ],
        )
    ])
    def test_normalize_attributes(
        self,
        smartcontent,
        enriched_product,
        attribute,
        expected,
        patch_storage_manager_get_json
    ):
        smartcontent.enriched_product['metadata'] = attribute

        with patch_storage_manager_get_json as mock_storage:
            mock_storage.return_value = {}
            smartcontent._normalize_attributes()

        attributes = smartcontent.raw_product['attributes']
        attributes = sorted(attributes, key=lambda k: k['type'])
        expected = sorted(expected, key=lambda k: k['type'])

        assert attributes == expected

    @settings_stub(ENABLE_SMARTCONTENT_ENRICHMENT_BY_CATEGORY=[])
    def test_should_skip_normalize_attributes_and_title(
        self,
        smartcontent
    ):
        smartcontent.raw_product['attributes'] = []
        smartcontent.apply()

        assert smartcontent.raw_product['attributes'] == []

    @settings_stub(ENABLE_SMARTCONTENT_ENRICHMENT_BY_CATEGORY=['EP'])
    def test_apply_normalize_when_there_is_category(
        self,
        smartcontent,
        enriched_product
    ):
        smartcontent.raw_product['attributes'] = []
        smartcontent.apply()

        assert smartcontent.raw_product['title'] == enriched_product['title']
        assert smartcontent.raw_product['description'] == enriched_product['description']  # noqa
        assert smartcontent.raw_product['brand'] == enriched_product['brand']

        assert smartcontent.raw_product['attributes'] == [{
            'type': 'voltage',
            'value': '220 volts'
        }]

    @settings_stub(ENABLE_SMARTCONTENT_ENRICHMENT_BY_CATEGORY=['EP'])
    def test_should_enrich_attributes_with_bucket_if_smartcontent_attributes_not_exist( # noqa
        self,
        patch_storage_manager_get_json,
        smartcontent
    ):
        assert smartcontent.raw_product['attributes'] == [{
            'type': 'voltage',
            'value': '110 volts'
        }]

        smartcontent.enriched_product['metadata'] = []

        with patch_storage_manager_get_json as mock_storage:
            mock_storage.return_value = {'attributes': [{
                "type": "capacity",
                "value": "10"
            }]}
            smartcontent.apply()

        assert smartcontent.raw_product['attributes'] == [{
            "type": "capacity",
            "value": "10"
        }]

    @settings_stub(ENABLE_SMARTCONTENT_ENRICHMENT_BY_CATEGORY=['EP'])
    def test_should_enrich_attributes_empty_when_bucket_is_empty(
        self,
        patch_storage_manager_get_json,
        smartcontent
    ):
        assert smartcontent.raw_product['attributes'] == [{
            'type': 'voltage',
            'value': '110 volts'
        }]
        smartcontent.enriched_product['metadata'] = []

        with patch_storage_manager_get_json as mock_storage:
            mock_storage.return_value = None
            smartcontent.apply()

        assert smartcontent.raw_product['attributes'] == []

    @settings_stub(
        ENABLE_SMARTCONTENT_ENRICHMENT_BY_CATEGORY=['EP'],
        SMARTCONTENT_CATEGORY_NOT_ALLOWED_REFERENCE=['EP']
    )
    @pytest.mark.parametrize(
        'concat', [
            ' - ', '- ', ' -', ' '
        ]
    )
    def test_when_category_allowed_to_have_reference_and_reference_is_in_title_then_should_clean_title( # noqa
        self,
        product,
        enriched_product,
        concat
    ):
        title = enriched_product['title']
        reference = 'AF-14 3,2L TIMER í'
        product['reference'] = reference
        enriched_product['title'] += f'{concat} {reference}'
        sc = SmartContentScope(product, enriched_product)
        sc.apply()

        assert sc.raw_product['reference'] == product['reference']
        assert sc.raw_product['title'] == title
        assert sc.raw_product['offer_title'] == '{} - {}'.format(
            title,
            reference
        )

    @settings_stub(
        ENABLE_SMARTCONTENT_ENRICHMENT_BY_CATEGORY=['EP'],
        SMARTCONTENT_CATEGORY_NOT_ALLOWED_REFERENCE=['EP']
    )
    def test_when_category_allowed_to_have_reference_and_reference_not_in_title_then_should_clean_reference( # noqa
        self,
        product,
        enriched_product
    ):
        sc = SmartContentScope(product, enriched_product)
        sc.apply()

        assert sc.raw_product['reference'] == ''

    @settings_stub(
        ENABLE_SMARTCONTENT_ENRICHMENT_BY_CATEGORY=['EP'],
        SMARTCONTENT_CATEGORY_NOT_ALLOWED_REFERENCE=['TE']
    )
    def test_when_category_allowed_to_have_reference_then_should_keep_value(
        self,
        smartcontent,
        product
    ):
        smartcontent.apply()
        assert (
            smartcontent.raw_product['reference'] == product['reference']
        )

    @settings_stub(
        ENABLE_SMARTCONTENT_ENRICHMENT_BY_CATEGORY=['EP'],
        SMARTCONTENT_CATEGORY_NOT_ALLOWED_REFERENCE=['TE']
    )
    def test_when_title_from_enriched_is_empty_then_should_not_change_title_value( # noqa
        self,
        product,
        enriched_product,
        mock_apply_cleanup_title
    ):
        enriched_product['title'] = ''
        sc = SmartContentScope(product, enriched_product)

        with mock_apply_cleanup_title as mock_apply_cleanup:
            sc.apply()

        assert sc.raw_product['title'] == product['title']
        mock_apply_cleanup.assert_not_called()
