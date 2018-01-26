"""Specified MySQL Executor."""
import subprocess

from mirakuru import TCPExecutor


class MySQLExecutor(TCPExecutor):
    """MySQL Executor for running MySQL server."""

    def __init__(
            self, mysqld_safe, mysqld, admin_exec, logfile_path,
            params, base_directory, user, host, port, timeout=60
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
        :param int timeut: executor's timeout for start and stop actions
        """
        self.mysqld_safe = mysqld_safe
        self.mysqd = mysqld
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

    def initialize(self):
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
        init_directory = (
            self.mysqd,
            '--initialize-insecure',
            '--datadir=%s' % self.datadir,
            '--tmpdir=%s' % self.base_directory,
            '--log-error=%s' % self.logfile_path,
        )
        subprocess.check_output(' '.join(init_directory), shell=True)
        self._initialised = True

    def start(self):
        """Trigger initialisation during start."""
        self.initialize()
        super(MySQLExecutor, self).start()

    def shutdown(self):
        """Send shutdown command to the server."""
        shutdown_server = (
            self.admin_exec,
            '--socket=%s' % self.unixsocket,
            '--user=%s' % self.user,
            'shutdown'
        )
        subprocess.check_output(' '.join(shutdown_server), shell=True)

    def stop(self):
        """Stop the server."""
        self.shutdown()
        super(MySQLExecutor, self).stop()
