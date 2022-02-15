CHANGELOG
=========

2.3.1
----------

Bugs
++++

- Now will accept correctly database names with hyphen

2.3.0
----------

Features
++++++++

- Import FixtureRequest from pytest, not private _pytest.
  Require at least pytest 6.2
- Replace tmpdir_factory with tmp_path_factory

Docs
++++

- List mysql_noproc in README's fixtures list

Fixes
+++++

- Database cleanup code will attempt to reconnect to mysql if test accidentally would close the connection

2.2.0
----------

Feature
+++++++

- add `user` option to setup and tear down mysql process as non-privileged

Misc
++++

- Add Python 3.10 to CI

2.1.0
----------

Feature
+++++++

- `mysql_noproc` fixture to connect to already running mysql server
- raise more meaningful error when the test database already exists

Misc
++++

- rely on `get_port` functionality delivered by `port_for`


Deprecation
+++++++++++

- Deprecated `mysql_logsdir` ini configuration and `--mysql-logsdir` command option
- Deprecated `logs_prefix` process fixture factory setting

Misc
++++

- Require minimum python 3.7
- Migrate CI to Github Actions

2.0.3
-------

- [enhancement] Do not assume that mysql executables are in /usr/bin

2.0.2
-------

- [enhancement] Preemptively read data after each test in mysql client fixture.
  This will make test run if the test itself forgot to fetch queried data.
- [enhnacement] Require at least mirakuru 2.3.0 - forced by changed stop method parameters change

2.0.1
-------

- [fix] Improved mysql version detection on osx
- [build] extracted xdist into separate stage on travis
- [build] have deployemt as separate stage on travis

2.0.0
-------

- [Enhancements] Add support for MySQL 5.7.6 and up with new configuration options. Legacy configuration supports older MySQL and MariaDB databases.
- [breaking] mysql_exec ini option replaced with mysql_mysqld_safe
- [breaking] --mysql-exec cmd option replaced with --mysql-mysqld-safe
- [breaking] replaced mysql_init ini option with mysql_install_db
- [breaking] replaced --mysql-init cmd option with --mysql-install-db 
- [breaking] added mysql_mysqld option and --mysql-mysqld cmd option

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
