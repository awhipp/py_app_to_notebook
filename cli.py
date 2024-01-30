import click
from py_app_to_notebook.commands import tree, validate, build

@click.group()
def cli():
    """Your Click CLI."""

# Add commands to the CLI
cli.add_command(tree)
cli.add_command(validate)
cli.add_command(build)

if __name__ == "__main__":
    cli()
