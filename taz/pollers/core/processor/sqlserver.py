import logging

from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from redis import Redis
from simple_settings import settings

from taz.pollers.core.base import Poller
from taz.pollers.core.exceptions import (
    ConverterException,
    DatabaseException,
    PollerCircuitBreaker
)
from taz.settings.otel import start_as_current_span

logger = logging.getLogger(__name__)


class SqlserverPoller(Poller):  # pragma: no cover

    def __init__(self):
        super().__init__()

    def poll(self):  # pragma: no cover
        self._starting()

        batch_cursor_key = '{}_latest_batch'.format(self.scope)

        db_cursor = self.data_source.fetch()

        batch_process = self.data_source.is_batch()

        batch_data = []
        batch_key = ''

        key_changed = False

        total_items = 0
        processed_batches_ids = set()

        errored = False
        errored_batch = ''
        latest_batch_cursor_key = self.get_redis().get(batch_cursor_key)
        if latest_batch_cursor_key:
            latest_batch_cursor_key = latest_batch_cursor_key.decode('utf-8')

        while db_cursor:
            try:
                data = db_cursor.fetchone()
            except Exception as e:
                logger.exception(
                    'A database error {error} occurred while fetching '
                    'data from {scope} and batch_key {batch}. '
                    'Stopping poller.'.format(
                        scope=self.scope,
                        batch=batch_key,
                        error=e
                    )
                )
                errored = True
                errored_batch = batch_key if not data else data['batch_key']
                self.shutdown()
                break

            if not data:
                db_cursor = False
                data = None
            else:
                data['batch_key'] = data['batch_key'].strip()
                total_items += 1
                logger.debug('Iterating over item {} on batch {}:{}'.format(
                    total_items,
                    data['batch_key'],
                    batch_key,
                ))

            if db_cursor:
                if batch_process:
                    if latest_batch_cursor_key:
                        if latest_batch_cursor_key != data['batch_key']:  # noqa
                            logger.debug(
                                SqlserverPoller._format_latest_run_message(
                                    data=data,
                                    latest_batch_cursor_key=latest_batch_cursor_key  # noqa
                                )
                            )
                            processed_batches_ids.add(data['batch_key'])
                            continue
                        else:
                            self.get_redis().delete(batch_cursor_key)
                            latest_batch_cursor_key = None

                    if batch_key == '' or batch_key == data['batch_key']:
                        batch_key = data['batch_key']
                        batch_data.append(data)
                    else:
                        key_changed = True

                else:
                    if batch_key == '':
                        batch_key = self.scope.strip()
                    batch_data.append(data)

            if key_changed or not db_cursor:
                if self.sender.halt_requested:
                    logger.warning(
                        'A stop was requested, '
                        'aborting processing for batch {}'.format(
                            batch_key
                        )
                    )

                logger.debug(
                    'Processed Batch: {batch}, '
                    'Total items: {total}, '
                    'Scope: {scope}'.format(
                        total=len(batch_data),
                        batch=batch_key,
                        scope=self.scope,
                    )
                )

                convertion_failed = False

                try:
                    self.converter.from_source(batch_data)
                except ConverterException as e:
                    convertion_failed = True

                    logger.exception(
                        'An error {error} occurred while converting '
                        '{scope} and batch_key {batch}.'
                        'Skipping batch.'.format(
                            scope=self.scope,
                            batch=batch_key,
                            error=e
                        )
                    )
                except DatabaseException as e:
                    logger.exception(
                        'A database error {error} occurred while fetching '
                        'data from {scope} and batch_key {batch}. '
                        'Stopping poller.'.format(
                            scope=self.scope,
                            batch=batch_key,
                            error=e
                        )
                    )
                    errored = True
                    errored_batch = (
                        batch_key if not data else data['batch_key']
                    )
                    self.shutdown()
                    break

                if not convertion_failed:
                    if not batch_key and not self.converter.get_items():
                        continue

                    self.compare_and_store(
                        batch_key,
                        self.converter.get_items()
                    )

                processed_batches_ids.add(batch_key)

                self.converter.flush_items()

                if key_changed:
                    batch_data = [data]
                    batch_key = data['batch_key']
                    key_changed = False

        with start_as_current_span(
            f'poller.execute.{self.scope}',
            kind=trace.SpanKind.CONSUMER
        ) as span:
            if not errored:
                self.get_redis().delete(batch_cursor_key)
                stored_batches = self.diff_storage.retrieve_many(self.scope)

                stored_batches_ids = set()
                for batch in stored_batches:
                    for batch_id in batch.keys():
                        stored_batches_ids.add(batch_id)

                skipped_batches_ids = stored_batches_ids.difference(
                    processed_batches_ids
                )

                if not skipped_batches_ids:
                    logger.debug('Shutdown, no skipped batches ids...')
                    self.shutdown()
                    return total_items

                self._delete_skipped_items(skipped_batches_ids, stored_batches)
                logger.info(
                    'Finished polling scope {} with a total of {} items'.format(  # noqa
                        self.scope,
                        total_items,
                    )
                )
                span.set_status(Status(StatusCode.OK))
            else:
                if not latest_batch_cursor_key:
                    self.get_redis().set(batch_cursor_key, errored_batch)
                logger.warning(
                    'Finished with error polling scope {} with a total of {} items'.format(  # noqa
                        self.scope,
                        total_items,
                    )
                )
                span.set_status(Status(StatusCode.ERROR))

        self.shutdown()
        return total_items

    @classmethod
    def _format_latest_run_message(cls, data, latest_batch_cursor_key):
        return 'Skipping batch {batch_key} for {scope} {sku}. Reason: seeking batch {latest_run} from latest run'.format(  # noqa
            batch_key=data['batch_key'],
            scope=cls.scope,
            latest_run=latest_batch_cursor_key,
            sku=data.get('sku', '')
        )

    @staticmethod
    def get_redis():
        return Redis(
            host=settings.REDIS_SETTINGS['host'],
            port=settings.REDIS_SETTINGS['port'],
            password=settings.REDIS_SETTINGS.get('password')
        )


class SqlServerPollerWithCircuitBreaker(SqlserverPoller):  # pragma: no cover
    control_key_prefix = 'POLLER_CONTROL'

    def poll(self):  # pragma: no cover
        try:
            last_skus_actives = int(self.get_redis().get(
                f'{self.control_key_prefix}::{self.scope}'
            ) or '0')
            logger.debug(f'last_skus_actives: {last_skus_actives}')
            skus_actives = list(self.data_source.fetch_counter())[0]['actives']
            logger.debug(f'skus_actives: {skus_actives}')
        except Exception as e:
            raise PollerCircuitBreaker(
                f'circuitbreaker setup error: {str(e)}'
            )

        change_percentage = 100 * abs(
            (last_skus_actives - skus_actives) / skus_actives
        )
        logger.debug(f'change_percentage: {change_percentage}')
        if change_percentage > settings.ALLOW_INACTIVATION_PERCENTAGE:
            raise PollerCircuitBreaker(
                f'circuitbreaker changing {change_percentage}% of actives skus'
            )

        super().poll()

        self.get_redis().set(
            f'{self.control_key_prefix}::{self.scope}',
            str(skus_actives)
        )
