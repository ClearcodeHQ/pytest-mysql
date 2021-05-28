class NoopMySQLExecutor:
    def __init__(
        self,
        user,
        host,
        port,
    ):
        self.user = user
        self.host = host
        self.port = port
        self.unixsocket = None

    def running(self):
        """Check if process is running."""
        return True

    def __enter__(self):
        """Dummy enter method."""
        pass

    def __exit__(self, *args, **kwargs):
        """Dummy exit method."""
        pass
