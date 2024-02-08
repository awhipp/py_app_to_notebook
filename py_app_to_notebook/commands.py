import os

import click

from py_app_to_notebook.utilities.dependencies import DependencyTree

from py_app_to_notebook.utilities.build_utils import build_temporary_directory, create_run_file

from py_app_to_notebook.utilities.dir_utils import archive_directory

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
    dependency_tree: DependencyTree = DependencyTree(entrypoint=entrypoint)
    temporary_directory, _= build_temporary_directory(dependency_tree=dependency_tree)
    _ = create_run_file(dependency_tree=dependency_tree, temporary_directory=temporary_directory)
    archive_directory(temporary_directory, output_name)
    click.echo(f"Generated notebook archive at {output_name}.")
