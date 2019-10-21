import os
import sys

current_dir = os.path.dirname(__file__)
base_dir = os.path.join(current_dir, '..')
config_filepath = os.path.join(base_dir, 'modpack-config')

sys.path.append(os.path.join(current_dir, ".."))
