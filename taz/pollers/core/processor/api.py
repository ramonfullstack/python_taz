import logging

from taz.constants import FIRST_FIVE_DIGITS
from taz.pollers.core.base import Poller
from taz.pollers.core.brokers.stream import KinesisBroker
from taz.pollers.core.data_storage.api import ApiDataStorage
from taz.pollers.core.exceptions import ConverterException

logger = logging.getLogger(__name__)


class ApiPoller(Poller):

    def poll(self):
        total_items = 0
        processed_batches_ids = []

        items = self._get_items()
        for item in items:
            batch_key = self._get_batch_key(item)
            total_items += 1
            convertion_has_failed = False
            batch_data = []

            try:
                batch_data.append(item)
                self.converter.from_source(batch_data)

            except ConverterException:
                convertion_has_failed = True

                logger.exception(
                    'An error occurred while converting {scope} and '
                    'item {item}. Skipping data.'.format(
                        scope=self.scope,
                        item=item
                    )
                )
            if not convertion_has_failed:
                self.compare_and_store(
                    batch_key,
                    self.converter.get_items()
                )

            processed_batches_ids.append(batch_key)

            self.converter.flush_items()

        stored_batches = self.diff_storage.retrieve_many(self.scope)
        stored_batches_ids = self._get_stored_batch_ids(stored_batches)
        skipped_batches_ids = stored_batches_ids.difference(
            processed_batches_ids
        )

        if not skipped_batches_ids:
            return total_items

        logger.info(
            (
                'Finished polling scope {scope}'
                ' with a total of {total} items'
            ).format(scope=self.scope, total=total_items)
        )

        self._delete_skipped_items(skipped_batches_ids, stored_batches)

        return total_items

    def get_sender(self):  # pragma: no cover
        return KinesisBroker(self.scope)

    def get_data_source(self):  # pragma: no cover
        return ApiDataStorage()

    def get_converter(self):  # pragma: no cover
        raise NotImplementedError()

    def _get_batch_key(self, item):
        if self.data_source.is_batch():
            return item[self.data_source.batch_key()][FIRST_FIVE_DIGITS]

        return item[self.data_source.batch_key()]

    def _get_items(self):
        items = self.data_source.fetch()
        return items if not self._has_results_key(items) else items['results']

    def _has_results_key(self, items):
        return isinstance(items, dict) and items.get('results')

    def _get_stored_batch_ids(self, batches):
        ids = set()
        for batch in batches:
            for batch_id in batch.keys():
                ids.add(batch_id)
        return ids

    def _convert_item(self, item):
        convert_has_failed = False
        try:
            self.converter.from_source(item)
        except ConverterException:
            convert_has_failed = True

            logger.exception(
                'An error occurred while converting {scope} and '
                'item {item}. Skipping data.'.format(
                    scope=self.scope,
                    item=item
                )
            )

        return convert_has_failed
