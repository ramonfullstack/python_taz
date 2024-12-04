from taz.pollers.core.data_storage.mssql import MsSqlDataStorage

from .query import STATEMENT


class CategoryDataStorage(MsSqlDataStorage):
    scope = 'category'
    statement = STATEMENT
