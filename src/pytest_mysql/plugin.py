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
"""Plugin definition."""
from tempfile import gettempdir

from pytest_mysql import factories


_help_executable = 'Path to MySQL executable'
_help_admin = 'Path to MySQL\'s admin executable'
_help_init = 'Path to MySQL\'s init executable'
_help_logsdir = "Logs directory location"
_help_host = 'Host at which MySQL will accept connections'
_help_port = 'Port at which MySQL will accept connections'
_help_user = "MySQL username"
_help_passwd = "MySQL password"
_help_dbname = "Test database name"
_help_params = "Starting parameters for the MySQL"


def pytest_addoption(parser):
    """Plugin configuration."""
    parser.addini(
        name='mysql_exec',
        help=_help_executable,
        default='/usr/bin/mysqld_safe'
    )

    parser.addini(
        name='mysql_admin',
        help=_help_admin,
        default='/usr/bin/mysqladmin'
    )

    parser.addini(
        name='mysql_init',
        help=_help_init,
        default='/usr/bin/mysql_install_db'
    )

    parser.addini(
        name='mysql_host',
        help=_help_host,
        default='localhost'
    )

    parser.addini(
        name='mysql_port',
        help=_help_port,
        default=None,
    )

    parser.addini(
        name='mysql_user',
        help=_help_user,
        default='root'
    )

    parser.addini(
        name='mysql_passwd',
        help=_help_passwd,
        default=''
    )

    parser.addini(
        name='mysql_dbname',
        help=_help_dbname,
        default='test'
    )

    parser.addini(
        name='mysql_params',
        help=_help_params,
        default=''
    )

    parser.addini(
        name='mysql_logsdir',
        help=_help_logsdir,
        default=gettempdir(),
    )

    parser.addoption(
        '--mysql-exec',
        action='store',
        metavar='path',
        dest='mysql_exec',
        help=_help_executable
    )

    parser.addoption(
        '--mysql-admin',
        action='store',
        metavar='path',
        dest='mysql_admin',
        help=_help_admin
    )

    parser.addoption(
        '--mysql-init',
        action='store',
        metavar='path',
        dest='mysql_init',
        help=_help_init
    )

    parser.addoption(
        '--mysql-host',
        action='store',
        dest='mysql_host',
        help=_help_host,
    )

    parser.addoption(
        '--mysql-port',
        action='store',
        dest='mysql_port',
        help=_help_port
    )

    parser.addoption(
        '--mysql-user',
        action='store',
        dest='mysql_user',
        help=_help_user
    )

    parser.addoption(
        '--mysql-passwd',
        action='store',
        dest='mysql_passwd',
        help=_help_passwd
    )

    parser.addoption(
        '--mysql-dbname',
        action='store',
        dest='mysql_dbname',
        help=_help_dbname
    )

    parser.addoption(
        '--mysql-params',
        action='store',
        dest='mysql_params',
        help=_help_params
    )

    parser.addoption(
        '--mysql-logsdir',
        action='store',
        metavar='path',
        dest='mysql_logsdir',
        help=_help_params
    )


mysql_proc = factories.mysql_proc()
mysql = factories.mysql('mysql_proc')
