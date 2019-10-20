import os
import shutil
import unittest

from pyminecraftserver.MinecraftServer import MinecraftServer


class TestSimpleSetupFromJSON(unittest.TestCase):

    def setUp(self) -> None:
        if os.path.exists('./tmp'):
            shutil.rmtree('./tmp')
        else:
            os.mkdir('./tmp')

    def tearDown(self) -> None:
        if os.path.exists('./tmp'):
            shutil.rmtree('./tmp')

    def testGlacial(self):

        minecraft_server = MinecraftServer.from_json(
            server_path=os.path.join('tmp', 'testcase-glacial-awakening'),
            json_path='../modpack-config/glacial-awakening.json'
        )

        self.assertTrue(minecraft_server.is_forge_server_installed())
