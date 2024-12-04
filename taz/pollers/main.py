import logging
import time
from functools import partial

from simple_settings import settings

from taz.pollers.base_price.poller import BasePricePoller
from taz.pollers.category.poller import CategoryPoller
from taz.pollers.factsheet.poller import FactsheetPoller
from taz.pollers.lu_content.poller import LuContentPoller
from taz.pollers.partner.poller import PartnerPoller
from taz.pollers.price.poller import PricePoller
from taz.pollers.price_campaign.poller import (
    PricePoller as PriceCampaignPoller
)
from taz.pollers.product.poller import ProductPoller
from taz.pollers.video.poller import VideoPoller

logger = logging.getLogger(__name__)


def poller_handler(poller_class, args):
    poller = poller_class()
    execute(poller)


partner_handler = partial(poller_handler, PartnerPoller)
product_handler = partial(poller_handler, ProductPoller)
category_handler = partial(poller_handler, CategoryPoller)
price_handler = partial(poller_handler, PricePoller)
price_campaign_handler = partial(poller_handler, PriceCampaignPoller)
base_price_handler = partial(poller_handler, BasePricePoller)
factsheet_handler = partial(poller_handler, FactsheetPoller)
lu_content_handler = partial(poller_handler, LuContentPoller)
video_handler = partial(poller_handler, VideoPoller)


def execute(poller):  # pragma: no cover
    logger.info('Starting poller for {} scope'.format(poller.scope))

    try:
        while True:
            start = time.time()

            poller.poll()

            logger.info('Done in {}s'.format(time.time() - start))
            logger.debug('Waiting {}s until next iteration...'.format(
                settings.POLLERS[poller.scope]['wait_time'])
            )

            poller.wait()
    except KeyboardInterrupt:
        logger.warning('Halting execution, user requested interruption.')
    except Exception as e:
        logger.exception('A serious error happened!')
        raise e
    finally:
        poller.shutdown()
