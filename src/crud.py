import os
import subprocess
from assets.alerts import *
from assets.assets import *
from about_author import about_author


# Mapped shells to their profile files path.
SHELL_PROFILE_MAP = {
    "bash": "~/.bashrc",
    "zsh": "~/.zshrc",
    "ksh": "~/.kshrc",
    "csh": "~/.cshrc",
    "tcsh": "~/.tcshrc",
    "fish": "~/.config/fish/config.fish",
    "ash": "~/.profile",
    "dash": "~/.profile",
    "sh": "~/.profile",
}


def ensure_aliases_file_exists_and_sourced():
    """Ensure the aliases file exists, creating it if necessary"""
    """Create the aliases file with initial content"""

    if not os.path.exists(ALIASES_DIR):
        os.makedirs(ALIASES_DIR)

    if not os.path.exists(ALIASES_FILE):
        with open(ALIASES_FILE, "w") as f:
            f.write(f"{about_author()}\n")

    alias_line = f"if [ -f '{ALIASES_FILE}' ]; then source '{ALIASES_FILE}'; fi"

    profile_file = detect_active_shell_profile()

    if not profile_file:
        error("Could not detect active shell or unsupported shell.")

    if os.path.exists(profile_file):
        with open(profile_file, "r") as file:
            content = file.read()

    if alias_line not in content:
        with open(profile_file, "a") as file:
            file.write(f"\n# Aliases Keeper\n{alias_line}\n")
            success(f"Added {ALIASES_FILE} to {profile_file}")


def source_shell_profile():
    """Source the Shell profile environment to make new aliases available"""
    profile_file = detect_active_shell_profile()

    if not profile_file:
        error('Could not detect active shell or unsupported shell.')
        die()

    shell = os.path.basename(os.environ.get("SHELL", ""))

    subprocess.run(f"exec {shell}", shell=True)

    # Inform the user how to source the profile manually
    success(f"Sourced {profile_file} to refresh the shell environment.")
    warning("If you encounter any issues, you can manually source the profile by running:")
    warning(f"source {profile_file}")


def detect_active_shell_profile():
    """Detect the active shell and return the corresponding profile file"""
    shell = os.path.basename(os.environ.get("SHELL", ""))

    profile = SHELL_PROFILE_MAP.get(shell)

    if profile:
        return os.path.expanduser(profile)
    return None


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
    ensure_aliases_file_exists_and_sourced()

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
            success(f"Alias '{alias_name}' created with value '{alias_value}' under group '{group}'.")
    else:
        error(f"Alias '{alias_name}' already exists.")


def delete_alias(alias_name):
    """Delete an alias from the aliases file by name"""

    ensure_aliases_file_exists_and_sourced()

    if not alias_exists(alias_name):
        error(f"Alias '{alias_name}' does not exist.")
        die()

    with open(ALIASES_FILE, "r") as f:
        lines = f.readlines()

    line_index = next((i for i, line in enumerate(lines) if f"alias {alias_name}=" in line), None)

    if line_index is None:
        error('Something went wrong.')
        die()
    else:
        # Remove the line containing the alias
        del lines[line_index]
        # Write the updated lines back to the file
        with open(ALIASES_FILE, "w") as f:
            f.writelines(lines)

        if LOG_OUTPUT:
            success(f"Alias '{alias_name}' has been deleted.")


def edit_aliases(alias_name, alias_value, group):
    global LOG_OUTPUT  # modify the global LOG_OUTPUT variable

    ensure_aliases_file_exists_and_sourced()

    LOG_OUTPUT = False

    if not alias_exists(alias_name):
        error(f"Alias '{alias_name}' does not exist.")
        die()

    delete_alias(alias_name)
    create_alias(alias_name, alias_value, group)
    success(f"Alias '{alias_name}' Updated with value '{alias_value}' under group '{group}'.")


def show_aliases():
    ensure_aliases_file_exists_and_sourced()
    output = subprocess.check_output(["cat", ALIASES_FILE], universal_newlines=True)
    print(output)


def flush_aliases():
    ensure_aliases_file_exists_and_sourced()
    with open(ALIASES_FILE, 'w'):
        pass
