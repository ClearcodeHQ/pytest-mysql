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
"""Client fixture factory for MySQL database."""

import pytest
import MySQLdb

from pytest_mysql.factories.process import get_config


def mysql(process_fixture_name, user=None, passwd=None, db=None,
          charset='utf8', collation='utf8_general_ci'):
    """
    Client fixture factory for MySQL server.

    Factory. Create connection to mysql. If you want you can give a scope,
    default is 'session'.

    For charset and collation meaning,
    see `Database Character Set and Collation
    <https://dev.mysql.com/doc/refman/5.5/en/charset-database.html>`_

    :param str process_fixture_name: process fixture name
    :param str user: mysql server user
    :param str passwd: mysql server's password
    :param str db: database's name
    :param str charset: MySQL characterset to use by default
        for *tests* database
    :param str collation: MySQL collation to use by default
        for *tests* database

    :returns: function ``mysql_fixture`` with suit scope
    :rtype: func
    """
    @pytest.fixture
    def mysql_fixture(request):
        """
        Client fixture for MySQL server.

        #. Get config.
        #. Try to import MySQLdb package.
        #. Connect to mysql server.
        #. Create database.
        #. Use proper database.
        #. Drop database after tests.

        :param FixtureRequest request: fixture request object

        :rtype: MySQLdb.connections.Connection
        :returns: connection to database
        """
        config = get_config(request)
        process = request.getfixturevalue(process_fixture_name)
        if not process.running():
            process.start()

        mysql_host = process.host
        mysql_user = user or config['user']
        mysql_passwd = passwd or config['passwd']
        mysql_db = db or config['dbname']

        unixsocket = process.socket_path

        mysql_conn = MySQLdb.connect(
            host=mysql_host,
            unix_socket=unixsocket,
            user=mysql_user,
            passwd=mysql_passwd,
        )

        mysql_conn.query(
            '''CREATE DATABASE {name}
            DEFAULT CHARACTER SET {charset}
            DEFAULT COLLATE {collation}'''
            .format(
                name=mysql_db, charset=charset, collation=collation
            )
        )
        mysql_conn.query('USE %s' % mysql_db)

        def drop_database():
            mysql_conn.query('DROP DATABASE IF EXISTS %s' % mysql_db)
            mysql_conn.close()

        request.addfinalizer(drop_database)

        return mysql_conn

    return mysql_fixture
