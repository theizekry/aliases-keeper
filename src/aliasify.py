import click
from colorama import Fore, Style
from crud import create_alias, delete_alias, show_aliases, edit_aliases
from about_author import about_author

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


@main.command(short_help="Create a new alias")
@click.argument("alias_name", required=True)
def delete(alias_name):
    """Delete an alias by name"""
    delete_alias(alias_name)


@main.command(short_help="Edit an alias by name, you can edit name and value along as the group of the alias")
@click.argument("alias_name", required=True)
@click.argument("alias_value", required=True)
@click.option("--group", "-g", default="Other", required=False)
def edit(alias_name, alias_value, group):
    """Edit an alias by name"""
    edit_aliases(alias_name, alias_value, group)


@main.command(short_help="Show aliases File content")
def show():
    """Show the Current Aliases"""
    show_aliases()


if __name__ == "__main__":
    main()
