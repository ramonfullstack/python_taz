import datetime

import pytest

from taz.api.sellers.helpers import (
    create_message,
    generate_task_id_with_seller_id_and_scope,
    parse_seller
)


class TestHelpers:

    @pytest.fixture
    def seller_id(self):
        return 'foo'

    @pytest.fixture
    def data(self, seller_id):
        return {
            'seller_id': seller_id
        }

    @pytest.fixture
    def scope(self):
        return 'marvin-ipdv-seller'

    def test_should_generate_same_task_id_with_same_seller_scope(
        self,
        seller_id,
        scope
    ):
        task_id = generate_task_id_with_seller_id_and_scope(
            seller_id=seller_id, scope=scope
        )

        assert task_id == '1a22a776eb821add2844aadbddca9cfa'

        other_task_id = generate_task_id_with_seller_id_and_scope(
            seller_id=seller_id, scope=scope
        )

        assert task_id == other_task_id

    def test_should_generate_different_task_id_with_different_scope(
        self,
        seller_id,
        scope
    ):
        task_id = generate_task_id_with_seller_id_and_scope(
            seller_id=seller_id, scope=scope
        )

        assert task_id == '1a22a776eb821add2844aadbddca9cfa'

        other_task_id = generate_task_id_with_seller_id_and_scope(
            seller_id=seller_id, scope='foo-scope'
        )

        assert task_id != other_task_id

    def test_should_create_message(
        self,
        data,
        scope
    ):
        message = create_message(
            scope=scope,
            data=data,
            task_id='bar'
        )

        assert message == {
            'scope': 'marvin-ipdv-seller',
            'action': 'update',
            'data': {'seller_id': 'foo'},
            'task_id': 'bar'
        }

    def test_should_parse_seller(
        self,
        seller,
        patch_datetime
    ):
        mock_current_datetime = datetime.datetime(2022, 1, 1, 0, 0, 0)
        with patch_datetime as mock_datetime:
            mock_datetime.now.return_value = mock_current_datetime
            payload = parse_seller(seller)

        assert payload == {
            'id': seller['id'],
            'legal_name': seller['legal_name'],
            'trading_name': seller['trading_name'],
            'name': seller['name'],
            'document_number': seller['document_number'],
            'address': seller['address'],
            'updated_at': mock_current_datetime.isoformat()
        }
