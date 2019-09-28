"""
This demo shows you how to use JSON files to set up minecraft servers.
"""

import os

from pyminecraftserver.MinecraftServer import MinecraftServer

if __name__ == '__main__':
    file_dir = os.path.dirname(__file__)

    minecraft_server = MinecraftServer.from_json(
        server_path=os.path.join(file_dir, 'persistent', 'example_server_setup_from_json'),
        json_path='./modpack-config/Volcano-Block-1.0.28/volcano_block_modpack.json'
    )

    print(minecraft_server)
