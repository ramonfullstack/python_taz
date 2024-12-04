import logging
import time

from taz import constants
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.core.score.criteria import ScoreCriteria
from taz.helpers.html import remove_html_tags

logger = logging.getLogger(__name__)


class BaseVersion(MongodbMixin):

    FIELDS = [
        {
            'field': 'full_title',
            'criteria': constants.SCORE_TITLE_CRITERIA
        },
        {
            'field': 'description',
            'criteria': constants.SCORE_DESCRIPTION_CRITERIA
        },
        {
            'field': 'images_count',
            'criteria': constants.SCORE_IMAGES_CRITERIA
        },
        {
            'field': 'reviews_count',
            'criteria': constants.SCORE_REVIEW_COUNT_CRITERIA
        },
        {
            'field': 'review_rating',
            'criteria': constants.SCORE_REVIEW_RATING_CRITERIA
        },
        {
            'field': 'offer_title',
            'criteria': constants.SCORE_OFFER_TITLE_CRITERIA
        },
        {
            'field': 'factsheet_attributes_count',
            'criteria': constants.SCORE_FACTSHEET_CRITERIA
        }
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.score_criteria = ScoreCriteria()

    def calculate(self, product):
        entity = product.get('entity')
        sku = product['sku']
        seller_id = product['seller_id']

        if not entity:
            logger.warning(
                'Entity not found for sku:{sku} seller_id:{seller_id}'.format(
                    sku=sku,
                    seller_id=seller_id
                )
            )

            return False

        sources = []
        for f in self.FIELDS:
            field = f['field']
            criteria = f['criteria']

            if not product.get(field):
                continue

            points, name = self.score_criteria.get(
                entity,
                criteria,
                product[field]
            )

            if field in ['full_title', 'description', 'offer_title']:
                product[field] = remove_html_tags(product[field])

            sources.append({
                'value': product[field],
                'points': points,
                'criteria': name
            })

        payload = {
            'sku': sku,
            'seller_id': seller_id,
            'timestamp': time.time(),
            'version': self.VERSION,
            'sources': sources,
            'entity_name': product['entity'],
            'category_id': product['category_id']
        }

        return payload
