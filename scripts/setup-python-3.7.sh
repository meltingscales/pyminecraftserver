#!/usr/bin/env bash

sudo apt-get install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa --yes
sudo apt-get update

sudo apt-get install -y python3.7
python3.7 -m pip install pipenv

# Install pipenv packages
cd $SCRIPT_DIR
python3.7 -m pipenv install