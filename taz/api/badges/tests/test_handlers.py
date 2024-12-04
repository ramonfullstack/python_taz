import json

import pytest

from taz import constants
from taz.api.badges.models import BadgeModel

DEFAULT_URL = '/badge'


class TestBadgeListHandler:

    @pytest.fixture
    def mock_url_list(self):
        return DEFAULT_URL + '/list'

    def test_list_badges(self, client, save_badges, mock_url_list):
        response = client.get(mock_url_list)

        assert len(response.json) == 4
        assert response.status_code == 200

    def test_list_badges_returns_empty_list(self, client, mock_url_list):
        response = client.get(mock_url_list)

        assert len(response.json) == 0
        assert response.status_code == 200

    def test_list_invalid_badges(
        self,
        client,
        save_invalid_badges,
        mock_url_list
    ):
        response = client.get(mock_url_list)

        assert len(response.json) == 3
        assert response.status_code == 200

    def test_list_invalid_badges_with_active_false(
        self,
        client,
        save_invalid_badges,
        mock_url_list
    ):
        response = client.get(mock_url_list, query_string='show_all=true')

        assert len(response.json) == 3
        assert response.status_code == 200


class TestBadgePaginatedListHandler:

    @pytest.fixture
    def mock_url_paginate(self):
        return '/v1/badges'

    def test_paginate_badges_with_default_offset(
        self,
        client,
        save_badges,
        mock_url_paginate
    ):
        response = client.get(path=mock_url_paginate)

        assert len(response.json['records']) == 4
        assert response.status_code == 200

    def test_paginate_badges_returns_empty_list(
        self,
        client,
        mock_url_paginate
    ):
        response = client.get(
            path=mock_url_paginate,
            query_string='offset=3&page_number=1'
        )

        assert len(response.json['records']) == 0
        assert response.status_code == 200

    def test_paginate_invalid_badges_without_name(
        self,
        client,
        save_badges_without_name,
        mock_url_paginate
    ):
        response = client.get(
            path=mock_url_paginate,
            query_string='offset=3&page_number=1'
        )

        assert len(response.json['records']) == 0
        assert response.status_code == 200

    def test_paginate_with_query_string(
        self,
        client,
        save_badges,
        mock_url_paginate
    ):
        response = client.get(
            path=mock_url_paginate,
            query_string='offset=3&page_number=1'
        )

        assert len(response.json['records']) == 3
        assert response.status_code == 200


class TestGetBadgeHandler:

    def test_get_a_badge(self, client, save_badges, badge_dict):
        response = client.get(
            '{}/{}'.format(DEFAULT_URL, badge_dict['slug'])
        )

        badge = response.json

        assert badge['text'] == badge_dict['text']
        assert badge['tooltip'] == badge_dict['tooltip']
        assert badge['image_url'] == badge_dict['image_url']
        assert badge['slug'] == badge_dict['slug']
        assert badge['priority'] == badge_dict['priority']

    def test_get_a_badge_returns_not_found(self, client):
        response = client.get('/badge/murcho')
        assert response.status_code == 404


class TestPostBadgeHandler:

    def test_create_a_badge(self, client, badge_dict):
        response = client.post(DEFAULT_URL, body=json.dumps(badge_dict))
        badge = BadgeModel.get(slug=badge_dict['slug'])

        assert badge['text'] == badge_dict['text']
        assert badge['tooltip'] == badge_dict['tooltip']
        assert badge['image_url'] == badge_dict['image_url']
        assert badge['slug'] == badge_dict['slug']

        assert response.status_code == 201

    def test_create_a_badge_returns_bad_request(self, client, badge_dict):
        del badge_dict['image_url']

        response = client.post(DEFAULT_URL, body=json.dumps(badge_dict))

        assert response.status_code == 400

    def test_should_return_400_with_existed_badge(self, client, badge_dict):
        BadgeModel(**badge_dict).save()

        response = client.post(DEFAULT_URL, body=json.dumps(badge_dict))

        assert response.status_code == 400


class TestPutBadgeHandler:

    def test_update_a_badge(self, client, badge_dict):
        BadgeModel(**badge_dict).save()

        badge_dict['name'] = 'Test'
        badge_dict['image_url'] = 'https://a-static.mlcdn.com.br/{w}x{h}/breki_fraude.jpg'  # noqa
        response = client.put(DEFAULT_URL, body=json.dumps(badge_dict))

        badge = BadgeModel.get(slug=badge_dict['slug'])

        assert badge['name'] == badge_dict['name']
        assert badge['image_url'] == badge_dict['image_url']
        assert response.status_code == 200

    def test_update_a_badge_returns_bad_request(self, client, badge_dict):
        response = client.put(DEFAULT_URL, body=json.dumps({}))
        assert response.status_code == 400

    def test_update_a_badge_returns_not_found(self, client, badge_dict):
        response = client.put(DEFAULT_URL, body=json.dumps(badge_dict))
        assert response.status_code == 404


