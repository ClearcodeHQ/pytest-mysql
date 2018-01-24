"""Specified MySQL Executor."""
from mirakuru import TCPExecutor


class MySQLExecutor(TCPExecutor):
    """MySQL Executor for running MySQL server."""

    def __init__(
            self, mysqld_safe, datadir, pidfile, unixsocket, logfile_path,
            params, tmpdir, host, port, timeout=60
    ):
        """MySQL Executor for running and managing MySQL server process."""

        command = '''
        {mysql_server} --datadir={datadir} --pid-file={pidfile}
        --port={port} --socket={socket} --log-error={logfile_path}
        --tmpdir={tmpdir} --skip-syslog {params}
        '''.format(
            mysql_server=mysqld_safe,
            port=port,
            datadir=datadir,
            pidfile=pidfile,
            socket=unixsocket,
            logfile_path=logfile_path,
            params=params,
            tmpdir=tmpdir,
        )
        self.socket_path = unixsocket.strpath
        super(MySQLExecutor, self).__init__(
            command, host, port, timeout=timeout
        )
