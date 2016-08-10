import os
import sys

_THIS_DIR_NAME = os.path.dirname(__file__)
_THIS_DIR_ABS_PATH = os.path.realpath(_THIS_DIR_NAME)
sys.path.append(_THIS_DIR_ABS_PATH)