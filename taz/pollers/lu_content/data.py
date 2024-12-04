from taz.pollers.core.data.sources import MsSql
from taz.pollers.core.data_storage.mssql import MsSqlDataStorage

from .query import STATEMENT, STATEMENT_DETAIL


class LuContentDataStorage(MsSqlDataStorage):  # pragma: no cover
    scope = 'lu_content'
    statement = STATEMENT

    def __init__(self):
        super().__init__()
        self.db_detail_connection = MsSql(scope=self.scope)

    def fetch_details(self, content_id):
        return self.db_detail_connection.execute(
            query=STATEMENT_DETAIL.format(content_id)
        )

    def shutdown(self):
        super().shutdown()
        self.db_detail_connection.shutdown()
