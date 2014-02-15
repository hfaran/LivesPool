#!/bin/bash

cp "starter.db" "cutthroat_test.db"
nosetests --with-cov --cov cutthroat src/cutthroat/tests/
rm "cutthroat_test.db"
