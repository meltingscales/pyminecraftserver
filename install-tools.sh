#!/usr/bin/env bash

# If java command does not exist, then install Java 8.
if ! hash java &>/dev/null; then
  sudo apt-add-repository ppa:webupd8team/java -y
  sudo apt-get update
  sudo apt-get install -y oracle-java8-installer
fi
