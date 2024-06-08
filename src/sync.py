import subprocess
import os
import sys
from configs import create_configs_file_if_not_exist, ask_for_dotfiles_repository_path;
from assets.alerts import *;
import click

def syncAliasify(type):
    sync_messages = {
        "local-to-remote": "You are about to sync your local aliases file with your remote Dotfiles Repository.\nThis will overwrite the remote file with your local changes.",
        "remote-to-local": "You are about to sync your remote aliases file to your local system.\nThis will overwrite your local file with the remote changes."
    }

    info(sync_messages[type])

    if click.confirm('Do you want to continue?', abort=False, default=True):
        if type == 'local-to-remote':
            syncLocalToRemote()
        else:
            syncRemoteToLocal()


def syncLocalToRemote():
    dotfilesPath = prepareToSync()

    # Change the directory to the dotfiles path
    os.chdir(os.path.expanduser(dotfilesPath))

    # Check the git status before any action!
    check_git_status()

    sweetInfo("Syncing to Remote Repository, Please wait...")

    result = subprocess.run(['cp', os.path.expanduser('~/.aliasify/aliasify'), dotfilesPath], capture_output=True, text=True)

    if result.returncode == 0:
        sweetInfo(f"Copied Successfully to {dotfilesPath}.")
    else:
        error(f"Command '{command}' failed with return code {result.returncode}.")
        return;

    try:
        run_git_command('git pull origin master')

        # After copy the aliases into dotfiles directory
        # the working directory now must be contained the updates
        # git status --porcelain check if we've files or dirs in working directory
        # now we can add, commit and push
        # Otherwise, it means almost that aliasify is copied but with same content which means no difference there!
        if subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True).stdout.strip():
            run_git_command('git add .')
            run_git_command('git commit -m "Synced aliasify from local to remote repository."')
            run_git_command('git add .')
            run_git_command('git push origin master')
            success("Pushed Successfully, Your DotFiles is now up to date!")
        else:
            sweetInfo('It seemed that you already synced with your Remote Dotfiles Repository.')
    except Exception as exc:
        error(f"Failed to sync aliasify from local to remote repository: {exc}")


def syncRemoteToLocal():
    prepareToSync()


def prepareToSync():
    sweetInfo("Preparing to sync to remote repository...")
    create_configs_file_if_not_exist()
    return ask_for_dotfiles_repository_path()


def check_git_status():
    try:
        # Execute git status command
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)

        # Check if there are changes in the working directory
        if result.stdout.strip():
            warning("It seems you've some updates inside your repository! Your working directory is not clean.")
            info("Syncing operation will be aborted to save your work.")
            note("So, please check your repository status and make your working tree clean. then try again to Syncing.")

            # Return to the previous working directory if it exists
            previous_dir = os.environ.get('OLDPWD')
            if previous_dir:
                os.chdir(previous_dir)

            sys.exit(0)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while checking the git status: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


def run_git_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        # print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{command}': {e.stderr}")