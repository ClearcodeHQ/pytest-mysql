"""Tests main conftest file."""
import sys
import warnings

from pytest_mysql import factories

if not sys.version_info >= (3, 5):
    warnings.simplefilter("error", category=DeprecationWarning)


# pylint:disable=invalid-name
mysql_proc2 = factories.mysql_proc(port=3308)
mysql2 = factories.mysql("mysql_proc2", dbname="test-db")
mysql_rand_proc = factories.mysql_proc(port=None)
mysql_rand = factories.mysql("mysql_rand_proc")
# pylint:enable=invalid-name
