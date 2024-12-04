import logging

from taz.constants import MAGAZINE_LUIZA_SELLER_ID
from taz.pollers.core.data.converter import BaseConverter
from taz.pollers.core.exceptions import ConverterException

logger = logging.getLogger(__name__)


class PriceConverter(BaseConverter):

    def _transform(self, raw):
        if raw['stock_count'] == 0:
            delivery_availability = 'unavailable'
        elif raw['nationwide_delivery']:
            delivery_availability = 'nationwide'
        elif raw['regional_delivery']:
            delivery_availability = 'regional'
        else:
            raise ConverterException(
                'No valid behaviour was mapped for this record to determine '
                'this product stock availability. Register is: {}'.format(
                    raw
                )
            )

        return {
            'sku': raw['sku'],
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'list_price': raw['list_price'],
            'price': raw['price'],
            'delivery_availability': delivery_availability,
            'stock_count': raw['stock_count'],
            'stock_type': raw['stock_type'],
            'campaign_code': raw['campaign_code'],
            'checkout_price': raw['checkout_price']
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
