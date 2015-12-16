import os
import sys

_THIS_DIR_NAME = os.path.dirname(__file__)
_THIS_DIR_ABS_PATH = os.path.realpath(_THIS_DIR_NAME)
sys.path.append(_THIS_DIR_ABS_PATH)

_PATH_TO_RANDOM_GENERATOR_DIR = os.path.join(_THIS_DIR_ABS_PATH, '..').join('randomgenerator')
sys.path.append(_PATH_TO_RANDOM_GENERATOR_DIR)