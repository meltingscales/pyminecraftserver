[![forthebadge](https://forthebadge.com/images/badges/made-with-crayons.svg)](https://forthebadge.com)

[![Build Status](https://travis-ci.org/HenryFBP/pyminecraftserver.svg?branch=master)](https://travis-ci.org/HenryFBP/pyminecraftserver)

[![Coverage Status](https://coveralls.io/repos/github/HenryFBP/pyminecraftserver/badge.svg)](https://coveralls.io/github/HenryFBP/pyminecraftserver)

# pyminecraftserver

This is a Python module to automate the process of setting up, configuring, and installing mods to minecraft servers.

## Issues

This works on Windows 10, OSX, and Ubuntu Linux AFAIK. See build status (travis badge at top)/`travis.yml` for setup and logs.

## Setup

Install Python 3.

Install `pipenv` by running `pip install pipenv`.

Then, run `pipenv install` in this directory to create a new virtualenv with all of the deps specified in `./Pipfile`.

`pipenv install --dev` to install development packages as well like `coverage`.

You can also run `pipenv install --system` to install the dependencies globally.

Then, run `pipenv shell` to run Python with the virtualenv's packages.

## Running tests

Run `python -m unittest discover` to run the test cases.

Alternatively, use `coverage run -m unittest discover` to run with coverage.

## Demos

`cd` into `demo/`.

Run `simple_server_setup_demo.py`, `simple_json_server_setup_demo.py` or `interactive-server-starter.py` for a taste of 
how this library can work.

I highly recommend `interactive-server-starter.py`.

## Troubleshooting

### Windows Path Length Limit

Because Windows&trade;, you may need to enable paths longer than 260 characters.

Yes, I know. That's very short.

See <https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file?redirectedfrom=MSDN#enable-long-paths-in-windows-10-version-1607-and-later> for advice on doing this.
