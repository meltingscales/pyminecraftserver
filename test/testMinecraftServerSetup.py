import os
import shutil
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
