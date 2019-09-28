"""
This demo shows you how to use Python code to set up minecraft servers.
"""

import os

from pyminecraftserver.MinecraftServer import MinecraftServer

if __name__ == '__main__':

    file_dir = os.path.dirname(__file__)

    # Don't want to delete people's stuff -- hardcoded path.
    minecraft_server = MinecraftServer(
        name='Volcano Block 1.0.28',
        server_path=os.path.join(file_dir, 'persistent', 'example_server_setup_from_code'))

    print(minecraft_server)

    # If forge server is not installed,
    if not minecraft_server.is_forge_server_installed():
        # Install a modpack from a URL.
        minecraft_server.install_modpack_zip_from_url(
            'https://www.curseforge.com/minecraft/modpacks/volcano-block/download/2786736/file')

    # Install mods from a URL.
    minecraft_server.install_mod_from_url(  # dynmap
        'https://www.curseforge.com/minecraft/mc-mods/dynmapforge/download/2722448/file')

    minecraft_server.run_forge_server_graphical()
