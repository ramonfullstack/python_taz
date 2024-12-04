import abc
import logging
import time
from decimal import Decimal

from simple_settings import settings

from taz.pollers.core.data.comparison import RedisStorage
from taz.pollers.core.exceptions import SendRecordsException
from taz.pollers.core.mixins.diff import DiffMixin
from taz.pollers.core.mixins.sort import SortMixin

logger = logging.getLogger(__name__)


class Poller(DiffMixin, SortMixin, metaclass=abc.ABCMeta):

    def __init__(self):
        self.is_running = False
        self._starting()

    @abc.abstractproperty
    def scope(self):
        pass  # pragma: no cover

    @abc.abstractmethod
    def get_sender(self):
        return  # pragma: no cover

    @abc.abstractmethod
    def get_data_source(self):
        return  # pragma: no cover

    @abc.abstractmethod
    def get_converter(self):
        return  # pragma: no cover

    @abc.abstractmethod
    def poll(self):
        return  # pragma: no cover

    def unpack(self, base_obj):
        return base_obj.values() if isinstance(base_obj, dict) else base_obj

    def has_nested_type(self, type_name, iterable_obj):
        return any(
            isinstance(value, type_name) for value in self.unpack(iterable_obj)
        )

    def strip_type(self, type_name, base_obj):
        items_without_type = []
        items_with_type = []
        for value in self.unpack(base_obj):
            if isinstance(value, type_name):
                items_with_type.append(value)
            else:
                items_without_type.append(value)
        return items_with_type, items_without_type

    def compare_types(self, type_name, obj_a, obj_b):
        nested_types_a, typeless_a = self.strip_type(
            type_name,
            obj_a
        )
        nested_types_b, typeless_b = self.strip_type(
            type_name,
            obj_b
        )

        if self.lists_differ(typeless_b, typeless_a):
            return True

        for values_a, values_b in zip(nested_types_a, nested_types_b):
            if (
                self.lists_differ(
                    self.unpack(values_b),
                    self.unpack(values_a)
                )
            ):
                return True

        return False

    def _normalize_primitives(self, items):
        return [
            Decimal(str(i)) if isinstance(i, float) else i
            for i in items
        ]

    def compare_and_store(self, batch_key, db_data):
        storage_data = self.diff_storage.retrieve(self.scope, batch_key)

        deleted, inserted, updated = self.diff(db_data, storage_data)

        if any(len(i) > 0 for i in (deleted, inserted, updated)):
            message = '''Polled {scope}[{batch_id}]. Here's the results:
            - {deleted_total} items will be deleted
            - {inserted_total} items will be inserted
            - {updated_total} items will be updated
            '''.format(
                scope=self.scope,
                batch_id=batch_key,
                deleted_total=len(deleted),
                inserted_total=len(inserted),
                updated_total=len(updated),
            )
            logger.info(message)

        logger.debug('[{scope}] Deleted items: {deleted_total}'.format(
            scope=self.scope,
            deleted_total=len(deleted))
        )
        logger.debug('[{scope}] Created items: {inserted_total}'.format(
            scope=self.scope,
            inserted_total=len(inserted))
        )
        logger.debug('[{scope}] Updated items: {updated_total}'.format(
            scope=self.scope,
            updated_total=len(updated))
        )

        try:
            if deleted:
                if self.scope == 'product':
                    for item in deleted:
                        logger.info(
                            'Deleting product sku:{sku} '
                            'active:False'.format(
                                sku=item['sku']
                            )
                        )
                        item['active'] = False

                self.sender.put_many('delete', deleted)
                del deleted

            if updated:
                self.sender.put_many('update', updated)
                del updated

            if inserted:
                self.sender.put_many('create', inserted)
                del inserted

            self.diff_storage.store(self.scope, batch_key, db_data)

            del storage_data
            del db_data
        except SendRecordsException:
            logger.error('Unable to process batch {}'.format(batch_key))

    def _delete_skipped_items(self, skipped_batches_ids, stored_batches):
        deleted_items = []
        for batch_id in skipped_batches_ids:
            for stored_batch in stored_batches:
                if batch_id not in stored_batch:
                    continue

                logger.info(
                    'Gathering items from '
                    'scope:{} batch:{} to request deletion'.format(
                        self.scope, batch_id
                    )
                )

                for batch in stored_batch.values():
                    for item in batch.values():
                        if self.scope == 'product':
                            logger.info(
                                'Deleting product sku:{sku} '
                                'active:False'.format(
                                    sku=item['sku']
                                )
                            )
                            item['active'] = False
                        deleted_items.append(item)

        if deleted_items:
            self.sender.put_many('delete', deleted_items)

            for batch_id in skipped_batches_ids:
                self.diff_storage.delete(self.scope, batch_id)

    def _starting(self):
        if not self.is_running:
            self.sender = self.get_sender()
            self.data_source = self.get_data_source()
            self.converter = self.get_converter()
            self.diff_storage = RedisStorage()
            self.is_running = True

    def shutdown(self):
        self.converter.shutdown()
        self.diff_storage.shutdown()
        self.data_source.shutdown()
        self.sender.shutdown()
        self.is_running = False

    def wait(self):
        time.sleep(int(settings.POLLERS[self.scope]['wait_time']))
