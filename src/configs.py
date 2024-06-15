import yaml
import os
import click
from assets.assets import *
from assets.alerts import *;

def create_configs_file_if_not_exist():
    # Create an empty YAML file with an empty dictionary
    try:
        if not os.path.exists(CONFIGS_FILE):
            with open(CONFIGS_FILE, 'w') as file:
                yaml.safe_dump({}, file)
    except Exception as exc:
        error(f"Error creating YAML file: {exc}")


def ask_for_dotfiles_repository_path():
    configs = load_configs()

    # Check if dotfiles path is already in configs
    if 'dotfiles_path' not in configs or not os.path.exists(os.path.expanduser(configs['dotfiles_path'])):
        while True:
            path = click.prompt('Please enter your dotfiles repository path')
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                # Save the path to the configs file
                configs['dotfiles_path'] = expanded_path
                try:
                    with open(CONFIGS_FILE, 'w') as file:
                        yaml.safe_dump(configs, file)
                        return expanded_path;
                except Exception as exc:
                    error(f"Error writing to YAML file: {exc}")
            else:
                error('Invalid path. Please try again.')


def ask_for_default_dotfiles_branch():
    configs = load_configs()

    # Check if git branch already defined ( configured ) .
    if 'dotfiles_default_branch' not in configs:
        while True:
            branch = click.prompt('Please enter the branch of your dotfiles repository that you are working on: ')

            # Set the branch & Save the file
            configs['dotfiles_default_branch'] = branch
            try:
                with open(CONFIGS_FILE, 'w') as file:
                    yaml.safe_dump(configs, file)
                    return configs['dotfiles_default_branch'];
            except Exception as exc:
                error(f"Error writing to YAML file: {exc}")


def load_configs():
    # Load existing configs file
    try:
        with open(CONFIGS_FILE, 'r') as file:
            return yaml.safe_load(file) or {}
    except Exception as exc:
        error(f"Error reading YAML file: {exc}")



