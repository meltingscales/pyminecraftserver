"""
This demo shows you how to use Python code to set up minecraft servers.
"""

import os

from config import *
from pyminecraftserver.MinecraftServer import MinecraftServer

if __name__ == '__main__':

    file_dir = os.path.dirname(__file__)

    # Don't want to delete people's stuff -- hardcoded path.
    minecraft_server = MinecraftServer(
        name='Volcano Block 1.0.28',
        server_path=os.path.join(base_dir, 'servers', 'example_server_setup', 'from_code-Volcano-Block'))

    print(minecraft_server)

    # If forge server is not installed,
    if not minecraft_server.is_forge_server_installed():
        # Install a modpack from a URL.
        minecraft_server.install_modpack_zip_from_url(
            'https://www.curseforge.com/minecraft/modpacks/volcano-block/download/2786736/file')

    # Install mods from URLs.
    minecraft_server.install_mods_from_urls([
        'https://www.curseforge.com/minecraft/mc-mods/dynmapforge/download/2722448/file',
        'https://www.curseforge.com/minecraft/mc-mods/morpheus/download/2664449/file',
    ])

    print(minecraft_server)

    # Now let's modify the server properties a bit!
    minecraft_server.set_server_properties('pvp', "false")
    minecraft_server.set_server_properties('max-players', "4")
    minecraft_server.set_server_properties('motd', 'Volcano Block set up with Python!')

    minecraft_server.run_forge_server_graphical()
