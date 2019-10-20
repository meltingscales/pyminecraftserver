import os
import shutil
import unittest


class TestCaseWithEphemeralTempDir(unittest.TestCase):
    temp_dir = os.path.join(os.path.dirname(__file__), 'tmp')

    def setUp(self) -> None:
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        else:
            os.mkdir(self.temp_dir)

    def tearDown(self) -> None:
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
