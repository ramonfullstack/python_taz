from typing import Dict
from unittest.mock import ANY, patch

import pytest
from falcon.testing import Result
from pymongo import MongoClient

from taz.api.conftest import Client
from taz.constants import (
    CREATE_ACTION,
    MAGAZINE_LUIZA_SELLER_ID,
    UPDATE_ACTION
)
from taz.helpers.json import json_dumps
from taz.utils import convert_id_to_nine_digits


class TestMinimumOrderQuantityBySkuAndSellerIdHandler:

    @pytest.fixture
    def url(self) -> str:
        return '/moq/seller_id/{seller_id}/sku/{sku}'

    def test_get_minimum_order_quantity_by_sku_and_seller_id_with_success(
        self,
        url: str,
        client: Client,
        sku: str,
        seller_id: str,
        save_minimum_order_quantity,
        mock_minimum_order_quantity: Dict
    ):
        response: Result = client.get(
            url.format(
                seller_id=seller_id,
                sku=sku
            )
        )

        mock_minimum_order_quantity.pop('_id')

        assert response.status_code == 200
        assert response.json == mock_minimum_order_quantity

    def test_get_minimum_order_quantity_by_sku_and_seller_id_not_found(
        self,
        url: str,
        client: Client,
        sku: str,
        seller_id: str,
        mock_minimum_order_quantity: Dict,
        caplog
    ):
        response: Result = client.get(
            url.format(seller_id=seller_id, sku=sku)
        )

        assert response.status_code == 404
        assert (
            f'Minimum order quantity not found for sku:{sku} '
            f'and seller_id:{seller_id}'
        ) in caplog.text

    def test_put_minimum_order_quantity_by_sku_and_seller_id_should_create_with_success( # noqa
        self,
        url: str,
        client: Client,
        sku: str,
        seller_id: str,
        mongo_database: MongoClient,
        mock_minimum_order_quantity: Dict,
        mock_prices: Dict,
        save_prices,
        save_products,
        patch_publish_manager: patch,
        pubsub_payload_expected: Dict,
        caplog
    ):
        prices = mongo_database.prices.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0}
        )

        assert not prices.get('minimum_order_quantity')

        with patch_publish_manager as mock_pubsub:
            response: Result = client.put(
                url.format(sku=sku, seller_id=seller_id),
                body=json_dumps(mock_minimum_order_quantity)
            )

        assert response.status_code == 200

        moq = mongo_database.minimum_order_quantity.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0}
        )

        mock_minimum_order_quantity.pop('updated_at', None)

        assert moq == {
            **mock_minimum_order_quantity,
            'created_at': ANY
        }

        prices = mongo_database.prices.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0}
        )

        mock_prices.pop('_id', None)
        mock_prices.update({'minimum_order_quantity': mock_minimum_order_quantity['value']}) # noqa

        assert prices == mock_prices

        assert (
            'Successfully {action} minimum order quantity:{moq} '
            'for sku:{sku} and seller_id:{seller_id}'.format(
                action=CREATE_ACTION,
                moq=mock_minimum_order_quantity['value'],
                sku=sku,
                seller_id=seller_id
            )
        ) in caplog.text

        mock_pubsub.assert_called_once_with(**pubsub_payload_expected)

    def test_put_minimum_order_quantity_by_sku_and_seller_id_should_update_with_success( # noqa
        self,
        url: str,
        client: Client,
        mongo_database: MongoClient,
        sku: str,
        seller_id: str,
        mock_minimum_order_quantity: Dict,
        mock_prices: Dict,
        pubsub_payload_expected: Dict,
        save_prices_with_minimum_order_quantity,
        save_products,
        save_minimum_order_quantity,
        patch_publish_manager: patch,
        caplog
    ):
        mock_minimum_order_quantity.pop('_id', None)
        mock_minimum_order_quantity['value'] = 20

        with patch_publish_manager as mock_pubsub:
            response: Result = client.put(
                url.format(sku=sku, seller_id=seller_id),
                body=json_dumps(mock_minimum_order_quantity)
            )

        assert response.status_code == 200

        moq = mongo_database.minimum_order_quantity.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0}
        )

        assert moq == {
            **mock_minimum_order_quantity,
            'created_at': ANY,
            'updated_at': ANY
        }

        prices = mongo_database.prices.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0}
        )

        mock_prices.update({'minimum_order_quantity': mock_minimum_order_quantity['value']}) # noqa
        assert prices == mock_prices

        assert (
            'Successfully {action} minimum order quantity:{moq} '
            'for sku:{sku} and seller_id:{seller_id}'.format(
                action=UPDATE_ACTION,
                moq=mock_minimum_order_quantity['value'],
                sku=sku,
                seller_id=seller_id
            )
        ) in caplog.text

        mock_pubsub.assert_called_once_with(**pubsub_payload_expected)

    def test_put_minimum_order_quantity_by_sku_and_seller_id_should_active_moq_inactive( # noqa
        self,
        url: str,
        client: Client,
        mongo_database: MongoClient,
        sku: str,
        seller_id: str,
        mock_minimum_order_quantity: Dict,
        mock_prices: Dict,
        pubsub_payload_expected: Dict,
        patch_publish_manager: patch,
        caplog,
        save_products
    ):
        mock_minimum_order_quantity['active'] = False
        mongo_database.minimum_order_quantity.insert_one(
            mock_minimum_order_quantity
        )

        mock_minimum_order_quantity.pop('_id', None)
        mock_minimum_order_quantity['value'] = 10

        with patch_publish_manager as mock_pubsub:
            response: Result = client.put(
                url.format(sku=sku, seller_id=seller_id),
                body=json_dumps(mock_minimum_order_quantity)
            )

        assert response.status_code == 200

        moq = mongo_database.minimum_order_quantity.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0, 'active': 1, 'value': 1}
        )

        assert moq['active']
        assert moq['value'] == mock_minimum_order_quantity['value']

        prices = mongo_database.prices.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0, 'minimum_order_quantity': 1}
        )

        assert prices['minimum_order_quantity'] == mock_minimum_order_quantity['value'] # noqa

        assert (
            'Successfully {action} minimum order quantity:{moq} '
            'for sku:{sku} and seller_id:{seller_id}'.format(
                action=UPDATE_ACTION,
                moq=mock_minimum_order_quantity['value'],
                sku=sku,
                seller_id=seller_id
            )
        ) in caplog.text

        mock_pubsub.assert_called_once_with(**pubsub_payload_expected)

    def test_put_minimum_order_quantity_by_sku_and_seller_id_with_create_product_should_return_not_found(  # noqa
        self,
        url: str,
        client: Client,
        sku: str,
        seller_id: str,
        navigation_id: str,
        mock_minimum_order_quantity: Dict,
        pubsub_payload_expected: Dict,
        caplog
    ):
        response: Result = client.put(
            url.format(sku=sku, seller_id=seller_id),
            body=json_dumps(mock_minimum_order_quantity)
        )

        assert response.status_code == 404
        assert (
            f'Product with sku:{sku} and seller_id:{seller_id} '
            'not found raw products'
        ) in caplog.text

    def test_put_minimum_order_quantity_by_sku_and_seller_id_with_create_when_price_not_exists_should_return_not_found(  # noqa
        self,
        url: str,
        client: Client,
        sku: str,
        seller_id: str,
        save_products,
        mock_minimum_order_quantity: Dict,
        pubsub_payload_expected: Dict,
        caplog
    ):
        response: Result = client.put(
            url.format(sku=sku, seller_id=seller_id),
            body=json_dumps(mock_minimum_order_quantity)
        )

        assert response.status_code == 404
        assert (
            f'Price not found for sku:{sku} and seller_id:{seller_id}'
        ) in caplog.text

    @pytest.mark.parametrize('remove_field', [
        'value',
        'user'
    ])
    def test_put_minimum_order_quantity_by_sku_and_seller_id_should_raise_bad_request( # noqa
        self,
        url: str,
        client: Client,
        mock_minimum_order_quantity: Dict,
        remove_field: str
    ):
        mock_minimum_order_quantity.pop(remove_field, None)

        response: Result = client.put(
            url.format(
                sku='sku',
                seller_id=MAGAZINE_LUIZA_SELLER_ID
            ),
            body=json_dumps(mock_minimum_order_quantity)
        )

        assert response.status_code == 400

    @pytest.mark.parametrize('value', [
        -1,
        0,
        1
    ])
    def test_put_minimum_order_quantity_by_sku_and_seller_id_with_invalid_value_should_raise_bad_request(  # noqa
        self,
        url: str,
        client: Client,
        mock_minimum_order_quantity: Dict,
        value: int,
        caplog
    ):
        mock_minimum_order_quantity['value'] = value

        response: Result = client.put(
            url.format(sku='sku', seller_id='seller_id'),
            body=json_dumps(mock_minimum_order_quantity)
        )

        assert response.status_code == 400
        assert 'O campo value precisa ser maior que 1' in caplog.text

    def test_delete_minimum_order_quantity_by_sku_and_seller_id_with_success(
        self,
        url: str,
        client: Client,
        mongo_database: MongoClient,
        sku: str,
        seller_id: str,
        patch_publish_manager: patch,
        save_minimum_order_quantity,
        save_prices_with_minimum_order_quantity,
        mock_minimum_order_quantity: Dict,
        pubsub_payload_expected: Dict,
        caplog
    ):
        with patch_publish_manager as mock_pubsub:
            response: Result = client.delete(
                url.format(sku=sku, seller_id=seller_id),
                body=json_dumps({'user': 'unit_test'})
            )

        mock_minimum_order_quantity.pop('_id')

        assert response.status_code == 204

        moq = mongo_database.minimum_order_quantity.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0, 'active': 1, 'user': 1}
        )
        assert moq['active'] is False
        assert moq['user'] == 'unit_test'

        prices = mongo_database.minimum_order_quantity.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0, 'minimum_order_quantity': 1}
        )

        assert not prices.get('minimum_order_quantity')
        assert (
            f'Delete minimum order quantity for sku:{sku} and '
            f'seller_id:{seller_id} with success'
        ) in caplog.text

        mock_pubsub.assert_called_once_with(**pubsub_payload_expected)

    def test_delete_minimum_order_quantity_by_sku_and_seller_id_product_not_found( # noqa
        self,
        url: str,
        client: Client,
        sku: str,
        seller_id: str,
        mock_minimum_order_quantity: Dict,
        caplog
    ):
        response: Result = client.delete(
            url.format(sku=sku, seller_id=seller_id),
            body=json_dumps({'user': mock_minimum_order_quantity['user']})
        )

        assert response.status_code == 404
        assert (
            f'Minimum order quantity not found for sku:{sku} '
            f'and seller_id:{seller_id}'
        ) in caplog.text

    def test_delete_minimum_order_quantity_by_sku_and_seller_id_when_product_already_inactive_then_return_not_found( # noqa
        self,
        url: str,
        client: Client,
        mongo_database: MongoClient,
        sku: str,
        seller_id: str,
        mock_minimum_order_quantity: Dict,
        caplog
    ):
        mock_minimum_order_quantity['active'] = False
        mongo_database.minimum_order_quantity.insert_one(
            mock_minimum_order_quantity
        )

        response: Result = client.delete(
            url.format(sku=sku, seller_id=seller_id),
            body=json_dumps({'user': mock_minimum_order_quantity['user']})
        )

        assert response.status_code == 404

    @pytest.mark.parametrize('user_payload', [
        {},
        {'user': ''}
    ])
    def test_delete_minimum_order_quantity_by_sku_and_seller_id_when_payload_without_user_then_raise_bad_request( # noqa
        self,
        url: str,
        client: Client,
        mongo_database: MongoClient,
        sku: str,
        seller_id: str,
        mock_minimum_order_quantity: Dict,
        user_payload: Dict
    ):
        response: Result = client.delete(
            url.format(sku=sku, seller_id=seller_id),
            body=json_dumps(user_payload)
        )

        assert response.status_code == 400


