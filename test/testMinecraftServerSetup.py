import os
import shutil
import time
import unittest

from pyminecraftserver.MinecraftServer import MinecraftServer
from test import config_dir
from test.sharedTest import TestCaseWithEphemeralTempDir


class TestSimpleSetupFromJSON(TestCaseWithEphemeralTempDir):

    def testGlacial(self):
        minecraft_server = MinecraftServer.from_json(
            server_path=os.path.join(self.temp_dir, 'testcase-glacial-awakening'),
            json_path=os.path.join(config_dir, 'glacial-awakening.json')
        )

        self.assertTrue(minecraft_server.is_forge_server_installed())

        self.assertTrue(os.path.exists(minecraft_server.get_eula_path()))

        # Start server, make sure it's running.
        minecraft_server.run_forge_server_headless()
        time.sleep(5)
        self.assertTrue(minecraft_server.is_running())
        print("Minecraft server is running.")

        # Stop it and make sure it is stopped.
        print("Trying to stop it...")
        minecraft_server.stop_politely(timeout=5)
        self.assertFalse(minecraft_server.is_running())
        print("It is stopped.")

