import logging

from slugify import slugify

from taz import constants
from taz.pollers.core.data.converter import BaseConverter

logger = logging.getLogger(__name__)


class CategoryConverter(BaseConverter):

    def _transform_category(self, raw):
        return {
            'id': raw['category_id'],
            'description': raw['category_description'],
            'slug': slugify(raw['category_description']),
            'parent_id': constants.MAGAZINE_LUIZA_DEFAULT_CATEGORY,
            'active': True
        }

    def _transform_subcategory(self, raw):
        return {
            'id': raw['subcategory_id'],
            'description': raw['subcategory_description'],
            'slug': slugify(raw['subcategory_description']),
            'parent_id': raw['category_id'],
            'active': raw.get('subcategory_active', -1) == 1
        }

    def _add_item(self, raw):
        if raw['subcategory_id']:
            item = self._transform_subcategory(raw)
        else:
            item = self._transform_category(raw)

        self.items.setdefault(raw['batch_key'], {}).update({item['id']: item})

    def from_source(self, data):
        logger.debug('Converting data: {}'.format(data))
        [self._add_item(item) for item in data]
