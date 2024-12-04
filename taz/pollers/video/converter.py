import logging

from taz.constants import MAGAZINE_LUIZA_SELLER_ID
from taz.pollers.core.data.converter import BaseConverter

logger = logging.getLogger(__name__)


class VideoConverter(BaseConverter):
    def _add_item(self, db_row):
        if db_row is None:
            return

        sku = db_row['batch_key']
        video = db_row['video']
        item = {
            'seller_id': MAGAZINE_LUIZA_SELLER_ID,
            'sku': sku,
            'videos': [video],
        }
        self.items.setdefault(sku, {}).update({sku: item})

    def from_source(self, data):
        logger.debug('Converting data: {}'.format(data))
        [self._add_item(item) for item in data]
