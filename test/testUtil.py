import unittest

from pyminecraftserver.MinecraftServer import get_fileid_from_curseurl, get_modname_from_curseURL


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(
            get_fileid_from_curseurl("https://www.curseforge.com/minecraft/mc-mods/waystones/files/2734498"), '2734498')

        self.assertEqual(
            get_modname_from_curseURL('https://www.curseforge.com/minecraft/mc-mods/waystones/files/2734498'),
            'waystones')

        self.assertEqual(get_modname_from_curseURL('https://www.curseforge.com/minecraft/potatoes/rotatoes/'), None)


class ExampleTestCase(unittest.TestCase):
    def testNotGoingNuts(self):
        self.assertTrue(True)
