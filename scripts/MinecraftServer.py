import os
import glob
import shutil
import time

import downloadlib
from typing import Union


class MinecraftServer:

    def delete(self):

        print("About to delete '{}'...".format(self.path))

        shutil.rmtree(self.path)

    def download_forge_installer(self, url):

        forge_response = downloadlib.get_results_from_url_cached(url)

        forge_file_path = os.path.join(self.path, os.path.basename(url))

        downloadlib.save_response_to_file(forge_response, forge_file_path)

    def get_forge_installer_path(self) -> Union[str, None]:
        results = glob.glob(os.path.join(self.path, "forge-*-installer.jar"))

        if len(results) == 0:
            return None

        if len(results) > 1:
            raise Exception("Multiple forge installers installed?", results)

        return results[0]

    def get_forge_server_path(self) -> Union[str, None]:
        results = glob.glob(os.path.join(self.path, "forge-*-universal.jar"))

        if len(results) == 0:
            return None

        if len(results) > 1:
            raise Exception("Multiple forge servers installed?", results)

        return results[0]

    def is_forge_server_installed(self):
        return self.get_forge_server_path() is not None

    def is_forge_installer_installed(self):
        return self.get_forge_installer_path() is not None

    def __init__(self, path: str):
        self.path = os.path.abspath(path)

        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def eula_path(self):
        return os.path.join(self.path, 'eula.txt')

    def accept_eula(self):
        raise NotImplementedError

    def run_forge_server(self):
        pass

    def install_forge_server(self):

        forge_location = self.get_forge_installer_path()

        os.chdir(self.path)
        os.system('java -jar {} --installServer'.format(forge_location))


if __name__ == '__main__':

    # Don't want to delete my shit. hardcoded path.
    mcs = MinecraftServer(path='/media/henryfbp/media/GitHub/Modded-Forge-Vagrant/persistent/server/')

    print(mcs)

    print("Forge dir: {}".format(mcs.get_forge_server_path()))

    if not mcs.is_forge_installer_installed():
        mcs.download_forge_installer(
            'https://files.minecraftforge.net/maven/net/minecraftforge/forge/'
            '1.12.2-14.23.5.2846/forge-1.12.2-14.23.5.2846-installer.jar')

    if not mcs.is_forge_server_installed():
        mcs.install_forge_server()
