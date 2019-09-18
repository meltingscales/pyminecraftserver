#!/usr/bin/env bash

sudo apt-get update

# If java command does not exist, then install Java 8.
if ! hash java &>/dev/null; then
  sudo apt-get install -y openjdk-8-jdk
fi

if ! hash unzip &>/dev/null; then
  sudo apt-get install unzip
fi

if ! hash bc &>/dev/null; then
    sudo apt-get install bc
fi