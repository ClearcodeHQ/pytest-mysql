from pytest_mysql import factories
from tests.test_mysql import QUERY

mysql_noproc2 = factories.mysql_noproc()
mysqlnoproc_client = factories.mysql("mysql_noproc2")


def test_mysql_noproc(mysqlnoproc_client):
    """Check if noproc fixture connects to the running mysql instance."""
    cursor = mysqlnoproc_client.cursor()
    cursor.execute(QUERY)
    mysqlnoproc_client.commit()
    cursor.close()
