CHANGELOG
=========

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
