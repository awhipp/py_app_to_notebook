# tests/test_commands.py
import os
from click.testing import CliRunner
from py_app_to_notebook.commands import print_dependency_tree, build

def test_print_dependency_tree(output_dependency_tree):
    """Ensure the print_dependency_tree command works. Tests output as well."""
    runner = CliRunner()
    # Invoke print_dependency_tree with the entrypoint option
    result = runner.invoke(print_dependency_tree, ["--entrypoint", f"queue_to_s3_sample{os.sep}app.py"])
    assert result.exit_code == 0
    assert result.output == f"{output_dependency_tree}\n" # Add newline to match expected output

def test_build():
    """Ensure the build command works. Tests output as well."""
    runner = CliRunner()
    result = runner.invoke(build)
    assert result.exit_code == 0
    assert "Building Notebook Archive." in result.output