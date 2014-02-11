`Lives Pool`
================

## Getting Started
    ./install.bash
    ./cutthroats.py
    # Visit localhost:8888

## TODO

* ~~Finish implementing Room routes~~
* ~~Auth~~
    * ~~Implement basic API authentication and auth-based actions~~ 
    * ~~Use some kind of hashing/salting~~
* Documentation
    * Document any undocumented functions
* Front-end
    * [Wireframe draft](http://sdrv.ms/NiHL7a)
* Write new database module; refactor API to use it
* Tests
    * Back-end unittests
    * API functional tests
    * Front-end tests
* Keep history
    * Currently, a lot of fields have a `current_` prefix; we should be storing data for completed games etc. for...;
    * A `Player` page where users can see past played games/stats/info etc.
* Optionally registering with email to be able to restore your password etc.
* Coroutines/Celery/explore asynchronous things
