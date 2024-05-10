"""Actual tests for pytest-mysql."""

from pymysql import Connection

from pytest_mysql.executor import MySQLExecutor

QUERY = """CREATE TABLE pet (name VARCHAR(20), owner VARCHAR(20),
    species VARCHAR(20), sex CHAR(1), birth DATE, death DATE);"""


def test_proc(mysql_proc: MySQLExecutor) -> None:
    """Check first, basic server fixture factory."""
    assert mysql_proc.running()


def test_mysql(mysql: Connection) -> None:
    """Check first, basic client fixture factory."""
    cursor = mysql.cursor()
    cursor.execute(QUERY)
    mysql.commit()
    cursor.close()


def test_mysql_test_without_cursor(mysql: Connection) -> None:
    """Run test without cursor and without fetching the data."""
    mysql.query("SELECT VERSION();")


def test_mysql_newfixture(mysql: Connection, mysql2: Connection) -> None:
    """More complext test with several mysql_processes."""
    cursor = mysql.cursor()
    cursor.execute(QUERY)
    mysql.commit()
    cursor.close()

    cursor = mysql2.cursor()
    cursor.execute(QUERY)
    mysql2.commit()
    cursor.close()


def test_random_port(mysql_rand: Connection) -> None:
    """Test if mysql fixture can be started on random port."""
    mysql = mysql_rand
    mysql.cursor()
