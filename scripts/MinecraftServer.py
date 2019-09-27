import os
import glob
import shutil
import time

import downloadlib
from typing import Union


class MinecraftServer:
    JAVA_NONMEM_FLAGS = '-XX:+UseG1GC -XX:+UnlockExperimentalVMOptions -XX:MaxGCPauseMillis=100 ' \
                        '-XX:+DisableExplicitGC -XX:TargetSurvivorRatio=90 -XX:G1NewSizePercent=50 ' \
                        '-XX:G1MaxNewSizePercent=80 -XX:G1MixedGCLiveThresholdPercent=35 -XX:+AlwaysPreTouch ' \
                        '-XX:+ParallelRefProcEnabled -Dusing.aikars.flags=mcflags.emc.gs '

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
        eula_content = None

        # read content
        with open(self.eula_path(), 'r') as f:
            eula_content = f.readlines()

        # replace false with true. This is illegal. Shh.
        for i in range(0, len(eula_content)):
            if 'false' in eula_content[i]:
                eula_content[i] = eula_content[i].replace('false', 'true')

        # Write content
        with open(self.eula_path(), 'w') as f:
            for line in eula_content:
                f.write(line)

    def run_forge_server(self):
        os.system('cd {path}; java {flags} -Xms2000M -Xmx2000M -jar {forge_jar}'.format(
            path=self.path,
            flags=self.JAVA_NONMEM_FLAGS,
            forge_jar=self.get_forge_server_path(),
        ))

    def install_forge_server(self):

        forge_location = self.get_forge_installer_path()

        os.system('cd {path}; java -jar {forgejar} --installServer'.format(
            path=self.path,
            forgejar=forge_location))

        # If the EULA does not exist, we must run the forge server once to accept it.
        if not os.path.exists(self.eula_path()):
            self.run_forge_server()
            self.accept_eula()


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

    mcs.accept_eula()
    mcs.run_forge_server()
