from setuptools import setup, Command
import subprocess
import shutil
import os

class GenerateCommand(Command):
    """A custom command to generate the executables using PyInstaller."""

    description = 'Generate single executable files using PyInstaller.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # Run PyInstaller command for Linux
        subprocess.call(['pyinstaller', '--onefile', '--distpath', './bin/linux', './src/aliasify.py'])

        # Remove the build directory
        shutil.rmtree('build', ignore_errors=True)

        # Remove the spec file
        os.remove('aliasify.spec')

        # Run PyInstaller command for macOS
        subprocess.call(['pyinstaller', '--onefile', '--distpath', './bin/macos', './src/aliasify.py'])

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
