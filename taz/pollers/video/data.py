from taz.pollers.core.data_storage.mssql import MsSqlDataStorage

from .query import STATEMENT


class VideoDataStorage(MsSqlDataStorage):
    scope = 'video'
    statement = STATEMENT
