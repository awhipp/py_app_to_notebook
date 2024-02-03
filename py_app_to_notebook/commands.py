import click

from py_app_to_notebook.utilities.dir import Dependency

# TODO - Implementation needed

@click.command()
@click.option('--entrypoint', help='The entrypoint for the application.')
def print_dependency_tree(entrypoint: str):
    """Prints the dependency tree for a given entrypoint."""
    # Get entrypoint from options
    if not entrypoint:
        click.echo("No entrypoint provided.")
        return
    tree: str = Dependency(path=entrypoint).dependency_tree_as_string()
    click.echo(tree)


@click.command()
def build():
    """Builds a notebook archive for a given directory."""
    click.echo("Building Notebook Archive.")
