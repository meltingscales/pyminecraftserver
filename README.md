# pyminecraftserver

This is a Python module to automate the process of setting up, configuring, and installing mods to minecraft servers.

## Setup

Install Python 3.

Install `pipenv` by running `pip install pipenv`.

Then, run `pipenv install` in this directory to create a new virtualenv with all of the deps specified in `./Pipfile`.

You can also run `pipenv install --system` to install the dependencies globally.

## Demos

Run `simple_server_setup_demo.py`, `simple_json_server_setup_demo.py` or `interactive-server-starter.py` for a taste of how this library can work.

I highly recommend `interactive-server-starter.py`.

## Troubleshooting

### Windows Path Length Limit

Because Windows&trade;, you may need to enable paths longer than 260 characters.

Yes, I know. That's short as hell.

See <https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file?redirectedfrom=MSDN#enable-long-paths-in-windows-10-version-1607-and-later> for advice on doing this.
