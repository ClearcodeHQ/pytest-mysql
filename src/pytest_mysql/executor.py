"""Specified MySQL Executor."""
import subprocess
from pkg_resources import parse_version

import re
from mirakuru import TCPExecutor


class MySQLUnsupported(Exception):
    """Exception raised when an unsupported MySQL has been encountered."""


class MySQLExecutor(TCPExecutor):
    """MySQL Executor for running MySQL server."""

    VERSION_RE = re.compile(r'(?:[a-z_ ]+)(Ver)? (?P<version>[\d.]+).*', re.I)
    IMPLEMENTATION_RE = re.compile(r'.*MariaDB.*')

    def __init__(
            self, mysqld_safe, mysqld, admin_exec, logfile_path,
            params, base_directory, user, host, port, timeout=60,
            install_db=None
    ):
        """
        Specialised Executor to run and manage MySQL server process.

        :param str mysqld_safe: path to mysqld_safe executable
        :param str mysqld: path to mysqld executable
        :param str admin_exec: path to mysqladmin executable
        :param str logfile_path: where the server shoyld wrute it's logs
        :param str params: string containing additional starting parameters
        :param path base_directory: base directory where the temporary files,
            database files, socket and pid will be placed in.
        :param str user: mysql user name
        :param str host: server's host
        :param int port: server's port
        :param int timeout: executor's timeout for start and stop actions
        :param int install_db:
        """
        self.mysqld_safe = mysqld_safe
        self.mysqld = mysqld
        self.install_db = install_db
        self.admin_exec = admin_exec
        self.base_directory = base_directory
        self.datadir = self.base_directory.mkdir(
            'mysqldata_{port}'.format(port=port)
        )
        self.pidfile = self.base_directory.join(
            'mysql-server.{port}.pid'.format(port=port)
        )
        self.unixsocket = self.base_directory.join(
            'mysql.{port}.sock'.format(port=port)
        )
        self.logfile_path = logfile_path
        self.user = user
        self._initialised = False
        command = '''
        {mysql_server} --datadir={datadir} --pid-file={pidfile}
        --port={port} --socket={socket} --log-error={logfile_path}
        --tmpdir={tmpdir} --skip-syslog {params}
        '''.format(
            mysql_server=self.mysqld_safe,
            port=port,
            datadir=self.datadir,
            pidfile=self.pidfile,
            socket=self.unixsocket,
            logfile_path=self.logfile_path,
            params=params,
            tmpdir=self.base_directory,
        )
        super(MySQLExecutor, self).__init__(
            command, host, port, timeout=timeout
        )

    def version(self):
        """Read MySQL's version."""
        version_output = subprocess.check_output(
            [self.mysqld, '--version']
        ).decode('utf-8')
        return self.VERSION_RE.match(version_output).groupdict()['version']

    def implementation(self):
        """Detect MySQL Implementation."""
        version_output = subprocess.check_output(
            [self.mysqld, '--version']
        ).decode('utf-8')
        if self.IMPLEMENTATION_RE.search(version_output):
            return 'mariadb'
        return 'mysql'

    def initialize_mysqld(self):
        """
        Initialise mysql directory.

        #. Remove mysql directory if exist.
        #. `Initialize MySQL data directory
            <https://dev.mysql.com/doc/refman/5.7/en/data-directory-initialization-mysqld.html>`_

        :param str mysql_init: mysql_init executable
        :param str datadir: path to datadir
        :param str base_directory: path to base_directory

        """
        if self._initialised:
            return
        init_command = (
            '{mysqld} --initialize-insecure '
            '--datadir={datadir} --tmpdir={tmpdir} '
            '--log-error={log}'
        ).format(
            mysqld=self.mysqld,
            datadir=self.datadir,
            tmpdir=self.base_directory,
            log=self.logfile_path
        )
        subprocess.check_output(init_command, shell=True)
        self._initialised = True

    def initialise_mysql_db_install(self):
        """
        Initialise mysql directory for older MySQL installations or MariaDB.

        #. Remove mysql directory if exist.
        #. `Initialize MySQL data directory
            <https://dev.mysql.com/doc/refman/5.7/en/data-directory-initialization-mysqld.html>`_

        :param str mysql_init: mysql_init executable
        :param str datadir: path to datadir
        :param str base_directory: path to base_directory

        """
        if self._initialised:
            return
        init_command = (
            '{mysql_init} --user={user} '
            '--datadir={datadir} --tmpdir={tmpdir}'
        ).format(
            mysql_init=self.install_db,
            user=self.user,
            datadir=self.datadir,
            tmpdir=self.base_directory,
        )
        subprocess.check_output(init_command, shell=True)
        self._initialised = True

    def start(self):
        """Trigger initialisation during start."""
        implementation = self.implementation()
        if implementation == 'mysql' and \
                parse_version(self.version()) > parse_version('5.7.6'):
            self.initialize_mysqld()
        elif implementation in ['mysql', 'mariadb']:
            if self.install_db:
                self.initialise_mysql_db_install()
            else:
                raise MySQLUnsupported('mysqld_init path is missing.')
        else:
            raise MySQLUnsupported(
                'Only MySQL and MariaDB servers are supported with MariaDB.'
            )
        super(MySQLExecutor, self).start()

    def shutdown(self):
        """Send shutdown command to the server."""
        shutdown_command = (
            '{admin} --socket={socket} --user={user} shutdown'
        ).format(
            admin=self.admin_exec,
            socket=self.unixsocket,
            user='root'
        )
        subprocess.check_output(shutdown_command, shell=True)

    def stop(self):
        """Stop the server."""
        self.shutdown()
        super(MySQLExecutor, self).stop()
