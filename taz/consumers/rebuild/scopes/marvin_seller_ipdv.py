import logging

from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.marvin import MarvinRequest
from taz.consumers.rebuild.scopes.base import BaseRebuild

logger = logging.getLogger(__name__)


class RebuildMarvinSellerIpdv(MongodbMixin, BaseRebuild):
    poller_scope = 'marvin_seller_ipdv'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _rebuild(self, action, data):
        try:
            seller_id = data.get('id')
            platform = (data.get('integration_info') or {}).get('platform')
            account_name = 'MC-{}'.format(seller_id)

            if platform:
                if platform.upper() == 'IPDV':
                    account_name = 'ParceiroMagalu-{}'.format(seller_id)

                payload = {
                    'seller_id': seller_id,
                    'account_name': account_name
                }

                self._register_ipdv_seller(payload)

                logger.info(
                    'Successfully rebuild the register of '
                    'ipdv seller:{}'.format(seller_id)
                )

            return True

        except Exception as e:
            logger.error(
                'Could not rebuild ipdv seller register for error:{error} '
                'data:{data}'.format(
                    data=data,
                    error=e
                )
            )

            raise e

    def _register_ipdv_seller(self, payload):
        MarvinRequest().post(payload)
