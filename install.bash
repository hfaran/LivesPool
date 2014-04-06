#!/bin/bash

# This script is meant to set up LivesPool quickly with a default config.
# It would probably be a good idea to explore some config option changes
#   before deploying.


LOGDIR="/var/log/cutthroat"
CONFDIR="/etc/cutthroat"
DATADIR="/var/lib/cutthroat"
ORIGUSER="$USER"


# Install any system packages (Ubuntu/Debian only) that are pre-requisites
echo -e "\n\nInstalling required system packages . . ."
sudo apt-get install gcc build-essential python-dev
sudo apt-get install python-setuptools
sudo apt-get install libffi-dev  # For python bcrypt package
# Install pip if required
if ! which pip; then
    sudo easy_install-2.7 pip
fi


# Install all required Python packages
echo -e "\n\nInstalled required Python packages with pip . . ."
sudo pip install -r requirements.txt

# Create log directory and give $USER access to the folder
sudo mkdir -p $LOGDIR
sudo chown -hR $ORIGUSER $LOGDIR
# Create config directory and give $USER access to the folder
sudo mkdir -p $CONFDIR
sudo chown -hR $ORIGUSER $CONFDIR
# Create data directory and give $USER access to the folder
sudo mkdir -p $DATADIR
sudo chown -hR $ORIGUSER $DATADIR
# Copy config file over to $CONFDIR
cp --no-clobber "config/cutthroat.conf" "${CONFDIR}/cutthroat.conf"
# For a quickstart; ideally the DB should be placed elsewhere
cp --no-clobber "starter.db" "${DATADIR}/cutthroat.db"


echo -e "\n\nBootstrapping complete."
