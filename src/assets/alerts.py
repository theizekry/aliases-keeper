import subprocess

# Define the color commands
colors = {
    "BLACK": "tput setaf 0",
    "RED": "tput setaf 1",
    "GREEN": "tput setaf 2",
    "YELLOW": "tput setaf 3",
    "BLUE": "tput setaf 4",
    "MAGENTA": "tput setaf 5",
    "CYAN": "tput setaf 6",
    "WHITE": "tput setaf 7",
    "RESET": "tput sgr0",
}


def color_message(message, color):
    # Get the tput command for the specified color
    color_command = colors.get(color.upper(), colors["RESET"])
    reset_command = colors["RESET"]

    # Construct the full command to get the color escape sequences
    color_sequence = subprocess.run(color_command, shell=True, capture_output=True, text=True).stdout.strip()
    reset_sequence = subprocess.run(reset_command, shell=True, capture_output=True, text=True).stdout.strip()

    # Return the message with color and reset sequences
    return f"{color_sequence}{message}{reset_sequence}"


def info(message):
    print(color_message(message, "CYAN"))


def success(message):
    print(color_message(message, "GREEN"))


def danger(message):
    print(color_message(message, "RED"))


def error(message):
    print(color_message(message, "RED"))


def warning(message):
    print(color_message(message, "YELLOW"))


def note(message):
    print(color_message(message, "WHITE"))


def sweet_info(message):
    print(color_message(message, "MAGENTA"))


__all__ = [
    'info',
    'success',
    'danger',
    'warning',
    'error',
    'note',
    'sweet_info',
]
