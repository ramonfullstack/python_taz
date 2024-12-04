from pymssql._mssql import MSSQLException
from simple_settings import settings

from taz.pollers.core.data.sources import MsSql
from taz.pollers.core.data_storage.mssql import MsSqlDataStorage

from .query import STATEMENT_DETAILS, STATEMENT_LIST_SKUS


class FactsheetDataStorage(MsSqlDataStorage):  # pragma: no cover
    scope = 'factsheet'
    statement = STATEMENT_LIST_SKUS

    def __init__(self):
        super().__init__()
        self.db_detail_connection = MsSql(scope=self.scope)

    def fetch_details(self, factsheet_id, product_id):
        return self._make_fetch(
            query=STATEMENT_DETAILS.format(factsheet_id, product_id)
        )

    def _make_fetch(self, query, retry=1):
        try:
            return self.db_detail_connection.execute(
                query=query
            )
        except MSSQLException as e:
            if retry <= settings.FACTSHEET_FETCH_MAX_RETRIES:
                self.db_detail_connection.create_new_connection()
                return self._make_fetch(query, retry=retry + 1)
            raise e

    def shutdown(self):
        super().shutdown()
        self.db_detail_connection.shutdown()
