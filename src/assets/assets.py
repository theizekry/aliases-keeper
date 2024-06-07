import os
import colorama

# Initialize colorama
colorama.init()

# Directory to store aliases files
ALIASES_DIR   = os.path.expanduser("~/.aliases_keeper")
ALIASES_FILE  = os.path.join(ALIASES_DIR, "aliasify")
CONFIGS_FILE  = os.path.join(ALIASES_DIR, "configs.yml")
PROFILE_FILES = [os.path.expanduser("~/.bashrc"), os.path.expanduser("~/.zshrc")]

LOG_OUTPUT = True


# Specify what gets imported with *
__all__ = [
    'ALIASES_DIR',
    'ALIASES_FILE',
    'CONFIGS_FILE',
    'PROFILE_FILES',
    'LOG_OUTPUT'
]