"""Module containing Noop executor."""


class NoopMySQLExecutor:
    """
    Noop Executor.

    Used to mimic in necessary scope the MySQL executor inside fixtures.
    """

    def __init__(
        self,
        user,
        host,
        port,
    ):
        """Initialize NoopMySQLExecutor."""
        self.user = user
        self.host = host
        self.port = port
        self.unixsocket = None

    def running(self):
        """Check if process is running."""
        return True

    def __enter__(self):
        """Do nothing enter method."""
        pass

    def __exit__(self, *args, **kwargs):
        """Do nothing exit method."""
        pass
