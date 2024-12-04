from unittest.mock import patch

import pytest

from taz.constants import UPDATE_ACTION
from taz.consumers.matching_product.consumer import MatchingProductProcessor


class TestMatchingProductConsumer:

    @pytest.fixture
    def patch_raw_products(self):
        return patch.object(MatchingProductProcessor, 'raw_products')

    @pytest.fixture
    def payload_matching_uuid(self):
        return {
            'navigation_id': '023384700',
            'matching_uuid': '5a0ef10f915a426084d112c379d6775a',
            'matching_type': 'UNITARY',
            'sku': '023384700',
            'seller_id': 'magazineluiza'
        }

    @pytest.fixture
    def payload_parent_matching(self):
        return {
            'navigation_id': '023384700',
            'sku': '023384700',
            'seller_id': 'magazineluiza',
            'parent_matching_uuid': '27006db39089436fb52c5c00c8464034'
        }

    @pytest.mark.parametrize('input_payload', [
        'payload_matching_uuid',
        'payload_parent_matching'
    ])
    def test_when_product_not_exists_then_save_log_and_ack_message(
        self,
        input_payload,
        request,
        patch_raw_products,
        patch_publish_manager,
        caplog
    ):
        payload = request.getfixturevalue(input_payload)

        with patch_raw_products as mock_raw_products:
            with patch_publish_manager as mock_pubsub:
                mock_raw_products.update_one.return_value = MockResult(0)

                consumer = MatchingProductProcessor('matching_product')
                consumer.process_message(payload)

        sku = payload['sku']
        seller_id = payload['seller_id']
        navigation_id = payload['navigation_id']
        matching_uuid = payload.get('matching_uuid')
        matching_type = payload.get('matching_type')
        parent_matching_uuid = payload.get('parent_matching_uuid')

        message = (
            f'sku:{sku} seller_id:{seller_id} navigation_id:{navigation_id} '
            f'matching_uuid:{matching_uuid} matching_type:{matching_type} '
            f'parent_matching_uuid:{parent_matching_uuid} cannot update '
            'the product'
        )

        assert not mock_pubsub.called
        assert message in caplog.text

    @pytest.mark.parametrize('input_payload', [
        'payload_matching_uuid',
        'payload_parent_matching'
    ])
    def test_when_product_exists_then_should_update_data(
        self,
        input_payload,
        request,
        patch_raw_products,
        patch_publish_manager,
        caplog
    ):
        payload = request.getfixturevalue(input_payload)

        with patch_raw_products as mock_raw_products:
            with patch_publish_manager as mock_pubsub:
                mock_raw_products.update_one.return_value = MockResult(1)
                consumer = MatchingProductProcessor('matching_product')
                consumer.process_message(payload)

        sku = payload['sku']
        seller_id = payload['seller_id']
        navigation_id = payload['navigation_id']
        matching_uuid = payload.get('matching_uuid')
        matching_type = payload.get('matching_type')
        parent_matching_uuid = payload.get('parent_matching_uuid')

        message = (
            f'sku:{sku} seller_id:{seller_id} navigation_id:{navigation_id} '
            f'matching_uuid:{matching_uuid} matching_type:{matching_type} '
            f'parent_matching_uuid:{parent_matching_uuid} was updated '
            'and pubsub stream successfully'
        )

        assert message in caplog.text
        mock_pubsub.assert_called_once_with(
            content={
                'sku': '023384700',
                'seller_id': 'magazineluiza',
                'navigation_id': '023384700',
                'tracking_id': None,
                'scope': 'matching_product',
                'action': UPDATE_ACTION
            },
            attributes={
                'scope': 'matching_product',
                'action': UPDATE_ACTION
            },
            topic_name='taz-match-products',
            project_id='maga-homolog'
        )
        mock_raw_products.update_one.assert_called_once_with(
            {'sku': sku, 'seller_id': seller_id},
            {
                '$set': {
                    'matching_uuid': matching_uuid,
                    'matching_type': matching_type
                } if matching_uuid else {
                    'parent_matching_uuid': parent_matching_uuid
                }
            }
        )


class MockResult:

    def __init__(self, modified_count):
        self.modified_count = modified_count
