import click
from about_author import about_author
from crud import create_alias, delete_alias, show_aliases, edit_aliases, source_shell_profile, flush_aliases
from sync import sync_aliasify
from assets.alerts import *


@click.group()
def main():
    """Aliases Keeper - Manage and synchronize your aliases"""
    pass


@main.command()
def about():
    """Display a welcome message"""
    info('Welcome to Aliases Keeper!')
    success(about_author())


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
@click.option("--direction", "-d", type=click.Choice(['local-to-remote', 'remote-to-local']), required=True,
              help="Sync direction: 'local-to-remote' or 'remote-to-local'.", default='local-to-remote')
def sync(direction):
    """Sync aliases between local and remote Dotfiles repository."""
    sync_aliasify(direction)


if __name__ == "__main__":
    main()
