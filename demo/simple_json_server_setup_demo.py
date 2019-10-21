"""
This demo shows you how to use JSON files to set up minecraft servers.
"""

import os

from config import *
from pyminecraftserver.MinecraftServer import MinecraftServer

if __name__ == '__main__':

    minecraft_server = MinecraftServer.from_json(
        server_path=os.path.join(base_dir, 'servers', 'example_server_setup', 'from_json-glacial-awakening'),
        json_path=os.path.join(config_filepath, 'glacial-awakening.json')
    )

    print(minecraft_server)

    minecraft_server.run_forge_server_graphical()
