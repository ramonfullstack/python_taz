import logging

from mongoengine import DynamicDocument

logger = logging.getLogger(__name__)


class BlacklistModel(DynamicDocument):
    meta = {
        'collection': 'blacklist'
    }
