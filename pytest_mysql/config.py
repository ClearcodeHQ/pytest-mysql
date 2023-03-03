def get_config(request):
    """Return a dictionary with config options."""
    config = {}
    options = [
        "mysqld",
        "mysqld_safe",
        "admin",
        "host",
        "port",
        "user",
        "passwd",
        "dbname",
        "params",
        "logsdir",
        "install_db",
    ]
    for option in options:
        option_name = "mysql_" + option
        conf = request.config.getoption(option_name) or request.config.getini(
            option_name
        )
        config[option] = conf
    return config
