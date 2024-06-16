import os
import pprint
import sys

# Directory to store aliases files
ALIASES_DIR = os.path.expanduser("~/.aliasify")
ALIASES_FILE = os.path.join(ALIASES_DIR, "aliasify")
CONFIGS_FILE = os.path.join(ALIASES_DIR, "configs.yml")
PROFILE_FILES = [os.path.expanduser("~/.bashrc"), os.path.expanduser("~/.zshrc")]

LOG_OUTPUT = True


def dd(*args):
    """
     Dump the contents of multiple variables and stop script execution.
     :param args: Any number of Python variables to be dumped
     """
    for arg in args:
        pprint.pprint(arg)
        print()  # Add a newline for better readability between dumps
    sys.exit()


def die():
    sys.exit()


# Specify what gets imported with *
__all__ = [
    'ALIASES_DIR',
    'ALIASES_FILE',
    'CONFIGS_FILE',
    'PROFILE_FILES',
    'LOG_OUTPUT',
    'dd',
    'die'
]
