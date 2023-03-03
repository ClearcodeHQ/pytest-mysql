"""Specified MySQL Executor."""
import re
import subprocess
from pkg_resources import parse_version

from mirakuru import TCPExecutor

from pytest_mysql.exceptions import MySQLUnsupported, VersionNotDetected


class MySQLExecutor(TCPExecutor):
    """MySQL Executor for running MySQL server."""

    VERSION_RE = re.compile(r"(?:[a-z_ ]+)(Ver)? (?P<version>[\d.]+).*", re.I)
    IMPLEMENTATION_RE = re.compile(r".*MariaDB.*")

    def __init__(
        self,
        mysqld_safe,
        mysqld,
        admin_exec,
        logfile_path,
        params,
        base_directory,
        user,
        host,
        port,
        timeout=60,
        install_db=None,
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
        self.datadir = self.base_directory.mkdir(f"mysqldata_{port}")
        self.pidfile = self.base_directory.join(f"mysql-server.{port}.pid")
        self.unixsocket = str(self.base_directory.join(f"mysql.{port}.sock"))
        self.logfile_path = logfile_path
        self.user = user
        self._initialised = False
        command = (
            f"{self.mysqld_safe} "
            f"--datadir={self.datadir} "
            f"--pid-file={self.pidfile} "
            f"--port={port} "
            f"--socket={self.unixsocket} "
            f"--log-error={self.logfile_path} "
            f"--tmpdir={self.base_directory} "
            f"--skip-syslog {params}"
        )
        super().__init__(command, host, port, timeout=timeout)

    def version(self):
        """Read MySQL's version."""
        version_output = subprocess.check_output(
            [self.mysqld, "--version"]
        ).decode("utf-8")
        try:
            return self.VERSION_RE.search(version_output).groupdict()["version"]
        except AttributeError as exc:
            raise VersionNotDetected(version_output) from exc

    def implementation(self):
        """Detect MySQL Implementation."""
        version_output = subprocess.check_output(
            [self.mysqld, "--version"]
        ).decode("utf-8")
        if self.IMPLEMENTATION_RE.search(version_output):
            return "mariadb"
        return "mysql"

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
            f"{self.mysqld} --initialize-insecure "
            f"--datadir={self.datadir} --tmpdir={self.base_directory} "
            f"--log-error={self.logfile_path}"
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
            f"{self.install_db} --user={self.user} "
            f"--datadir={self.datadir} --tmpdir={self.base_directory}"
        )
        subprocess.check_output(init_command, shell=True)
        self._initialised = True

    def start(self):
        """Trigger initialisation during start."""
        implementation = self.implementation()
        if implementation == "mysql" and parse_version(
            self.version()
        ) > parse_version("5.7.6"):
            self.initialize_mysqld()
        elif implementation in ["mysql", "mariadb"]:
            if self.install_db:
                self.initialise_mysql_db_install()
            else:
                raise MySQLUnsupported("mysqld_init path is missing.")
        else:
            raise MySQLUnsupported(
                "Only MySQL and MariaDB servers are supported with MariaDB."
            )
        super().start()

    def shutdown(self):
        """Send shutdown command to the server."""
        shutdown_command = (
            f"{self.admin_exec} --socket={self.unixsocket} "
            f"--user={self.user} shutdown"
        )
        try:
            subprocess.check_output(shutdown_command, shell=True)
        except subprocess.CalledProcessError:
            # Fallback to using root user for shutdown
            shutdown_command = (
                f"{self.admin_exec} --socket={self.unixsocket} "
                f"--user=root shutdown"
            )
            subprocess.check_output(shutdown_command, shell=True)

    def stop(self, sig=None, exp_sig=None):
        """Stop the server."""
        self.shutdown()
        super().stop(sig, exp_sig)
