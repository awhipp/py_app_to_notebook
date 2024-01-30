# tests/test_cli.py
from click.testing import CliRunner
from cli import cli
 
def test_cli_tree():
    """Ensure the tree command works. Core functionality already tested in commands test."""
    runner = CliRunner()
    result = runner.invoke(cli, ["tree"])
    assert result.exit_code == 0

def test_cli_validate():
    """Ensure the validate command works. Core functionality already tested in commands test."""
    runner = CliRunner()
    result = runner.invoke(cli, ["validate"])
    assert result.exit_code == 0

def test_cli_build():
    """Ensure the build command works. Core functionality already tested in commands test."""
    runner = CliRunner()
    result = runner.invoke(cli, ["build"])
    assert result.exit_code == 0
