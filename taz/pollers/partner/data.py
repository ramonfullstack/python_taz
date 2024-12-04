from taz.pollers.core.data_storage.mssql import MsSqlDataStorage

from .query import STATEMENT


class PartnerDataStorage(MsSqlDataStorage):
    scope = 'partner'
    statement = STATEMENT
