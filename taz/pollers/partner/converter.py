import logging

from taz.pollers.core.data.converter import BaseConverter

logger = logging.getLogger(__name__)


class PartnerConverter(BaseConverter):

    def _transform(self, raw):
        return {
            'id': str(raw['id']),
            'description': raw['strdescricao']
        }

    def _add_item(self, raw):
        item = self._transform(raw)

        logger.debug('Db item: {}'.format(raw))
        logger.debug('Converted item: {}'.format(item))

        self.items.setdefault(raw['batch_key'], {}).update({
            item['id']: item
        })

    def from_source(self, data):
        logger.debug('Converting data: {}'.format(data))
        [self._add_item(item) for item in data]
