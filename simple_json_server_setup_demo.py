"""
This demo shows you how to use JSON files to set up minecraft servers.
"""

import os

from pyminecraftserver.MinecraftServer import MinecraftServer

if __name__ == '__main__':
    file_dir = os.path.dirname(__file__)

    minecraft_server = MinecraftServer.from_json(
        server_path=os.path.join(file_dir, 'servers', 'example_server_setup_from_json-glacial-awakening'),
        json_path='./modpack-config/glacial-awakening.json'
    )

    print(minecraft_server)

    minecraft_server.run_forge_server_graphical()
