"""MySQL tests that do not start mysql server."""

from pymysql import Connection

from pytest_mysql import factories
from tests.test_mysql import QUERY

mysql_noproc2 = factories.mysql_noproc()
mysqlnoproc_client = factories.mysql("mysql_noproc2")


def test_mysql_noproc(mysqlnoproc_client: Connection) -> None:
    """Check if noproc fixture connects to the running mysql instance."""
    cursor = mysqlnoproc_client.cursor()
    cursor.execute(QUERY)
    mysqlnoproc_client.commit()
    cursor.close()


def test_mysql_noproc_closing_connection_not_throwing_exception(
    mysqlnoproc_client: Connection,
) -> None:
    """Check if closing the connection doesn't throw an exception.

    When cleaning the fixture.
    """
    cursor = mysqlnoproc_client.cursor()
    cursor.execute(QUERY)
    mysqlnoproc_client.commit()
    cursor.close()
    mysqlnoproc_client.close()
