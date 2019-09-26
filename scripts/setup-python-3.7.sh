#!/usr/bin/env bash

if ! hash python3.7 ; then

    echo "python 3.7 doesn't exist. installing..."

    rm -rf /tmp/py3.7
    mkdir /tmp/py3.7 -p
    pushd /tmp/py3.7

    # Prepare to install py3.7
    sudo apt update
    sudo apt-get install -y libffi-dev libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev openssl

    # DL source
    wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tar.xz

    # Unzip
    tar -xf $(ls Python-*.tar.xz)

    # Go into source
    pushd Python-3.7.4

    #Config
    ./configure

    exit 1 #TODO debug remove this

    # Install
    sudo make && sudo make install

    # Set defaults for commands
    sudo update-alternatives --set python /usr/bin/python3.7
    sudo update-alternatives --set pip /usr/local/bin/pip3.7

    python3.7 -m pip install pipenv

    # Install pipenv packages
    pushd "$SCRIPT_DIR"
    python3.7 -m pipenv install
    popd

    popd

    popd
fi
