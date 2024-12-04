from unittest.mock import ANY, patch

import pytest

from taz.constants import SOURCE_HECTOR, SOURCE_RECLASSIFICATION_PRICE_RULE
from taz.consumers.price_rule import SCOPE
from taz.consumers.price_rule.consumer import (
    MAIOR_IGUAL,
    MENOR_IGUAL,
    TYPE_ENRICHED_PRODUCT,
    PriceRuleProcessor
)


class TestPriceRuleProcessor:

    @pytest.fixture
    def consumer(self):
        return PriceRuleProcessor(SCOPE)

    @pytest.fixture
    def patch_notification(self):
        return patch.object(PriceRuleProcessor, '_send_notification')

    @pytest.fixture
    def patch_enriched_product(self):
        return patch.object(PriceRuleProcessor, 'enriched_products')

    @pytest.fixture
    def patch_prices(self):
        return patch.object(PriceRuleProcessor, 'prices')

    @pytest.fixture
    def patch_category_merge(self):
        return patch.object(PriceRuleProcessor, 'category_merger')

    @pytest.fixture
    def patch_delete_taz_enriched_product(self):
        return patch.object(PriceRuleProcessor, 'delete_taz_enriched_product')

    @pytest.fixture
    def patch_post_taz_enriched_product(self):
        return patch.object(PriceRuleProcessor, 'post_taz_enriched_product')

    @pytest.fixture
    def patch_send_notification(self):
        return patch.object(PriceRuleProcessor, '_send_notification')

    @pytest.fixture
    def classifications_rules(self):
        return [
            {
                '_id': '7ae906d8-2690-4802-8cca-350776cca944',
                'operation': MENOR_IGUAL,
                'price': 1000.00,
                'product_type': 'Refrigerador',
                'active': True,
                'to': {
                    'product_type': 'Peças para Refrigerador',
                    'category_id': 'ED',
                    'subcategory_ids': ['FAPG', 'REFR', 'ACRF'],
                },
            },
            {
                '_id': '88d7e43d-74e4-4a05-b049-3c8ef7af2317',
                'operation': MAIOR_IGUAL,
                'price': 2000.00,
                'product_type': 'Refrigerador',
                'active': True,
                'to': {
                    'product_type': 'Super Refrigerador',
                    'category_id': 'ED',
                    'subcategory_ids': ['SFAPG', 'SREFR', 'SACRF'],
                },
            }
        ]

    @pytest.fixture
    def enriched_products(self):
        return [
            {
                'sku': '230382400',
                'seller_id': 'magazineluiza',
                'navigation_id': '230382400',
                'classifications': [
                    {
                        'product_type': 'Refrigerador',
                        'category_id': 'ED',
                        'subcategories': ['FAPG', 'REFR', 'ACRF'],
                        'channel': 'magazineluiza'
                    }
                ],
                'source': SOURCE_HECTOR,
            },
            {
                'seller_id': 'magazineluiza',
                'sku': '228622200',
                'navigation_id': '228622200',
                'rule_id': 'id of classifications_rules',
                'price': 300.00,
                'from': {
                    'product_type': 'Refrigerador',
                    'category_id': 'ED',
                    'subcategories': ['REFR']
                },
                'category_id': 'ED',
                'subcategory_ids': ['FAPG', 'REFR', 'ACRF'],
                'product_type': 'Peças para Refrigerador',
                'source': SOURCE_RECLASSIFICATION_PRICE_RULE,
            }
        ]

    @pytest.fixture
    def mock_expected_enriched_product(self):
        return {
            'sku': '230382400',
            'seller_id': 'magazineluiza',
            'navigation_id': '230382400',
            'price': 300.00,
            'from': {
                'product_type': 'Refrigerador',
                'category_id': 'ED',
                'subcategory_ids': [
                    'FAPG',
                    'REFR',
                    'ACRF',
                ],
                'source': 'hector',
            },
            'rule_id': '7ae906d8-2690-4802-8cca-350776cca944',
            'category_id': 'ED',
            'subcategory_ids': ['FAPG', 'REFR', 'ACRF'],
            'product_type': 'Peças para Refrigerador',
            'source': SOURCE_RECLASSIFICATION_PRICE_RULE,
        }

    @pytest.fixture
    def save_enriched_product(self, enriched_products, mongo_database):
        mongo_database.enriched_products.insert_many(enriched_products)

    @pytest.fixture
    def save_classification_rule(self, classifications_rules, mongo_database):
        mongo_database.classifications_rules.insert_many(classifications_rules)

    def test_with_source_reclassification_and_type_enriched(
        self,
        consumer,
        patch_notification,
        caplog
    ):
        with patch_notification as mock_notification:
            result = consumer.process_message(
                {
                    'sku': 'sku',
                    'seller_id': 'seller_id',
                    'navigation_id': 'navigation_id',
                    'type': TYPE_ENRICHED_PRODUCT,
                    'source': SOURCE_RECLASSIFICATION_PRICE_RULE,
                    'tracking_id': 'tracking_id',
                    'origin': 'test_price_rule'
                }
            )
            assert result is True

        assert (
            'Request price rule sku:sku seller_id:seller_id '
            'navigation_id:navigation_id source:reclassification_price_rule '
            'from origin:test_price_rule' in caplog.text
        )

        mock_notification.assert_called_once_with(
            action=ANY,
            sku='sku',
            seller_id='seller_id',
            navigation_id='navigation_id',
            tracking_id='tracking_id',
        )

    def test_with_type_price_not_found_in_enriched(
        self,
        consumer,
        patch_enriched_product,
        patch_send_notification,
    ):
        with patch_enriched_product as mock_enriched_product:
            with patch_send_notification as mock_send_notification:
                mock_enriched_product.find.return_value = []
                mock_send_notification.return_value = None
                result = consumer.process_message(
                    {
                        'sku': 'sku',
                        'seller_id': 'seller_id',
                        'navigation_id': 'navigation_id',
                        'type': TYPE_ENRICHED_PRODUCT
                    }
                )
                mock_enriched_product.find.assert_called_once_with({
                    'sku': 'sku',
                    'seller_id': 'seller_id',
                    'source': ANY
                })
                assert mock_send_notification.call_count == 1
                assert result is True

    def test_enriched_product_rule_change(
        self,
        consumer,
        save_enriched_product,
        patch_delete_taz_enriched_product,
    ):
        with patch_delete_taz_enriched_product as mock_delete_taz_enriched_product: # noqa
            mock_delete_taz_enriched_product.return_value = None
            result = consumer.process_message(
                {
                    'sku': '228622200',
                    'seller_id': 'magazineluiza',
                    'navigation_id': '228622200',
                    'type': SOURCE_RECLASSIFICATION_PRICE_RULE,
                }
            )
            assert result is True
            mock_delete_taz_enriched_product.assert_called_once_with(
                seller_id='magazineluiza',
                sku='228622200',
                source=SOURCE_RECLASSIFICATION_PRICE_RULE,
            )

    def test_without_match_for_any_rule(
        self,
        consumer,
        patch_prices,
        save_enriched_product,
        save_classification_rule,
        patch_post_taz_enriched_product,
        patch_delete_taz_enriched_product,
        patch_send_notification,
    ):
        sku = '230382400'
        seller_id = 'magazineluiza'
        navigation_id = '230382400'

        with patch_prices as mock_prices:
            with patch_delete_taz_enriched_product as mock_delete_taz_enriched_product: # noqa
                with patch_post_taz_enriched_product as mock_post_taz_enriched_product: # noqa
                    with patch_send_notification as mock_send_notification:
                        mock_prices.find_one.return_value = {'price': 1400.00}
                        mock_delete_taz_enriched_product.return_value = None

                        result = consumer.process_message(
                            {
                                'sku': sku,
                                'seller_id': seller_id,
                                'navigation_id': navigation_id,
                                'type': TYPE_ENRICHED_PRODUCT,
                            }
                        )
                        assert result is True
                        mock_delete_taz_enriched_product.assert_not_called()
                        mock_post_taz_enriched_product.assert_not_called()
                        assert mock_send_notification.call_count == 1

    def test_with_source_price_with_rule_less_or_equal(
        self,
        consumer,
        save_enriched_product,
        save_classification_rule,
        patch_prices,
        patch_post_taz_enriched_product,
        mock_expected_enriched_product
    ):
        sku = '230382400'
        seller_id = 'magazineluiza'
        navigation_id = '230382400'

        with patch_prices as mock_prices:
            with patch_post_taz_enriched_product as mock_post_taz_enriched_product: # noqa
                mock_prices.find_one.return_value = {'price': 300.00}
                mock_post_taz_enriched_product.return_value = None

                result = consumer.process_message(
                    {
                        'sku': sku,
                        'seller_id': seller_id,
                        'navigation_id': navigation_id,
                        'type': 'price',
                    }
                )

                mock_post_taz_enriched_product.assert_called_once_with(
                    mock_expected_enriched_product
                )
                assert result is True

    def test_when_not_have_changed_classification_without_reclassification_return_true(  # noqa
        self,
        classifications_rules,
        consumer
    ):
        assert consumer._has_changed_classification_rule(
            rule=classifications_rules[1],
            enriched={}
        )

    def test_when_the_selected_rule_has_already_been_applied_then_return_false(
        self,
        classifications_rules,
        mock_expected_enriched_product,
        consumer
    ):
        assert not consumer._has_changed_classification_rule(
            rule=classifications_rules[0],
            enriched=mock_expected_enriched_product
        )

    def test_when_has_changed_applied_rule_then_return_true(
        self,
        classifications_rules,
        mock_expected_enriched_product,
        consumer
    ):
        assert consumer._has_changed_classification_rule(
            rule=classifications_rules[1],
            enriched=mock_expected_enriched_product
        )
