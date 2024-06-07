import yaml
import os
import click
from assets.assets import *

def create_configs_file_if_not_exist():
    # Create an empty YAML file with an empty dictionary
    try:
        if not os.path.exists(CONFIGS_FILE):
            with open(CONFIGS_FILE, 'w') as file:
                yaml.safe_dump({}, file)
    except Exception as exc:
        print(f"Error creating YAML file: {exc}")


def ask_for_dotfiles_repository_path():
    configs = load_configs()

    # Check if dotfiles path is already in configs
    if 'dotfiles_path' in configs and os.path.exists(os.path.expanduser(configs['dotfiles_path'])):
        return configs['dotfiles_path']
    else:
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
                    click.echo(f"Error writing to YAML file: {exc}")
            else:
                click.echo('Invalid path. Please try again.')


def load_configs():
    # Load existing configs file
    try:
        with open(CONFIGS_FILE, 'r') as file:
            return yaml.safe_load(file) or {}
    except Exception as exc:
        click.echo(f"Error reading YAML file: {exc}")



