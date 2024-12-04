import logging

from mongoengine import DynamicDocument

logger = logging.getLogger(__name__)


class MetabooksCategoryModel(DynamicDocument):
    meta = {
        'collection': 'metabooks_categories'
    }
