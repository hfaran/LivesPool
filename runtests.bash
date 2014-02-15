#!/bin/bash

cp "starter.db" "cutthroat_test.db"
nosetests --with-cov --cov-report term-missing --cov cutthroat src/cutthroat/tests/
#rm "cutthroat_test.db"
