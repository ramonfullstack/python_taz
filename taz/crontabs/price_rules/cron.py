import logging
from concurrent.futures import ThreadPoolExecutor, wait
from functools import cached_property
from json import dumps, loads
from time import perf_counter
from typing import Dict, List, Optional, Tuple

from pymongo.collection import Collection
from pymongo.results import UpdateResult
from redis import Redis
from simple_settings import settings

from taz.api.classifications_rules.schemas import ClassificationsRulesStatus
from taz.constants import SOURCE_HECTOR, SOURCE_OMNILOGIC, UPDATE_ACTION
from taz.consumers.core.database.mongodb import MongodbMixin
from taz.consumers.core.google.stream import StreamPublisherManager
from taz.consumers.core.notification import Notification
from taz.crontabs.base import CronBase
from taz.helpers.pagination import Pagination

logger = logging.getLogger(__name__)


class PriceRulesCrontab(CronBase, MongodbMixin):

    cron_name = 'PriceRulesCrontab'
    PRICE_RULES_CACHE_KEY: str = '{cron_name}::{product_type}'
    MAX_WORKERS = 10

    @cached_property
    def pubsub(self):
        return StreamPublisherManager()

    @cached_property
    def classifications_rules(self) -> Collection:
        return self.get_collection('classifications_rules')

    @cached_property
    def enriched_products(self) -> Collection:
        return self.get_collection('enriched_products')

    @cached_property
    def pagination(self):
        return Pagination(self.enriched_products)

    @cached_property
    def cache(self) -> Redis:
        return Redis(
            host=settings.REDIS_LOCK_SETTINGS['host'],
            port=settings.REDIS_LOCK_SETTINGS['port'],
            password=settings.REDIS_LOCK_SETTINGS.get('password'),
            socket_connect_timeout=int(
                settings.REDIS_LOCK_SETTINGS['socket_connect_timeout']
            ),
            socket_timeout=int(settings.REDIS_LOCK_SETTINGS['socket_timeout'])
        )

    def mount_cache_key(self, product_type: str) -> str:
        return self.PRICE_RULES_CACHE_KEY.format(
            cron_name=self.cron_name,
            product_type=product_type
        )

    def _save_progress(
        self,
        product_type: str,
        source: str,
        navigation_id: str
    ) -> None:
        self.cache.setex(
            name=self.mount_cache_key(product_type),
            value=dumps({'source': source, 'navigation_id': navigation_id}),
            time=int(settings.PRICE_RULE_PROGRESS_TTL)
        )

    def _get_progress(self, product_type: str) -> Optional[Dict]:
        if (recovered_progress := self.cache.get(
            self.mount_cache_key(product_type)
        )):
            return loads(recovered_progress)

    def _clear_progress(self, product_type: str) -> None:
        self.cache.delete(self.mount_cache_key(product_type))

    def run(self) -> None:
        logger.info('PriceRules crontab started')

        start = perf_counter()

        rules_not_applied = list(
            self.classifications_rules.find(
                {'status': {'$ne': ClassificationsRulesStatus.applied.value}},
                {'_id': 0, 'product_type': 1}
            )
        )

        if not rules_not_applied:
            logger.info(
                'Rules without applied status not found, finish process '
                f'in {perf_counter() - start:.3f}s'
            )
            return

        filter_product_types: List[str] = sorted({
            rule['product_type'] for rule in rules_not_applied
        })

        self.find_products_and_notify(filter_product_types)

        logger.info(
            'Price rules crontab finish process with success '
            f'in {perf_counter() - start:.3f}s'
        )

    def _load_progress(
        self,
        product_type: str
    ) -> Tuple[Optional[str], Optional[str]]:
        recovered_source: Optional[str] = None
        recovered_navigation_id: Optional[str] = None
        if (progress := self._get_progress(product_type)):
            recovered_navigation_id: str = progress['navigation_id']
            recovered_source: str = progress['source']
            logger.info(
                f'Process for product_type:{product_type} '
                f'recovered progress:{progress}'
            )

        return recovered_source, recovered_navigation_id

    def __mount_criteria(self, source: str, product_type: str) -> str:
        return (
            {'source': source, 'entity': product_type}
            if source == SOURCE_OMNILOGIC
            else {
                'source': source,
                'classifications.product_type': product_type
            }
        )

    def _check_skip_notification(
        self,
        recovered_source: Optional[str],
        recovered_navigation_id: Optional[str],
        current_source: str,
        last_navigation_id: str
    ) -> bool:
        if not recovered_source or not recovered_navigation_id:
            return False

        return (
            recovered_source == current_source and
            last_navigation_id <= recovered_navigation_id
        ) or (
            recovered_source == SOURCE_HECTOR and
            current_source == SOURCE_OMNILOGIC
        )

    def find_products_and_notify(self, product_types: List[str]) -> None:
        for product_type in product_types:
            logger.info(f'Starting process for product_type:{product_type}')
            recovered_source, recovered_navigation_id = (
                self._load_progress(product_type)
            )

            notification_products = set()
            for source in [SOURCE_OMNILOGIC, SOURCE_HECTOR]:
                last_navigation_id: Optional[str] = None

                while True:
                    start: float = perf_counter()
                    products = list(
                        self.pagination._paginate_keyset(
                            criteria=self.__mount_criteria(
                                source, product_type
                            ),
                            fields={
                                '_id': 0,
                                'sku': 1,
                                'seller_id': 1,
                                'navigation_id': 1
                            },
                            limit_size=int(
                                settings.PAGINATION_LIMIT_PRICE_RULE_CRON
                            ),
                            sort=[('navigation_id', 1)],
                            field_offset='navigation_id',
                            offset=last_navigation_id,
                            no_cursor_timeout=False
                        )
                    )

                    logger.debug(
                        f'Fetched data for product_type:{product_type} in '
                        f'{perf_counter()-start:.3f}s'
                    )

                    if not products:
                        if not last_navigation_id:
                            logger.warning(
                                'Products not found in enriched products with '
                                f'product_type:{product_type} '
                                f'and source:{source}'
                            )
                        break

                    last_navigation_id: str = products[-1]['navigation_id']
                    skip_notification: bool = self._check_skip_notification(
                        recovered_source,
                        recovered_navigation_id,
                        source,
                        last_navigation_id
                    )

                    self.send_notification(
                        products=products,
                        notification_products=notification_products,
                        product_type=product_type,
                        source=source,
                        skip_notification=skip_notification
                    )

                    self._save_progress(
                        product_type=product_type,
                        source=source,
                        navigation_id=last_navigation_id
                    )

            result: UpdateResult = self.classifications_rules.update_many(
                {'product_type': product_type},
                {'$set': {'status': ClassificationsRulesStatus.applied.value}}
            )

            self._clear_progress(product_type=product_type)

            logger.info(
                f'Finished process for product_type:{product_type} '
                f'with {result.modified_count} updated documents'
            )

    def send_notification(
        self,
        products: List[Dict],
        notification_products: set,
        product_type: str,
        source: str,
        skip_notification: bool
    ) -> None:
        start: float = perf_counter()
        products_to_notify = []
        for product in products:
            key = (product['sku'], product['seller_id'])
            if not skip_notification and key not in notification_products:
                products_to_notify.append(
                    Notification.format_payload(
                        sku=product['sku'],
                        seller_id=product['seller_id'],
                        navigation_id=product.get('navigation_id'),
                        action=UPDATE_ACTION,
                        scope='price',
                        origin='price_rule_cron'
                    )
                )

            notification_products.add(key)

        if products_to_notify:
            with ThreadPoolExecutor(
                max_workers=int(settings.MAX_WORKERS_PRICE_RULE_CRON)
            ) as executor:
                futures = [
                    executor.submit(
                        self.pubsub.publish,
                        p,
                        settings.PUBSUB_RECLASSIFICATION_PRICE_RULE_NAME,
                        settings.GOOGLE_PROJECT_ID
                    ) for p in products_to_notify
                ]

            wait(futures)

        logger.info(
            f'Sent {len(products_to_notify)} products out of a total:'
            f'{len(products)} with product_type:{product_type} '
            f'and source:{source} to '
            f'{settings.PUBSUB_RECLASSIFICATION_PRICE_RULE_NAME} '
            f'in {perf_counter()-start:.3f}s'
        )


if __name__ == '__main__':  # pragma: no cover
    crontab = PriceRulesCrontab()
    crontab.start()
