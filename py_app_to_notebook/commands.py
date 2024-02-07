import click

from py_app_to_notebook.utilities.dependencies import DependencyTree

# TODO - Implementation needed

@click.command()
@click.option('--entrypoint', help='The entrypoint for the application.')
def print_dependency_tree(entrypoint: str):
    """Prints the dependency tree for a given entrypoint."""
    # Get entrypoint from options
    if not entrypoint:
        click.echo("No entrypoint provided.")
        return
    tree: str = DependencyTree(entrypoint=entrypoint).tree_as_string()
    click.echo(tree)


@click.command()
@click.option('--entrypoint', help='The entrypoint for the application.')
@click.option('--output_name', help='The name of the notebook archive to generate (optional).', default='notebook_archive.zip')
def build(entrypoint: str, output_name: str):
    """Builds a notebook archive for a given directory."""
    # Get entrypoint from options
    if not entrypoint:
        click.echo("No entrypoint provided.")
        return
    
    click.echo(f"Building notebook archive ({output_name}) for {entrypoint}...")
