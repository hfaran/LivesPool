`Lives Pool`
================
[![Build Status](https://travis-ci.org/hfaran/LivesPool.png)](https://travis-ci.org/hfaran/LivesPool)
[![Coverage Status](http://coveralls.io/repos/hfaran/LivesPool/badge.png?branch=master)](https://coveralls.io/r/hfaran/LivesPool?branch=master)
[![Stories in Ready](https://badge.waffle.io/hfaran/LivesPool.png?label=ready)](https://waffle.io/hfaran/LivesPool)


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

### Future TODO
* Keep history
    * Currently, a lot of fields have a `current_` prefix; we should be storing data for completed games etc. for...;
    * A `Player` page where users can see past played games/stats/info etc.
* Tournament Mode (or something similar)
* Optionally registering with email to be able to restore your password etc.
* Coroutines/Celery/explore asynchronous things
