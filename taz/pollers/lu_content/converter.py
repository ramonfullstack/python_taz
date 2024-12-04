import logging

from taz.pollers.core.data.converter import BaseConverter
from taz.pollers.core.exceptions import DatabaseException

logger = logging.getLogger(__name__)


class LuContentConverter(BaseConverter):

    def __init__(self, data_source):
        super().__init__()
        self.data_source = data_source

    def _add_item(self, raw):
        content = None
        try:
            cursor = self.data_source.fetch_details(raw['id'])

            content = cursor.fetchall()
            if content:
                content = content[0]['html']

            cursor.close()
        except Exception as e:
            raise DatabaseException(
                'Error fetching details from factsheet {id}: {msg}'.format(
                    id=raw['id'],
                    msg=str(e)
                )
            )

        image = (
            'https://c.mlcdn.com.br/{{w}}x{{h}}/'
            'portaldalu/fotosconteudo/{}'.format(
                raw['image']
            )
        )

        display_sessions = raw.get('display_sessions') or ''

        item = {
            'id': raw['id'],
            'image': image,
            'title': raw['title'],
            'subtitle': raw['subtitle'],
            'caption': raw['caption'],
            'content_type_id': raw['contentTypeId'],
            'classification': raw['classification'],
            'product': {
                'id': raw['productCode'],
                'category': raw['productCategory'],
                'subcategory': raw['productSubSategory'],
                'title': raw['productDescription'],
                'reference': raw['productReference'],
                'webvideo': raw['videoUrl'],
                'brand': raw['productBrand']
            },
            'category_values': self._transform_category(
                raw.get('category_values') or ''
            ),
            'display': display_sessions.split('|'),
            'content': content
        }

        self.items.setdefault(raw['batch_key'], {}).update({raw['sku']: item})

    def _transform_category(self, category):
        categories = []

        for value in category.split('|'):
            categories.extend(value.split(';'))

        return categories

    def from_source(self, data):
        logger.debug('Converting data: {}'.format(data))
        [self._add_item(item) for item in data]
