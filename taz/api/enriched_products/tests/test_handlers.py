from unittest.mock import ANY

import pytest

from taz.constants import (
    DELETE_ACTION,
    MAGAZINE_LUIZA_SELLER_ID,
    SOURCE_DATASHEET,
    SOURCE_GENERIC_CONTENT,
    SOURCE_METABOOKS,
    SOURCE_OMNILOGIC,
    SOURCE_RECLASSIFICATION_PRICE_RULE,
    UPDATE_ACTION
)
from taz.core.matching.common.enriched_products import EnrichedProductSamples
from taz.helpers.json import json_loads


class TestEnrichedProducts:

    @pytest.fixture
    def expected_parameters(self):
        return {
            'navigation_id': '6815536',
            'sku': '2546',
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'metadata': {
                'Modelo': '1 Million',
                'Gênero': 'Masculino',
                'Produto': 'Perfume',
                'Ocasião': 'Diurno',
                'Marca': 'Paco Rabanne',
                'Concentração': 'Eau de Toilette',
                'Volume': '50ml'
            }
        }

    @pytest.fixture
    def enriched_products(self):
        return [
            {
                'seller_id': MAGAZINE_LUIZA_SELLER_ID,
                'product_name_metadata': [
                    'Produto',
                    'Marca',
                    'Modelo',
                    'Concentração',
                    'Gênero'
                ],
                'filters_metadata': [
                    'Produto',
                    'Marca',
                    'Modelo',
                    'Concentração',
                    'Gênero',
                    'Ocasião',
                    'Volume'
                ],
                'source': SOURCE_OMNILOGIC,
                'metadata': {
                    'Modelo': '1 Million',
                    'Gênero': 'Masculino',
                    'Produto': 'Perfume',
                    'Ocasião': 'Diurno',
                    'Marca': 'Paco Rabanne',
                    'Concentração': 'Eau de Toilette',
                    'Volume': '50ml'
                },
                'sku': '2546',
                'product_matching_metadata': [
                    'Produto',
                    'Marca',
                    'Modelo'
                ],
                'navigation_id': '6815536',
                'sku_metadata': [
                    'Volume'
                ],
                'category_id': 'CP',
                'product_hash': 'b9efe4e50a2529bbe4176812ac208f8a',
                'timestamp': 1524762426.821082
            },
            EnrichedProductSamples.generic_content_sku_fd3e322aab()
        ]

    @pytest.fixture
    def saved_enriched_products(self, mongo_database, enriched_products):
        payload = enriched_products[0]
        mongo_database.enriched_products.insert_one(payload)

        del payload['_id']
        payload['navigation_id'] = '467890900'

        mongo_database.enriched_products.insert_one(payload)

        del payload['_id']
        payload['source'] = 'murcho'
        payload['navigation_id'] = '6815536'

        mongo_database.enriched_products.insert_one(payload)

    @pytest.fixture
    def save_raw_products(self, mongo_database, enriched_products):
        mongo_database.raw_products.insert_one(
            {
                'sku': enriched_products[-1]['sku'],
                'navigation_id': enriched_products[-1]['navigation_id'],
                'seller_id': enriched_products[-1]['seller_id'],
            }
        )

    @pytest.mark.parametrize(
        'navigation_id,expected_navigation_id',
        [
            ('6815536', '6815536'),
            ('681553600', '6815536'),
            ('467890900', '467890900')
        ]
    )
    def test_find_variation_id(
        self,
        client,
        navigation_id,
        expected_navigation_id,
        expected_parameters,
        saved_enriched_products
    ):
        response = client.get(
            '/enriched_product/{nav}'.format(
                nav=navigation_id
            )
        )
        assert response.status_code == 200

        data = response.json['data']

        assert data[0]['navigation_id'] == expected_navigation_id
        assert data[0]['sku'] == expected_parameters['sku']
        assert data[0]['metadata'] == expected_parameters['metadata']

    def test_not_find_variation_id(
        self,
        client,
        expected_parameters,
        saved_enriched_products
    ):

        response = client.get(
            '/enriched_product/{nav}'.format(
                nav='an-invalid-navigation-id'
            )
        )

        assert response.status_code == 404

    def test_find_enriched_product_with_seller_and_sku(
        self,
        client,
        expected_parameters,
        saved_enriched_products
    ):
        response = client.get(
            '/enriched_product/sku/{sku}/seller/{seller_id}'.format(
                sku=expected_parameters['sku'],
                seller_id=expected_parameters['seller_id']
            )
        )

        assert response.status_code == 200
        data = response.json['data']

        assert data[0]['navigation_id'] == expected_parameters['navigation_id']
        assert data[0]['sku'] == expected_parameters['sku']
        assert data[0]['seller_id'] == expected_parameters['seller_id']
        assert len(data) == 3

    def test_cannot_find_enriched_product_with_invalid_seller_and_sku(
        self,
        client,
        expected_parameters,
        saved_enriched_products
    ):
        response = client.get(
            '/enriched_product/sku/{sku}/seller/{seller_id}'.format(
                sku='invalid-seller',
                seller_id='invalid-sku'
            )
        )

        assert response.status_code == 404

    def test_delete_enriched_product_return_success(
        self,
        client,
        saved_enriched_products,
        mongo_database,
        patch_sqs_manager_put,
        patch_notification_put,
    ):
        criteria = {
            'sku': '2546',
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'source': SOURCE_OMNILOGIC
        }

        count_docs_before = mongo_database.enriched_products.count_documents(criteria)  # noqa

        with patch_sqs_manager_put as mock_sqs_manager_put:
            with patch_notification_put as mock_notification_put:
                response = client.delete(
                    '/enriched_product/sku/{sku}/seller/{seller_id}/source/{source}'.format(**criteria) # noqa
                )

        count_docs_after = mongo_database.enriched_products.count_documents(criteria)  # noqa

        assert not mock_notification_put.called
        assert response.status_code == 204
        assert count_docs_after == count_docs_before - 1
        assert not mock_sqs_manager_put.called

    def test_delete_source_generic_content_source_enriched_products_with_success( # noqa
        self,
        client,
        enriched_products,
        mongo_database,
        patch_pubsub_client
    ):
        generic_content = enriched_products[1]
        url = '/enriched_product/sku/{sku}/seller/{seller_id}/source/{source}'

        mongo_database.enriched_products.insert_one(generic_content)
        mongo_database.raw_products.insert_one(
            {
                'sku': generic_content['sku'],
                'seller_id': generic_content['seller_id'],
                'navigation_id': generic_content['navigation_id']
            }
        )
        assert generic_content['active']

        with patch_pubsub_client as mock_pubsub:
            response = client.delete(
                url.format(
                    sku=generic_content['sku'],
                    seller_id=generic_content['seller_id'],
                    source=generic_content['source']
                )
            )

        enriched_product = mongo_database.enriched_products.find_one(
            {
                'sku': generic_content['sku'],
                'seller_id': generic_content['seller_id']
            }
        )

        assert not enriched_product['active']
        assert response.status_code == 204

        data = json_loads(mock_pubsub.call_args_list[0][1]['data'].decode())

        assert data == {
            'action': DELETE_ACTION,
            'navigation_id': 'abcdefgh',
            'origin': 'enriched_product',
            'seller_id': generic_content['seller_id'],
            'sku': generic_content['sku'],
            'source': SOURCE_GENERIC_CONTENT,
            'task_id': ANY,
            'timestamp': ANY,
            'type': 'enriched_product'
        }

    def test_when_source_generic_content_active_is_true_when_receive_false_then_should_process_with_success( # noqa
        self,
        client,
        mongo_database,
        patch_pubsub_client
    ):
        url = '/enriched_product/sku/{sku}/seller/{seller_id}/source/{source}'

        generic_content = EnrichedProductSamples.generic_content_sku_fd3e322aab() # noqa
        mongo_database.enriched_products.insert_one(generic_content)
        mongo_database.raw_products.insert_one(
            {
                'sku': generic_content['sku'],
                'seller_id': generic_content['seller_id'],
                'navigation_id': generic_content['navigation_id']
            }
        )

        assert generic_content['active']

        with patch_pubsub_client as mock_pubsub:
            response = client.delete(
                url.format(
                    sku=generic_content['sku'],
                    seller_id=generic_content['seller_id'],
                    source=generic_content['source']
                )
            )

        generic_content_db = mongo_database.enriched_products.find_one(
            {
                'sku': generic_content['sku'],
                'seller_id': generic_content['seller_id']
            }
        )

        assert response.status_code == 204
        assert not generic_content_db['active']
        assert generic_content['md5'] != generic_content_db['md5']
        assert mock_pubsub.call_count == 1

    def test_when_source_is_generic_content_and_not_found_enriched_product_then_should_return_not_found( # noqa
        self,
        client,
        mongo_database,
        patch_pubsub_client,
        caplog
    ):
        url = '/enriched_product/sku/{sku}/seller/{seller_id}/source/{source}'

        with patch_pubsub_client as mock_pubsub:
            response = client.delete(
                url.format(
                    sku='123',
                    seller_id=MAGAZINE_LUIZA_SELLER_ID,
                    source=SOURCE_GENERIC_CONTENT
                )
            )

        assert response.status_code == 404
        assert not mock_pubsub.called
        assert (
            'enriched product with sku:123 seller_id:magazineluiza '
            f'and source:{SOURCE_GENERIC_CONTENT} not found'
        ) in caplog.text

    def test_when_delete_enriched_nonexistent_then_returns_not_found(
        self,
        client,
        saved_enriched_products,
        mongo_database,
        patch_pubsub_client,
        patch_notification_put,
    ):
        criteria = {
            'sku': '123',
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'source': SOURCE_OMNILOGIC
        }

        count_docs_before = mongo_database.enriched_products.count_documents(criteria)  # noqa
        with patch_pubsub_client as mock_pubsub:
            with patch_notification_put as mock_notification_put:
                response = client.delete(
                    '/enriched_product/sku/{sku}/seller/{seller_id}/source/{source}'.format(**criteria) # noqa
                )

        count_docs_after = mongo_database.enriched_products.count_documents(criteria)  # noqa

        assert not mock_notification_put.called
        assert not mock_pubsub.called
        assert response.status_code == 404
        assert count_docs_after == count_docs_before

    @pytest.mark.parametrize(
        'source', [
            SOURCE_DATASHEET,
            SOURCE_METABOOKS
        ]
    )
    def test_when_delete_enriched_then_rebuild_product(
        self,
        client,
        mongo_database,
        patch_publish_manager,
        source,
        patch_notification_put,
    ):
        criteria = {
            'sku': '2546',
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'source': source
        }

        mongo_database.enriched_products.insert_one(criteria)
        count_docs_before = mongo_database.enriched_products.count_documents(
            criteria
        )

        with patch_publish_manager as mock_pubsub:
            with patch_notification_put as mock_notification_put:
                response = client.delete(
                    '/enriched_product/sku/{sku}/seller/{seller_id}/source/{source}'.format(**criteria)  # noqa
                )

        count_docs_after = mongo_database.enriched_products.count_documents(
            criteria
        )

        assert not mock_notification_put.called
        assert response.status_code == 204
        assert count_docs_after == count_docs_before - 1
        assert mock_pubsub.call_args_list[0][1].get('content') == {
            'scope': 'maas_product_reprocess',
            'action': UPDATE_ACTION,
            'data': {
                'seller_id': MAGAZINE_LUIZA_SELLER_ID,
                'sku': '2546',
                'source': source
            }
        }

    def test_when_delete_enriched_to_reclassification(
        self,
        client,
        mongo_database,
        patch_notification_put,
    ):
        criteria = {
            'sku': '2546',
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'source': SOURCE_RECLASSIFICATION_PRICE_RULE,
        }

        mongo_database.enriched_products.insert_one(criteria)
        count_docs_before = mongo_database.enriched_products.count_documents(
            criteria
        )

        with patch_notification_put as mock_notification_put:
            response = client.delete(
                '/enriched_product/sku/{sku}/seller/{seller_id}/source/{source}'.format(**criteria)  # noqa
            )

        count_docs_after = mongo_database.enriched_products.count_documents(
            criteria
        )

        assert response.status_code == 204
        assert count_docs_after == count_docs_before - 1
        mock_notification_put.assert_called_once_with(
            data={
                'seller_id': criteria['seller_id'],
                'sku': criteria['sku'],
                'source': criteria['source']
            },
            scope='enriched_product',
            action=DELETE_ACTION
        )

    def test_get_enriched_product_with_source_return_success(
        self,
        client,
        mongo_database,
        enriched_products,
        save_raw_products
    ):
        mongo_database.enriched_products.insert_one(
            enriched_products[-1]
        )

        del enriched_products[-1]['_id']

        response = client.get(
            '/enriched_product/navigation_id/{navigation_id}/source/{source}'.format(  # noqa
                navigation_id=enriched_products[-1]['navigation_id'],
                source=enriched_products[-1]['source']
            )
        )

        assert response.status_code == 200
        assert response.json == enriched_products[-1]

    def test_get_enriched_product_with_source_return_product_not_found(
        self,
        client,
        enriched_products,
        caplog
    ):
        navigation_id = enriched_products[-1]['navigation_id']
        response = client.get(
            '/enriched_product/navigation_id/{navigation_id}/source/{source}'.format(  # noqa
                navigation_id=navigation_id,
                source=enriched_products[-1]['source']
            )
        )

        assert response.status_code == 404
        assert (
            f'Product with navigation_id:{navigation_id}'
            'not found in raw products' in caplog.text
        )

    def test_get_enriched_product_with_source_return_enriched_product_not_found(  # noqa
        self,
        client,
        enriched_products,
        save_raw_products,
        caplog
    ):
        sku = enriched_products[-1]['sku']
        seller_id = enriched_products[-1]['seller_id']

        response = client.get(
            '/enriched_product/navigation_id/{navigation_id}/source/{source}'.format(  # noqa
                navigation_id=enriched_products[-1]['navigation_id'],
                source=enriched_products[-1]['source']
            )
        )

        assert response.status_code == 404
        assert (
            f'Product with sku:{sku} and seller_id:{seller_id}'
            'not found in enriched products' in caplog.text
        )