class TestMinimumOrderQuantityByNavigationIdHandler:

    @pytest.fixture
    def url(self) -> str:
        return '/moq/navigation_id/{navigation_id}'

    def test_get_minimum_order_quantity_by_navigation_id_with_success(
        self,
        url: str,
        client: Client,
        navigation_id: str,
        save_minimum_order_quantity,
        mock_minimum_order_quantity: Dict
    ):
        response: Result = client.get(
            url.format(navigation_id=navigation_id)
        )

        mock_minimum_order_quantity.pop('_id')

        assert response.status_code == 200
        assert response.json == mock_minimum_order_quantity

    def test_get_minimum_order_quantity_by_navigation_id_not_found(
        self,
        url: str,
        client: Client,
        navigation_id: str,
        mock_minimum_order_quantity: Dict,
        caplog
    ):
        response: Result = client.get(
            url.format(navigation_id=navigation_id)
        )

        assert response.status_code == 404
        assert (
            'Minimum order quantity not found for '
            f'navigation_id:{navigation_id}'
        ) in caplog.text

    @pytest.mark.parametrize('navigation_id', ['237216200', '2372162'])
    def test_put_minimum_order_quantity_by_navigation_id_should_create_with_success( # noqa
        self,
        url: str,
        client: Client,
        mongo_database: MongoClient,
        sku: str,
        seller_id: str,
        mock_minimum_order_quantity: Dict,
        mock_prices: Dict,
        save_prices,
        save_products,
        patch_publish_manager: patch,
        pubsub_payload_expected: Dict,
        caplog,
        navigation_id
    ):
        prices = mongo_database.prices.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0}
        )

        assert not prices.get('minimum_order_quantity')

        with patch_publish_manager as mock_pubsub:
            response: Result = client.put(
                url.format(navigation_id=navigation_id),
                body=json_dumps(mock_minimum_order_quantity)
            )

        navigation_id = convert_id_to_nine_digits(navigation_id)

        assert response.status_code == 200

        moq = mongo_database.minimum_order_quantity.find_one(
            {'navigation_id': navigation_id},
            {'_id': 0}
        )

        mock_minimum_order_quantity.pop('updated_at', None)

        assert moq == {
            **mock_minimum_order_quantity,
            'created_at': ANY
        }

        prices = mongo_database.prices.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0}
        )

        mock_prices.pop('_id', None)
        mock_prices.update({'minimum_order_quantity': mock_minimum_order_quantity['value']}) # noqa

        assert prices == mock_prices

        assert (
            'Successfully {action} minimum order quantity:{moq} '
            'for navigation_id:{navigation_id}'.format(
                action=CREATE_ACTION,
                moq=mock_minimum_order_quantity['value'],
                navigation_id=navigation_id
            )
        ) in caplog.text

        mock_pubsub.assert_called_once_with(**pubsub_payload_expected)

    @pytest.mark.parametrize('navigation_id', ['237216200', '2372162'])
    def test_put_minimum_order_quantity_by_navigation_id_should_update_with_success( # noqa
        self,
        url: str,
        client: Client,
        mongo_database: MongoClient,
        sku: str,
        seller_id: str,
        mock_minimum_order_quantity: Dict,
        mock_prices: Dict,
        pubsub_payload_expected: Dict,
        save_prices_with_minimum_order_quantity,
        save_products,
        save_minimum_order_quantity,
        patch_publish_manager: patch,
        caplog,
        navigation_id: str
    ):
        mock_minimum_order_quantity.pop('_id', None)
        mock_minimum_order_quantity['value'] = 20

        with patch_publish_manager as mock_pubsub:
            response: Result = client.put(
                url.format(navigation_id=navigation_id),
                body=json_dumps(mock_minimum_order_quantity)
            )

        navigation_id = convert_id_to_nine_digits(navigation_id)

        assert response.status_code == 200

        moq = mongo_database.minimum_order_quantity.find_one(
            {'navigation_id': navigation_id},
            {'_id': 0}
        )

        assert moq == {
            **mock_minimum_order_quantity,
            'created_at': ANY,
            'updated_at': ANY
        }

        prices = mongo_database.prices.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0}
        )

        mock_prices.update({'minimum_order_quantity': mock_minimum_order_quantity['value']}) # noqa
        assert prices == mock_prices

        assert (
            'Successfully {action} minimum order quantity:{moq} '
            'for navigation_id:{navigation_id}'.format(
                action=UPDATE_ACTION,
                moq=mock_minimum_order_quantity['value'],
                navigation_id=navigation_id
            )
        ) in caplog.text

        mock_pubsub.assert_called_once_with(**pubsub_payload_expected)

    @pytest.mark.parametrize('navigation_id', ['237216200', '2372162'])
    def test_put_minimum_order_quantity_by_navigation_id_should_active_moq_inactive( # noqa
        self,
        url: str,
        client: Client,
        mongo_database: MongoClient,
        sku: str,
        seller_id: str,
        mock_minimum_order_quantity: Dict,
        mock_prices: Dict,
        save_products,
        pubsub_payload_expected: Dict,
        patch_publish_manager: patch,
        caplog,
        navigation_id: str
    ):
        mock_minimum_order_quantity['active'] = False
        mongo_database.minimum_order_quantity.insert_one(
            mock_minimum_order_quantity
        )

        mock_minimum_order_quantity.pop('_id', None)
        mock_minimum_order_quantity['value'] = 10

        with patch_publish_manager as mock_pubsub:
            response: Result = client.put(
                url.format(navigation_id=navigation_id),
                body=json_dumps(mock_minimum_order_quantity)
            )

        navigation_id = convert_id_to_nine_digits(navigation_id)

        assert response.status_code == 200

        moq = mongo_database.minimum_order_quantity.find_one(
            {'navigation_id': navigation_id},
            {'_id': 0, 'active': 1, 'value': 1}
        )

        assert moq['active']
        assert moq['value'] == mock_minimum_order_quantity['value']

        prices = mongo_database.prices.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0, 'minimum_order_quantity': 1}
        )

        assert prices['minimum_order_quantity'] == mock_minimum_order_quantity['value'] # noqa

        assert (
            'Successfully {action} minimum order quantity:{moq} '
            'for navigation_id:{navigation_id}'.format(
                action=UPDATE_ACTION,
                moq=mock_minimum_order_quantity['value'],
                navigation_id=navigation_id
            )
        ) in caplog.text

        mock_pubsub.assert_called_once_with(**pubsub_payload_expected)

    def test_put_minimum_order_quantity_by_navigation_id_with_create_product_should_return_not_found(  # noqa
        self,
        url: str,
        client: Client,
        sku: str,
        seller_id: str,
        navigation_id: str,
        mock_minimum_order_quantity: Dict,
        pubsub_payload_expected: Dict,
        caplog
    ):
        response: Result = client.put(
            url.format(navigation_id=navigation_id),
            body=json_dumps(mock_minimum_order_quantity)
        )

        assert response.status_code == 404
        assert (
            f'Product with navigation_id:{navigation_id} '
            'not found raw products'
        )

    def test_put_minimum_order_quantity_by_navigation_id_with_create_when_price_not_exists_should_return_not_found(  # noqa
        self,
        url: str,
        client: Client,
        sku: str,
        seller_id: str,
        navigation_id: str,
        save_products,
        mock_minimum_order_quantity: Dict,
        pubsub_payload_expected: Dict,
        caplog
    ):
        response: Result = client.put(
            url.format(navigation_id=navigation_id),
            body=json_dumps(mock_minimum_order_quantity)
        )

        assert response.status_code == 404
        assert (
            f'Price not found for sku:{sku} and seller_id:{seller_id}'
        ) in caplog.text

    @pytest.mark.parametrize('remove_field', [
        'value',
        'user'
    ])
    def test_put_minimum_order_quantity_by_navigation_id_should_raise_bad_request( # noqa
        self,
        url: str,
        client: Client,
        mock_minimum_order_quantity: Dict,
        remove_field: str
    ):
        mock_minimum_order_quantity.pop(remove_field, None)

        response: Result = client.put(
            url.format(
                navigation_id='navigation_id'
            ),
            body=json_dumps(mock_minimum_order_quantity)
        )

        assert response.status_code == 400

    @pytest.mark.parametrize('value', [
        -1,
        0,
        1
    ])
    def test_put_minimum_order_quantity_by_navigation_id_with_invalid_value_should_raise_bad_request(  # noqa
        self,
        url: str,
        client: Client,
        mock_minimum_order_quantity: Dict,
        value: int,
        caplog
    ):
        mock_minimum_order_quantity['value'] = value

        response: Result = client.put(
            url.format(
                navigation_id='navigation_id'
            ),
            body=json_dumps(mock_minimum_order_quantity)
        )

        assert response.status_code == 400
        assert 'O campo value precisa ser maior que 1' in caplog.text

    def test_delete_minimum_order_quantity_by_navigation_id_with_success(
        self,
        url: str,
        client: Client,
        mongo_database: MongoClient,
        sku: str,
        seller_id: str,
        navigation_id: str,
        patch_publish_manager: patch,
        save_minimum_order_quantity,
        save_prices_with_minimum_order_quantity,
        mock_minimum_order_quantity: Dict,
        pubsub_payload_expected: Dict,
        caplog
    ):
        with patch_publish_manager as mock_pubsub:
            response: Result = client.delete(
                url.format(navigation_id=navigation_id),
                body=json_dumps({'user': 'unit_test'})
            )

        mock_minimum_order_quantity.pop('_id')

        assert response.status_code == 204

        moq = mongo_database.minimum_order_quantity.find_one(
            {'navigation_id': navigation_id},
            {'_id': 0, 'active': 1, 'user': 1}
        )
        assert moq['active'] is False
        assert moq['user'] == 'unit_test'

        prices = mongo_database.minimum_order_quantity.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0, 'minimum_order_quantity': 1}
        )

        assert not prices.get('minimum_order_quantity')
        assert (
            'Delete minimum order quantity for '
            f'navigation_id:{navigation_id} with success'
        ) in caplog.text

        mock_pubsub.assert_called_once_with(**pubsub_payload_expected)

    def test_delete_minimum_order_quantity_by_navigation_id_when_product_not_found( # noqa
        self,
        url: str,
        client: Client,
        navigation_id: str,
        mock_minimum_order_quantity: Dict,
        caplog
    ):
        response: Result = client.delete(
            url.format(navigation_id=navigation_id),
            body=json_dumps({'user': mock_minimum_order_quantity['user']})
        )

        assert response.status_code == 404
        assert (
            'Minimum order quantity not found for '
            f'navigation_id:{navigation_id}'
        ) in caplog.text

    def test_delete_minimum_order_quantity_by_navigation_id_when_product_already_inactive_then_return_not_found( # noqa
        self,
        url: str,
        client: Client,
        mongo_database: MongoClient,
        navigation_id: str,
        mock_minimum_order_quantity: Dict,
        caplog
    ):
        mock_minimum_order_quantity['active'] = False
        mongo_database.minimum_order_quantity.insert_one(
            mock_minimum_order_quantity
        )

        response: Result = client.delete(
            url.format(navigation_id=navigation_id),
            body=json_dumps({'user': mock_minimum_order_quantity['user']})
        )

        assert response.status_code == 404

    @pytest.mark.parametrize('user_payload', [
        {},
        {'user': ''}
    ])
    def test_delete_minimum_order_quantity_by_navigation_id_when_payload_without_user_then_raise_bad_request( # noqa
        self,
        url: str,
        client: Client,
        mongo_database: MongoClient,
        navigation_id: str,
        mock_minimum_order_quantity: Dict,
        user_payload: Dict
    ):
        response: Result = client.delete(
            url.format(navigation_id=navigation_id),
            body=json_dumps(user_payload)
        )
        assert response.status_code == 400
