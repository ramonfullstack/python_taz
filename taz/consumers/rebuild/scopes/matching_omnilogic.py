import logging
from concurrent.futures import ThreadPoolExecutor, wait

from simple_settings import settings

from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.google.stream import StreamPublisherManager
from taz.consumers.rebuild.scopes.base import BaseRebuild

logger = logging.getLogger(__name__)


class RebuildMatchingOmnilogic(MongodbMixin, BaseRebuild):
    poller_scope = 'matching_omnilogic'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pubsub = StreamPublisherManager()

    @property
    def enriched_products(self):
        return self.get_collection('enriched_products')

    def _rebuild(self, action, data):
        logger.info(
            'Starting matching omnilogic rebuild with request:{}'.format(data)
        )

        enriched_products = self.enriched_products.find(
            {'entity': data['entity']},
            no_cursor_timeout=True
        )

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(self._send, enriched_product)
                for enriched_product in list(enriched_products)
            ]

        wait(futures)

        logger.info('Finish matching omnilogic rebuild')

        return True

    def _send(self, enriched_product):
        seller_id = enriched_product['seller_id']
        sku = enriched_product['sku']
        navigation_id = enriched_product['navigation_id']

        self.pubsub.publish(
            content=enriched_product,
            project_id=settings.GOOGLE_PROJECT_ID,
            topic_name=settings.PUBSUB_NOTIFICATION_TOPIC_NAME,
        )

        logger.info(
            'Rebuild to matching omnilogic for sku:{sku} '
            'seller_id:{seller_id} navigation_id:{navigation_id} '.format(
                sku=sku,
                seller_id=seller_id,
                navigation_id=navigation_id
            )
        )
