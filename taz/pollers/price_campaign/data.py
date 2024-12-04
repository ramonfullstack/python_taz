from taz.pollers.core.data_storage.mssql import MsSqlDataStorage

from .query import STATEMENT


class PriceDataStorage(MsSqlDataStorage):
    scope = 'price_campaign'
    statement = STATEMENT
