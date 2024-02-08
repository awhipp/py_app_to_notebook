import click
from py2databricks.commands import print_dependency_tree, build

@click.group()
def cli():
    """Your Click CLI."""

# Add commands to the CLI
cli.add_command(print_dependency_tree)
cli.add_command(build)

if __name__ == "__main__":
    cli()
