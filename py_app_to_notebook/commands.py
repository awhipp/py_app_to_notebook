import click

# TODO - Implementation needed

@click.command()
def validate():
    """Validates an application for a given directory."""
    click.echo("Validating Application.")

@click.command()
def tree():
    """Builds the application tree for a given directory."""
    click.echo("Application Tree.")

@click.command()
def build():
    """Builds a notebook archive for a given directory."""
    click.echo("Building Notebook Archive.")
