import logging
from datetime import datetime
from functools import cached_property
from typing import Dict, Optional

import falcon
from marshmallow import ValidationError

from taz.api.common.exceptions import BadRequest
from taz.api.common.handlers.base import BaseHandler
from taz.api.minimum_order_quantity.schemas import MinimumOrderQuantity
from taz.constants import CREATE_ACTION, UPDATE_ACTION
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.notification import Notification
from taz.helpers.json import json_dumps
from taz.utils import convert_id_to_nine_digits, cut_product_id

logger = logging.getLogger(__name__)


class MinimumOrderQuantityBase(BaseHandler, MongodbMixin):

    @cached_property
    def minimum_order_quantity(self):
        return self.get_collection('minimum_order_quantity')

    @cached_property
    def raw_products(self):
        return self.get_collection('raw_products')

    @cached_property
    def prices(self):
        return self.get_collection('prices')

    @cached_property
    def notification(self):
        return Notification()

    def get_minimum_order_quantity_by_navigation_id(
        self,
        navigation_id: str
    ) -> Dict:
        moq: Dict = self.minimum_order_quantity.find_one(
            {'navigation_id': navigation_id},
            {'_id': 0}
        ) or {}

        if not moq:
            logger.warning(
                'Minimum order quantity not found for '
                f'navigation_id:{navigation_id}'
            )

        return moq

    def get_minimum_order_quantity_by_sku_and_seller_id(
        self,
        sku: str,
        seller_id: str
    ) -> Dict:
        moq: Dict = self.minimum_order_quantity.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0}
        ) or {}

        if not moq:
            logger.warning(
                f'Minimum order quantity not found for sku:{sku} '
                f'and seller_id:{seller_id}'
            )

        return moq

    def get_product_by_sku_and_seller_id(
        self,
        sku: str,
        seller_id: str
    ):
        product = self.raw_products.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0, 'navigation_id': 1}
        ) or {}

        if not product:
            logger.error(
                f'Product with sku:{sku} and seller_id:{seller_id} '
                'not found raw products'
            )

        return product

    def get_product_by_navigation_id(
        self,
        navigation_id: str
    ):
        query = {
            '$or': [
                {'navigation_id': convert_id_to_nine_digits(navigation_id)},
                {'navigation_id': cut_product_id(navigation_id)}
            ],
        }

        product = self.raw_products.find_one(
            query,
            {'_id': 0, 'sku': 1, 'seller_id': 1, 'navigation_id': 1}
        ) or {}

        if not product:
            logger.error(
                f'Product with navigation_id:{navigation_id} '
                'not found raw products'
            )

        return product

    def inactive_minimum_order_quantity(
        self,
        sku: str,
        seller_id: str,
        user: str
    ):
        self.minimum_order_quantity.update_one(
            {'sku': sku, 'seller_id': seller_id},
            {
                '$set': {
                    'active': False,
                    'user': user,
                    'updated_at': datetime.utcnow().isoformat()
                }
            }
        )

        self.prices.update_one(
            {'sku': sku, 'seller_id': seller_id},
            {'$unset': {'minimum_order_quantity': ''}}
        )

    def notify(
        self,
        sku: str,
        seller_id: str,
        navigation_id: str,
        action: str
    ) -> None:
        payload = {
            'sku': sku,
            'seller_id': seller_id,
            'navigation_id': navigation_id
        }

        self.notification.put(
            data=payload,
            scope='stock',
            origin='api_minimum_order_quantity',
            action=action
        )

    def exists_price(self, sku: str, seller_id: str):
        prices = self.prices.find_one(
            {'sku': sku, 'seller_id': seller_id},
            {'_id': 0, 'sku': sku, 'seller_id': seller_id}
        ) or {}

        if not prices:
            logger.error(
                f'Price not found for sku:{sku} and '
                f'seller_id:{seller_id}'
            )

        return bool(prices)

    @staticmethod
    def format_payload(
        minimum_order_quantity: Dict,
        payload: Dict,
        sku: str,
        seller_id: str,
        navigation_id: str
    ):
        action = UPDATE_ACTION if minimum_order_quantity else CREATE_ACTION
        date = {
            'updated_at': datetime.utcnow().isoformat()
        } if minimum_order_quantity else {
            'created_at': datetime.utcnow().isoformat()
        }

        data = {
            **payload,
            **date,
            'sku': sku,
            'seller_id': seller_id,
            'navigation_id': navigation_id,
            'active': True
        }

        return data, action

    @staticmethod
    def validate_schema(
        schema,
        payload: Dict,
    ) -> Optional[Dict]:
        try:
            return schema().load(payload)
        except ValidationError as ex:
            errors: str = json_dumps(ex.messages)
            logger.error(
                f'Failed process minimum order quantity with '
                f'payload:{json_dumps(payload)} '
                f'errors:{errors}'
            )
            raise BadRequest(message=errors)


