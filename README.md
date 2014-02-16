`Lives Pool`
================
[![Build Status](https://travis-ci.org/hfaran/LivesPool.png)](https://travis-ci.org/hfaran/LivesPool)
[![Coverage Status](http://coveralls.io/repos/hfaran/LivesPool/badge.png?branch=master)](https://coveralls.io/r/hfaran/LivesPool?branch=master)


## Getting Started
```bash
./install.bash
src/cutthroats.py
# Visit localhost:8888
```

## Running Tests
```bash
./runtests.bash
```

## TODO

* ~~Finish implementing Room routes~~
* ~~Auth~~
    * ~~Implement basic API authentication and auth-based actions~~
    * ~~Use some kind of hashing/salting~~
* Documentation
    * Document any undocumented functions
* Front-end
    * ~~[Wireframe draft](http://sdrv.ms/NiHL7a)~~
    * ~~Sign-in views~~
    * ~~Room views~~
    * Game views
* Write new database module; refactor API to use it
    * ~~DBObjectMapping~~
    * Refactor code out of `db` into `db2` and the RequestHandlers
* Tests
    * Back-end unittests
    * ~~API functional tests; 90%+ coverage;~~
    * Front-end tests

### Future TODO
* Keep history
    * Currently, a lot of fields have a `current_` prefix; we should be storing data for completed games etc. for...;
    * A `Player` page where users can see past played games/stats/info etc.
* Tournament Mode (or something similar)
* Optionally registering with email to be able to restore your password etc.
* Coroutines/Celery/explore asynchronous things
