import click
from colorama import Fore, Style
from about_author import about_author
from assets.assets import *
from configs import create_configs_file_if_not_exist, ask_for_dotfiles_repository_path;
from crud import create_alias, delete_alias, show_aliases, edit_aliases, source_shell_profile, flush_aliases


@click.group()
def main():
    """Aliases Keeper - Manage and synchronize your aliases"""
    pass


@main.command()
def about():
    """Display a welcome message"""
    click.echo(Fore.BLUE + "Welcome to Aliases Keeper!")
    click.echo(Fore.GREEN + about_author())


@main.command(short_help="Create a new alias")
@click.argument("alias_name", required=True)
@click.argument("alias_value", required=True)
@click.option("--group", "-g", default="Other", required=False)
def create(alias_name, alias_value, group):
    """Create a new alias"""
    create_alias(alias_name, alias_value, group)
    source_shell_profile()


@main.command(short_help="Create a new alias")
@click.argument("alias_name", required=True)
def delete(alias_name):
    """Delete an alias by name"""
    delete_alias(alias_name)
    source_shell_profile()


@main.command(short_help="Edit an alias by name, you can edit name and value along as the group of the alias")
@click.argument("alias_name", required=True)
@click.argument("alias_value", required=True)
@click.option("--group", "-g", default="Other", required=False)
def edit(alias_name, alias_value, group):
    """Edit an alias by name"""
    edit_aliases(alias_name, alias_value, group)
    source_shell_profile()


@main.command(short_help="Show aliases File content")
def show():
    """Show the Current Aliases"""
    show_aliases()
    source_shell_profile()


@main.command(short_help="Flush all the aliases.")
def flush():
    """Show the Current Aliases"""
    if click.confirm('All the saved aliases will be flushed. Do you want to continue?', abort=True):
        flush_aliases()
        source_shell_profile()


@main.command(short_help="Sync your aliases with your Dotfiles Repository.")
@click.option("--sync", "-s", default=False, required=True)
@click.option("--type", "-t", type=click.Choice(['local-to-remote', 'remote-to-local']), required=True, help="Sync direction: 'local-to-remote' or 'remote-to-local'.")
def sync(sync, type):
    print(sync, type)
    if click.confirm('Do you want to continue?', abort=True):
        create_configs_file_if_not_exist()
        dotfilesPath = ask_for_dotfiles_repository_path()
        print(dotfilesPath);


if __name__ == "__main__":
    main()
