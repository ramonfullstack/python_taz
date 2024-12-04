import json
import logging
from datetime import datetime

from mongoengine import DateTimeField, DynamicDocument
from pytz import timezone

from taz.api.common.pagination import Pagination

logger = logging.getLogger(__name__)


class BadgeModel(DynamicDocument):
    meta = {
        'collection': 'badges'
    }
    raw_query = {'name': {'$exists': True}}
    start_at = DateTimeField(required=True)
    end_at = DateTimeField(required=True)

    @classmethod
    def list(cls, show_all=False):
        datetime_now = datetime.now(timezone('America/Sao_Paulo'))

        if not show_all:
            payload = BadgeModel.objects(
                start_at__lte=datetime_now,
                end_at__gte=datetime_now,
                __raw__=cls.raw_query
            )

            logger.info(
                'List active badges start:{start_at} end:{end_at} '
                'query:{query}'.format(
                    start_at=datetime_now,
                    end_at=datetime_now,
                    query=payload._query
                )
            )
        else:
            payload = BadgeModel.objects(
                __raw__=cls.raw_query
            )

        logger.info('List all badges')
        return json.loads(payload.to_json())

    @classmethod
    def paginate(cls, page_number, offset):
        pagination = Pagination(BadgeModel)
        payload = pagination.paginate(
            criteria=cls.raw_query,
            page_number=page_number,
            offset=offset,
            sort_by='name',
            fields={'products': 0}
        )
        return payload

    @classmethod
    def get(cls, slug):
        payload = BadgeModel.objects(
            slug=slug,
            __raw__=cls.raw_query
        ).first()

        if not payload:
            return

        return json.loads(payload.to_json())
