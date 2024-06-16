import subprocess
import os
import sys
import click
from assets.alerts import *
from assets.assets import *
from configs import load_configs
from crud import source_shell_profile
from configs import create_configs_file_if_not_exist, ask_for_dotfiles_repository_path, ask_for_default_dotfiles_branch


def sync_aliasify(direction):
    sync_messages = {
        "local-to-remote": "You are about to sync your local aliases file with your remote Dotfiles Repository.\nThis will overwrite the remote file with your local changes.",
        "remote-to-local": "You are about to sync your remote aliases file to your local system.\nThis will overwrite your local file with the remote changes."
    }

    info(sync_messages[direction])

    if click.confirm('Do you want to continue?', abort=False, default=True):
        if type == 'local-to-remote':
            sync_local_to_remote()
        else:
            sync_remote_to_local()


def sync_local_to_remote():
    """ Local -> Remote """
    prepare_to_sync()

    configs = load_configs()
    dotfiles_path = configs['dotfiles_path']
    branch = configs['dotfiles_default_branch']

    # Change the directory to the dotfiles path
    os.chdir(os.path.expanduser(dotfiles_path))

    # Check the git status before any action!
    check_git_status()

    sweet_info(' - Syncing to Remote Repository, Please wait ...')

    result = subprocess.run(['cp', os.path.expanduser('~/.aliasify/aliasify'), dotfiles_path], capture_output=True,
                            text=True)

    if result.returncode == 0:
        sweet_info(' - Copied Successfully')
    else:
        error('something went wrong.')
        return

    try:
        result = run_git_command(f'git pull origin {branch}')

        if result is None or result.returncode != 0:
            error('Failed to sync, something went wrong!')
            die()

        # After copy the aliases into dotfiles directory
        # the working directory now must be contained the updates
        # git status --porcelain check if we've files or dirs in working directory
        # now we can add, commit and push
        # Otherwise, it means almost that aliasify is copied but with same content which means no difference there!
        if subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True).stdout.strip():
            run_git_command('git add .')
            run_git_command('git commit -m "Synced aliasify from local to remote repository."')
            run_git_command('git add .')
            run_git_command('git push origin ' + branch)

            success(' - Pushed Successfully, Your DotFiles is now up to date!')
        else:
            success(' - It seemed that you already synced with your Remote Dotfiles Repository.')
    except Exception as exc:
        error(f"Failed to sync aliasify from local to remote repository: {exc}")


def sync_remote_to_local():
    """ Local <- Remote """
    prepare_to_sync()

    configs = load_configs()
    dotfiles_path = configs['dotfiles_path']
    branch = configs['dotfiles_default_branch']
    aliasify_source_path = dotfiles_path + '/aliasify'
    aliasify_destination_path = os.path.expanduser('~/.aliasify/aliasify')
    previous_dir = os.environ.get('PWD')

    # Change the directory to the dotfiles path
    os.chdir(os.path.expanduser(dotfiles_path))

    sweet_info(' - Syncing The Remote Repository to your local, Please wait ...')

    # Check the git status before any action!
    check_git_status()

    sweet_info(' - Pulling Dotfiles ...')

    # Start Pulling Operation
    try:
        result = run_git_command(f'git pull origin {branch}')

        if result is None or result.returncode != 0:
            error('Failed to sync, something went wrong!')
            die()

        # Copy the newest dotfiles
        result = subprocess.run(['cp', aliasify_source_path, aliasify_destination_path], capture_output=True, text=True)

        # Refresh the current shell session to take effects.
        # Return to the previous working directory if it exists
        if result.returncode == 0:
            if previous_dir:
                os.chdir(previous_dir)
                success(' - Synced Successfully. Your local is now up to date.')
                source_shell_profile()
        else:
            error('Failed to sync, something went wrong!')
            die()

    except Exception as exc:
        error(f"Failed to Pull dotfiles : {exc}")


def prepare_to_sync():
    sweet_info(' - Preparing ...')

    create_configs_file_if_not_exist()
    ask_for_dotfiles_repository_path()
    ask_for_default_dotfiles_branch()


def check_git_status():
    try:
        # Execute git status command
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)

        # Check if there are changes in the working directory
        if result.stdout.strip():
            error(' - Sorry, Your dotfiles Repository has uncommitted changes. Sync aborted to save work.')

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
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{command}': {e.stderr}")
        return None
