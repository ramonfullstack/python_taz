from taz.pollers.core.data_storage.mssql import MsSqlDataStorageCircuitBreaker
from taz.pollers.product.control_query import CONTROL_STATEMENT
from taz.pollers.product.query import STATEMENT


class ProductDataStorage(MsSqlDataStorageCircuitBreaker):
    scope = 'product'
    statement = STATEMENT
    control_statement = CONTROL_STATEMENT
