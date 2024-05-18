from setuptools import setup, Command
import subprocess
import shutil
import os

class GenerateCommand(Command):
    """A custom command to generate the executable using PyInstaller."""

    description = 'Generate a single executable file using PyInstaller.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # Run PyInstaller command
        subprocess.call(['pyinstaller', '--onefile', '--distpath', './bin', './src/aliasify.py'])

        # Remove the build directory
        shutil.rmtree('build', ignore_errors=True)

        # Remove the spec file
        os.remove('aliasify.spec')

setup(
    name='aliasify',
    version='1.0',
    # other setup options...
    cmdclass={
        'generate': GenerateCommand,
    },
    entry_points={
        'console_scripts': [
            'generate = aliasify.module:main',  # Adjust this to your package/module
        ],
    },
)
