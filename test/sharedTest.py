import os
import shutil
import tempfile
import time
import unittest
import uuid


class TestCaseWithEphemeralTempDir(unittest.TestCase):
    temp_dir = tempfile.mkdtemp()
