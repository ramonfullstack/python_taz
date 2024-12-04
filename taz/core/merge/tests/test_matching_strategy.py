import pytest
from simple_settings.utils import settings_stub

from taz.constants import (
    CHESTER_STRATEGY,
    MAGAZINE_LUIZA_SELLER_ID,
    OMNILOGIC_STRATEGY,
    SINGLE_SELLER_STRATEGY,
    SOURCE_METABOOKS,
    SOURCE_OMNILOGIC,
    SOURCE_WAKKO
)
from taz.core.merge.matching_strategy import (
    ChesterMatchingStrategy,
    OmnilogicMatchingStrategy
)


class TestChesterMatchingStrategy:

    @pytest.fixture
    def chester(self):
        return ChesterMatchingStrategy()

    @settings_stub(ENABLED_CHESTER_STRATEGY=True)
    @settings_stub(ENABLED_CATEGORIES_CHESTER_STRATEGY=['LI'])
    @settings_stub(ENABLED_SUBCATEGORIES_CHESTER_STRATEGY=['OTLI'])
    def test_when_all_validation_from_chester_strategy_is_true_then_should_return_payload_with_success( # noqa
        self,
        chester,
        mock_matching_uuid
    ):
        result = chester.validate_and_get_matching_strategy(
            product={
                'categories': [
                    {
                        'id': 'LI',
                        'subcategories': [{'id': 'OTLI'}]
                    }
                ],
                'matching_strategy': SINGLE_SELLER_STRATEGY,
                'matching_uuid': mock_matching_uuid
            }
        )

        assert result == {'matching_strategy': CHESTER_STRATEGY}

    @pytest.mark.parametrize(
        'enabled_chester,'
        'matching_uuid,'
        'category_allowed,'
        'category,'
        'subcategories_allowed,'
        'subcategories,', [
            (False, True, 'LI', 'LI', ['*'], 'OTLI'),
            (True, False, 'LI', 'LI', ['*'], 'OTLI'),
            (True, True, 'LI', 'MD', ['*'], 'OTLI'),
            (True, True, 'LI', 'LI', ['OTLI'], 'OT')
        ]
    )
    def test_when_chester_strategy_failed_validation_then_should_return_empty_payload( # noqa
        self,
        chester,
        mock_matching_uuid,
        enabled_chester,
        matching_uuid,
        category_allowed,
        category,
        subcategories_allowed,
        subcategories
    ):
        with settings_stub(
            ENABLED_CHESTER_STRATEGY=enabled_chester,
            ENABLED_CATEGORIES_CHESTER_STRATEGY=[category_allowed],
            ENABLED_SUBCATEGORIES_CHESTER_STRATEGY=subcategories_allowed
        ):
            result = chester.validate_and_get_matching_strategy(
                product={
                    'categories': [
                        {
                            'id': category,
                            'subcategories': [{'id': subcategories}]
                        }
                    ],
                    'matching_strategy': SINGLE_SELLER_STRATEGY,
                    'matching_uuid': (
                        mock_matching_uuid if matching_uuid
                        else ''
                    )
                }
            )

        assert not result


class TestOmnilogicMatchingStrategy:

    @pytest.fixture
    def omnilogic(self):
        return OmnilogicMatchingStrategy()

    @pytest.fixture
    def mock_enriched_products_db(self):
        return [
            {
                'sku': '123',
                'seller_id': MAGAZINE_LUIZA_SELLER_ID,
                'source': SOURCE_METABOOKS
            },
            {
                'sku': '123',
                'seller_id': MAGAZINE_LUIZA_SELLER_ID,
                'product_hash': 'e57e41cd7437c12600b6e74e234f872e',
                'entity': 'Livro',
                'source': SOURCE_OMNILOGIC
            },
            {
                'sku': '123',
                'seller_id': MAGAZINE_LUIZA_SELLER_ID,
                'source': SOURCE_WAKKO
            }
        ]

    @settings_stub(ENABLE_MATCHING_FROM_ENTITY=['Livro'])
    def test_when_all_validation_from_omnilogic_strategy_is_true_then_should_return_payload_with_success( # noqa
        self,
        omnilogic,
        mock_enriched_products_db
    ):
        result = omnilogic.validate_and_get_matching_strategy(
            enriched_products=mock_enriched_products_db
        )

        assert result == {'matching_strategy': OMNILOGIC_STRATEGY}

    @pytest.mark.parametrize(
        'source_omnilogic,'
        'product_hash,'
        'entity_allowed,'
        'entity', [
            (False, True, 'Livro', 'Livro'),
            (True, False, 'Livro', 'Livro'),
            (True, True, 'Livro', 'Celular')
        ]
    )
    def test_when_omnilogic_strategy_failed_validation_then_should_return_empty_payload( # noqa
        self,
        omnilogic,
        mock_enriched_products_db,
        source_omnilogic,
        product_hash,
        entity_allowed,
        entity
    ):
        if not source_omnilogic:
            del mock_enriched_products_db[1]

        if not product_hash:
            del mock_enriched_products_db[1]['product_hash']

        mock_enriched_products_db[1]['entity'] = entity

        with settings_stub(ENABLE_MATCHING_FROM_ENTITY=[entity_allowed]):
            result = omnilogic.validate_and_get_matching_strategy(
                enriched_products=mock_enriched_products_db
            )

        assert not result
