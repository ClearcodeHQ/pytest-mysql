# Copyright (C) 2013 by Clearcode <http://clearcode.cc>
# and associates (see AUTHORS).

# This file is part of pytest-mysql.

# pytest-mysql is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pytest-mysql is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with pytest-mysql.  If not, see <http://www.gnu.org/licenses/>.
"""Process fixture factory for MySQL database."""

import os
import py
from warnings import warn

import pytest
from pytest import FixtureRequest, TempPathFactory
from port_for import get_port

from pytest_mysql.config import get_config
from pytest_mysql.executor import MySQLExecutor


def mysql_proc(
    mysqld_exec=None,
    admin_executable=None,
    mysqld_safe=None,
    host=None,
    user=None,
    port=-1,
    params=None,
    logs_prefix="",
    install_db=None,
):
    """
    Process fixture factory for MySQL server.

    :param str mysqld_exec: path to mysql executable
    :param str admin_executable: path to mysql_admin executable
    :param str mysqld_safe: path to mysqld_safe executable
    :param str host: hostname
    :param str user: user name
    :param str|int|tuple|set|list port:
        exact port (e.g. '8000', 8000)
        randomly selected port (None) - any random available port
        [(2000,3000)] or (2000,3000) - random available port from a given range
        [{4002,4003}] or {4002,4003} - random of 4002 or 4003 ports
        [(2000,3000), {4002,4003}] -random of given range and set
    :param str params: additional command-line mysqld parameters
    :param str logs_prefix: prefix for log filename
    :param str install_db: path to legacy mysql_install_db script
    :rtype: func
    :returns: function which makes a redis process

    """

    @pytest.fixture(scope="session")
    def mysql_proc_fixture(
        request: FixtureRequest, tmp_path_factory: TempPathFactory
    ):
        """
        Process fixture for MySQL server.

        #. Get config.
        #. Initialize MySQL data directory
        #. `Start a mysqld server
            <https://dev.mysql.com/doc/refman/5.0/en/mysqld-safe.html>`_
        #. Stop server and remove directory after tests.
            `See <https://dev.mysql.com/doc/refman/5.6/en/mysqladmin.html>`_

        :param FixtureRequest request: fixture request object
        :param tmp_path_factory: pytest fixture for temporary directories
        :rtype: pytest_dbfixtures.executors.TCPExecutor
        :returns: tcp executor

        """
        config = get_config(request)
        mysql_mysqld = mysqld_exec or config["mysqld"]
        mysql_admin_exec = admin_executable or config["admin"]
        mysql_mysqld_safe = mysqld_safe or config["mysqld_safe"]
        mysql_port = get_port(port) or get_port(config["port"])
        mysql_host = host or config["host"]
        mysql_params = params or config["params"]
        mysql_install_db = install_db or config["install_db"]

        tmpdir = py.path.local(
            tmp_path_factory.mktemp(f"pytest-mysql-{request.fixturename}")
        )

        if logs_prefix:
            warn(
                f"logfile_prefix factory argument is deprecated, "
                f"and will be dropped in future releases. All fixture related "
                f"data resides within {tmpdir}, and logs_prefix is only used, "
                f"if deprecated logsdir is configured",
                DeprecationWarning,
            )

        logsdir = config["logsdir"]
        if logsdir:
            warn(
                f"mysql_logsdir and --mysql-logsdir config option is "
                f"deprecated, and will be dropped in future releases. "
                f"All fixture related data resides within {tmpdir}",
                DeprecationWarning,
            )
            if logs_prefix:
                logfile_path = os.path.join(
                    logsdir,
                    f"{logs_prefix}mysql-server.{mysql_port}.log",
                )
        else:
            logfile_path = tmpdir.join(f"mysql-server.{port}.log")

        mysql_executor = MySQLExecutor(
            mysqld_safe=mysql_mysqld_safe,
            mysqld=mysql_mysqld,
            admin_exec=mysql_admin_exec,
            logfile_path=logfile_path,
            base_directory=tmpdir,
            params=mysql_params,
            user=user or config["user"] or "root",
            host=mysql_host,
            port=mysql_port,
            install_db=mysql_install_db,
        )
        with mysql_executor:
            yield mysql_executor

    return mysql_proc_fixture
