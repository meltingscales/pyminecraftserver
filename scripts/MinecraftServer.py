import os
import glob
import shutil
import tempfile
import time
import zipfile

from downloadlib import *
from typing import Union


class MinecraftServer:
    JAVA_NONMEM_FLAGS = '-XX:+UseG1GC -XX:+UnlockExperimentalVMOptions -XX:MaxGCPauseMillis=100 ' \
                        '-XX:+DisableExplicitGC -XX:TargetSurvivorRatio=90 -XX:G1NewSizePercent=50 ' \
                        '-XX:G1MaxNewSizePercent=80 -XX:G1MixedGCLiveThresholdPercent=35 -XX:+AlwaysPreTouch ' \
                        '-XX:+ParallelRefProcEnabled -Dusing.aikars.flags=mcflags.emc.gs '

    def clean_temp_dir(self) -> str:
        """Make a new temporary directory and make sure it's empty."""

        tempdir = os.path.join(tempfile.gettempdir(), self.__class__.__name__, self.name)

        if os.path.exists(tempdir):
            shutil.rmtree(tempdir)

        os.makedirs(tempdir)

        return tempdir

    def delete(self):

        print("About to delete '{}'...".format(self.path))

        shutil.rmtree(self.path)

    def download_forge_installer(self, url):

        forge_response = get_results_from_url(url)

        forge_file_path = os.path.join(self.path, url_filename(url))

        save_response_to_file(forge_response, forge_file_path)

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

    def is_forge_installer_downloaded(self):
        return self.get_forge_installer_path() is not None

    def __init__(self, name: str, path: str):

        self.name = name

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

    def install_modpack_zip_from_url(self, url):

        modpack_response = get_results_from_url(url)

        tempdir = self.clean_temp_dir()

        modpack_zip_temp_filepath = os.path.join(tempdir, response_filename(modpack_response))

        modpack_unzipped_path = os.path.join(tempdir, 'unzipped')
        os.makedirs(modpack_unzipped_path)

        save_response_to_file(modpack_response, modpack_zip_temp_filepath)

        print("Extracting to '{}'...".format(modpack_unzipped_path))
        with zipfile.ZipFile(modpack_zip_temp_filepath, 'r') as zip_ref:
            zip_ref.extractall(modpack_unzipped_path)
        print("Done!")


if __name__ == '__main__':

    # Don't want to delete my shit. hardcoded path.
    mcs = MinecraftServer(
        name='volcano block',
        path='/media/henryfbp/media/GitHub/Modded-Forge-Vagrant/persistent/server/')

    print(mcs)

    print("Forge dir: {}".format(mcs.get_forge_server_path()))

    # If forge server is not installed,
    if not mcs.is_forge_server_installed():
        # Install a modpack from a URL.
        mcs.install_modpack_zip_from_url(
            'https://www.curseforge.com/minecraft/modpacks/volcano-block/download/2786736/file')
