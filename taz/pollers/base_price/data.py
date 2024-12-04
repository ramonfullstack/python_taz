from taz.pollers.core.data_storage.mssql import MsSqlDataStorage

from .query import STATEMENT


class BasePriceDataStorage(MsSqlDataStorage):
    scope = 'base_price'
    statement = STATEMENT
