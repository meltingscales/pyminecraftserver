#!/usr/bin/env bash

# If java command does not exist, then install Java 8.
if ! hash java &>/dev/null; then
  sudo apt-get update
  sudo apt-get install -y openjdk-8-jdk
fi

if ! hash unzip &>/dev/null; then
  sudo apt-get update
  sudo apt-get install unzip
fi