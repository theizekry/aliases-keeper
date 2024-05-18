import click
import colorama
import os
import subprocess
from colorama import Fore

from about_author import about_author

# Initialize colorama
colorama.init()

# Directory to store aliases file
ALIASES_DIR = os.path.expanduser("~/.aliases_keeper")
ALIASES_FILE = os.path.join(ALIASES_DIR, "aliases.txt")
LOG_OUTPUT = True


def ensure_aliases_file_exists():
    """Ensure the aliases file exists, creating it if necessary"""
    """Create the aliases file with initial content"""

    if not os.path.exists(ALIASES_DIR):
        os.makedirs(ALIASES_DIR)

    if not os.path.exists(ALIASES_FILE):
        with open(ALIASES_FILE, "w") as f:
            f.write(f"{about_author()}\n")


def alias_exists(alias_name):
    """Check if an alias exists in the aliases file"""
    if os.path.exists(ALIASES_FILE):
        with open(ALIASES_FILE, "r") as f:
            for line in f:
                if line.startswith(f"alias {alias_name}="):
                    return True
    return False


def create_alias(alias_name, alias_value, group="Other"):
    """Create a new alias under the specified group"""
    ensure_aliases_file_exists()

    with open(ALIASES_FILE, "r") as f:
        lines = f.readlines()

    # Find the index of the group in the lines
    group_index = next((i for i, line in enumerate(lines) if f"[{group}]" in line), None)

    if not alias_exists(alias_name):
        # if group found push under this group
        if group_index is not None:
            lines.insert(group_index + 1, f"alias {alias_name}='{alias_value}'\n")
        else:
            # If the group does not exist, create the group and add the alias under it
            lines.append(f"\n\n# [{group}]\n")
            lines.append(f"alias {alias_name}='{alias_value}'\n")

        # Write the modified lines back to the aliases file
        with open(ALIASES_FILE, "w") as f:
            f.writelines(lines)

        if LOG_OUTPUT:
            click.echo(Fore.GREEN + f"Alias '{alias_name}' created with value '{alias_value}' under group '{group}'.")
    else:
        click.echo(Fore.RED + f"Alias '{alias_name}' already exists.")


def delete_alias(alias_name):
    """Delete an alias from the aliases file by name"""

    ensure_aliases_file_exists()

    if not alias_exists(alias_name):
        click.echo(Fore.RED + f"Alias '{alias_name}' does not exist.")
        return

    with open(ALIASES_FILE, "r") as f:
        lines = f.readlines()

    line_index = next((i for i, line in enumerate(lines) if f"alias {alias_name}=" in line), None)

    if line_index is None:
        click.echo(Fore.RED + "Something went wrong.")
        return
    else:
        # Remove the line containing the alias
        del lines[line_index]
        # Write the updated lines back to the file
        with open(ALIASES_FILE, "w") as f:
            f.writelines(lines)

        if LOG_OUTPUT:
            click.echo(Fore.GREEN + f"Alias '{alias_name}' has been deleted.")


def edit_aliases(alias_name, alias_value, group):
    global LOG_OUTPUT  # modify the global LOG_OUTPUT variable

    ensure_aliases_file_exists()

    LOG_OUTPUT = False

    if not alias_exists(alias_name):
        click.echo(Fore.RED + f"Alias '{alias_name}' does not exist.")
        return

    delete_alias(alias_name)
    create_alias(alias_name, alias_value, group)
    click.echo(Fore.GREEN + f"Alias '{alias_name}' Updated with value '{alias_value}' under group '{group}'.")


def show_aliases():
    ensure_aliases_file_exists()

    output = subprocess.check_output(["cat", ALIASES_FILE], universal_newlines=True)

    print(output)
