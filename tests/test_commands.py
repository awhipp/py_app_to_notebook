# tests/test_commands.py
from click.testing import CliRunner
from py_app_to_notebook.commands import tree, validate, build

def test_tree():
    """Ensure the tree command works. Tests output as well."""
    runner = CliRunner()
    result = runner.invoke(tree)
    assert result.exit_code == 0
    assert "Application Tree." in result.output

def test_validate():
    """Ensure the validate command works. Tests output as well."""
    runner = CliRunner()
    result = runner.invoke(validate)
    assert result.exit_code == 0
    assert "Validating Application." in result.output

def test_build():
    """Ensure the build command works. Tests output as well."""
    runner = CliRunner()
    result = runner.invoke(build)
    assert result.exit_code == 0
    assert "Building Notebook Archive." in result.output