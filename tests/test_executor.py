"""Executor tests."""

import pytest
from mock import patch

from pytest_mysql.executor import MySQLExecutor, MySQLUnsupported


@pytest.mark.parametrize('verstr, version', (
    (b'mysql_install_db Ver 5.7.21, for Linux on x86_64', '5.7.21'),
    (
        (
            b'mysqld  Ver 5.7.21-0ubuntu0.17.10.1 '
            b'for Linux on x86_64 ((Ubuntu))'
        ),
        '5.7.21'
    ),
    (b'mysql 5.5.55', '5.5.55')
))
def test_version_check(verstr, version, tmpdir_factory):
    """Test executor's version property."""
    executor = MySQLExecutor(
        mysqld_safe='',
        mysqld='',
        admin_exec='',
        logfile_path='',
        params={},
        base_directory=tmpdir_factory.mktemp('pytest-mysql'),
        user='',
        host='',
        port=8838
    )

    with patch(
            'subprocess.check_output',
            lambda *args: verstr
    ):
        assert version == executor.version()


@pytest.mark.parametrize('verstr', (
    b'mysql_install_db Ver 5.7.1, for Linux on x86_64',
    b'mysqld  Ver 5.7.1-0ubuntu0.17.10.1 for Linux on x86_64 ((Ubuntu))',
    b'mysql 5.5.55',
))
def test_exception_raised(verstr, tmpdir_factory):
    """Raise exception on not supported versions."""
    executor = MySQLExecutor(
        mysqld_safe='',
        mysqld='',
        admin_exec='',
        logfile_path='',
        params={},
        base_directory=tmpdir_factory.mktemp('pytest-mysql'),
        user='',
        host='',
        port=8838
    )

    with patch(
            'subprocess.check_output',
            lambda *args: verstr
    ), pytest.raises(MySQLUnsupported):
        executor.start()
