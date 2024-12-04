
import json
import logging
from datetime import datetime

import falcon

from taz.api.common.exceptions import BadRequest, NotFound
from taz.api.common.handlers.base import BaseHandler
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.core.price_lock.models import PriceLockModel

logger = logging.getLogger(__name__)


class PriceLockHandler(BaseHandler, MongodbMixin):
    def on_get(self, request, response, seller_id):

        payload = PriceLockModel.objects(seller_id=seller_id).first()
        if not payload:
            raise NotFound(
                'Price lock for seller {} not found'.format(seller_id)
            )

        self.write_response(
            response,
            falcon.HTTP_200,
            {'data': json.loads(payload.to_json())}
        )

    def on_post(self, request, response):
        data = request.context

        if 'user' not in data:
            logger.error(
                'User not found on payload: {payload}'.format(
                    payload=data
                )
            )
            raise BadRequest

        if 'seller_id' not in data or 'percent' not in data:
            logger.error(
                'Missing keys seller_id or percent '
                'on payload: {payload}'.format(
                    payload=data
                )
            )
            raise BadRequest

        try:
            data['percent'] = float(data['percent'])
        except ValueError:
            logger.error(
                'Invalid percent value on request: {value}'.format(
                    value=data['percent']
                )
            )
            raise BadRequest

        criteria = {'seller_id': data['seller_id']}

        now = datetime.utcnow()
        data.update({
            'updated_at': now,
            'percent': float(data.get('percent'))
        })

        logger.info(
            'Price lock received with data:{data}'
            'from user {user}'.format(
                data=data,
                user=data['user']
            )
        )

        payload = {
            'seller_id': data['seller_id'],
            'percent': data['percent'],
            'user': data['user']
        }

        try:
            self.get_collection('price_lock').update(
                criteria, payload, upsert=True
            )

        except Exception as e:
            logger.warning(
                'Error price lock with data:{data}, '
                'error:{error}'.format(
                    data=payload,
                    error=e
                )
            )
            raise
        self.write_response(response, falcon.HTTP_200)


class PriceLockListHandler(BaseHandler):

    def on_get(self, request, response):
        price_locks = PriceLockModel.objects

        self.write_response(
            response,
            falcon.HTTP_200,
            {'data': json.loads(price_locks.to_json())}
        )
