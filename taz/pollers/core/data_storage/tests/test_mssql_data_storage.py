import pytest

from taz.pollers.category.query import STATEMENT
from taz.pollers.core.data_storage.mssql import MsSqlDataStorage


class TestMsSqlDataStorage:

    @pytest.fixture
    def statement(self):
        return STATEMENT

    @pytest.fixture
    def data_storage(self, statement):
        MsSqlDataStorage.statement = statement
        MsSqlDataStorage.scope = 'test_scope'
        return MsSqlDataStorage()

    def test_scope_should_be_the_same_for_db_connection_and_data_storage(
        self,
        data_storage
    ):
        assert data_storage.scope == data_storage.db_connection.scope

    def test_should_be_true_when_there_is_batch_key_in_statement(
        self,
        data_storage
    ):
        assert data_storage.is_batch()

    def test_should_be_false_when_there_is_no_batch_key_in_statement(
        self
    ):

        MsSqlDataStorage.statement = """
        SELECT
            l.strCodigo as category_id,
            l.strDescricao as category_description,
            s.strSetor as subcategory_id,
            s.strDescricao as subcategory_description,
            s.blnAtivo as subcategory_active
        FROM
            tablinha l (nolock)
        JOIN
            tabsetor s (nolock) ON l.strcodigo = s.strlinha
            AND l.strCodigo <> 'TM'
        """

        data_storage = MsSqlDataStorage()
        assert data_storage.is_batch() is False
