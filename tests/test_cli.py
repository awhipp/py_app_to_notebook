# tests/test_cli.py
import os
from click.testing import CliRunner
from cli import cli
 
def test_cli_tree(output_dependency_tree):
    """Ensure the tree command works. Core functionality already tested in commands test."""
    runner = CliRunner()
    result = runner.invoke(cli, ["print-dependency-tree", "--entrypoint", f"queue_to_s3_sample{os.sep}app.py"])
    assert result.exit_code == 0
    assert result.output == f"{output_dependency_tree}\n" # Add newline to match expected output

def test_cli_build():
    """Ensure the build command works. Core functionality already tested in commands test."""
    runner = CliRunner()
    result = runner.invoke(cli, ["build"])
    assert result.exit_code == 0
