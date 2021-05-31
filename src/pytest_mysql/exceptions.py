class PytestMySQLException(Exception):
    """Base plguin's exceptions"""


class MySQLUnsupported(PytestMySQLException):
    """Exception raised when an unsupported MySQL has been encountered."""


class VersionNotDetected(PytestMySQLException):
    """Exception raised when exector could not detect mysqls' version."""

    def __init__(self, output):
        """Create error message."""
        super().__init__("Could not detect version in {}".format(output))


class DatabaseExists(PytestMySQLException):
    """Raise this exception, when the database already exists"""
