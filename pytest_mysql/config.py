"""Config module."""

from pathlib import Path
from typing import Any, TypedDict

from pytest import FixtureRequest


class MySQLConfigType(TypedDict):
    """Configuration type dict."""

    mysqld: Path
    mysqld_safe: Path
    admin: str
    host: str
    port: str
    user: str
    passwd: str
    dbname: str
    params: str
    logsdir: str
    install_db: str


def get_config(request: FixtureRequest) -> MySQLConfigType:
    """Return a dictionary with config options."""

    def get_conf_option(option: str) -> Any:
        option_name = "mysql_" + option
        return request.config.getoption(option_name) or request.config.getini(option_name)

    config: MySQLConfigType = {
        "mysqld": Path(get_conf_option("mysqld")),
        "mysqld_safe": Path(get_conf_option("mysqld_safe")),
        "admin": get_conf_option("admin"),
        "host": get_conf_option("host"),
        "port": get_conf_option("port"),
        "user": get_conf_option("user"),
        "passwd": get_conf_option("passwd"),
        "dbname": get_conf_option("dbname"),
        "params": get_conf_option("params"),
        "logsdir": get_conf_option("logsdir"),
        "install_db": get_conf_option("install_db"),
    }
    return config
