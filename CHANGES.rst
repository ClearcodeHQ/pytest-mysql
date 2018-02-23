CHANGELOG
=========

unreleased
-------

- [breaking] Add support for MySQL 5.7.6 and up. Drop support for older MySQL versions.
- [breaking] mysql_exec ini option replaced with mysql_mysqld_safe
- [breaking] --mysql-exec cmd option replaced with --mysql-mysqld-safe
- [breaking] dropped mysql_init ini option, --mysql-init cmd option
- [breaking] added mysql_mysqld option and --mysql-mysqld cmd option
- [enhancement] check mysql's version and raise exception on unsupported

1.1.1
-------

- [enhancements] removed path.py dependency

1.1.0
-------

- [enhancement] change deprecated getfuncargvalaue to getfixturevalues, require at least pytest 3.0.0

1.0.0
-------

- [enhancements] create command line and pytest.ini configuration options for mysql's log directory location
- [enhancements] create command line and pytest.ini configuration options for mysql's starting parametetrs
- [enhancements] create command line and pytest.ini configuration options for mysql test database name
- [enhancements] create command line and pytest.ini configuration options for mysql's user password
- [enhancements] create command line and pytest.ini configuration options for mysql user
- [enhancements] create command line and pytest.ini configuration options for mysql host
- [enhancements] create command line and pytest.ini configuration options for mysql port
- [enhancements] create command line and pytest.ini configuration options for mysql's init executable
- [enhancements] create command line and pytest.ini configuration options for mysql's admin executable
- [enhancements] create command line and pytest.ini configuration options for mysql executable
- [enhancements] create command line and pytest.ini configuration options for mysql logsdir
