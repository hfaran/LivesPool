`Lives Pool`
================
[![Build Status](https://travis-ci.org/hfaran/LivesPool.png)](https://travis-ci.org/hfaran/LivesPool)
[![Coverage Status](http://coveralls.io/repos/hfaran/LivesPool/badge.png?branch=master)](https://coveralls.io/r/hfaran/LivesPool?branch=master)
[![Stories in Ready](https://badge.waffle.io/hfaran/LivesPool.png?label=in_progress)](https://waffle.io/hfaran/LivesPool)


## Getting Started
```bash
./install.bash
src/cutthroats.py
# Visit localhost:9700
```

## Running with ``supervisord``
```bash
# If supervisord isn't already going, start it
supervisord -c supervisord.conf
# We can use the following commands to get status, start, stop, restart
supervisorctl status
supervisorctl start all
supervisorctl restart all
supervisorctl stop all
# These commands must all be run from the root directory
```

## Running Tests

### Back-end tests
```bash
./runtests.bash
```

### Front-end tests

Front-end functional tests literally use `supervisorctl` to start the server to talk to.
Therefore, you must have LivesPool "installed" already (i.e., have run `install.bash`).

Additionally, manually sign up a user with username "test" and password "test".

```bash
# Must be run from the root directory of the repository
src/tests/frontend_test.py
```

## API Documentation
* [Markdown](https://github.com/hfaran/LivesPool/blob/master/docs/API_Documentation.md)
* [HTML](http://hfaran.github.io/LivesPool/API_Documentation/)
