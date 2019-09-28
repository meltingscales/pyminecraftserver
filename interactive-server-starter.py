"""
This script is an interactive script that goes over all of your JSON server config files and lets you run them.
"""

import os
import pathlib

from pyminecraftserver.MinecraftServer import MinecraftServer

current_dir = os.path.dirname(__file__)
config_filepath = os.path.join(current_dir, 'modpack-config')

if __name__ == '__main__':

    json_filepaths = []
    for file in os.listdir(config_filepath):
        json_filepaths.append(os.path.join(config_filepath, file))

    print("Which JSON file would you like to start a server from?")

    i = 0
    for json_filepath in json_filepaths:
        print("{}) {}".format(i, os.path.basename(json_filepath)))
        i += 1

    choice = int(input(" > "))

    if choice >= len(json_filepaths) or choice < 0:
        raise Exception("Choice is out of range.")

    json_filepath = json_filepaths[choice]
    json_name = os.path.splitext(os.path.basename(json_filepath))[0]

    mcserver = MinecraftServer.from_json(
        server_path=os.path.join(current_dir, 'servers', 'interactive-server-starter', json_name),
        json_path=json_filepath
    )

    mcserver.run_forge_server_graphical()