class TestDeleteBadgeHandler:

    @pytest.fixture
    def mock_url(self, badge_dict):
        return '{base_url}/{slug}'.format(
            base_url=DEFAULT_URL,
            slug=badge_dict['slug']
        )

    def test_delete_a_badge(self, client, badge_dict, mock_url):
        BadgeModel(**badge_dict).save()

        response = client.delete(mock_url)

        badge = BadgeModel.get(slug=badge_dict['slug'])
        assert not badge

        assert response.status_code == 204

    def test_delete_a_badge_returns_not_found(
        self,
        client,
        badge_dict,
        mock_url
    ):
        response = client.delete(mock_url)
        assert response.status_code == 404


class TestProductItemBadgeHandler:

    def test_delete_a_product_in_badge(
        self,
        client,
        patch_redis,
        patch_publish_manager,
        badge_dict,
        logger_stream
    ):
        BadgeModel(**badge_dict).save()

        main_product = badge_dict['products'][0]

        with patch_redis as mock_redis, patch_publish_manager as mock_pubsub:
            response = client.delete(
                '/badge/{slug}/sku/{sku}/seller/{seller_id}'.format(
                    slug=badge_dict['slug'],
                    sku=main_product['sku'],
                    seller_id=main_product['seller_id']
                )
            )

        log = logger_stream.getvalue()

        badge = BadgeModel.get(slug=badge_dict['slug'])

        mock_pubsub_args = mock_pubsub.call_args_list[0][1]['content']
        redis_called_args = mock_redis.call_args[0][0]

        assert len(badge['products']) == 1
        assert response.status_code == 204
        assert mock_pubsub_args['sku'] == main_product['sku']
        assert mock_pubsub_args['seller_id'] == main_product['seller_id']
        assert mock_pubsub_args['origin'] == 'taz.api.badges.helpers'
        assert mock_pubsub_args['action'] == constants.UPDATE_ACTION
        assert mock_pubsub_args['force']
        assert redis_called_args == constants.BADGE_CACHE_KEY.format(
            sku=main_product['sku'],
            seller_id=main_product['seller_id']
        )
        assert (
            'Notifying the product sku:{sku} seller:{seller_id} '
            'action:{action} in the product writer queue through '
            'badge product API'.format(
                sku=main_product['sku'],
                seller_id=main_product['seller_id'],
                action=constants.UPDATE_ACTION
            )
        ) in log
        assert (
            'Removed cache from product badge '
            'sku:{sku} seller:{seller} successfully.'.format(
                sku=main_product['sku'],
                seller=main_product['seller_id'],
            )
        ) in log

    def test_delete_a_product_in_badge_returns_not_found(
        self,
        client,
        badge_dict
    ):
        main_product = badge_dict['products'][0]

        response = client.delete(
            '/badge/{slug}/sku/{sku}/seller/{seller_id}'.format(
                slug=badge_dict['slug'],
                sku=main_product['sku'],
                seller_id=main_product['seller_id']
            )
        )

        assert response.status_code == 404


class TestProductListItemHandler:

    def test_delete_a_product_in_badge(
        self,
        client,
        patch_redis,
        patch_publish_manager,
        badge_dict,
        logger_stream
    ):
        BadgeModel(**badge_dict).save()

        main_product = [badge_dict['products'][0]]

        with patch_redis as mock_redis, patch_publish_manager as mock_pubsub:
            response = client.delete(
                '/badge/{slug}/products'.format(
                    slug=badge_dict['slug']
                ), body=json.dumps(main_product)
            )

        log = logger_stream.getvalue()

        badge = BadgeModel.get(slug=badge_dict['slug'])

        redis_called_args = mock_redis.call_args[0][0]
        mock_pubsub_args = mock_pubsub.call_args_list[0][1]['content']

        assert mock_pubsub_args['sku'] == main_product[0]['sku']
        assert mock_pubsub_args['seller_id'] == main_product[0]['seller_id']
        assert mock_pubsub_args['origin'] == 'taz.api.badges.helpers'
        assert mock_pubsub_args['action'] == constants.UPDATE_ACTION
        assert mock_pubsub_args['force']
        assert redis_called_args == constants.BADGE_CACHE_KEY.format(
            sku=main_product[0]['sku'],
            seller_id=main_product[0]['seller_id']
        )
        assert len(badge['products']) == 1
        assert response.status_code == 204
        assert (
            'Notifying the product sku:{sku} seller:{seller_id} '
            'action:{action} in the product writer queue through '
            'badge product API'.format(
                sku=main_product[0]['sku'],
                seller_id=main_product[0]['seller_id'],
                action=constants.UPDATE_ACTION
            )
        ) in log
        assert (
            'Removed cache from product badge '
            'sku:{sku} seller:{seller} successfully.'.format(
                sku=main_product[0]['sku'],
                seller=main_product[0]['seller_id'],
            )
        ) in log

    def test_delete_a_product_in_badge_returns_not_found(
        self,
        client,
        badge_dict
    ):
        main_product = [badge_dict['products'][0]]

        response = client.delete(
            '/badge/{slug}/products'.format(
                slug=badge_dict['slug']
            ), body=json.dumps(main_product)
        )

        payload = response.json
        assert response.status_code == 404
        assert payload == {
            'error_message': 'Badge black-fraude not found'
        }
