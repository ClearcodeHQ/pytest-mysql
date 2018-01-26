"""Specified MySQL Executor."""
from mirakuru import TCPExecutor


class MySQLExecutor(TCPExecutor):
    """MySQL Executor for running MySQL server."""

    def __init__(
            self, mysqld_safe, datadir, pidfile, unixsocket, logfile_path,
            params, tmpdir, host, port, timeout=60
    ):
        """Specialised Executor to run and manage MySQL server process."""
        self.mysqld_safe = mysqld_safe
        self.datadir = datadir
        self.pidfile = pidfile
        self.unixsocket = unixsocket
        self.logfile_path = logfile_path
        self.tmpdir = tmpdir
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
