from unittest.mock import patch

import pytest
from simple_settings.utils import settings_stub

from taz import constants
from taz.consumers.core.exceptions import NotFound
from taz.consumers.product_score.consumer import ProductScoreProcessor
from taz.core.matching.common.enriched_products import EnrichedProductSamples
from taz.core.matching.common.samples import ProductSamples
from taz.core.score import Score
from taz.utils import cut_product_id


class TestProductScoreConsumer:

    @pytest.fixture
    def scope(self):
        return "product_score"

    @pytest.fixture
    def consumer(self, scope):
        return ProductScoreProcessor(scope)

    @pytest.fixture
    def product(self):
        return ProductSamples.magazineluiza_sku_0233847()

    @pytest.fixture
    def message(self, product):
        return {
            'origin': 'xablau',
            'seller_id': product['seller_id'],
            'sku': product['sku']
        }

    @pytest.fixture
    def save_product(self, mongo_database, product):
        mongo_database.raw_products.save(product)

    @pytest.fixture
    def save_enriched_product(self, mongo_database):
        enriched = EnrichedProductSamples.magazineluiza_sku_0233847()
        mongo_database.enriched_products.save(enriched)

    @pytest.fixture
    def save_medias(self, mongo_database, product):
        media = {
            'images': [
                'd2e14e48997a911745931e6a2991b2cf.jpg'
            ],
            'seller_id': product['seller_id'],
            'sku': product['sku']
        }

        mongo_database.medias.save(media)

    @pytest.fixture
    def save_customer_behaviors(self, mongo_database, product):
        customer_behaviors = [{
            'product_id': cut_product_id(product['navigation_id']),
            'type': constants.META_TYPE_PRODUCT_TOTAL_REVIEW_COUNT,
            'value': 658
        }, {
            'product_id': cut_product_id(product['navigation_id']),
            'type': constants.META_TYPE_PRODUCT_AVERAGE_RATING,
            'value': 4.730769230769231
        }]

        for customer_behavior in customer_behaviors:
            mongo_database.customer_behaviors.save(customer_behavior)

    @pytest.fixture
    def mock_create_payload_product(self):
        return {
            'seller_description': 'Magazine Luiza',
            'title': 'Fritadeira Elétrica Air Fryer/Sem Óleo Mondial',
            'grade': 1010,
            'dimensions': {
                'depth': 0.32,
                'weight': 12.33,
                'height': 0.36,
                'width': 0.32
            },
            'seller_id': 'magazineluiza',
            'brand': 'mondial',
            'created_at': '2017-07-21T08:44:22.543000',
            'last_updated_at': '2018-05-07T13:07:52.507805',
            'md5': '305042de772de075df1c2f6891a468d5',
            'disable_on_matching': False,
            'matching_strategy': 'SINGLE_SELLER',
            'description': 'O que era inimaginável agora é real, sim, você pode fritar alimentos sem usar óleo, sem deixar cheiro de gordura ou fumaça pela casa, e tem mais, você também pode preparar alimentos de maneira incrivelmente rápida e deixar tudo crocante, gostoso e mais saudável para a sua família!\nCom a incrível Fritadeira Sem Óleo Inox RED Premium da Mondial tudo isso está ao seu alcance.  Painel em aço inox e design sofisticado, lâmpadas-piloto que indicam o funcionamento do produto e do aquecimento, controle de temperatura até 200 ºC para a escolha da temperatura ideal de acordo com diferentes tipos de alimentos, cesta removível segura e prática para facilitar o manuseio dos alimentos, timer de 60 minutos com sinal sonoro e desligamento automático. Com muita praticidade, você pode prepara batatas crocantes em apenas 12 min, e com o livro de receitas você também pode preparar pão de queijo, carnes, aperitivos, peixes, frango a passarinho, pastéis doces e muito mais. \n', # noqa
            'main_variation': True,
            'ean': '7899882302516',
            'type': 'product',
            'reference': 'AF-14 3,2L Timer',
            'updated_at': '2018-05-07T09:45:14.827000',
            'main_category': {
                'subcategory': {
                    'id': 'FREL'
                },
                'id': 'EP'
            },
            'sold_count': 35,
            'selections': {
                '12966': [
                    '16734',
                    '16737'
                ],
                '0': [
                    '17637',
                    '19107',
                    '21750',
                    '22009',
                    '22163',
                    '22330',
                    '7291'
                ]
            },
            'sku': '023384700',
            'navigation_id': '023384700',
            'sells_to_company': True,
            'attributes': [
                {
                    'type': 'voltage',
                    'value': '110 volts'
                }
            ],
            'categories': [
                {
                    'subcategories': [
                        {
                            'id': 'FREL'
                        },
                        {
                            'id': 'EFSO'
                        },
                        {
                            'id': 'ELCO'
                        }
                    ],
                    'id': 'EP'
                }
            ],
            'parent_sku': '0233847',
            'media': {
                'images': [
                    '/{w}x{h}/cama-box-queen-size-box/magazineluiza/023384700/13ee4a66986591c0a586f68b.jpg'  # noqa
                ]
            },
            'entity': 'Fritadeira Elétrica',
            'full_title': 'Fritadeira Elétrica Air Fryer/Sem Óleo Mondial - AF-14 3,2L Timer',  # noqa
            'images_count': 1,
            'category_id': 'EP',
            'reviews_count': 658,
            'review_rating': 4.730769230769231,
            'active': True,
            'factsheet_attributes_count': 11
        }

    def test_process_message_should_return_product_not_found(
        self,
        consumer,
        message,
        caplog,
        product,
        patch_pubsub_client
    ):
        with patch_pubsub_client as mock_pubsub:
            consumer.process_message(message)

        assert caplog.records[0].getMessage() == (
            'Product not found for sku:{} seller_id:{}'
        ).format(product['sku'], product['seller_id'])

        assert not mock_pubsub.called

    def test_process_message_should_return_navigation_id_not_exists(
        self,
        consumer,
        message,
        caplog,
        mongo_database,
        patch_pubsub_client
    ):
        product = {
            'sku': message['sku'],
            'seller_id': message['seller_id']
        }

        mongo_database.raw_products.insert_one(product)
        mongo_database.scores.insert_many([
            {
                'origin': 'xablau',
                'seller_id': product['seller_id'],
                'sku': product['sku'],
                'active': True
            },
            {
                'origin': 'xablau',
                'seller_id': product['seller_id'],
                'sku': product['sku'],
                'active': True
            },
            {
                'origin': 'xablau',
                'seller_id': product['seller_id'],
                'sku': product['sku']
            }
        ])

        with patch_pubsub_client as mock_pubsub:
            consumer.process_message(message)

        score_all = mongo_database.scores.find().count()
        score_not_active = mongo_database.scores.find(
            {'active': False}
        ).count()

        assert (
            'Product does not have a navigation_id'
        ) in caplog.records[0].getMessage()

        assert not mock_pubsub.called
        assert score_all == 3
        assert score_not_active == 2

    def test_process_message_should_return_enriched_product_not_found(
        self,
        consumer,
        message,
        caplog,
        save_product,
        product,
        save_score_criteria,
        mongo_database,
        patch_pubsub_client
    ):
        with patch_pubsub_client as mock_pubsub:
            consumer.process_message(message)

        payload = mongo_database.scores.find_one({
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'active': True
        })

        assert payload['md5']
        assert payload['sku'] == product['sku']
        assert payload['seller_id'] == product['seller_id']
        assert mock_pubsub.called

    def test_process_message_should_score_with_rc_category(
        self,
        consumer,
        message,
        caplog,
        save_score_criteria,
        product,
        mongo_database,
        patch_pubsub_client
    ):
        del product['categories']
        mongo_database.raw_products.save(product)

        with patch_pubsub_client as mock_pubsub:
            consumer.process_message(message)

        payload = mongo_database.scores.find_one({
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'active': True
        })

        assert payload['category_id'] == 'RC'
        assert mock_pubsub.called

    def test_process_message_should_score(
        self,
        consumer,
        message,
        caplog,
        save_product,
        save_enriched_product,
        save_score_criteria,
        product,
        mongo_database,
        patch_pubsub_client
    ):
        with patch_pubsub_client as mock_pubsub:
            consumer.process_message(message)

        payload = mongo_database.scores.find_one({
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'active': True
        })

        assert payload['md5']
        assert len(payload['sources']) == 2
        assert payload['sku'] == product['sku']
        assert payload['seller_id'] == product['seller_id']
        assert mock_pubsub.called

    def test_process_message_should_score_with_medias(
        self,
        consumer,
        message,
        caplog,
        save_product,
        save_enriched_product,
        save_score_criteria,
        save_medias,
        product,
        mongo_database,
        patch_pubsub_client
    ):
        with patch_pubsub_client as mock_pubsub:
            consumer.process_message(message)

        payload = mongo_database.scores.find_one({
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'active': True
        })

        assert payload['md5']
        assert len(payload['sources']) == 3
        assert payload['sku'] == product['sku']
        assert payload['seller_id'] == product['seller_id']
        assert mock_pubsub.called

    def test_process_message_should_score_with_customer_behaviors(
        self,
        consumer,
        message,
        caplog,
        save_product,
        save_enriched_product,
        save_score_criteria,
        save_medias,
        save_customer_behaviors,
        product,
        mongo_database,
        patch_pubsub_client
    ):
        with patch_pubsub_client as mock_pubsub:
            consumer.process_message(message)

        payload = mongo_database.scores.find_one({
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'active': True
        })

        assert payload['md5']
        assert len(payload['sources']) == 5
        assert payload['sku'] == product['sku']
        assert payload['seller_id'] == product['seller_id']
        assert mock_pubsub.called

    def test_process_message_should_score_original_and_enriched_product(
        self,
        consumer,
        message,
        caplog,
        save_enriched_product,
        save_score_criteria,
        save_medias,
        save_customer_behaviors,
        product,
        mongo_database,
        patch_pubsub_client
    ):
        product['offer_title'] = 'Fritadeira Elétrica Air Fryer/Sem Óleo Mondial - Preta - 110v - Mondial' # noqa
        mongo_database.raw_products.save(product)

        with patch_pubsub_client as mock_pubsub:
            consumer.process_message(message)

        payload = mongo_database.scores.find_one({
            'sku': product['sku'],
            'seller_id': product['seller_id'],
            'active': True
        })

        assert payload['md5']
        assert len(payload['sources']) == 6
        assert payload['sku'] == product['sku']
        assert payload['seller_id'] == product['seller_id']
        assert mock_pubsub.called

    def test_process_message_with_score_v2_then_should_skip_get_factsheet(
        self,
        consumer,
        message,
        caplog,
        save_enriched_product,
        save_score_criteria,
        save_medias,
        save_customer_behaviors,
        product,
        mongo_database,
        patch_pubsub_client,
        patch_storage_manager_get_json
    ):
        mongo_database.raw_products.save(product)

        with patch_pubsub_client as mock_pubsub:
            with patch_storage_manager_get_json as mock_factsheet:
                consumer.process_message(message)

        assert not mock_factsheet.called
        assert mock_pubsub.called

    @settings_stub(SCORE_VERSION='0.3.0')
    def test_process_message_with_score_v3_then_should_get_factsheet_and_process_with_success( # noqa
        self,
        message,
        caplog,
        save_enriched_product,
        save_score_criteria,
        save_medias,
        save_customer_behaviors,
        product,
        mongo_database,
        patch_pubsub_client,
        patch_storage_manager_get_json,
        factsheet_product_227747300,
        mock_create_payload_product,
        scope
    ):
        mongo_database.raw_products.save(product)
        product['factsheet_attributes_count'] = 11

        with patch_pubsub_client as mock_pubsub:
            with patch_storage_manager_get_json as mock_factsheet:
                with patch.object(Score, 'calculate') as mock_calculate:
                    mock_factsheet.return_value = factsheet_product_227747300
                    ProductScoreProcessor(scope).process_message(message)

        mock_calculate.assert_called_once_with(mock_create_payload_product)
        assert mock_factsheet.called
        assert mock_pubsub.called

    @settings_stub(SCORE_VERSION='0.3.0')
    def test_process_message_with_score_v3_and_factsheet_raise_not_found_then_should_process_with_success_without_factsheet(  # noqa
        self,
        message,
        save_enriched_product,
        save_score_criteria,
        save_medias,
        save_customer_behaviors,
        product,
        mongo_database,
        patch_pubsub_client,
        patch_storage_manager_get_json,
        mock_create_payload_product,
        scope
    ):
        mongo_database.raw_products.save(product)

        with patch_pubsub_client as mock_pubsub:
            with patch_storage_manager_get_json as mock_factsheet:
                mock_factsheet.side_effect = NotFound()
                with patch.object(Score, 'calculate') as mock_calculate:
                    ProductScoreProcessor(scope).process_message(message)

        del mock_create_payload_product['factsheet_attributes_count']
        mock_calculate.assert_called_once_with(mock_create_payload_product)
        assert mock_factsheet.called
        assert mock_pubsub.called

    @pytest.mark.parametrize('navigation_id', [
        '023384700',
        '0233847'
    ])
    def test_process_message_with_navigation_with_7_and_9_digits_then_should_find_values( # noqa
        self,
        message,
        save_enriched_product,
        save_score_criteria,
        save_medias,
        product,
        mongo_database,
        patch_pubsub_client,
        navigation_id,
        scope
    ):
        product['navigation_id'] = navigation_id
        mongo_database.raw_products.save(product)

        customer_behaviors = [
            {
                'product_id': navigation_id,
                'type': constants.META_TYPE_PRODUCT_TOTAL_REVIEW_COUNT,
                'value': 658
            },
            {
                'type': constants.META_TYPE_PRODUCT_AVERAGE_RATING,
                'value': 4.730769230769231,
                'product_id': navigation_id,
            }
        ]

        for customer_behavior in customer_behaviors:
            mongo_database.customer_behaviors.save(customer_behavior)

        with patch_pubsub_client as mock_pubsub:
            with patch.object(Score, 'calculate') as mock_calculate:
                ProductScoreProcessor(scope).process_message(message)

        assert mock_pubsub.called
        assert mock_calculate.called
