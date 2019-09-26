#!/usr/bin/env bash

# Make sure that a command exists.
# If not, install a package that provides it using apt.
# ARG1 is the command name that can determine if a package is installed.
# ARG2 is the package that needs to be installed.
#
function apt_ensure_exists() {
    local COMMAND_NAME="$1"
    local APT_PACKAGE_NAME="$2"

    if ! hash "$COMMAND_NAME" &> /dev/null; then
        sudo apt-get install -y "$APT_PACKAGE_NAME"
    else
        echo "${COMMAND_NAME} exists, not installing ${APT_PACKAGE_NAME}."
    fi
}

# If java command does not exist, then install Java 8.
apt_ensure_exists "java" "openjdk-8-jdk"
apt_ensure_exists "http" "httpie"

# Install deps from scripts dir.
pushd "$SCRIPT_DIR"
python3.7 -m pip install pipenv
python3.7 -m pipenv install --system
popd

apt_ensure_exists "unzip" "unzip"
apt_ensure_exists "tree" "tree"
apt_ensure_exists "bc" "bc"
apt_ensure_exists "htop" "htop"
apt_ensure_exists "lynx" "lynx"
apt_ensure_exists "jq" "jq"