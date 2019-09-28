import json
import glob
import os
import shutil
import tempfile
import time
import uuid
import zipfile
import psutil
from jproperties import Properties

from pyminecraftserver import DownloadLib
from typing import Union


def folders_in_path(path: str) -> int:
    i = 0

    for subpath in os.listdir(path):
        if os.path.isdir(os.path.join(path, subpath)):
            i += 1

    return i


def files_in_path(path: str) -> int:
    i = 0

    for subpath in os.listdir(path):
        if os.path.isfile(os.path.join(path, subpath)):
            i += 1

    return i


# Stolen from https://stackoverflow.com/questions/11210104/check-if-a-program-exists-from-a-python-script
def is_tool(name):
    """Check whether `name` is on PATH."""

    from distutils.spawn import find_executable

    return find_executable(name) is not None


def spawn_graphical_terminal(command: str):
    """    Spawn a graphical terminal and run a command in it.

    This will search for various tools like 'cmd' and 'gnome-terminal' and try to use ones that exist.
    """

    ensure_java_exists()

    if is_tool('gnome-terminal') and is_tool('bash'):
        cmd = '''gnome-terminal -- bash -c "{}; sleep 99999"  '''.format(command)

        os.system(cmd)
    elif is_tool('cmd'):
        cmd = ''' cmd.exe /K {} '''.format(command)

        os.system(cmd)
    else:
        raise NotImplementedError("Not implemented for this system.")


def ensure_java_exists(java_exe='java'):
    if not is_tool(java_exe):
        raise Exception("Could not find `{}` executable on the path.".format(java_exe))


def get_available_virtual_memory_in_mb() -> int:
    # bytes -> kb -> mb
    return int((psutil.virtual_memory().available / 1024) / 1024)


def get_minecraft_server_memory_in_mb(cap=8000):
    mem = get_available_virtual_memory_in_mb()

    if mem >= cap:
        return cap
    else:
        return mem


