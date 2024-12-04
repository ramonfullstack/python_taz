import logging

from taz.constants import MAGAZINE_LUIZA_SELLER_ID
from taz.pollers.core.data.converter import BaseConverter

logger = logging.getLogger(__name__)


class BasePriceConverter(BaseConverter):

    def _transform(self, raw):
        return {
            'sku': raw['sku'],
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'list_price': '{0:.2f}'.format(raw['list_price']),
            'gemco_id': raw['gemco_id'],
            'bundles': raw['bundles']
        }

    def _add_item(self, raw):
        item = self._transform(raw)

        logger.debug('Db item: {}'.format(raw))
        logger.debug('Converted item: {}'.format(item))

        self.items.setdefault(raw['batch_key'], {}).update({
            item['sku']: item
        })

    def from_source(self, data):
        logger.debug('Converting data: {}'.format(data))
        [self._add_item(item) for item in data]
