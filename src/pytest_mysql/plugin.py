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


_help_executable = 'Path to PostgreSQL executable'
_help_logsdir = "Logs directory location"


def pytest_addoption(parser):
    """Plugin configuration."""
    parser.addini(
        name='mysql_exec',
        help=_help_executable,
        default='/usr/bin/mysqld_safe'
    )

    parser.addini(
        name='mysql_logsdir',
        help='logsdir',
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
        '--mysql-logsdir',
        action='store',
        metavar='path',
        dest='mysql_logsdir',
    )


mysql_proc = factories.mysql_proc()
mysql = factories.mysql('mysql_proc')
