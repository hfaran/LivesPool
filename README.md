`Lives Pool`
================
[![Build Status](https://travis-ci.org/hfaran/LivesPool.png)](https://travis-ci.org/hfaran/LivesPool)
[![Coverage Status](http://coveralls.io/repos/hfaran/LivesPool/badge.png?branch=master)](https://coveralls.io/r/hfaran/LivesPool?branch=master)
[![Stories in Ready](https://badge.waffle.io/hfaran/LivesPool.png?label=in_progress)](https://waffle.io/hfaran/LivesPool)


## Getting Started
```bash
./install.bash
src/cutthroats.py
# Visit localhost:8888
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
```bash
./runtests.bash
```

## API Documentation
* [Markdown](https://github.com/hfaran/LivesPool/blob/master/docs/API_Documentation.md)
* [HTML](http://hfaran.github.io/LivesPool/API_Documentation/)
