#!/bin/bash

# NOTE: Be sure to make equivalent changes in .travis.yml

cp "starter.db" "cutthroat_test.db"
nosetests --with-cov --cov-report term-missing --cov cutthroat src/tests/
# rm "cutthroat_test.db"
