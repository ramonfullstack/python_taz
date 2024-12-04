import logging

import falcon

from taz.api.common.handlers.base import BaseHandler
from taz.consumers.core.database.mongodb import MongodbMixin

from .models import MetabooksCategoryModel

logger = logging.getLogger(__name__)


class MetabooksCategoryHandler(BaseHandler, MongodbMixin):

    def on_post(self, request, response):

        categories = request.context

        for category in categories:
            payload = MetabooksCategoryModel.objects(
                metabook_id=category['metabook_id']
            ).first()

            if payload:
                payload.delete()

            MetabooksCategoryModel(**category).save()

        logger.info(
            'Import Metabooks categories with payload:{}'.format(categories)
        )

        self.write_response(response, falcon.HTTP_201)
