from taz.pollers.core.data.sources import MsSql

from .base import DataStorageBase


class MsSqlDataStorage(DataStorageBase):

    scope = None
    statement = None

    def __init__(self):
        self.db_connection = MsSql(scope=self.scope)

    def fetch(self):  # pragma: no cover
        return self.db_connection.execute(query=self.statement)

    def is_batch(self):  # pragma: no cover
        return 'batch_key' in self.statement

    def shutdown(self):  # pragma: no cover
        self.db_connection.shutdown()


class MsSqlDataStorageCircuitBreaker(MsSqlDataStorage):
    def fetch_counter(self):
        return self.db_connection.execute(query=self.control_statement)
