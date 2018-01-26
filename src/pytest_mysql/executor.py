"""Specified MySQL Executor."""
import subprocess

from mirakuru import TCPExecutor


class MySQLExecutor(TCPExecutor):
    """MySQL Executor for running MySQL server."""

    def __init__(
            self, mysqld_safe, mysqld, admin_exec,
            datadir, pidfile, unixsocket, logfile_path,
            params, tmpdir, user, host, port, timeout=60
    ):
        """Specialised Executor to run and manage MySQL server process."""
        self.mysqld_safe = mysqld_safe
        self.mysqd = mysqld
        self.admin_exec = admin_exec
        self.datadir = datadir
        self.pidfile = pidfile
        self.unixsocket = unixsocket
        self.logfile_path = logfile_path
        self.tmpdir = tmpdir
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
            tmpdir=self.tmpdir,
        )
        super(MySQLExecutor, self).__init__(
            command, host, port, timeout=timeout
        )

    def initialize(self):
        """
        Initialise mysql directory.

        #. Remove mysql directory if exist.
        #. `Initialize MySQL data directory
            <https://dev.mysql.com/doc/refman/5.0/en/mysql-install-db.html>`_

        :param str mysql_init: mysql_init executable
        :param str datadir: path to datadir
        :param str tmpdir: path to tmpdir

        """
        if self._initialised:
            return
        init_directory = (
            self.mysqd,
            '--initialize-insecure',
            '--datadir=%s' % self.datadir,
            '--tmpdir=%s' % self.tmpdir,
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