class MinecraftServer:
    JAVA_NONMEM_FLAGS = '-XX:+UseG1GC -XX:+UnlockExperimentalVMOptions -XX:MaxGCPauseMillis=100 ' \
                        '-XX:+DisableExplicitGC -XX:TargetSurvivorRatio=90 -XX:G1NewSizePercent=50 ' \
                        '-XX:G1MaxNewSizePercent=80 -XX:G1MixedGCLiveThresholdPercent=35 -XX:+AlwaysPreTouch ' \
                        '-XX:+ParallelRefProcEnabled -Dusing.aikars.flags=mcflags.emc.gs '

    # Prefix mods with this to make it obvious they're downloaded by the tool
    _mod_prefix = '_pyminecraft_'

    def get_mods_folder_path(self) -> str:
        return os.path.join(self.server_path, 'mods')

    def get_eula_path(self) -> str:
        return os.path.join(self.server_path, 'eula.txt')

    def get_properties_path(self) -> str:
        return os.path.join(self.server_path, 'server.properties')

    def get_properties(self) -> Properties:
        """
        :return: The properties file of this server.
        """

        p = Properties()

        with open(self.get_properties_path(), 'rb') as f:
            p.load(f, 'utf-8')

        return p

    def save_properties(self, p: Properties):

        with open(self.get_properties_path(), 'wb') as f:
            p.store(f, encoding='utf-8')

        return

    def get_memory_flags(self) -> str:
        return "-Xms{mb}M -Xmx{mb}M".format(mb=get_minecraft_server_memory_in_mb())

    def __str__(self):

        booltochar = {True: "x",
                      False: ' '}

        return """
        Minecraft Server '{mcservername}':
        PATH: '{path}'
        [{does_forge_installer_exist}] Forge installer downloaded: '{forge_installer_path}'
        [{is_forge_installed}] Forge jar installation: '{forge_server_path}'
        Java memory flags: '{mem_flags}'
        """.format(
            mcservername=self.name,
            path=self.server_path,
            does_forge_installer_exist=booltochar[self.is_forge_installer_downloaded()],
            forge_installer_path=self.get_forge_installer_path(),
            is_forge_installed=booltochar[self.is_forge_server_installed()],
            forge_server_path=self.get_forge_server_path(),
            mem_flags=self.get_memory_flags(),
        )

    def __init__(self, name: str, server_path: str):

        ensure_java_exists()

        self.name = name

        self.server_path = os.path.abspath(server_path)

        if not os.path.exists(self.server_path):
            os.makedirs(self.server_path)

    def set_server_properties(self, key, value):
        """Modify the server's 'server.properties' file."""
        prop = self.get_properties()

        prop[key] = value

        self.save_properties(prop)

    @classmethod
    def from_json(cls, server_path, json_path):
        """
        Given a JSON file and a server folder path, detect an MC server and attempt to set it up from that file.
        """

        with open(json_path, 'r') as f:
            json_data = json.load(f)

        server_name = json_data['name']

        mcserver = MinecraftServer(name=server_name, server_path=server_path)

        # If the forge server isn't installed,
        if not mcserver.is_forge_server_installed():

            # If the forge installer isn't downloaded,
            if not mcserver.is_forge_installer_downloaded():
                # Install modpack from a zip file.
                mcserver.install_modpack_zip_from_url(json_data['modpack_zip_url'])
            else:
                mcserver.install_forge_server()

        if 'mods' in json_data:
            mod_urls = json_data['mods']

            for name, url in mod_urls.items():
                mcserver.install_mod_from_url(url)

        return mcserver

    def get_base_temp_dir(self) -> str:
        return os.path.join(self.server_path, 'tmp')

    def generate_clean_temp_dir(self) -> str:
        """Make a new temporary directory and make sure it's empty."""

        tempdir = os.path.join(self.get_base_temp_dir())

        if os.path.exists(tempdir):
            shutil.rmtree(tempdir)

        os.makedirs(tempdir)

        return tempdir

    def delete(self):

        print("About to delete '{}'...".format(self.server_path))

        time.sleep(10)

        shutil.rmtree(self.server_path)

    def download_forge_installer(self, url):

        forge_response = DownloadLib.get_results_from_url(url)

        forge_file_path = os.path.join(self.server_path, DownloadLib.url_filename(url))

        DownloadLib.save_response_to_file(forge_response, forge_file_path)

    def get_forge_installer_path(self) -> Union[str, None]:
        results = glob.glob(os.path.join(self.server_path, "forge-*-installer.jar"))

        if len(results) == 0:
            return None

        if len(results) > 1:
            raise Exception("Multiple forge installers installed?", results)

        return results[0]

    def get_forge_server_path(self) -> Union[str, None]:
        results = glob.glob(os.path.join(self.server_path, "forge-*-universal.jar"))

        if len(results) == 0:
            return None

        if len(results) > 1:
            raise Exception("Multiple forge servers installed?", results)

        return results[0]

    def is_forge_server_installed(self):
        return self.get_forge_server_path() is not None

    def is_forge_installer_downloaded(self):
        return self.get_forge_installer_path() is not None

    def accept_eula(self):

        # read content
        with open(self.get_eula_path(), 'r') as f:
            eula_content = f.readlines()

        # replace false with true. This is illegal. Shh.
        for i in range(0, len(eula_content)):
            if 'false' in eula_content[i]:
                eula_content[i] = eula_content[i].replace('false', 'true')

        # Write content
        with open(self.get_eula_path(), 'w') as f:
            for line in eula_content:
                f.write(line)

        print("EULA accepted.")

    def get_forge_server_command(self) -> str:
        """Return a command that will run the Forge server."""
        return 'cd "{path}"; java {flags} {memflags} -jar "{forge_jar}"'.format(
            path=self.server_path,
            flags=self.JAVA_NONMEM_FLAGS,
            memflags=self.get_memory_flags(),
            forge_jar=self.get_forge_server_path(),
        )

    def run_forge_server_headless(self):
        """Runs the forge server in the current terminal. Non-interactive."""
        command = (self.get_forge_server_command())

        print(command)

        os.system(command)

    def run_forge_server_graphical(self):
        """Run the forge server in a new terminal window in a graphical environment."""
        spawn_graphical_terminal(self.get_forge_server_command())

    def install_forge_server(self):

        forge_location = self.get_forge_installer_path()

        os.system('cd {path}; java -jar {forgejar} --installServer'.format(
            path=self.server_path,
            forgejar=forge_location))

        # If the EULA does not exist, we must run the forge server once to accept it.
        if not os.path.exists(self.get_eula_path()):

            print("EULA does not exist. Running MC Forge headless once.")

            self.run_forge_server_headless()

        self.accept_eula()

    def install_modpack_zip_from_url(self, url):

        modpack_response = DownloadLib.get_results_from_url(url)

        tempdir = self.generate_clean_temp_dir()

        modpack_zip_temp_filepath = os.path.join(tempdir, DownloadLib.response_filename(modpack_response))

        modpack_unzipped_path = os.path.join(tempdir, 'unzipped')
        os.makedirs(modpack_unzipped_path)

        DownloadLib.save_response_to_file(modpack_response, modpack_zip_temp_filepath)

        print("Extracting to '{}'...".format(modpack_unzipped_path))
        with zipfile.ZipFile(modpack_zip_temp_filepath, 'r') as zip_ref:
            zip_ref.extractall(modpack_unzipped_path)
        print("Done!")

        folders = folders_in_path(modpack_unzipped_path)
        files = files_in_path(modpack_unzipped_path)

        print("{} folders, {} files from the zip file.".format(
            folders, files))

        if (folders is 1) and (files is 0):
            print("Installing in 'copy directory' mode because there is only one folder here.")

            modpack_files_path = glob.glob("{}/*".format(modpack_unzipped_path))

            if len(modpack_files_path) != 1:
                raise ValueError("Should be exactly one one folder in '{}'!".format(modpack_unzipped_path))

            self._install_modpack_copy_directory(modpack_files_path[0])

        else:
            raise NotImplemented(
                "Not implemented yet.",
                "I have not programmed this tool to be able to install this kind of modpack zip file structure yet.",
                "I only know how to install modpack zips that have a SINGLE FOLDER and ZERO FILES in them.",
                "Complain to me and let me know the modpack download link."
            )

        if not self.is_forge_server_installed():

            if self.is_forge_installer_downloaded():
                self.install_forge_server()
            else:
                # No installer and no forge, no way to run the server.
                raise Exception("Forge installer seems to be missing after installing a modpack!",
                                "You may need to install Forge BEFORE installing this modpack!")

    def _install_modpack_copy_directory(self, modpack_directory):
        """
        Install a modpack by copying all files from a directory into my server folder.
        :param modpack_directory:
        :return:
        """

        print(modpack_directory)

        for subpath in os.listdir(modpack_directory):
            print('copying "{}" to "{}"...'.format(subpath, self.server_path))

            abs_source_path = os.path.join(modpack_directory, subpath)
            abs_dest_path = os.path.join(self.server_path, subpath)

            if os.path.isfile(abs_source_path):
                shutil.copy(abs_source_path, abs_dest_path)
            else:
                shutil.copytree(abs_source_path, abs_dest_path)

    def install_mods_from_json_file(self, mods_list_json_path):

        with open(mods_list_json_path, 'r') as file:
            jsonobj: dict = json.load(file)

        if 'mods' not in jsonobj:
            raise ValueError("No key 'mods' in '{}'!".format(mods_list_json_path))

        for mod_name, url in jsonobj['mods'].items():
            self.install_mod_from_url(url)

    def install_mod_from_url(self, url: str):

        mod_response = DownloadLib.get_results_from_url(url)
        mod_filename = self._mod_prefix + DownloadLib.response_filename(mod_response)
        mod_filepath = os.path.join(self.get_mods_folder_path(), mod_filename)

        # If mod not downloaded,
        if not os.path.isfile(mod_filepath):
            print("[ DL ]", end='')
            DownloadLib.save_response_to_file(mod_response, mod_filepath)
        else:
            print("[ OK ]", end='')

        print(" '{}' at '{}'".format(mod_filename, mod_filepath))