class MinimumOrderQuantityBySkuAndSellerIdHandler(MinimumOrderQuantityBase):

    def on_get(
        self,
        request: falcon.Request,
        response: falcon.Response,
        sku: str,
        seller_id: str
    ) -> falcon.Response:
        moq: Dict = self.get_minimum_order_quantity_by_sku_and_seller_id(
            sku=sku,
            seller_id=seller_id
        )

        if not moq:
            return self.write_response(
                response,
                falcon.HTTP_404
            )

        self.write_response(
            response,
            falcon.HTTP_200,
            moq
        )

    def on_put(
        self,
        request: falcon.Request,
        response: falcon.Response,
        sku: str,
        seller_id: str
    ):
        data: Dict = request.context or {}

        payload = self.validate_schema(
            schema=MinimumOrderQuantity,
            payload=data
        )

        product = self.get_product_by_sku_and_seller_id(
            sku=sku,
            seller_id=seller_id
        )

        if not product:
            return self.write_response(response, falcon.HTTP_404)

        moq = self.get_minimum_order_quantity_by_sku_and_seller_id(
            sku=sku,
            seller_id=seller_id
        )

        moq, action = self.format_payload(
            minimum_order_quantity=moq,
            payload=payload,
            sku=sku,
            seller_id=seller_id,
            navigation_id=product['navigation_id']
        )

        if action == CREATE_ACTION and not self.exists_price(
            sku=sku,
            seller_id=seller_id
        ):
            return self.write_response(response, falcon.HTTP_404)

        self.minimum_order_quantity.update_one(
            {'sku': sku, 'seller_id': seller_id},
            {'$set': moq},
            upsert=True
        )

        self.prices.update_one(
            {'sku': sku, 'seller_id': seller_id},
            {'$set': {'minimum_order_quantity': moq['value']}},
            upsert=True
        )

        self.notify(
            sku=sku,
            seller_id=seller_id,
            navigation_id=moq['navigation_id'],
            action=UPDATE_ACTION
        )

        logger.info(
            'Successfully {action} minimum order quantity:{moq} '
            'for sku:{sku} and seller_id:{seller_id}'.format(
                action=action,
                moq=moq['value'],
                sku=sku,
                seller_id=seller_id
            )
        )

        self.write_response(response, falcon.HTTP_200)

    def on_delete(
        self,
        request: falcon.Request,
        response: falcon.Response,
        sku: str,
        seller_id: str
    ):
        payload: Dict = request.context or {}

        if not payload.get('user'):
            raise BadRequest('Payload without user')

        moq: Dict = self.get_minimum_order_quantity_by_sku_and_seller_id(
            sku=sku,
            seller_id=seller_id
        )

        if not moq or not moq.get('active'):
            return self.write_response(
                response,
                falcon.HTTP_404
            )

        self.inactive_minimum_order_quantity(
            sku=sku,
            seller_id=seller_id,
            user=payload['user']
        )

        self.notify(
            sku=sku,
            seller_id=seller_id,
            navigation_id=moq['navigation_id'],
            action=UPDATE_ACTION
        )

        logger.info(
            f'Delete minimum order quantity for sku:{sku} and '
            f'seller_id:{seller_id} with success'
        )

        self.write_response(response, falcon.HTTP_204)


class MinimumOrderQuantityByNavigationIdHandler(MinimumOrderQuantityBase):

    def on_get(
        self,
        request: falcon.Request,
        response: falcon.Response,
        navigation_id: str
    ) -> falcon.Response:

        moq: Dict = self.get_minimum_order_quantity_by_navigation_id(
            navigation_id=navigation_id
        )

        if not moq:
            return self.write_response(
                response,
                falcon.HTTP_404
            )

        self.write_response(
            response,
            falcon.HTTP_200,
            moq
        )

    def on_put(
        self,
        request: falcon.Request,
        response: falcon.Response,
        navigation_id: str
    ):
        data: Dict = request.context or {}

        payload = self.validate_schema(
            schema=MinimumOrderQuantity,
            payload=data
        )

        product = self.get_product_by_navigation_id(
            navigation_id=navigation_id
        )

        if not product:
            return self.write_response(response, falcon.HTTP_404)

        moq = self.get_minimum_order_quantity_by_navigation_id(
            navigation_id=product['navigation_id']
        )

        moq, action = self.format_payload(
            minimum_order_quantity=moq,
            payload=payload,
            sku=product['sku'],
            seller_id=product['seller_id'],
            navigation_id=product['navigation_id']
        )

        if action == CREATE_ACTION and not self.exists_price(
            sku=product['sku'],
            seller_id=product['seller_id']
        ):
            return self.write_response(
                response,
                falcon.HTTP_404
            )

        self.minimum_order_quantity.update_one(
            {'navigation_id': product['navigation_id']},
            {'$set': moq},
            upsert=True
        )

        self.prices.update_one(
            {'sku': product['sku'], 'seller_id': product['seller_id']},
            {'$set': {'minimum_order_quantity': moq['value']}},
            upsert=True
        )

        self.notify(
            sku=product['sku'],
            seller_id=product['seller_id'],
            navigation_id=product['navigation_id'],
            action=UPDATE_ACTION
        )

        logger.info(
            'Successfully {action} minimum order quantity:{moq} '
            'for navigation_id:{navigation_id}'.format(
                action=action,
                moq=moq['value'],
                navigation_id=product['navigation_id']
            )
        )

        self.write_response(response, falcon.HTTP_200)

    def on_delete(
        self,
        request: falcon.Request,
        response: falcon.Response,
        navigation_id: str
    ):
        payload: Dict = request.context or {}

        if not payload.get('user'):
            raise BadRequest('Payload without user')

        moq: Dict = self.get_minimum_order_quantity_by_navigation_id(
            navigation_id=navigation_id
        )

        if not moq or not moq.get('active'):
            return self.write_response(
                response,
                falcon.HTTP_404
            )

        self.inactive_minimum_order_quantity(
            sku=moq['sku'],
            seller_id=moq['seller_id'],
            user=payload['user']
        )

        self.notify(
            sku=moq['sku'],
            seller_id=moq['seller_id'],
            navigation_id=navigation_id,
            action=UPDATE_ACTION
        )

        logger.info(
            'Delete minimum order quantity for '
            f'navigation_id:{navigation_id} with success'
        )

        self.write_response(response, falcon.HTTP_204)
