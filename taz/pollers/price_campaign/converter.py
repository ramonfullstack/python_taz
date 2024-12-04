import logging

from taz.constants import MAGAZINE_LUIZA_SELLER_ID
from taz.pollers.core.data.converter import BaseConverter

logger = logging.getLogger(__name__)


class PriceConverter(BaseConverter):

    def _transform(self, raw):
        return {
            'sku': raw['sku'],
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'prices': raw['prices']
        }

    def _add_item(self, raw):
        item = self._transform(raw)

        logger.debug('Db item: {}'.format(raw))
        logger.debug('Converted item: {}'.format(item))

        self.items.setdefault(raw['batch_key'], {}).update({
            item['sku']: item
        })

        logger.debug(
            'Convert price_campaign poller with sku:{sku} '
            'and payload:{payload}'.format(
                sku=item['sku'],
                payload=item
            )
        )

    def from_source(self, data):
        logger.debug('Converting data: {}'.format(data))
        [self._add_item(item) for item in data]
